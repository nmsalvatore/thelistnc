const colorSchemes = [
    "scheme-1",
    "scheme-2",
    "scheme-3",
    "scheme-4",
    "scheme-5",
    "scheme-6",
];

function setColorScheme() {
    const savedColorScheme = getSavedColorScheme();
    if (savedColorScheme) {
        setSavedColorScheme(savedColorScheme);
    } else {
        setDefaultColorScheme();
    }
    setBodyToVisible();
}

function getSavedColorScheme() {
    const savedColorSchemeIndex = localStorage.getItem("colorSchemeIndex");
    const savedColorScheme = colorSchemes[savedColorSchemeIndex];
    return savedColorScheme;
}

function setDefaultColorScheme() {
    if (darkModeEnabled()) {
        document.body.classList.add("scheme-5");
    } else {
        document.body.classList.add("scheme-1");
    }
}

function setSavedColorScheme(savedColorScheme) {
    document.body.classList.add(savedColorScheme);
}

function darkModeEnabled() {
    return (
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches
    );
}

function setDefaultColorSchemeChangeListener() {
    setDarkModeChangeListener();
    setLightModeChangeListener();
}

function setDarkModeChangeListener() {
    const query = window.matchMedia("(prefers-color-scheme: dark)");
    query.addEventListener("change", (e) => {
        if (e.matches) {
            localStorage.removeItem("colorSchemeIndex");
            document.body.className = "";
            document.body.classList.add("scheme-5");
        }
    });
}

function setLightModeChangeListener() {
    const query = window.matchMedia("(prefers-color-scheme: light)");
    query.addEventListener("change", (e) => {
        if (e.matches) {
            localStorage.removeItem("colorSchemeIndex");
            document.body.className = "";
            document.body.classList.add("scheme-1");
        }
    });
}

const setBodyToVisible = () => (document.body.style.visibility = "visible");

document.addEventListener("DOMContentLoaded", () => {
    setDefaultColorSchemeChangeListener();
    setColorScheme();
});
