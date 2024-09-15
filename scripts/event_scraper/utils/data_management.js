import { getUTCDateString } from "./dates.js";

async function filterOutModifiedEvents(events, venue, sql) {
    const modifiedEvents = await getModifiedEvents(venue, sql);

    if (modifiedEvents.length > 0) {
        return events.filter((event) => {
            for (let modifiedEvent of modifiedEvents) {
                const duplicate = checkDuplicate(event, modifiedEvent);

                if (!duplicate) {
                    return event;
                }
            }
        });
    }

    return events;
}

function checkDuplicate(sourceEvent, modifiedEvent) {
    const modifiedEventDate = getUTCDateString(modifiedEvent.start_date);
    const sameStartDate = sourceEvent.startDate === modifiedEventDate;

    console.log(modifiedEventDate, sourceEvent.startDate);

    const similarTitle = checkSimilarTitle(
        sourceEvent.title,
        modifiedEvent.title,
    );
    const isDuplicate = sameStartDate && similarTitle;
    return isDuplicate;

    function checkSimilarTitle(sourceTitle, modifiedTitle) {
        const title1 = sourceTitle.toLowerCase();
        const title2 = modifiedTitle.toLowerCase();
        return title1.includes(title2) || title2.includes(title1);
    }
}

async function getModifiedEvents(venue, sql) {
    const events =
        await sql`SELECT title, start_date FROM events_event WHERE venue = ${venue} AND manual_upload = TRUE`;
    return events;
}

export { filterOutModifiedEvents };
