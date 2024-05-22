// confirmations

function confirmDelete() {
    const titleElement = document.getElementById("id_title");
    const title = titleElement.value;
    return confirm(
        `Are you sure that you want to delete the following event:\n\n${title}\n\nThis operation cannot be reversed.`,
    );
}

function confirmUpdate() {
    return confirm(
        "Are you sure that you want to update this event?\n\nThis operation will overwrite pre-existing data.",
    );
}

// alert user of multiple listing creation if end date exists

function checkForMultipleListings() {
    const endDateField = document.getElementById("id_end_date");
    const endDateValue = endDateField.value;

    if (endDateValue) {
        const startDateField = document.getElementById("id_start_date");
        const startDateValue = startDateField.value;

        const startDate = new Date(formatDate(startDateValue));
        const endDate = new Date(formatDate(endDateValue));
        const allDates = getAllDates(startDate, endDate);
        const allDatesFormatted = allDates.join("\n");

        return confirm(
            `You are about to create identical listings for the following dates:\n\n${allDatesFormatted}\n\nClick OK if you wish to proceed.`,
        );
    }

    function getAllDates(startDate, endDate) {
        const allDates = [];

        let currentDate = startDate;

        while (currentDate <= endDate) {
            allDates.push(currentDate.toLocaleDateString());
            currentDate.setDate(currentDate.getDate() + 1);
        }

        return allDates;
    }

    function formatDate(date) {
        let [year, month, day] = date.split("-");
        return `${month}-${day}-${year}`;
    }
}

// listeners

document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("id_continuous");
    const endDateField = document.getElementById("id_end_date");

    if (checkbox && endDateField) {
        const endDateContainer = endDateField.parentElement;
        const isChecked = checkbox.checked;
        toggleEndDateDisplay(isChecked);

        checkbox.addEventListener("click", () => {
            const isChecked = checkbox.checked;
            toggleEndDateDisplay(isChecked);
        });

        function toggleEndDateDisplay(isChecked) {
            if (isChecked) {
                endDateContainer.style.display = "flex";
            } else {
                endDateContainer.removeAttribute("style");
            }
        }
    }
});
