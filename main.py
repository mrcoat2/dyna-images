#!/home/ammon/dyna-images/bin/python3

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, send_file, render_template
import requests
import io

app = Flask(__name__)


@app.route('/phone')
def phone():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)

    color = (255,255,255)
    paste_image = Image.open('unknown.png')

    big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=40)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=20)
    text = "You're probably on windows or something idk"
    type = request.args.get('query')
    if "Linux" in user_agent:
        text = "You are the goodest boy \nfor using linux"
        paste_image = Image.open('linux.jpg')
    
    if "Android" in user_agent or type=="android":
        # android settings
        color = (61, 220, 132)
        try:
            text = "You have a: \n" + user_agent.split("; M:")[1].split(";")[0]
        except IndexError:
            text = "You have an android"
        
        paste_image = Image.open('android.jpg')
        
    if "Darwin" in user_agent or "iPhone" in user_agent or type=="iphone":
        # apples settings
        color = (0, 122, 255)
        text = "You have an iphone, \nI'm sorry that you do :("
        
        paste_image = Image.open('apple.png')

    bottom_text = "This image changes depending on your device, \ntry it with a friend and see"
    img = Image.new("RGB", (540, 1218), color)
    draw = ImageDraw.Draw(img)

    # Draw shapes
    paste_image = paste_image.convert('RGBA')
    img.paste(paste_image, (70, 200), paste_image)

    # Add text
    draw.text((0, 700), text, fill="black", font=big_font)
    draw.text((0, 1000), bottom_text, fill="black", font=small_font)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0) # Reset buffer to the beginning

    return send_file(img_io, mimetype='image/png')

@app.route('/ip')
def ip():
    ip = request.headers.get("X-Forwarded-For")
    print(ip)

    color = (255,255,255)
    

    # big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=40)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=30)
    info = requests.get("https://ipinfo.io/"+ip+"/json").json()
    print(info)
    text = ""
    text += info['ip'] + '\n'
    text += info['city'] +'\n'
    text += info['region'] +'\n'
    text += info['country'] +'\n'
    text += info['loc'] +'\n'
    text += info['org'] +'\n'

    img = Image.new("RGB", (540, 1218), color)
    draw = ImageDraw.Draw(img)
    draw.text((0, 400), text, fill="black", font=small_font)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0) # Reset buffer to the beginning

    return send_file(img_io, mimetype='image/png')

@app.route('/spotify')
def spotify():
    path = "spotify.html"
    return render_template('spotify.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
