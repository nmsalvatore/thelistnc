import jsdom from "jsdom";
import { extractTimes, formatTime } from "../utils/dates.js";
import { filterOutModifiedEvents } from "../utils/data_management.js";
import { getUTCDateString, getTomorrow } from "../utils/dates.js";

async function getAllEvents(sql) {
    const venue = "Crazy Horse Saloon";
    await sql`DELETE FROM events_event WHERE venue = ${venue} and manual_upload = FALSE`;

    let startDate = getUTCDateString(new Date());
    let pageEvents;
    let events = [];

    do {
        pageEvents = await getPageEvents(startDate);
        if (pageEvents.length > 0) {
            events = events.concat(pageEvents);
            const lastEvent = pageEvents[pageEvents.length - 1];
            const lastDate = lastEvent.startDate;
            startDate = getTomorrow(lastDate);
        }
    } while (pageEvents.length > 0);

    const filteredEvents = await filterOutModifiedEvents(events, venue, sql);
    console.log(`Retrieved ${filteredEvents.length} events from ${venue}`);
    return filteredEvents;
}

async function getPageDocument(startDate) {
    const url = `https://crazyhorsenc.com/shows/list/?tribe-bar-date=${startDate}`;
    const response = await fetch(url);
    const html = await response.text();
    const { JSDOM } = jsdom;
    const dom = new JSDOM(html);
    const document = dom.window.document;
    return document;
}

async function getEventRows(startDate) {
    const pageDocument = await getPageDocument(startDate);
    const selector =
        ".tribe-common-g-row.tribe-events-calendar-list__event-row";
    return pageDocument.querySelectorAll(selector);
}

async function getPageEvents(pageNum) {
    const events = [];
    const rows = await getEventRows(pageNum);

    for (let row of rows) {
        events.push({
            title: getTitle(row),
            venue: "Crazy Horse Saloon",
            city: "Nevada City",
            startDate: getStartDate(row),
            startTime: getStartTime(row),
            endTime: getEndTime(row),
            admission: getAdmission(row),
            url: getUrl(row),
        });
    }

    return events;
}

function getTitle(element) {
    const selector = ".tribe-events-calendar-list__event-title-link";
    const title = element.querySelector(selector);
    return title.textContent.trim();
}

function getStartDate(element) {
    const selector = ".tribe-events-calendar-list__event-date-tag-datetime";
    const datetime = element.querySelector(selector);
    return datetime?.getAttribute("datetime") || null;
}

function getTimes(element) {
    const selector = ".tribe-events-calendar-list__event-datetime";
    const timeString = element.querySelector(selector).textContent;
    const times = extractTimes(timeString);
    return times;
}

function getStartTime(element) {
    const times = getTimes(element);
    const startTime = formatTime(times[0]);
    return startTime;
}

function getEndTime(element) {
    const times = getTimes(element);
    const endTime = formatTime(times[1]);
    return endTime;
}

function getAdmission(element) {
    const selector = ".tribe-events-c-small-cta__price";
    const price = element.querySelector(selector);
    return price?.textContent.trim() || null;
}

function getUrl(element) {
    const selector = ".tribe-events-calendar-list__event-title-link";
    const link = element.querySelector(selector);
    return link?.href || null;
}

export default getAllEvents;
