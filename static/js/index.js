// confirmations

function confirmDelete() {
    return confirm('Are you sure that you want to delete this event?\n\nThis operation cannot be reversed.')
}

function confirmUpdate() {
    return confirm('Are you sure that you want to update this event?\n\nThis operation will overwrite pre-existing data.')
}

// listeners

document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('id_continuous');
    const endDateField = document.getElementById('id_end_date');
    const endDateContainer = endDateField.parentElement;
    const isChecked = checkbox.checked;
    toggleEndDateDisplay(isChecked)

    checkbox.addEventListener('click', () => {
        const isChecked = checkbox.checked;
        toggleEndDateDisplay(isChecked)
    });

    function toggleEndDateDisplay(isChecked) {
        if (isChecked) {
            endDateContainer.style.display = 'flex';
        } else {
            endDateContainer.removeAttribute('style');
        }
    }
});