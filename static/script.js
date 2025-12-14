/**
 * Calculates date difference in days (inclusive).
 */
function daysBetween(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    if (d1 > d2) return 0; // Invalid range
    const diffTime = Math.abs(d2 - d1);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // +1 to be inclusive
}

/**
 * Handles date changes on the booking form to update the price summary.
 */
function updateBookingSummary() {
    const startDate = document.getElementById('book-start-date').value;
    const endDate = document.getElementById('book-end-date').value;

    const numShelvesText = document.getElementById('book-shelf-count').textContent.trim();
    const numShelves = parseInt(numShelvesText) || 0;

    const priceText = document.getElementById('book-shelf-price').textContent.trim();
    // Use a regular expression to extract the numeric price (e.g., "2.50" from "$2.50 per day")
    const priceMatch = priceText.match(/\$(\d+\.\d{2})/);
    const pricePerShelf = priceMatch ? parseFloat(priceMatch[1]) : 0;

    const summaryEl = document.getElementById('booking-summary');
    
    if (startDate && endDate && numShelves > 0) {
        const numDays = daysBetween(startDate, endDate);
        
        if (numDays > 0) {
            const pricePerDay = numShelves * pricePerShelf;
            const totalPrice = numDays * pricePerDay;
            
            document.getElementById('book-total-days').textContent = numDays;
            document.getElementById('book-price-per-day').textContent = `$${pricePerDay.toFixed(2)}`;
            document.getElementById('book-total-price').textContent = `$${totalPrice.toFixed(2)}`;
            summaryEl.classList.remove('d-none');
        } else {
            summaryEl.classList.add('d-none');
        }
    } else {
            summaryEl.classList.add('d-none');
    }
}


// --- APP INITIALIZATION (Event Listeners) ---
document.addEventListener('DOMContentLoaded', () => {
    // Only attach listeners if the form exists (i.e., we are on the booking page)
    const startDateEl = document.getElementById('book-start-date');
    const endDateEl = document.getElementById('book-end-date');

    if (startDateEl && endDateEl) {
        startDateEl.addEventListener('change', updateBookingSummary);
        endDateEl.addEventListener('change', updateBookingSummary);
        
        // Run once on load to populate if dates are pre-filled
        updateBookingSummary(); 
    }

});

document.addEventListener('DOMContentLoaded', () => {
    const cancelModal = document.getElementById('cancelBookingModal');
    if (cancelModal) {
        cancelModal.addEventListener('show.bs.modal', function (event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            
            // Extract info from data-bs-booking-id attribute
            const bookingId = button.getAttribute('data-bs-booking-id');
            
            // Find the hidden input in the modal
            const bookingIdInput = cancelModal.querySelector('#modalBookingId');

            var cancelForm = document.getElementById('cancelBookingForm');
            
            // Update the hidden input's value
            if (bookingIdInput) {
                bookingIdInput.value = bookingId;
                cancelForm.action = `/bookings/cancel/${bookingId}/`;
            }
        });
    }

});

document.addEventListener('DOMContentLoaded', () => {
    const bookingItems = document.querySelectorAll('.js-booking-item');

    bookingItems.forEach(item => {
    // find options panel once per item
    const optionsDiv = item.querySelector('.js-booking-option');

    // nothing to do if an item has no options block
    if (!optionsDiv) return;

    // stop clicks on interactive elements inside options from bubbling up
    optionsDiv.addEventListener('click', (e) => {
        const interactive = e.target.closest('a, button, input, label, select, textarea, .dropdown-item');
        if (interactive) e.stopPropagation();
    });

    // toggle options when clicking the item (but not when clicking inside options)
    item.addEventListener('click', (event) => {
        // if click happened inside the options area, ignore (safety double-check)
        if (optionsDiv.contains(event.target) || event.target.closest('.js-booking-option')) {
        return;
        }
        optionsDiv.classList.toggle('d-none');
    });
    });

    bookingItems.forEach(clickedItem => {
            clickedItem.addEventListener('click', function() {
            // FIX HERE: Changed selector to .js-booking-option (singular)
            const clickedOptions = this.querySelector('.js-booking-option'); 

            // Loop through all items again
            bookingItems.forEach(otherItem => {
                // FIX HERE: Changed selector to .js-booking-option (singular)
                const otherOptions = otherItem.querySelector('.js-booking-option');
                
                // Hide options on all other items *if* they are currently visible.
                if (otherOptions && otherOptions !== clickedOptions) {
                    otherOptions.classList.add('d-none');
                }
            });
            });
    });

});

document.addEventListener('DOMContentLoaded', function() {
    const locationSelect = document.querySelector('select[name="location-area"]');
    const priceInput = document.getElementById('shelf-price');

    if (locationSelect && priceInput) {
        locationSelect.addEventListener('change', function() {
            const selectedCode = this.value;
            if (PRICE_MAP[selectedCode] !== undefined) {
                priceInput.value = PRICE_MAP[selectedCode];
            } else {
                priceInput.value = 6.99.toFixed(2);
            }
        });
    }
});

document.getElementById('logout-button').addEventListener('click', function(e){
  e.preventDefault();
  document.getElementById('logout-form').submit();
});
