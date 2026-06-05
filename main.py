#!/home/hudboi/containers/caddy/site/dyna/dyna-images/venv/python3

from PIL import Image, ImageDraw, ImageFont
<<<<<<< HEAD
from flask import Flask, request, send_file, send_from_directory
=======
from flask import Flask, request, send_file, send_from_directory, render_template
import json
>>>>>>> e987ab2 (Minor changes)
import requests
import io
import os
import difflib
import datetime   # >>> LOGGING <<<

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# >>> LOGGING <<<
def log_request(info: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("access.log", "a") as f:
        f.write(f"[{timestamp}] {info}\n")


# ---------------
#|Footer message|
# ---------------

def draw_footer(draw, img_width, img_height):
    footer_font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=18
    )

    footer_text = "github.com/mrcoat2/dyna-images\nyour.server.url"

    draw.text(
        (img_width // 2, img_height - 40),
        footer_text,
        fill="black",
        font=footer_font,
        anchor="mm",
        align="center"
    )


# -------------------------
# LAN IP detection
# -------------------------
def is_lan(ip: str) -> bool:
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        (ip.startswith("172.") and 16 <= int(ip.split(".")[1]) <= 31)
    )


# -------------------------
# Normalize ISP name
# -------------------------
def normalize_isp(name: str) -> str:
    if not name:
        return ""
    return (
        name.lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
            .replace(",", "")
            .replace(".", "")
    )


# -------------------------
# Extract ISP brand name (universal)
# -------------------------
def extract_brand(name: str) -> str:
    if not name:
        return ""

    if name.upper().startswith("AS") and " " in name:
        name = name.split(" ", 1)[1]

    clean = (
        name.lower()
            .replace(",", "")
            .replace(".", "")
            .replace("inc", "")
            .replace("llc", "")
            .replace("corp", "")
            .replace("corporation", "")
            .replace("communications", "")
            .replace("communication", "")
            .replace("services", "")
            .replace("service", "")
            .replace("solutions", "")
            .replace("networks", "")
            .replace("network", "")
            .replace("enterprises", "")
            .replace("enterprise", "")
            .replace("holdings", "")
            .replace("holding", "")
            .replace("company", "")
            .replace("co", "")
            .replace("group", "")
            .replace("broadband", "")
            .replace("cable", "")
            .replace("telecom", "")
            .replace("usa", "")
            .replace("internet", "")
            .replace("llp", "")
            .replace("plc", "")
            .replace("gmbh", "")
            .replace("sa", "")
            .replace("spa", "")
    )

    clean = " ".join(clean.split())
    brand = clean.split(" ")[0]
    return normalize_isp(brand)


# -------------------------
# Dual‑mode ISP resolver
# -------------------------
def resolve_isp_logo(org_name: str) -> str:
    if not org_name:
        return "unknown.png"

    brand = extract_brand(org_name)

    files = os.listdir("isp_logo")
    logos = [f.replace(".png", "").lower() for f in files if f.endswith(".png")]

    if brand in logos:
        return brand + ".png"

    match = difflib.get_close_matches(brand, logos, n=1, cutoff=0.3)
    if match:
        return match[0] + ".png"

    return "unknown.png"


