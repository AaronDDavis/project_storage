"""
Encapsulates inventory logic including availability search, layout generation, and state transitions.
"""

from .models import Space, Rack, Shelf, SHELF_LENGTH, SHELF_WIDTH, SHELF_HEIGHT
from .exceptions import InvalidSpaceStateError, SpaceStateTransitionError
from django.db.models import Count, Q, Value, IntegerField, OuterRef, Subquery
from math import ceil

class SpaceService:
    """
    Handles retrieval, creation, and filtering of inventory objects.
    """
    @staticmethod
    def get_spaces(renter = None, status = None):
        """
        Retrieves a filtered QuerySet of Space objects.

        Args:
            renter (CustomUser, optional): Filter by owner.
            status (str, optional): Filter by Space.Status code.

        Returns:
            QuerySet: Filtered Space objects.
        """
        spaces = Space.objects.all()

        if renter:
            spaces = spaces.filter(renter = renter)
        
        if SpaceStateService.is_valid_status(status):
            spaces = spaces.filter(status=status)

        return spaces
    
    @staticmethod
    def get_racks(space: Space):
        """
        Retrieves all Racks associated with a Space.

        Args:
            space (Space): The parent Space.

        Returns:
            QuerySet: Associated Rack objects.
        """
        return space.rack_set

    @staticmethod
    def create_shelves(space: Space, num_rack: int, num_shelf_per_rack: int):
        """
        Generates Rack and Shelf records for a new Space.

        Args:
            space (Space): The parent Space.
            num_rack (int): Number of racks to create.
            num_shelf_per_rack (int): Number of shelves per rack.
        """
        for _ in range(num_rack):
            rack = Rack()
            rack.space = space
            rack.length = num_shelf_per_rack * SHELF_LENGTH
            rack.save()
        
            for i in range(num_shelf_per_rack):
                shelf = Shelf()
                shelf.rack = rack
                shelf.shelf_label = str(i).zfill(3)
                shelf.save()

    @staticmethod
    def get_available_spaces(search_location: str, search_length: int, search_width: int, search_height: int):
        """
        Retrieves approved spaces with sufficient capacity for the specified item dimensions.

        Args:
            search_location (str): Case-insensitive partial match for the location area.
            search_length (int): Length of the item in cm.
            search_width (int): Width of the item in cm.
            search_height (int): Height of the item in cm.

        Returns:
            QuerySet: Space objects annotated with 'available_shelves' and 'num_shelves'.
        """
        available_spaces = SpaceService.get_spaces(status = Space.Status.APPROVED)

        # Normalize dimensions: length should be the larger of the two
        search_length, search_width = max(search_length, search_width), min(search_length, search_width)

        if search_width > SHELF_WIDTH:
            return available_spaces.none()
         
        if search_height > SHELF_HEIGHT:
            return available_spaces.none()

        if search_location:
            available_spaces = available_spaces.filter(location__area__icontains=search_location)
        
        # Filter for spaces with at least one rack long enough
        available_spaces = available_spaces.filter(rack__length__gte=search_length).distinct()
                
        min_shelves_required = ceil(search_length / SHELF_LENGTH)

        space_ids = []
        for space in available_spaces:
            rack_set = space.rack_set
            # Annotate racks with available shelf count
            rack_set = rack_set.annotate(available_shelves = Count('shelf', filter=Q(shelf__is_available = True)))
            
            if rack_set.filter(available_shelves__gte=min_shelves_required).exists():
                space_ids.append(space.id)
        
        available_spaces = available_spaces.filter(id__in=space_ids)

        # Calculate max contiguous available shelves per space for display
        rack_avail_qs = (
            Rack.objects
            .filter(space=OuterRef('pk'))
            .annotate(
                max_available_shelves = Count('shelf', filter = Q(shelf__is_available = True))
            )
            .order_by('-max_available_shelves')
            .values('max_available_shelves')[:1]
        )

        available_spaces = available_spaces.annotate(
            available_shelves = Subquery(rack_avail_qs)
        )

        available_spaces = available_spaces.annotate(
            num_shelves = Value(min_shelves_required, output_field = IntegerField())
        )
        
        return available_spaces


class SpaceStateService:
    """
    Manages state transitions for Space objects.
    """
    @staticmethod
    def is_valid_status(status):
        """
        Validates if a status code exists in Space.Status.

        Args:
            status (str): The status code to validate.

        Returns:
            bool: True if valid.
        """
        return status in Space.Status.values

    @staticmethod
    def transition(space: Space, new_status: Space.Status) -> bool:
        """
        Updates a Space's status if the transition is valid.

        Args:
            space (Space): The object to update.
            new_status (Space.Status): The target status.

        Returns:
            bool: True if successful.

        Raises:
            InvalidSpaceStateError: If the status code is invalid.
            SpaceStateTransitionError: If the transition violates business rules.
        """
        if not SpaceStateService.is_valid_status(new_status):
            raise InvalidSpaceStateError(new_status)

        if not SpaceStateService.is_valid_transition(space.status, new_status):
            raise SpaceStateTransitionError(space.status, new_status)
        
        space.status = new_status
        space.save()
        return True

    @staticmethod
    def is_valid_transition(old_status: Space.Status, new_status: Space.Status):
        """
        Enforces business rules for status changes.

        Args:
            old_status (Space.Status): Current status.
            new_status (Space.Status): Target status.

        Returns:
            bool: True if transition is allowed.
        """
        if new_status == Space.Status.PENDING:
            return False
        
        elif old_status in (Space.Status.APPROVED, Space.Status.ON_HOLD) and new_status == Space.Status.REJECTED:
            return False
        
        elif new_status == old_status:
            return False
        
        else:
            return True


class SpaceLayoutService:
    """
    Generates shelf availability maps for UI rendering.
    """
    @staticmethod
    def get_shelf_layout(space: Space) -> list[list[bool]]:
        """
        Constructs a boolean matrix representing shelf availability per rack.

        Args:
            space (Space): The target Space.

        Returns:
            list[list[bool]]: A list of racks, where each inner list contains booleans (True=Available).
        """
        space_shelf_layout = []
        
        total_shelves_per_rack = space.rack_set.first().length // space.rack_set.first().shelf_set.first().length

        available_shelves_per_rack = space.rack_set.annotate(
            available_shelves=Count(
                'shelf',
                filter=Q(shelf__is_available=True),
                distinct=True
            )
        ).order_by('id').values('available_shelves')

        for rack_data in available_shelves_per_rack:
            rack_shelf_layout = [True] * rack_data['available_shelves']
            rack_shelf_layout += [False] * (total_shelves_per_rack - rack_data['available_shelves'])
            space_shelf_layout.append(rack_shelf_layout)
        
        return space_shelf_layout
