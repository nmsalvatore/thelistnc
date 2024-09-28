import puppeteer from "puppeteer";

async function captureXHR(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    const xhrRequests = [];
    page.on("request", (request) => {
        if (request.resourceType() === "xhr") {
            xhrRequests.push({
                url: request.url(),
                method: request.method(),
            });
        }
    });

    try {
        await page.goto(url, { waitUntil: "networkidle0" });
        return xhrRequests;
    } catch (error) {
        console.error("An error occurred:", error.message);
    } finally {
        await browser.close();
    }

    return xhrRequests;
}

export async function getAPIEndpointByKey(url, key) {
    const xhrRequests = await captureXHR(url);

    console.log(`Retrieving API endpoint containing key "${key}"`);

    for (let request of xhrRequests) {
        try {
            if (!request.url.includes(".json")) {
                continue;
            }

            const response = await fetch(request.url);
            const data = await response.json();
            const isMovieNode = JSON.stringify(data).includes(`"${key}"`);

            if (isMovieNode) {
                const endpoint = request.url;
                console.log("Found API endpoint:", endpoint);
                return endpoint;
            }
        } catch (error) {
            console.error("An error occurred:", error.message);
        }
    }
}
