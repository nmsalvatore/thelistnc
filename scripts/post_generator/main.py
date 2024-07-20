import os
import psycopg
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from decouple import config


def get_todays_events():
    dbname = config("DB_NAME")
    dbuser = config("DB_USER")
    dbpass = config("DB_PASSWORD")
    with psycopg.connect(
        host="localhost",
        port="5432",
        user=dbuser,
        password=dbpass,
        dbname=dbname
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT title, start_date, start_time, end_time, venue FROM events_event WHERE start_date = (CURRENT_TIMESTAMP AT TIME ZONE 'America/Los_Angeles')::date ORDER BY start_time ASC, end_time ASC, title ASC")
            events = cur.fetchall()
    return events


def create_event_image(events, page_num):
    title_font_size = 32
    date_font_size = 60
    body_font_size = 26

    body_font = ImageFont.truetype("fonts/Inter-Medium.ttf", body_font_size)

    darkest_fill = "#084747"
    dark_fill = "#006F6F"
    medium_fill = "#99CCCC"
    light_fill = "#F1F8F8"
    primary_fill = "#008080"
    accent_fill = "#d56100"

    img = Image.new("RGB", (1080, 1080), color="white")
    draw = ImageDraw.Draw(img)

    x_pos = (17 + 80)
    y_pos = (17 + 80 + title_font_size)

    draw_background(draw, outline_fill=medium_fill, shadow_fill=light_fill, outline_width=2)
    draw_site_title(draw, x_pos,y_pos , darkest_fill, primary_fill, title_font_size)

    if page_num == 1:
        y_pos += (date_font_size + 70)
        draw_date(draw, x_pos, y_pos, primary_fill, 60)

    y_pos += 115
    leftover_events = draw_events(draw, x_pos, y_pos, events, body_font, dark_fill, darkest_fill)

    if len(leftover_events) == 0:
        draw_conclusion_text(draw, x_pos, (1062 - 80), darkest_fill, primary_fill)
    else:
        paste_arrow_icon(img)


    today = date.today()
    today_id = today.strftime("%Y%m%d")
    path = f"../../ig_posts/{today_id}"

    if not os.path.exists(path):
        os.mkdir(path)

    img.save(f"{path}/{today_id}_{page_num}.png")
    return leftover_events


def paste_arrow_icon(img):
    icon = Image.open("icons/arrow_right_dark_solid.png")
    x_pos = (1062 - (80 + int(icon.width / 1.5)))
    y_pos = (1062 - (80 + int(icon.height / 1.5)))
    img.paste(icon, (x_pos, y_pos), icon)


def draw_events(draw, x_pos, y_pos, events, font, time_fill, event_fill):
    leftover_events = []

    for event in events:
        title = event[0]
        venue = event[4]

        if "downtown" in venue.lower():
            event_text = f"{title} in {venue}"
        if venue.lower() == "union street":
            event_text = f"{title} on {venue}"
        else:
            event_text = f"{title} @ {venue}"

        event_time = get_event_time(event)

        if y_pos < (1062 - 200):
            draw.text((x_pos, y_pos), f"{event_time}", fill=time_fill, font=font, anchor="ls")
            y_pos = draw_wrapped_text(draw, event_text, font=font, max_width=(1062 - 80 - 300), x=300, y=y_pos, fill=event_fill, anchor="ls")
        else:
            leftover_events.append(event)

    return leftover_events


def draw_background(draw, outline_fill, shadow_fill, outline_width, background_fill="#fff"):
    draw.rectangle((23, 23, 1069, 1069), shadow_fill)
    draw.rectangle((17, 17, 1062, 1062), background_fill, outline=outline_fill, width=outline_width)


def draw_site_title(draw, x_pos, y_pos, fill1, fill2, font_size):
    font = ImageFont.truetype("fonts/Inter-Medium.ttf", font_size)
    text = "The List NC"
    draw_text_with_last_word_accented(draw, x_pos, y_pos, text, font, fill1, fill2, anchor="ls")


def draw_date(draw, x_pos, y_pos, fill, font_size):
    date_font = ImageFont.truetype("fonts/IBMPlexSans-Medium.ttf", font_size)
    today = date.today().strftime("%a, %B %d")
    draw.text((x_pos, y_pos), today, fill=fill, font=date_font, anchor="ls")


def draw_conclusion_text(draw, x_pos, y_pos, fill1, fill2):
    font = ImageFont.truetype("fonts/Inter-Medium.ttf", 28)
    text = "For more information, visit thelistnc.org"
    draw_text_with_last_word_accented(draw, x_pos, y_pos, text, font, fill1, fill2, anchor="ls")


def draw_text_with_last_word_accented(draw, x_pos, y_pos, text, font, main_fill, accent_fill, anchor):
    words = text.split()
    for index, word in enumerate(words):
        segment = word + " "
        width = draw.textlength(segment, font=font)
        last_index = len(words)-1
        if index < last_index:
            draw.text((x_pos, y_pos), segment, fill=main_fill, font=font, anchor=anchor)
        else:
            draw.text((x_pos, y_pos), segment, fill=accent_fill, font=font, anchor=anchor)
        x_pos += width


def draw_wrapped_text(draw, text, font, max_width, x, y, fill, anchor):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)
    for index, event in enumerate(lines):
        draw.text((x, y), event.strip(), font=font, fill=fill, anchor=anchor)
        if index == len(lines)-1:
            y += 60
        else:
            y += 40

    return y

def get_event_time(event):
    start_time = get_natural_time(event[2])
    end_time = get_natural_time(event[3])
    event_time = start_time
    return event_time


def get_natural_time(time):
    if time == None:
        return ""
    hour = int(time.strftime("%I"))
    minutes = int(time.strftime("%M"))
    am_pm = time.strftime("%p").lower()
    if minutes:
        return f"{hour}:{minutes}{am_pm}"
    else:
        return f"{hour}{am_pm}"


if __name__ == "__main__":
    page_num = 1
    events = get_todays_events()
    leftover_events = create_event_image(events, page_num)

    while True:
        page_num += 1
        if len(leftover_events) < 1:
            break;
        else:
            leftover_events = create_event_image(leftover_events, page_num)
