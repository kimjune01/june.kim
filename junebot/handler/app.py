import json
import os

import boto3
from anthropic import Anthropic
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from prompts import system_blocks
from tools import TOOL_SCHEMAS, dispatch

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
MAX_TOOL_ROUNDS = 6
SSM_PARAM = os.environ.get("ANTHROPIC_KEY_PARAM", "/junebot/anthropic-api-key")


def _load_api_key() -> str:
    direct = os.environ.get("ANTHROPIC_API_KEY")
    if direct:
        return direct
    ssm = boto3.client("ssm")
    resp = ssm.get_parameter(Name=SSM_PARAM, WithDecryption=True)
    return resp["Parameter"]["Value"]


client = Anthropic(api_key=_load_api_key())
# CORS is handled by the Lambda Function URL config, not here — adding
# CORSMiddleware would duplicate the Access-Control-Allow-Origin header
# and browsers reject that with a NetworkError.
app = FastAPI()


class ChatIn(BaseModel):
    slug: str | None = None
    messages: list[dict]


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


def _seed_messages(body: ChatIn) -> list[dict]:
    msgs = list(body.messages)
    if body.slug and msgs and msgs[0].get("role") == "user":
        prefix = f"[visitor is reading post: {body.slug}]\n\n"
        first = msgs[0]
        content = first["content"]
        if isinstance(content, str):
            msgs[0] = {**first, "content": prefix + content}
    return msgs


def _run_agent_loop(body: ChatIn):
    """Run tool-use loop, yielding SSE events.

    Each round: call the model (non-streaming to inspect tool_use blocks),
    stream any text blocks back as tokens, handle tool calls, repeat until
    the model stops."""
    system = system_blocks()
    messages = _seed_messages(body)

    for _ in range(MAX_TOOL_ROUNDS):
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            tools=TOOL_SCHEMAS,
            messages=messages,
        ) as stream:
            for event in stream:
                if event.type == "content_block_delta" and event.delta.type == "text_delta":
                    yield f"data: {json.dumps({'type': 'text', 'text': event.delta.text})}\n\n"

            final = stream.get_final_message()

        assistant_blocks = [b.model_dump() for b in final.content]
        messages.append({"role": "assistant", "content": assistant_blocks})

        tool_uses = [b for b in final.content if b.type == "tool_use"]
        if not tool_uses:
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        tool_results = []
        for tu in tool_uses:
            result = dispatch(tu.name, dict(tu.input))
            tool_results.append(
                {"type": "tool_result", "tool_use_id": tu.id, "content": result}
            )
        messages.append({"role": "user", "content": tool_results})

    yield f"data: {json.dumps({'type': 'error', 'text': 'max tool rounds reached'})}\n\n"


@app.post("/api/chat")
def chat(body: ChatIn):
    if not body.messages:
        raise HTTPException(400, "messages required")
    return StreamingResponse(_run_agent_loop(body), media_type="text/event-stream")
