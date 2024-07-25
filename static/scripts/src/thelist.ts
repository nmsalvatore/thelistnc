document.addEventListener("DOMContentLoaded", () => {
    renderEvents();
    setSearchListener();
});

function renderEvents(filterValue = "") {
    const eventDataScript = document.getElementById(
        "event_data",
    ) as HTMLScriptElement;
    const eventData = eventDataScript.textContent as string;
    const events = JSON.parse(eventData).map((event) => event.fields);
    const filteredEvents = filterEvents(events, filterValue);
    const groupedData = groupEventsByDate(filteredEvents);

    const eventList = document.querySelector(".the-list") as HTMLDivElement;
    eventList.innerHTML = "";

    for (const date in groupedData) {
        const groupContainer = document.createElement("div") as HTMLDivElement;
        const groupList = document.createElement("ul") as HTMLUListElement;
        const groupHeading = document.createElement("h2") as HTMLHeadingElement;
        const groupEvents = groupedData[date];

        groupContainer.className = "group";
        groupHeading.textContent = formatDate(date);
        groupHeading.className = "group-heading";
        groupList.className = "group-list";

        for (const event of groupEvents) {
            const listItem = document.createElement("li") as HTMLLIElement;
            listItem.className = "list-item";

            const timeText = getTimeText(event);
            const eventText = document.createTextNode(
                `${timeText} - ${event.title} at ${event.venue}, ${event.city}`,
            );

            if (event.url) {
                const link = document.createElement("a") as HTMLAnchorElement;
                link.href = event.url;
                link.appendChild(eventText);
                listItem.appendChild(link);
            } else {
                listItem.appendChild(eventText);
            }

            groupList.appendChild(listItem);
        }

        groupContainer.appendChild(groupHeading);
        groupContainer.appendChild(groupList);
        eventList.appendChild(groupContainer);
    }
}

function groupEventsByDate(events) {
    const dates = new Set(events.map((event) => event.start_date));
    const data = {};

    for (const date of dates) {
        data[date] = events.filter((event) => event.start_date === date);
    }

    return data;
}

function setSearchListener() {
    const searchInput = document.getElementById(
        "event_search",
    ) as HTMLInputElement;
    searchInput.addEventListener("keyup", (e) => {
        const target = e.target as HTMLInputElement;
        const value = target.value;
        renderEvents(value);
    });
}

function filterEvents(events, filterValue) {
    const filteredEvents = events.filter((event) => {
        const title = event.title.toLowerCase();
        const venue = event.venue.toLowerCase();
        const city = event.city.toLowerCase();
        const searchString = `__${title} __${venue} __${city} `;

        if (searchString.includes(filterValue)) {
            return event;
        }
    });
    return filteredEvents;
}

function formatTime(time) {
    let [hours, minutes, seconds] = time.split(":");
    let period = "am";

    hours = Number(hours);

    if (hours === 0) {
        hours = 12;
    }

    if (hours > 12) {
        hours -= 12;
        period = "pm";
    }

    if (Number(minutes) != 0) {
        return `${hours}:${minutes}${period}`;
    }

    return `${hours}${period}`;
}

function formatDate(dateString) {
    const [year, month, day] = dateString.split("-");
    return new Date(year, month - 1, day).toLocaleDateString("en-US", {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

function getTimeText(event) {
    const startTime = formatTime(event.start_time);
    let timeText = "";

    if (event.end_time) {
        const endTime = formatTime(event.end_time);
        timeText = `${startTime}-${endTime}`;
    } else {
        timeText = `${startTime}`;
    }

    return timeText;
}
