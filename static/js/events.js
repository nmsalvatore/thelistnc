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

const sortOptions = document.querySelectorAll("a.option");
sortOptions.forEach((option) => {
    option.addEventListener("click", () => {
        sortOptions.forEach((option) => (option.dataset.activeSort = false));
        option.dataset.activeSort = true;
        const activeSearch = document.getElementById("active_search");
        activeSearch.value = "";
    });
});
