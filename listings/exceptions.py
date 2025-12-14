"""
Custom exceptions for enforcing Space status transitions.
"""

from .models import Space

# Mapping of internal status codes to human-readable names.
status_dict = dict(Space.Status.choices)

class SpaceStateError(Exception):
    """
    Base exception for Space state management errors.

    Attributes:
        message (str): The error message.
    """
    def __init__(self, message):
        """
        Initializes the SpaceStateError.

        Args:
            message (str): Description of the failure.
        """
        self.message = message
        super().__init__(self.message)


class InvalidSpaceStateError(SpaceStateError):
    """
    Raised when an operation references an undefined status code.
    """
    def __init__(self, status):
        """
        Initializes the InvalidSpaceStateError.

        Args:
            status (str): The invalid status code.
        """
        super().__init__(f"Update unsuccessful - No valid state {status}")


class SpaceStateTransitionError(SpaceStateError):
    """
    Raised when a status transition violates business rules.
    """
    def __init__(self, status: Space.Status, new_status: Space.Status):
        """
        Initializes the SpaceStateTransitionError.

        Args:
            status (Space.Status): The current state.
            new_status (Space.Status): The target state.
        """
        super().__init__(f"Update unsuccessful - Invalid status update from {status_dict.get(status)} to {status_dict.get(new_status)}")
