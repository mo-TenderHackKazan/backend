"""
Notifications email provider
meta params:
    - user_id: int, optional
    - email: str, optional, if user_id is provided
"""

from .send import send_notification  # noqa
