"""Tests for the email-to-post handler."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from handler import (
    slugify,
    parse_tags,
    extract_image,
    extract_body_text,
    escape_yaml_string,
    get_sender,
)


def make_email(subject, body, image_bytes=None, image_ext="jpg", sender="june@june.kim"):
    """Build a test email message."""
    if image_bytes:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = "post@agent.june.kim"
        msg.attach(MIMEText(body, "plain"))
        img = MIMEImage(image_bytes, _subtype=image_ext)
        img.add_header("Content-Disposition", "attachment", filename=f"photo.{image_ext}")
        msg.attach(img)
    else:
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = "post@agent.june.kim"
    return msg


FAKE_JPG = b"\xff\xd8\xff\xe0" + b"\x00" * 100


# --- slugify ---

def test_slugify_basic():
    assert slugify("My Latest Woodwork") == "my-latest-woodwork"


def test_slugify_special_chars():
    assert slugify("Hello, World! (2026)") == "hello-world-2026"


def test_slugify_extra_spaces():
    assert slugify("  too   many  spaces  ") == "too-many-spaces"


def test_slugify_empty_result():
    assert slugify("!!!") == "untitled"


def test_slugify_punctuation_only():
    assert slugify("...") == "untitled"


# --- escape_yaml_string ---

def test_escape_yaml_quotes():
    assert escape_yaml_string('He said "hello"') == 'He said \\"hello\\"'


def test_escape_yaml_newline():
    assert escape_yaml_string("line1\nline2") == "line1 line2"


def test_escape_yaml_backslash():
    assert escape_yaml_string("path\\to\\file") == "path\\\\to\\\\file"


def test_escape_yaml_clean():
    assert escape_yaml_string("Normal Title") == "Normal Title"


# --- parse_tags ---

def test_parse_tags_comma_separated():
    assert parse_tags("crafting, coding, poetry") == ["crafting", "coding", "poetry"]


def test_parse_tags_space_separated():
    assert parse_tags("crafting coding") == ["crafting", "coding"]


def test_parse_tags_filters_unknown():
    assert parse_tags("crafting, unknown, coding") == ["crafting", "coding"]


def test_parse_tags_case_insensitive():
    assert parse_tags("Crafting, CODING") == ["crafting", "coding"]


def test_parse_tags_empty():
    assert parse_tags("") == []


def test_parse_tags_all_unknown():
    assert parse_tags("foo bar baz") == []


# --- get_sender ---

def test_get_sender_angle_brackets():
    msg = make_email("Test", "body", sender="June Kim <june@june.kim>")
    assert get_sender(msg) == "june@june.kim"


def test_get_sender_bare():
    msg = make_email("Test", "body", sender="june@june.kim")
    assert get_sender(msg) == "june@june.kim"


def test_get_sender_case():
    msg = make_email("Test", "body", sender="June@June.Kim")
    assert get_sender(msg) == "june@june.kim"


def test_sender_in_default_allowlist():
    """Default ALLOWED_SENDERS includes june@june.kim."""
    from handler import ALLOWED_SENDERS
    msg = make_email("Test", "body", sender="june@june.kim")
    assert get_sender(msg) in ALLOWED_SENDERS


def test_sender_not_in_allowlist():
    from handler import ALLOWED_SENDERS
    msg = make_email("Test", "body", sender="attacker@evil.com")
    assert get_sender(msg) not in ALLOWED_SENDERS


# --- extract_image ---

def test_extract_image_found():
    msg = make_email("Test", "body", image_bytes=FAKE_JPG, image_ext="jpeg")
    data, ext = extract_image(msg)
    assert data is not None
    assert ext == ".jpeg"


def test_extract_image_missing():
    msg = make_email("Test", "body")
    data, ext = extract_image(msg)
    assert data is None
    assert ext is None


# --- extract_body_text ---

def test_extract_body_plain():
    msg = make_email("Test", "crafting\nThis is my post.")
    text = extract_body_text(msg)
    assert "crafting" in text
    assert "This is my post." in text


def test_extract_body_multipart():
    msg = make_email("Test", "crafting\nContent here", image_bytes=FAKE_JPG)
    text = extract_body_text(msg)
    assert "crafting" in text
    assert "Content here" in text


# --- integration: full parse ---

def test_full_parse():
    msg = make_email(
        "My Dovetail Joint",
        "crafting, projects\nFirst attempt at hand-cut dovetails.",
        image_bytes=FAKE_JPG,
        image_ext="jpeg",
    )
    subject = msg["subject"]
    body = extract_body_text(msg)
    lines = [l for l in body.strip().splitlines() if l.strip()]
    tags = parse_tags(lines[0])
    content = "\n".join(lines[1:]) if len(lines) > 1 else ""
    image_data, image_ext = extract_image(msg)

    assert subject == "My Dovetail Joint"
    assert tags == ["crafting", "projects"]
    assert content == "First attempt at hand-cut dovetails."
    assert image_data is not None
    assert image_ext == ".jpeg"
    assert slugify(subject) == "my-dovetail-joint"


def test_tags_only_no_content():
    msg = make_email("Quick Photo", "crafting", image_bytes=FAKE_JPG)
    body = extract_body_text(msg)
    lines = [l for l in body.strip().splitlines() if l.strip()]
    tags = parse_tags(lines[0])
    content = "\n".join(lines[1:]) if len(lines) > 1 else ""

    assert tags == ["crafting"]
    assert content == ""


def test_no_matching_tags_defaults_to_crafting():
    """When no known tags match, the handler defaults to 'crafting'."""
    tags = parse_tags("something unknown")
    tags_str = " ".join(tags) if tags else "crafting"
    assert tags_str == "crafting"


def test_injectable_title_escaped():
    """YAML injection in subject should be neutralized."""
    dangerous = 'Title"\ntags: hacked'
    safe = escape_yaml_string(dangerous)
    assert "\n" not in safe
    assert '\\"' in safe
