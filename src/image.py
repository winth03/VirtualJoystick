from PIL import Image, ImageDraw

IMG_PATH = "src/mask.png"
image = None
offset = 0

def new_image(size):
    global image
    image = Image.new("RGB", size, "white")

def draw_from_widget(widget_dict, window, first=False):
    draw = ImageDraw.Draw(image)
    if not first:
        draw.ellipse((widget_dict['pos'][0], window.height - widget_dict['pos'][1] + offset - widget_dict['size'][1], (widget_dict['pos'][0] + widget_dict['size'][0], window.height - widget_dict['pos'][1] + offset)), fill="black")
    if 'children' in widget_dict:
        for child in widget_dict['children']:
            draw_from_widget(child, window)
    save_image()

def save_image():
    image.save(IMG_PATH)
