from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict

# ----------------------------
# Endpoint 1: Top Products
# ----------------------------
def get_top_products(db: Session, limit: int = 10) -> List[Dict]:
    """
    Returns the most frequently mentioned products/terms from fct_messages.
    """
    sql = text("""
        SELECT word AS product, COUNT(*) AS count FROM (
            SELECT unnest(string_to_array(message_text, ' ')) AS word
            FROM analytics_analytics.fct_messages
        ) AS words
        GROUP BY word
        ORDER BY count DESC
        LIMIT :limit;
    """)
    result = db.execute(sql, {"limit": limit}).mappings().all()
    return [{"product": row["product"], "count": row["count"]} for row in result]


# ----------------------------
# Endpoint 2: Channel Activity
# ----------------------------
def get_channel_activity(db: Session, channel_key: str) -> List[Dict]:
    """
    Returns message counts per day for a given channel.
    """
    sql = text("""
        SELECT
            channel_key,
            CAST(date_key AS date) AS date,
            COUNT(*) AS message_count
        FROM analytics_analytics.fct_messages
        WHERE channel_key = :channel_key
        GROUP BY channel_key, CAST(date_key AS date)
        ORDER BY date ASC;
    """)
    result = db.execute(sql, {"channel_key": channel_key}).mappings().all()
    return [
        {
            "channel_key": row["channel_key"],
            "date": row["date"],
            "message_count": row["message_count"]
        }
        for row in result
    ]


# ----------------------------
# Endpoint 3: Message Search
# ----------------------------
def search_messages(db: Session, query: str, limit: int = 20) -> List[Dict]:
    """
    Searches messages containing a specific keyword (case-insensitive).
    """
    sql = text("""
        SELECT
            message_id,
            channel_key,
            message_text,
            view_count
        FROM analytics_analytics.fct_messages
        WHERE message_text ILIKE :query
        ORDER BY date_key DESC
        LIMIT :limit;
    """)
    query_param = f"%{query}%"
    result = db.execute(sql, {"query": query_param, "limit": limit}).mappings().all()
    return [
        {
            "message_id": row["message_id"],
            "channel_key": row["channel_key"],
            "message_text": row["message_text"],
            "view_count": row["view_count"]
        }
        for row in result
    ]


# ----------------------------
# Endpoint 4: Visual Content Stats
# ----------------------------
def get_visual_content_stats(db: Session) -> List[Dict]:
    """
    Returns statistics about image usage across channels by category.
    Categories:
      - promotional: person + product
      - product_display: product only
      - lifestyle: person only
      - other: neither
    Assumes fct_image_detections table has 'channel_key' and 'image_category' columns.
    """
    sql = text("""
        SELECT
            channel_key,
            image_category,
            COUNT(*) AS image_count
        FROM analytics_analytics.fct_image_detections
        GROUP BY channel_key, image_category
        ORDER BY channel_key, image_category;
    """)
    result = db.execute(sql).mappings().all()
    return [
        {
            "channel_key": row["channel_key"],
            "image_category": row["image_category"],
            "image_count": row["image_count"]
        }
        for row in result
    ]
