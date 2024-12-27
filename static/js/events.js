const backToTopButton = document.querySelector("a.back-to-top");

document.addEventListener("scroll", (e) => {
    const backToTopButtonVisible = backToTopButton.style.bottom === "0";

    if (window.scrollY !== 0) {
        if (!backToTopButtonVisible) {
            backToTopButton.style.bottom = "0";
        }
    } else {
        backToTopButton.style.bottom = "-38.5px";
    }
});

document.addEventListener("click", (e) => {
    try {
        const deleteButton = e.target.closest("a.delete");
        if (deleteButton) {
            const sortGroup = deleteButton.closest(".sort-group");
            const event = deleteButton.closest("li.event");

            let titleElement;
            if (sortGroup.classList.contains("by-title")) {
                titleElement = sortGroup.querySelector("hgroup h2.title");
            } else {
                titleElement = event.querySelector(".title");
            }

            let dateElement;
            if (sortGroup.classList.contains("by-date")) {
                dateElement = sortGroup.querySelector("hgroup time.date");
            } else {
                dateElement = event.querySelector(".date > a");
            }

            const timeElement = event.querySelector(".start-time");
            const time = timeElement?.textContent.trim();
            const title = titleElement?.textContent.trim();
            const date = dateElement?.textContent.trim();

            const confirmation = confirm(
                `Are you sure that you want to delete the following event:

                "${title.trim()}" on ${date.trim()} at ${time.trim()}

                This operation cannot be reversed.`,
            );

            if (!confirmation) {
                e.preventDefault();
            }
        }
    } catch (error) {
        e.preventDefault();
        throw new Error("Failed to delete event:", error);
    }
});

const sortOptions = document.querySelectorAll("#sort_options > a.option");
sortOptions.forEach((option) => {
    option.addEventListener("click", () => {
        sortOptions.forEach((option) => (option.dataset.activeSort = false));
        option.dataset.activeSort = true;

        const p = document.createElement("p");
        p.id = "loading_event_data";
        p.textContent = "Loading event data...";

        const activeSearch = document.getElementById("active_search");
        if (activeSearch) {
            activeSearch.value = "";

            const loading = document.getElementById("loading_event_data");
            if (!loading) {
                activeSearch.parentElement.after(p);
            }
        }
    });
});

function callback(mutationsList) {
    mutationsList.forEach((mutation) => {
        if (mutation.target.classList.length === 0) {
            const loading = document.getElementById("loading_event_data");
            if (loading) {
                loading.remove();
            }
        }
    });
}

const mutationObserver = new MutationObserver(callback);
const eventData = document.getElementById("event_data");

if (eventData) {
    mutationObserver.observe(eventData, { attributes: true });
}
