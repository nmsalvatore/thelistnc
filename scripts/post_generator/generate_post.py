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
            cur.execute("SELECT title, start_date, start_time, end_time, venue FROM events_event WHERE start_date < (CURRENT_TIMESTAMP AT TIME ZONE 'America/Los_Angeles')::date ORDER BY start_time ASC, end_time ASC, title ASC")
            events = cur.fetchall()
    return events


def create_event_image(events, page_num):
    base_font_size = 60
    regular_font = ImageFont.truetype("fonts/IBMPlexMono-Regular.ttf", base_font_size)
    bold_font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", base_font_size)

    color1 = "#f9f7f6"
    color2 = "#f1eae4"
    color3 = "#457aa1"
    color4 = "#204560"

    img = Image.new("RGB", (2160, 2700), color=color1)
    draw = ImageDraw.Draw(img)

    # draw site title
    x = base_font_size * 3
    y = base_font_size * 3
    draw_site_title(draw, x, y, color4, color3, color2)

    if page_num == 1:
        y = y + (base_font_size * 4)
        draw_date(draw, x, y, color4)

    # draw events
    y = y + (base_font_size * 5)
    remaining_events = draw_events(draw, x, y, events, time_fill=color4, event_fill=color4)

    if len(remaining_events) == 0:
        draw_conclusion_text(draw, x, 2460, color4)
    else:
        paste_arrow_icon(img)

    today = date.today()
    today_id = today.strftime("%Y%m%d")
    path = f"../../ig_posts/{today_id}"

    if not os.path.exists(path):
        os.mkdir(path)

    img.save(f"{path}/{today_id}_{page_num}.png")
    return remaining_events


def paste_arrow_icon(img):
    icon = Image.open("icons/arrow_right_dark_blue.png")
    x_pos = (2160 - (180 + int(icon.width / 1.5)))
    y_pos = (2700 - (180 + int(icon.height / 1.5)))
    img.paste(icon, (x_pos, y_pos), icon)


def draw_conclusion_text(draw, x, y, fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 50)
    plain_text = "For more information, visit "
    draw.text((x, y), plain_text, font=font, fill=fill)
    plain_text_width = draw.textlength(plain_text, font)
    x = x + plain_text_width
    draw_highlighted_text(draw, x, y, "thelistnc.org", font, "#457aa1", "#f1eae4")


def draw_site_title(draw, x, y, fill1, fill2, fill3):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 60)
    text1 = "The List "
    text2 = "NC"
    draw.text((x, y), text1, fill=fill1, font=font)
    text1_length = draw.textlength(text1, font)
    x = x + text1_length
    draw_highlighted_text(draw, x, y, text2, font, fill2, fill3, title=True)


def draw_highlighted_text(draw, x, y, text, font, text_fill, highlight_fill, title=False):
    left, top, right, bottom = draw.textbbox((x, y), text, font=font)
    if title:
        draw.rectangle((left, top-12, right, bottom+10), fill=highlight_fill)
    else:
        draw.rectangle((left, y+6, right, y+64), fill=highlight_fill)
    draw.text((x, y), text, fill=text_fill, font=font)


def draw_date(draw, x_pos, y_pos, fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 90)
    today = date.today().strftime("%a, %b %-d")
    draw.text((x_pos, y_pos), today, fill=fill, font=font)


def draw_events(draw, x, y, events, time_fill, event_fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 50)
    remaining_events = []

    time_x_thresh = x + 420
    event_x_thresh = 1980
    event_x_start = x + 560

    for event in events:
        title = event[0]
        venue = event[4]

        # test final y value
        event_test_text = f"{title} {venue}"
        event_depth = test_event_depth(draw, event_test_text, event_x_start, y, event_x_thresh)

        if event_depth < (2700 - (7 * 60)):
            draw_time(draw, event, x, y, time_x_thresh, time_fill)
            y = draw_event(draw, title, venue, font, event_x_start, y, event_x_thresh, event_fill)
        else:
            remaining_events.append(event)

    return remaining_events


def draw_time(draw, event, x, y, x_thresh, fill):
    font = ImageFont.truetype("fonts/IBMPlexMono-Regular.ttf", 50)
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
           y = y + 70
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
            y += 70

    return (ending_x, y)


def draw_venue(draw, text, x, y, x_start, x_thresh):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 50)
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
            y += 70
        else:
            y += 140
    return y


def test_event_depth(draw, text, x, y, x_thresh):
    font = ImageFont.truetype("fonts/IBMPlexMono-SemiBold.ttf", 50)
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        width = draw.textlength(test_line, font=font)
        if x + width < x_thresh:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    for index, line in enumerate(lines):
        if index != len(lines)-1:
            y += 70

    return y + 50


if __name__ == "__main__":
    page_num = 1
    events = get_todays_events()
    remaining_events = create_event_image(events, page_num)

    while True:
        page_num += 1
        if len(remaining_events) < 1:
            break;
        else:
            remaining_events = create_event_image(remaining_events, page_num)
