"""
Business logic for reservation management, pricing, and shelf allocation.
"""
from .models import Booking
from users.models import CustomUser
from django.utils.timezone import localdate
from django.db.models import QuerySet, Count, Q
from listings.models import Space
from listings.services import SpaceService
# from .exceptions import BookingStatusException

class BookingService:
    """
    Handles retrieval, cancellation, and shelf calculation for Bookings.
    """
    @staticmethod
    def get_bookings(space = None, status = None):
        """Retrieves bookings filtered by space or status."""
        bookings = Booking.objects.all()

        if space:
            bookings = bookings.filter(rack__space = space)

        if status:
            bookings = bookings.filter(status = status)

        return bookings

    @staticmethod
    def cancel_booking(booking: Booking, user: CustomUser) -> bool:
        """Cancels a booking if the requesting user is the owner (Lessee)."""
        if booking.lessee == user:
            BookingStateService.update_status(booking, Booking.Status.CANCELLED)
            return True
        else:
            return False
    
    @staticmethod
    def get_total_days(booking: Booking) -> int:
        """Calculates the duration of the booking in days."""
        return DateMgr.get_total_days(booking.start_date, booking.end_date)
    
    @staticmethod
    def get_price_per_day(booking: Booking):
        """Derives the daily cost per shelf from the total price."""
        return booking.total_price / (booking.num_shelves_occupied * BookingService.get_total_days(booking))
    
    @staticmethod
    def get_shelves(booking: Booking) -> QuerySet:
        """
        Retrieves the specific Shelf objects assigned to this booking.
        """
        shelves = booking.rack.shelf_set

        # If the booking is active, we look for shelves marked 'unavailable' (because we are the ones occupying them).
        # If it's just a future booking, we look for 'available' shelves to assign.
        if booking.occupying_space:
            shelves = shelves.filter(is_available = False)
        else:
            shelves = shelves.filter(is_available = True)
        
        # Limit the selection to the number of shelves paid for.
        shelves = shelves.order_by('id')[ : booking.num_shelves_occupied]

        shelf_ids = shelves.values_list('id', flat = True)

        return booking.rack.shelf_set.filter(id__in = shelf_ids)


class BookingStateService:
    """
    Manages the lifecycle state of a Booking (Booked -> Active -> Past).
    """
    @staticmethod
    def is_valid_status(status: str) -> bool:
        return status in Booking.Status.values
    
    @staticmethod
    def update_status_all():
        """Batch updates the status of all bookings in the system."""
        for booking in Booking.objects.all():
            BookingStateService.update_status(booking)

    @staticmethod
    def update_status(booking: Booking, new_status: str = None):
        """Updates a booking's status based on current date or manual override."""
        if new_status:
            if BookingStateService.is_valid_status(new_status):
                booking.status = new_status
        else:
            # Automatic status updates based on the current date
            if not booking.status == Booking.Status.CANCELLED:
                if booking.end_date < localdate():
                    booking.status = Booking.Status.PAST
                elif booking.start_date <= localdate():
                    booking.status = Booking.Status.ACTIVE
                else:
                    booking.status = Booking.Status.BOOKED
        BookingStateService.update_space(booking)
    
    @staticmethod
    def update_space(booking: Booking):
        """Syncs the physical shelf availability with the booking status."""
        # Release space if the booking is over/cancelled but still holds the shelves
        if booking.status != Booking.Status.ACTIVE and booking.occupying_space:
            BookingStateService.release_space(booking)
        # Occupy space if the booking just became active
        elif booking.status == Booking.Status.ACTIVE and not booking.occupying_space:
            BookingStateService.occupy_space(booking)
        '''
        else:
            raise BookingStatusException("Corrupted Data - Value Mismatch")
        '''

        booking.save()
    
    @staticmethod
    def release_space(booking: Booking):
        """Marks shelves associated with the booking as available."""
        BookingService.get_shelves(booking).update(is_available = True)
        booking.occupying_space = False
    
    @staticmethod
    def occupy_space(booking: Booking):
        """Marks shelves associated with the booking as unavailable."""
        BookingService.get_shelves(booking).update(is_available = False)
        booking.occupying_space = True


class BookingFormService:
    """
    Helper logic for booking creation forms.
    """
    @staticmethod
    def get_rack(space: Space, min_shelves: int) -> Space:
        """Finds the first rack in a space that has enough available shelves."""
        return SpaceService.get_racks(space)\
        .annotate(
            available_shelves =
            Count(
                'shelf',
                filter = Q(shelf__is_available = True)
                )
            )\
        .filter(
            available_shelves__gte = min_shelves
            )\
        .order_by(
            'available_shelves'
            )\
        .first()

class DateMgr:
    """Utilities for date calculation."""
    @staticmethod
    def get_total_days(start_date, end_date) -> int:
        return (end_date - start_date).days + 1
