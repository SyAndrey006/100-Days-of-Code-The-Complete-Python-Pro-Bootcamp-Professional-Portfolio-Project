from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def get_top_colors(image):
    pixels = image.load()

    color_count = {}

    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]

            if (r, g, b) in color_count:
                color_count[(r, g, b)] += 1
            else:
                color_count[(r, g, b)] = 1

    sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)

    top_colors = []
    for i in range(10):
        r, g, b = sorted_colors[i][0]
        top_colors.append(rgb_to_hex(r, g, b))

    return top_colors

@app.route("/", methods=["GET", "POST"])
def index():
    colors = []

    if request.method == "POST":
        file = request.files["image"]
        image = Image.open(file).convert("RGB")
        colors = get_top_colors(image)

    return render_template("index.html", colors=colors)

if __name__ == "__main__":
    app.run(debug=True)
