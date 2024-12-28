import { filterOutModifiedEvents } from "../utils/data_management.js";

async function getAllEvents(sql) {
    const venue = "Friar Tuck's Restaurant & Bar";
    await sql`DELETE FROM events_event WHERE venue = ${venue} AND manual_upload = FALSE`;

    const events = await getEvents();
    const filteredEvents = await filterOutModifiedEvents(events, venue, sql);
    console.log(`Retrieved ${filteredEvents.length} events from ${venue}`);
    return filteredEvents;
}

async function getEventData(month, year) {
    const response = await fetch(
        `https://www.friartucks.com/api/open/GetItemsByMonth?month=${month}-${year}&collectionId=66e0e02849d6b726adc8fdc1&crumb=BdJE6NxHlozbMzA2M2QwN2I5OGRmZTEzZGE1YjJiNzI3NjVlZmJh`,
    );
    return response.json();
}

async function getEvents() {
    let month = new Date().getMonth() + 1;
    let year = new Date().getFullYear();

    let monthEvents = await getMonthEvents(month, year);
    let events = [].concat(monthEvents);

    while (monthEvents.length !== 0) {
        month = Number(month);
        month += 1;

        if (month > 12) {
            month = 1;
            year += 1;
        }

        month = month.toString().padStart(2, "0");
        monthEvents = await getMonthEvents(month, year);
        events = events.concat(monthEvents);
    }

    return events;
}

async function getMonthEvents(month, year) {
    const ROOT_URL = "https://www.friartucks.com/live-music/";
    const events = [];

    const data = await getEventData(month, year);

    for (const event of data) {
        const title = event.title.replace("&amp;", "&").trim();
        if (!title) {
            continue;
        }

        const startDateInSeconds = event.startDate;
        if (!startDateInSeconds) {
            continue;
        }

        const start = new Date(startDateInSeconds);
        const dateOptions = { timeZone: "America/Los_Angeles" };
        const startDate = start.toLocaleDateString("en-US", dateOptions);
        const startTime = start.toLocaleTimeString("en-US", dateOptions);

        const end = new Date(event.endDate);
        const endTime = end.toLocaleTimeString("en-US", dateOptions);

        const url = ROOT_URL + event.urlId;
        const venue = "Friar Tuck's Restaurant & Bar";
        const city = "Nevada City";
        const admission = null;

        events.push({
            title,
            venue,
            city,
            startDate,
            startTime,
            endTime,
            url,
            admission,
        });
    }

    return events;
}

export default getAllEvents;
