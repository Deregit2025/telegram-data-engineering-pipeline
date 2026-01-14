def extract_message_data(message, channel_name, image_path=None):
    """
    Extracts raw message data from a Telegram message.
    """
    return {
        "message_id": message.id,
        "channel_name": channel_name,
        "message_date": message.date.isoformat() if message.date else None,
        "message_text": message.text,
        "views": message.views,
        "forwards": message.forwards,
        "has_media": bool(message.media),
        "image_path": image_path,
    }
