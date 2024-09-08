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
    base_font_size = 30
    regular_font = ImageFont.truetype("fonts/IBMPlexMono-Regular.ttf", base_font_size)
    bold_font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", base_font_size)

    color1 = "#f9f7f6"
    color2 = "#f1eae4"
    color3 = "#457aa1"
    color4 = "#204560"

    img = Image.new("RGB", (1080, 1080), color=color1)
    draw = ImageDraw.Draw(img)

    # draw site title
    x = base_font_size * 3
    y = base_font_size * 3
    draw_site_title(draw, x, y, color4, color3, color2)

    # draw post date
    y = y + 15 + (base_font_size * 3)
    draw_date(draw, x, y, color4)

    # draw events
    y = y + 45 + (base_font_size * 3)
    draw_events(draw, x, y, events, time_fill=color4, event_fill=color4)

    # set image path
    today = date.today()
    today_id = today.strftime("%Y%m%d")
    path = f"posts/{today_id}"

    # save image
    if not os.path.exists(path):
        os.mkdir(path)
    img.save(f"{path}/test.png")


def draw_site_title(draw, x, y, fill1, fill2, fill3):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 30)
    text1 = "The List "
    text2 = "NC"
    draw.text((x, y), text1, fill=fill1, font=font)
    text1_length = draw.textlength(text1, font)
    x = x + text1_length
    draw_highlighted_text(draw, x, y, text2, font, fill2, fill3)


def draw_highlighted_text(draw, x, y, text, font, text_fill, highlight_fill):
    left, top, right, bottom = draw.textbbox((x, y), text, font=font)
    draw.rectangle((left, top-6, right, bottom+5), fill=highlight_fill)
    draw.text((x, y), text, fill=text_fill, font=font)


def draw_date(draw, x_pos, y_pos, fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 45)
    today = date.today().strftime("%a, %b %-d")
    draw.text((x_pos, y_pos), today, fill=fill, font=font)


def draw_events(draw, x, y, events, time_fill, event_fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 25)
    remaining_events = []

    for event in events:
        title = event[0]
        venue = event[4]

        if y < (1080 - (9 * 30)):
            time_x_thresh = x + 180
            event_x_thresh = 990
            event_x_start = x + 240
            draw_time(draw, event, x, y, time_x_thresh, time_fill)
            y = draw_event(draw, title, venue, font, event_x_start, y, event_x_thresh, event_fill)


def draw_time(draw, event, x, y, x_thresh, fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-Regular.ttf", 25)
    start_time = get_natural_time(event[2])
    end_time = get_natural_time(event[3])

    if not end_time:
        draw.text((x, y), start_time, font=font, fill=fill)
    else:
        test_line = f"{start_time}-{end_time}"
        test_line_width = draw.textlength(test_line, font)
        if x + test_line_width < x_thresh:
            draw.text((x, y), test_line, font=font, fill=fill)
        else:
           draw.text((x, y), start_time + "-", font=font, fill=fill)
           y = y + 30
           draw.text((x, y), end_time, font=font, fill=fill)


def get_natural_time(time):
    if time == None:
        return ""
    hour = int(time.strftime("%I"))
    minutes = int(time.strftime("%M"))
    am_pm = time.strftime("%p").lower()
    if minutes:
        return f"{hour}:{minutes}{am_pm}"
    return f"{hour}{am_pm}"


def draw_event(draw, title, venue, font, x, y, x_thresh, fill):
    x_venue_start, y = draw_title(draw, title, font, x, y, x_thresh, fill)
    y = draw_venue(draw, venue, x, y, x_venue_start, x_thresh)
    return y


def draw_title(draw, text, font, x, y, x_thresh, fill):
    lines = []

    current_line = ""
    words = text.split()
    for word in words:
        test_line = current_line + word + " "
        test_line_width = draw.textlength(test_line, font=font)
        if x + test_line_width < x_thresh:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    ending_x = x + draw.textlength(current_line, font=font)

    for index, line in enumerate(lines):
        draw.text((x, y), line.strip(), font=font, fill=fill)
        last_line = index == len(lines)-1
        if not last_line:
            y += 40

    return (ending_x, y)


def draw_venue(draw, text, x, y, x_start, x_thresh):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold", 25)
    fill = "#457aa1"
    highlight = "#f1eae4"

    lines = []
    current_line = ""
    words = text.split()
    x_test_start = x_start

    for word in words:
        test_line = current_line + word + " "
        test_line_width = draw.textlength(test_line, font=font)

        if x_test_start + test_line_width < x_thresh:
            current_line = test_line
        else:
            x_test_start = x
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    for index, line in enumerate(lines):
        line = line.strip()
        if index == 0:
            draw_highlighted_text(draw, x_start, y, line, font, fill, highlight)
        else:
            draw_highlighted_text(draw, x, y, line, font, fill, highlight)
        last_line = index == len(lines)-1
        if not last_line:
            y += 35
        else:
            y += 65
    return y


if __name__ == "__main__":
    page_num = 1
    events = get_todays_events()
    create_event_image(events, page_num)
