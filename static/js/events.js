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
    if (e.target.closest("a.delete")) {
        const details = e.target.closest(".details");
        if (details) {
            const title = details.querySelector(".title").textContent;
            const confirmation = confirm(
                `Are you sure that you want to delete the following event:\n\n${title}\n\nThis operation cannot be reversed.`,
            );
            if (!confirmation) {
                e.preventDefault();
            }
        }
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
            activeSearch.parentElement.after(p);
        }
    });
});

const eventData = document.getElementById("event_data");
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
mutationObserver.observe(eventData, { attributes: true });
