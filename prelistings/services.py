"""
Business logic for processing installation requests.
"""
from .models import InstallationRequest
from users.models import CustomUser
from django.db.models import QuerySet
from .exceptions import InstallationRequestError, InvalidInstallationRequestStateError, InstallationRequestStateTransitionError, IncompleteInstallationRequestError
from listings.models import Space, SHELF_HEIGHT
from listings.services import SpaceService

class InstallationRequestService:
    """
    Handles retrieval and conversion of Installation Requests.
    """
    @staticmethod
    def get_installation_requests(renter:CustomUser = None) -> QuerySet:
        """
        Retrieves requests, optionally filtered by renter.
        """
        installation_requests = InstallationRequest.objects.all()

        if renter:
            installation_requests = installation_requests.filter(renter = renter)

        return installation_requests
    
    @staticmethod
    def get_total_shelves(installation_request: InstallationRequest) -> int:
        """
        Calculates total shelves configured for this request.
        """
        return installation_request.num_rack * installation_request.num_shelves_per_rack
    
    @staticmethod
    def convert_to_space(installation_request: InstallationRequest) -> Space:
        """
        Converts a 'COMPLETED' request into a live Space object.

        Side Effects:
            - Creates a new Space record.
            - Creates associated Racks and Shelves.
            - Deletes the original InstallationRequest.
        """
        if installation_request.status == InstallationRequest.Status.COMPLETED:
            space = Space(
                renter = installation_request.renter,
                location = installation_request.location,
                environment_conditions = installation_request.environment_conditions,
                height = SHELF_HEIGHT * installation_request.num_rack,
                status = Space.Status.APPROVED,
                price_per_day = installation_request.price_per_day,
                description = installation_request.description
                )
            space.save()
        
            
            SpaceService.create_shelves(
                space = space,
                num_rack = installation_request.num_rack,
                num_shelf_per_rack = installation_request.num_shelves_per_rack
                )
            
            installation_request.delete()
            
            return space
        else:
            raise InstallationRequestError(installation_request.status)


class InstallationRequestStateService:
    """
    Manages state transitions for Installation Requests (Pending -> Approved -> Completed).
    """
    @staticmethod
    def is_valid_status(status):
        return status in InstallationRequest.Status.values

    @staticmethod
    def transition(installation_request: InstallationRequest, new_status: InstallationRequest.Status) -> bool:        
        """
        Updates the request status if the transition is valid.
        """
        if not InstallationRequestStateService.is_valid_status(new_status):
            raise InvalidInstallationRequestStateError(new_status)

        if not InstallationRequestStateService.is_valid_transition(installation_request.status, new_status):
            raise InstallationRequestStateTransitionError(installation_request.status, new_status)

        elif new_status == InstallationRequest.Status.COMPLETED and installation_request.num_rack * installation_request.num_shelves_per_rack == 0:
            raise IncompleteInstallationRequestError('Number of racks and shelves per rack must be non-zero values')

        else:
            installation_request.status = new_status
            installation_request.save()
            return True

    @staticmethod
    def is_valid_transition(old_status: InstallationRequest.Status, new_status: InstallationRequest.Status):
        if old_status == InstallationRequest.Status.PENDING and new_status in (InstallationRequest.Status.APPROVED, InstallationRequest.Status.REJECTED):
            return True

        elif old_status == InstallationRequest.Status.APPROVED and new_status == InstallationRequest.Status.COMPLETED:
            return True

        else:
            return True
