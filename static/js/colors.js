function cycleColorScheme() {
    const savedSchemeIndex = localStorage.getItem("colorSchemeIndex");
    const noSavedScheme = savedSchemeIndex === null;

    let currentSchemeIndex;

    if (noSavedScheme) {
        if (darkModeEnabled()) {
            currentSchemeIndex = 4;
        } else {
            currentSchemeIndex = 0;
        }
    } else {
        currentSchemeIndex = Number(savedSchemeIndex);
    }

    document.body.classList.remove(colorSchemes[currentSchemeIndex]);
    currentSchemeIndex = (currentSchemeIndex + 1) % colorSchemes.length;
    document.body.classList.add(colorSchemes[currentSchemeIndex]);
    localStorage.setItem("colorSchemeIndex", currentSchemeIndex);
}

const colorCycleButton = document.querySelector("button#colorCycle");
colorCycleButton.addEventListener("click", cycleColorScheme);
