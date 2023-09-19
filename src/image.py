from PIL import Image, ImageDraw

IMG_PATH = "img/temp_mask.png"
image = None
offset = 0

def new_image(size):
    global image
    image = Image.new("RGBA", size, (0, 0, 0, 0))

def draw_from_widget(widget, window, depth=0, parent=False):
    draw = ImageDraw.Draw(image)
    if not parent:
        draw.ellipse((widget.pos[0], window.height - widget.pos[1] + offset - widget.height, (widget.pos[0] + widget.width, window.height - widget.pos[1] + offset)), fill="black")
    if widget.children and depth < 1:
        for child in widget.children:
            draw_from_widget(child, window, depth=depth+1)

def fill_all():
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, image.width, image.height), fill="black")

def save_image():
    image.save(IMG_PATH)
