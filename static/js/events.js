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
