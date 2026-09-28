"""Helpers that turn CSV templates into unique, run-specific test data."""
import uuid


def unique_id():
    """Short random id, e.g. '3f9a1c2b'."""
    return uuid.uuid4().hex[:8]


def fill_placeholders(value, uid=None):
    """Replace the '{uid}' placeholder used in CSV data with a unique id.

    Unique e-mails keep tests independent: the demo site locks an e-mail
    after several failed logins, and registered e-mails cannot be reused.
    """
    return value.replace("{uid}", uid or unique_id())


def unique_email(prefix="capstone"):
    return f"{prefix}_{unique_id()}@example.com"