# -------------------------
# /phone endpoint
# -------------------------
@app.route('/phone')
def phone():
    user_agent = request.headers.get('User-Agent', '')
    ip_addr = (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For")
        or request.remote_addr
    )

    # >>> LOGGING <<<
    log_request(f"PHONE  IP={ip_addr}  UA='{user_agent}'")

    color = (255, 255, 255)
    paste_image = Image.open('unknown.png')

    big_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    big_font = ImageFont.truetype(big_font_path, size=40)
    small_font = ImageFont.truetype(big_font_path, size=20)

    text = "Your OS can't be detected \nBut it's probably Windows"

    font_size = 40
    max_width = 540 * 0.9
    max_height = 200

    while True:
        test_font = ImageFont.truetype(big_font_path, size=font_size)
        text_width = test_font.getlength(text)
        text_height = test_font.getbbox(text)[3] - test_font.getbbox(text)[1]
        if (text_width <= max_width and text_height <= max_height) or font_size <= 20:
            break
        font_size -= 2

    device_font = ImageFont.truetype(big_font_path, size=font_size)

    type_override = request.args.get('query')
    header_text = ""
    device_font = big_font

    if "Linux" in user_agent or type_override == "linux":
        header_text = "Elite choice."
        text = "You are the goodest boy \nfor using linux"
        paste_image = Image.open('linux.jpg')

    if "Android" in user_agent or type_override == "android":
        header_text = "You're using:"
        color = (61, 220, 132)
        paste_image = Image.open('android.jpg')

        try:
            device_name = user_agent.split("; M:")[1].split(";")[0]
        except:
            device_name = "non-recognized android device"

        font_size = 40
        while True:
            test_font = ImageFont.truetype(big_font_path, size=font_size)
            if test_font.getlength(device_name) <= 540 * 0.9 or font_size <= 20:
                break
            font_size -= 2

        device_font = ImageFont.truetype(big_font_path, size=font_size)
        text = f"You have a:\n{device_name}"

    if "iPhone" in user_agent or "Darwin" in user_agent or type_override in ("iphone", "darwin"):
        header_text = "Bold move."
        color = (0, 122, 255)
        paste_image = Image.open('apple.png')

        courage_text = "But where's your courage™?"

        font_size = 40
        while True:
            test_font = ImageFont.truetype(big_font_path, size=font_size)
            if test_font.getlength(courage_text) <= 540 * 0.9 or font_size <= 20:
                break
            font_size -= 2

        device_font = ImageFont.truetype(big_font_path, size=font_size)
        text = courage_text

    bottom_text = "This image changes depending on your device,\ntry it with a friend and see"

    img = Image.new("RGB", (540, 1218), color)
    draw = ImageDraw.Draw(img)

    draw.text((img.width // 2, 120), header_text, fill="black", font=big_font, anchor="mm")

    paste_image = paste_image.convert('RGBA')
    img.paste(paste_image, (70, 200), paste_image)

    draw.multiline_text(
        (img.width // 2, 700),
        text,
        fill="black",
        font=device_font,
        anchor="mm",
        align="center"
    )

    draw.text(
        (img.width // 2, 1000),
        bottom_text,
        fill="black",
        font=small_font,
        anchor="mm",
        align="center"
    )

    draw_footer(draw, img.width, img.height)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


# -------------------------
# /ip endpoint
# -------------------------
@app.route('/ip')
def ip():
    ip_addr = (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For")
        or request.remote_addr
    )

    # >>> LOGGING <<<
    log_request(f"IPLOOKUP  IP={ip_addr}")

    color = (255, 255, 255)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=30)
<<<<<<< HEAD
    header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=28)

    if is_lan(ip_addr):
        info = {}
        text = f"IP: {ip_addr}\nType: LAN IP\n"
    else:
        info = requests.get(f"https://ipinfo.io/{ip_addr}/json").json()
        loc = info.get("loc", "0,0")
        text = (
            f"IP: {info.get('ip', 'Unknown')}\n"
            f"City: {info.get('city', 'Unknown')}\n"
            f"Region: {info.get('region', 'Unknown')}\n"
            f"Country: {info.get('country', 'Unknown')}\n"
            f"Location: {loc}\n"
        )

        # >>> LOGGING <<<
        log_request(
            f"IPLOOKUP  IP={ip_addr}  City={info.get('city')}  Region={info.get('region')}  Country={info.get('country')}"
        )

    img = Image.new("RGB", (540, 1218), color)
    draw = ImageDraw.Draw(img)

    draw.multiline_text(
        (img.width // 2, 250),
        text,
        fill="black",
        font=small_font,
        anchor="mm",
        align="center"
    )

    if is_lan(ip_addr):
        logo_file = "lan.png"
    else:
        org = info.get("org", "")
        logo_file = resolve_isp_logo(org)

    logo_path = f"isp_logo/{logo_file}"

    draw.text(
        (img.width // 2, 600),
        "Connection provided by",
        font=header_font,
        fill="black",
        anchor="mm"
    )

    try:
        logo = Image.open(logo_path).convert("RGBA")
        max_logo_width = int(img.width * 0.6)
        scale = max_logo_width / logo.width
        new_size = (int(logo.width * scale), int(logo.height * scale))
        logo = logo.resize(new_size, Image.LANCZOS)

        logo_x = (img.width - logo.width) // 2
        logo_y = 650
        img.paste(logo, (logo_x, logo_y), logo)
    except Exception as e:
        print("LOGO ERROR:", e)

    draw.text(
        (img.width // 2, 1100),
        "If this seems incorrect:\ntry refreshing or\nclearing your cache",
        font=header_font,
        fill="black",
        anchor="mm",
        align="center"
    )

    draw_footer(draw, img.width, img.height)

=======
    smaller_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=10)
    info = requests.get("https://ipinfo.io/"+ip+"/json").json()
    print(info)
    text = ""
    text += info['ip'] + '\n'
    text += info['city'] +'\n'
    text += info['region'] +'\n'
    text += info['country'] +'\n'
    text += info['loc'] +'\n'
    text += info['org'] +'\n'
    #headers = json.dumps(dict(request.headers))

    #for key, value in request.headers.items():
    #    text += f"{key}: {value}\n"

    img = Image.new("RGB", (540, 1218), color)
    draw = ImageDraw.Draw(img)
    draw.text((0, 400), text, fill="black", font=small_font)
    #draw.text((0, 1000), headers, fill="black", font=smaller_font)
>>>>>>> e987ab2 (Minor changes)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route('/isp_logo/<path:filename>')
def isp_logo(filename):
    return send_from_directory('isp_logo', filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
