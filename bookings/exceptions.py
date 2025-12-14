"""
Custom exceptions for booking operations.
"""

class BookingStatusException(Exception):
    """
    Base exception for booking status and logic errors.
    """
    def __init__(self, message):
        self.messsage = message
        super().__init__(message)
