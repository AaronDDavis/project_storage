"""
Exceptions for the installation request workflow.
"""
from .models import InstallationRequest

status_dict = dict(InstallationRequest.Status.choices)


class InstallationRequestError(Exception):
    """Base exception for Installation Request errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InstallationRequestConversionError(InstallationRequestError):
    """Raised when a request cannot be converted to a Space."""
    def __init__(self, status: InstallationRequest.Status):
        super().__init__(f'Installation Request in {status_dict.get(status)} state cannot be converted into a Space.')


class InstallationRequestStateError(InstallationRequestError):
    """Base exception for state management errors."""
    def __init__(self, message):
        super().__init__(message)


class InvalidInstallationRequestStateError(InstallationRequestStateError):
    """Raised when an undefined status code is used."""
    def __init__(self, status):
        super().__init__(f"Update unsucessful - No valid state {status}")


class InstallationRequestStateTransitionError(InstallationRequestStateError):
    """Raised when a status transition violates business rules."""
    def __init__(self, status: InstallationRequest.Status, new_status: InstallationRequest.Status):
        super().__init__(f"Update unsucessful - Invalid status update from {status_dict.get(status)} to {status_dict.get(new_status)}")


class IncompleteInstallationRequestError(InstallationRequestError):
    """Raised when completing a request without defining rack parameters."""
    def __init__(self, message):
        super().__init__(message)
