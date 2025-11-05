def compose_message_id(channel: str, ts: str) -> str:
    """Compose a stable unique message ID from channel ID and Slack timestamp."""
    return f"{channel}:{ts}"
