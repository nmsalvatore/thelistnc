import jsdom from "jsdom";
import { filterOutModifiedEvents } from "../utils/data_management.js";

export default getAllEvents;

async function getAllEvents(sql) {
    const venue = "Off Broadstreet";
    await sql`DELETE FROM events_event WHERE (venue = ${venue}) AND manual_upload = FALSE`;
    const events = await scrapeEvents();
    const filteredEvents = await filterOutModifiedEvents(events, venue, sql);
    console.log(`Retrieved ${filteredEvents.length} events from ${venue}`);
    return filteredEvents;
}

async function scrapeEvents() {
    const url = "https://www.offbroadstreet.com/calendar.htm";

    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error: status ${response.status}`);
    }

    const html = await response.text();
    if (!html) {
        throw new Error(`No HTML received from: ${url}`);
    }

    const document = getHTMLDocument(html);
    if (!document) {
        throw new Error("Failed to create valid HTML document");
    }

    const events = [];

    const iframes = document.querySelectorAll("iframe");
    for (const iframe of iframes) {
        const src = iframe.src;
        const response = await fetch(src);
        const srcHTML = await response.text();
        const srcDocument = getHTMLDocument(srcHTML);

        const eventContainers =
            srcDocument.querySelectorAll("tr.event-wrapper");
        for (const eventContainer of eventContainers) {
            const event = {
                title: getTitle(eventContainer),
                venue: "Off Broadstreet",
                city: "Nevada City",
                startDate: getStartDate(eventContainer),
                startTime: getStartTime(eventContainer),
                endTime: null,
                admission: null,
                url: getUrl(eventContainer),
            };

            events.push(event);
        }
    }

    return events;
}

function getHTMLDocument(html) {
    if (typeof html !== "string") {
        throw new TypeError("HTML input must be a string");
    }

    try {
        const { JSDOM } = jsdom;
        const dom = new JSDOM(html);
        const document = dom.window.document;
        return document;
    } catch (error) {
        throw new Error(`Failed to parse HTML with JSDOM: ${error.message}`);
    }
}

function getTitle(element) {
    const title = element.querySelector("span[itemprop='name']");

    if (!title) {
        return null;
    }

    return title.textContent;
}

function getStartDate(element) {
    const dateString = getDateString(element);
    if (!dateString) {
        return null;
    }

    const date = formatDate(dateString);
    return date;
}

function getStartTime(element) {
    const dateString = getDateString(element);
    if (!dateString) {
        return null;
    }

    const time = formatTime(dateString);
    return time;
}

function getDateString(element) {
    const time = element.querySelector("time[itemprop='startDate']");
    if (!time) {
        return null;
    }

    const dateString = time.getAttribute("content");
    if (!dateString) {
        return null;
    }

    return dateString;
}

function formatDate(dateString) {
    const datePart = dateString.split("-")[0].trim();
    const components = datePart.split(",");
    const dateWithoutDay = components[1].trim();

    const [monthStr, day] = dateWithoutDay.split(" ");
    const year = components[2].trim();

    const months = {
        January: "01",
        February: "02",
        March: "03",
        April: "04",
        May: "05",
        June: "06",
        July: "07",
        August: "08",
        September: "09",
        October: "10",
        November: "11",
        December: "12",
    };

    const month = months[monthStr];

    return `${month}-${day.padStart(2, "0")}-${year}`;
}

function formatTime(dateString) {
    const components = dateString.split("-");
    const time = components[1].trim();
    return time;
}

function getUrl(element) {
    const url = element.querySelector("a.btn-success.float-right")?.href;
    if (!url) {
        return null;
    }

    return "https://offbroadstreet.thundertix.com" + url;
}
