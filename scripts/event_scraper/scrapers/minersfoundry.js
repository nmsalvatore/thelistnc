import jsdom from "jsdom";
import { filterOutModifiedEvents } from "../utils/data_management.js";

export default getAllEvents;

scrapeEvents();

async function getAllEvents(sql) {
    const venue = "Miners Foundry Cultural Center";
    await sql`DELETE FROM events_event WHERE (venue = ${venue}) AND manual_upload = FALSE`;
    const events = await scrapeEvents();
    const filteredEvents = await filterOutModifiedEvents(events, venue, sql);
    console.log(`Retrieved ${filteredEvents.length} events from ${venue}`);
    return filteredEvents;
}

async function scrapeEvents() {
    try {
        const url = "https://minersfoundry.org/all-events/";
        const mainDocument = await getPageDocument(url);
        if (!mainDocument) {
            throw new Error("Failed to load main listing page");
        }

        const listingImages = mainDocument.querySelectorAll(
            ".listing-item a.image",
        );
        if (!listingImages || listingImages.length === 0) {
            console.log("No events found on the page");
            return [];
        }

        const events = [];

        for (const listingImage of listingImages) {
            try {
                const url = listingImage.href;
                if (!url) {
                    console.warn("Skipping event - no URL found");
                    continue;
                }

                await new Promise((resolve) => setTimeout(resolve, 1000));

                const eventDocument = await getPageDocument(url);
                if (!eventDocument) {
                    console.warn(`Failed to load event page: ${url}`);
                    continue;
                }

                const event = {
                    title: getEventTitle(eventDocument),
                    venue: getEventVenue(eventDocument),
                    city: getEventCity(eventDocument),
                    startDate: getEventStartDate(eventDocument),
                    startTime: getEventStartTime(eventDocument),
                    endTime: getEventEndTime(eventDocument),
                    admission: getEventAdmission(eventDocument),
                    url,
                };

                if (!event.title || !event.startDate) {
                    console.warn(
                        `Skipping event - missing required data: ${url}`,
                    );
                    continue;
                }

                events.push(event);
            } catch (eventError) {
                console.error("Error processing individual event:", eventError);
                continue;
            }
        }

        return events;
    } catch (error) {
        console.error("Error in scrapeEvents:", error);
        throw error;
    }
}

async function getPageDocument(url) {
    try {
        if (!url || typeof url !== "string") {
            throw new Error("Invalid URL provided");
        }

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const html = await response.text();
        if (!html) {
            throw new Error("No HTML content received");
        }

        const { JSDOM } = jsdom;
        if (!JSDOM) {
            throw new Error("JSDOM not available");
        }

        const dom = new JSDOM(html);
        if (!dom || !dom.window || !dom.window.document) {
            throw new Error("Failed to create valid DOM");
        }

        return dom.window.document;
    } catch (error) {
        console.error("Error fetching page document:", error);
        throw error;
    }
}

function getEventTitle(document) {
    try {
        const element = document.querySelector(
            ".tribe-events-single-event-title",
        );
        if (!element) {
            return null;
        }

        const title = element.textContent;
        if (!title) {
            return null;
        }

        return title;
    } catch (error) {
        console.error("Error getting event title:", error);
    }
}

function getEventVenue(document) {
    try {
        const element = document.getElementById("tribe-events-header");
        if (!element) {
            return null;
        }

        const data = element.getAttribute("data-title");
        if (!data || typeof data !== "string") {
            return null;
        }

        const matches = data.match(/–\s*(.*?)\s*–/);
        if (!matches || !matches[1]) {
            return null;
        }

        const venue = matches[1].trim();
        if (!venue) {
            return null;
        }

        return venue;
    } catch (error) {
        console.error("Error getting event venue:", error);
        return null;
    }
}

function getEventCity(document) {
    try {
        const element = document.getElementById("tribe-events-header");
        if (!element) {
            return null;
        }

        const data = element.getAttribute("data-title");
        if (!data || typeof data !== "string") {
            return null;
        }

        const segments = data.split("–");
        if (!segments.length) {
            return null;
        }

        const lastSegment = segments.pop();
        if (!lastSegment) {
            return null;
        }

        const matches = lastSegment.match(/([^,]+),/);
        return matches ? matches[1].trim() : null;
    } catch (error) {
        console.error("Error getting event city:", error);
        return null;
    }
}

function getEventStartDate(document) {
    try {
        const element = document.querySelector(".tribe-event-date-start");
        if (!element) {
            return null;
        }

        const data = element.textContent;
        if (!data || data.trim() === "") {
            return null;
        }

        const date = extractDate(data);
        if (!date) {
            return null;
        }

        return date;
    } catch (error) {
        console.error("Error getting event start date:", error);
        return null;
    }
}

function extractDate(dateString) {
    const currentYear = new Date().getFullYear();
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

    const match = dateString.match(/([A-Za-z]+)\s+(\d{1,2})(?:,\s*(\d{4}))?/);
    if (!match) return null;

    const month = months[match[1]];
    const day = match[2].padStart(2, "0");
    const year = match[3] || currentYear;
    return `${year}-${month}-${day}`;
}

function getEventStartTime(document) {
    try {
        const element = document.querySelector(".tribe-event-date-start");
        if (!element) {
            return null;
        }

        const data = element.textContent;
        if (!data || data.trim() === "") {
            return null;
        }

        const time = extractTime(data);
        if (!time) {
            return null;
        }

        return time;
    } catch (error) {
        console.error("Error getting event start time:", error);
        return null;
    }
}

function getEventEndTime(document) {
    try {
        const element = document.querySelector(".tribe-event-time");
        if (!element) {
            return null;
        }

        const data = element.textContent;
        if (!data || data.trim() === "") {
            return null;
        }

        const time = extractTime(data);
        if (!time) {
            return null;
        }

        return time;
    } catch (error) {
        console.error("Error getting event end time:", error);
        return null;
    }
}

function extractTime(str) {
    try {
        if (!str || typeof str !== "string") {
            return null;
        }

        const matches = str.match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i);
        if (!matches) return null;

        let hour = parseInt(matches[1], 10);
        const minutes = matches[2];
        const period = matches[3].toUpperCase();

        // Validate hour and minutes
        if (isNaN(hour) || hour < 0 || hour > 12) {
            return null;
        }

        const minutesNum = parseInt(minutes, 10);
        if (isNaN(minutesNum) || minutesNum < 0 || minutesNum > 59) {
            return null;
        }

        if (period === "PM" && hour !== 12) {
            hour += 12;
        } else if (period === "AM" && hour === 12) {
            hour = 0;
        }

        return `${hour.toString().padStart(2, "0")}:${minutes}`;
    } catch (error) {
        console.error("Error extracting time:", error);
        return null;
    }
}

function getEventAdmission(document) {
    try {
        const element = document.querySelector(".tribe-events-cost");
        if (!element) {
            return null;
        }

        const admission = element.textContent;
        if (!admission || admission.trim() === "") {
            return null;
        }

        return admission.trim();
    } catch (error) {
        console.error("Error getting event admission:", error);
        return null;
    }
}
