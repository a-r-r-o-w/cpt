"""
api.codeforces.cfexception
--------------------------

This module contains a set of exceptions that can be
raised by the Codeforces API.
"""


class StatusNotFoundError(Exception):
    """Codeforces API call response does not contain a status message"""


class StatusFailedError(Exception):
    """Codeforces API call response contains {"status": "FAILED"} message"""


class CommentNotFoundError(Exception):
    """Reason for Codeforces API call {"status": "FAILED"} not found"""


class ResultNotFoundError(Exception):
    """Codeforces API call response does not contain result"""
