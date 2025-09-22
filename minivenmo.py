from models import User, Feed
from typing import List, Dict, Any


class MiniVenmo:
    @staticmethod
    def render_feed(activities: List[Feed]) -> List[Dict[str, Any]]:
        """
        Render the feed from a list of activities

        Args:
            activities: List of Feed objects to render

        Returns:
            List of dictionaries containing formatted feed items
        """
        feed_items = []

        for activity in activities:
            if activity.feed_type == "payment":
                # Format payment activity
                feed_item = {
                    "type": "payment",
                    "user": activity.user.name,
                    "related_user": (
                        activity.related_user.name if activity.related_user else None
                    ),
                    "detail": activity.detail,
                    "timestamp": activity.created_at.isoformat(),
                }
                feed_items.append(feed_item)

            elif activity.feed_type == "friend_add":
                # Format friend add activity
                feed_item = {
                    "type": "friend_add",
                    "user": activity.user.name,
                    "friend": (
                        activity.related_user.name if activity.related_user else None
                    ),
                    "detail": activity.detail,
                    "timestamp": activity.created_at.isoformat(),
                }
                feed_items.append(feed_item)

        return feed_items
