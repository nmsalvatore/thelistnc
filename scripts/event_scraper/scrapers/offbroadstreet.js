import jsdom from "jsdom";

scrapeEvents();

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

        const eventWrappers = srcDocument.querySelectorAll("tr.event-wrapper");
        for (const eventWrapper of eventWrappers) {
            const title = eventWrapper.querySelector(
                "span[itemprop='name']",
            )?.textContent;
            events.push({ title });
        }
    }

    console.log(events);
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
