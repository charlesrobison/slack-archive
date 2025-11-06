import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from sqlalchemy.orm import Session
from .config import settings
from .db import SessionLocal
from .models import Message
from .utils import compose_message_id
import logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Slack app
app = App(token=settings.SLACK_BOT_TOKEN)


def upsert_message(db: Session, event: dict):
    """Insert or update a Slack message record based on the event type."""
    channel = event.get("channel")
    subtype = event.get("subtype")

    # Handle edited messages
    if subtype == "message_changed":
        inner = event.get("message", {})
        ts = inner.get("ts")
        user = inner.get("user")
        text = inner.get("text")
        thread_ts = inner.get("thread_ts")
        edited_ts = inner.get("edited", {}).get("ts") if inner.get("edited") else event.get("ts")
        payload = inner
        deleted = False

    # Handle deleted messages
    elif subtype == "message_deleted":
        ts = event.get("previous_message", {}).get("ts")
        user = event.get("previous_message", {}).get("user")
        text = None
        thread_ts = None
        edited_ts = None
        payload = event
        deleted = True

    # Handle new messages
    else:
        ts = event.get("ts")
        user = event.get("user")
        text = event.get("text")
        thread_ts = event.get("thread_ts")
        edited_ts = None
        payload = event
        deleted = False

    if not channel or not ts:
        return  # safety guard

    msg_id = compose_message_id(channel, ts)

    existing = db.get(Message, msg_id)
    if existing:
        existing.text = text or existing.text
        existing.edited_ts = edited_ts or existing.edited_ts
        existing.deleted = deleted or existing.deleted
        existing.raw = payload
    else:
        db.add(Message(
            id=msg_id,
            channel_id=channel,
            user_id=user,
            text=text,
            ts=ts,
            thread_ts=thread_ts,
            edited_ts=edited_ts,
            deleted=deleted,
            raw=payload,
        ))


@app.event("message")
def handle_message_store(body, event, logger):
    """Triggered for every message (new, edit, delete)."""
    subtype = event.get("subtype")

    # Ignore bot messages to prevent feedback loops
    if subtype == "bot_message":
        return

    with SessionLocal() as db:
        upsert_message(db, event)
        db.commit()
        print(f"💾 Stored message from {event.get('user')} in {event.get('channel')}: {event.get('text')}")


@app.event("reaction_added")
def handle_reaction_added(body, event, logger):
    logger.info(f"reaction_added: {json.dumps(event)[:120]}")


@app.event("reaction_removed")
def handle_reaction_removed(body, event, logger):
    logger.info(f"reaction_removed: {json.dumps(event)[:120]}")

# Debug handler — log every incoming event
@app.event({"type": "message"})
def handle_message_events(event, say):
    user = event.get("user")
    text = event.get("text")
    channel = event.get("channel")
    print(f"🔔 Received message: user={user}, channel={channel}, text={text}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, settings.SLACK_APP_TOKEN)
    print("Listening for Slack events...")
    handler.start()
