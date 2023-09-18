import os

SAVE_PATH = os.environ['LOCALAPPDATA'] + '\\VirtualJoystick'
SAVE_FILE = SAVE_PATH + '\\save.txt'
save_dict = {}

def create_save():
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        print('Created save directory at ' + SAVE_PATH + '.')
    with open(SAVE_FILE, 'w') as save_file:
        save_file.write(str({}))

def load_save(retry=False):
    global save_dict
    if not os.path.exists(SAVE_FILE):
        create_save()
    with open(SAVE_FILE, 'r') as save_file:
        read_data = save_file.read()
        try:
            save_dict = eval(read_data)
        except SyntaxError:
            print('Error: Save file is corrupted.')
            if not retry:
                create_save()
                load_save(True)

def save(widget=None, *args, **kwargs):
    global save_dict
    load_save()
    with open(SAVE_FILE, 'w') as save_file:
        if widget:
            save_dict = serialize_save(widget, *args, **kwargs)
        save_file.write(str(save_dict))
    print('Saved to ' + SAVE_FILE + '.')

def serialize_save(widget, window=None):
    serialized = {}
    if window:
        serialized['size'] = window.size
        serialized['pos'] = (window.top, window.left)
    else:
        serialized['size'] = widget.size
        serialized['pos'] = widget.pos
    if widget.children:
        serialized['children'] = []
        for child in widget.children:
            serialized['children'].append(serialize_save(child))
    return serialized

def deserialize_save(widget, dict, window=None, exclude=[]):
    try:
        if window:
            window.top = dict['pos'][0]
            window.left = dict['pos'][1]
        elif widget not in exclude:
            widget.pos = dict['pos']
    except KeyError:
        print('Error: Widget mismatch', widget, dict)
        create_save()
        load_save()
    if 'children' in dict:
        for index, child in enumerate(dict['children']):
            try:
                deserialize_save(widget.children[index], child, exclude=exclude)
            except IndexError:
                print('Error: Widget mismatch')
                create_save()
                load_save()
                break
