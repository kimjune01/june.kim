"""
Lambda handler: receives emails from SES (via S3), parses them into Jekyll posts,
and commits to the GitHub repo via API.

Email format:
  To: post@agent.june.kim
  Subject: My Post Title
  Body line 1: tags (filtered against known tags)
  Body line 2+: post content (optional)
  Attachment: photo (required)
"""

import base64
import email
import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from email import policy

KNOWN_TAGS = [
    "coding",
    "cognition",
    "crafting",
    "envelopay",
    "improving",
    "methodology",
    "pageleft",
    "poetry",
    "projects",
    "reading",
    "reflecting",
    "vector-space",
]

ALLOWED_SENDERS = os.environ.get("ALLOWED_SENDERS", "june@june.kim").split(",")

GITHUB_REPO = "kimjune01/kimjune01.github.io"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"}


def get_github_token():
    """Fetch GitHub token from SSM Parameter Store."""
    ssm_name = os.environ.get("GITHUB_TOKEN_SSM", "/agent/github-token")
    import boto3
    ssm = boto3.client("ssm")
    resp = ssm.get_parameter(Name=ssm_name, WithDecryption=True)
    return resp["Parameter"]["Value"]


_github_token = None


def github_api(method, path, body=None):
    """Make a GitHub API request."""
    global _github_token
    if _github_token is None:
        _github_token = os.environ.get("GITHUB_TOKEN") or get_github_token()
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {_github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def slugify(title):
    """Convert title to URL-friendly slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-") or "untitled"


def escape_yaml_string(s):
    """Escape a string for safe YAML double-quoted inclusion."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", " ")
    s = s.replace("\r", "")
    return s


def parse_tags(line):
    """Filter first line of body for known tags."""
    candidates = re.split(r"[,\s]+", line.lower().strip())
    return [t for t in candidates if t in KNOWN_TAGS]


def extract_image(msg):
    """Extract the first image attachment from the email."""
    for part in msg.walk():
        content_type = part.get_content_type()
        if not content_type.startswith("image/"):
            continue
        filename = part.get_filename() or "photo.jpg"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            continue
        data = part.get_payload(decode=True)
        if data:
            return data, ext
    return None, None


def extract_body_text(msg):
    """Extract plain text body from email."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode("utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode("utf-8", errors="replace")
    return ""


def get_sender(msg):
    """Extract the sender email address."""
    from_header = msg["from"] or ""
    match = re.search(r"<([^>]+)>", from_header)
    if match:
        return match.group(1).lower()
    return from_header.strip().lower()


def get_latest_commit_sha():
    """Get the SHA of the latest commit on master."""
    ref = github_api("GET", "git/ref/heads/master")
    return ref["object"]["sha"]


def get_tree_sha(commit_sha):
    """Get the tree SHA for a commit."""
    commit = github_api("GET", f"git/commits/{commit_sha}")
    return commit["tree"]["sha"]


def create_blob(content_b64):
    """Create a blob in the repo."""
    blob = github_api("POST", "git/blobs", {
        "content": content_b64,
        "encoding": "base64",
    })
    return blob["sha"]


def commit_files(files, message):
    """Commit multiple files to the repo in a single commit.

    files: list of (path, content_bytes) tuples
    Retries once on ref-update race (409/422).
    """
    for attempt in range(2):
        base_sha = get_latest_commit_sha()
        base_tree = get_tree_sha(base_sha)

        tree_items = []
        for path, content in files:
            blob_sha = create_blob(base64.b64encode(content).decode())
            tree_items.append({
                "path": path,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha,
            })

        tree = github_api("POST", "git/trees", {
            "base_tree": base_tree,
            "tree": tree_items,
        })

        commit = github_api("POST", "git/commits", {
            "message": message,
            "tree": tree["sha"],
            "parents": [base_sha],
        })

        try:
            github_api("PATCH", "git/refs/heads/master", {
                "sha": commit["sha"],
            })
            return commit["sha"]
        except urllib.error.HTTPError as e:
            if attempt == 0 and e.code in (409, 422):
                print(f"Ref update race, retrying (attempt {attempt + 1})")
                continue
            raise


def handler(event, context):
    """AWS Lambda entry point. SES stores email in S3, triggers this."""
    import boto3

    s3 = boto3.client("s3")
    bucket = os.environ["S3_BUCKET"]

    for record in event["Records"]:
        ses_msg = record["ses"]
        message_id = ses_msg["mail"]["messageId"]

        # Check SES verdicts
        receipt = ses_msg.get("receipt", {})
        if receipt.get("spamVerdict", {}).get("status") == "FAIL":
            print(f"Spam verdict FAIL for {message_id}, skipping")
            continue
        if receipt.get("virusVerdict", {}).get("status") == "FAIL":
            print(f"Virus verdict FAIL for {message_id}, skipping")
            continue

        obj = s3.get_object(Bucket=bucket, Key=f"incoming/{message_id}")
        raw_email = obj["Body"].read()

        msg = email.message_from_bytes(raw_email, policy=policy.default)

        # Sender allowlist
        sender = get_sender(msg)
        if sender not in ALLOWED_SENDERS:
            print(f"Unauthorized sender {sender} for {message_id}, skipping")
            continue

        title = msg["subject"] or "Untitled"
        title = re.sub(r"^(Re|Fwd):\s*", "", title, flags=re.IGNORECASE).strip()

        body_text = extract_body_text(msg)
        lines = [l for l in body_text.strip().splitlines() if l.strip()]

        tags = []
        content = ""
        if lines:
            tags = parse_tags(lines[0])
            if len(lines) > 1:
                content = "\n".join(lines[1:])

        image_data, image_ext = extract_image(msg)
        if not image_data:
            print(f"No image attachment found in {message_id}, skipping")
            continue

        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        year = now.strftime("%Y")
        slug = slugify(title)
        # Include short message ID to prevent same-day/same-title overwrites
        short_id = message_id[:8]

        image_path = f"assets/{date_str}-{slug}-{short_id}{image_ext}"
        post_path = f"_posts/{year}/{date_str}-{slug}.md"

        tags_str = " ".join(tags) if tags else "crafting"
        safe_title = escape_yaml_string(title)

        post_content = f"""---
layout: post
title: "{safe_title}"
tags: {tags_str}
image: "/{image_path}"
---

![]({{% link {image_path} %}})
"""
        if content:
            post_content += f"\n{content}\n"

        post_bytes = post_content.encode("utf-8")

        sha = commit_files(
            [
                (image_path, image_data),
                (post_path, post_bytes),
            ],
            f"Post via email: {title}",
        )

        print(f"Committed {post_path} and {image_path} as {sha}")

    return {"statusCode": 200, "body": "OK"}
