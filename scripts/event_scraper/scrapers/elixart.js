import { filterOutModifiedEvents } from "../utils/data_management.js";

async function getAllEvents(sql) {
    const venue = "Elixart";
    await sql`DELETE FROM events_event WHERE venue = ${venue} AND manual_upload = FALSE`;

    let pageNum = 1;
    let nextPage;
    let events = [];

    do {
        const data = await getPageEventData(pageNum);
        const pageEvents = getPageEvents(data);
        nextPage = data.pages.nextPage;
        events = events.concat(pageEvents);
        pageNum++;
    } while (nextPage);

    const filteredEvents = await filterOutModifiedEvents(events, venue, sql);
    console.log(`Retrieved ${filteredEvents.length} events from ${venue}`);
    return filteredEvents;
}

async function getPageEventData(pageNum) {
    const response = await fetch(
        `https://api.eventcalendarapp.com/events?id=9221&page=${pageNum}`,
    );
    const data = response.json();
    return data;
}

function getPageEvents(data) {
    const events = [];

    for (let event of data.events) {
        const title = getTitle(event);
        if (!title) continue;

        events.push({
            title: title,
            venue: "Elixart",
            city: "Nevada City",
            startDate: getStartDate(event),
            startTime: getStartTime(event),
            endTime: getEndTime(event),
            admission: getAdmissionPrice(event),
            url: getUrl(event),
        });
    }

    return events;
}

function getTitle(event) {
    const title = event.summary?.trim();
    return title;
}

function getStartDate(event) {
    const date = event.timezoneStart.split("T");
    return date[0];
}

function getStartTime(event) {
    const dateString = event.timezoneStart;
    const time = getTime(dateString);
    return time;
}

function getEndTime(event) {
    const dateString = event.timezoneEnd;
    const time = getTime(dateString);
    return time;
}

function getTime(dateString) {
    const time = dateString.split("T");
    return time[1];
}

function getAdmissionPrice(event) {
    const text = event.description;
    if (!text) {
        return null;
    }

    const prices = matchPrices(text);
    if (!prices) {
        return null;
    }

    const [minPrice, maxPrice] = getMinMaxPrices(prices);
    const priceString = formatPriceString(minPrice, maxPrice);
    return priceString;
}

function formatPriceString(minPrice, maxPrice) {
    if (minPrice === maxPrice) {
        return `$${minPrice}`;
    }
    return `$${minPrice}-$${maxPrice}`;
}

function getMinMaxPrices(prices) {
    const numericPrices = prices.map((price) => Number(price.slice(1)));
    const minPrice = Math.min(...numericPrices);
    const maxPrice = Math.max(...numericPrices);
    return [minPrice, maxPrice];
}

function matchPrices(text) {
    const regex = /\$\d+/g;
    const prices = text.match(regex);
    return prices;
}

function getUrl(event) {
    const url = event.ticketsLink;
    return url || "https://elixart.com/pages/events";
}

export default getAllEvents;
