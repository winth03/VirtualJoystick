import save
from kivy.config import Config

save.load_save()
size = (save.save_dict['size'][0] if 'size' in save.save_dict else 1920, save.save_dict['size'][1] if 'size' in save.save_dict else 1021)
Config.set('graphics', 'width', size[0])
Config.set('graphics', 'height', size[1])
Config.set('graphics', 'shaped', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'always_on_top', 1)

from kivy.resources import resource_find
import image
image.new_image(size)
mask = resource_find('mask.png')

from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from joystick import Joystick
from buttons import Buttons
from kivy.app import App
import vgamepad as vg
import win32gui
import win32api
import win32con

def move_widgets_start(self, touch):
    if self.collide_point(*touch.pos):
        touch.grab(self)
        return True
    
def move_widgets_move(self, touch):
    if touch.grab_current is self:
        x, y = touch.pos
        self.pos = (x - self.width / 2, y - self.height / 2)
        return True
    
def move_widgets_stop(self, touch):
    if touch.grab_current is self:
        touch.ungrab(self)
        return True
    
def move_window_start(self, touch):
    if self.collide_point(*touch.pos):
        touch.grab(self)
        return True
    
def move_window_move(self, touch):
    if touch.grab_current is self:
        Window.top -= touch.dy * 0.75
        Window.left += touch.dx * 0.75
        return True
    
def move_window_stop(self, touch):
    if touch.grab_current is self:
        touch.ungrab(self)
        return True

class MainWindow(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gamepad = vg.VX360Gamepad()
        self.edit = Button(text="Edit", size_hint=(None,None), size=(100, 50), pos=(0, Window.height-50))
        self.close = Button(text="Close", size_hint=(None,None), size=(100, 50), pos=(Window.width-100, Window.height-50))
        self.grab = Image(size_hint=(None,None), size=(50, 50), pos=(Window.width/2-25, Window.height-50))
        self.leftjoy = Joystick(gamepad=self.gamepad, size_hint=(None,None), size=(300, 300), pos=(0, 0))
        self.rightjoy = Joystick(gamepad=self.gamepad, left=False, size_hint=(None,None), size=(300, 300), pos=(Window.width-300, 0))
        self.buttons = Buttons(gamepad=self.gamepad, size_hint=(None,None), size=(300, 300), pos=(Window.width-300, Window.height/2-150))
        self.dpads = Buttons(gamepad=self.gamepad, dpad=True, size_hint=(None,None), size=(300, 300), pos=(0, Window.height/2-150))

        self.add_widget(self.edit)
        self.add_widget(self.close)
        self.add_widget(self.grab)
        self.add_widget(self.leftjoy)
        self.add_widget(self.rightjoy)
        self.add_widget(self.buttons)
        self.add_widget(self.dpads)

        Clock.schedule_once(self.set_shape)
        self.bind(size=self.update_widgets)
        self.edit.bind(on_press=self.edit_widgets)
        self.close.bind(on_press=App.get_running_app().stop)

    def update_widgets(self, *args):
        self.edit.pos = (0, Window.height-50)
        self.close.pos = (Window.width-100, Window.height-50)
        self.grab.pos = (Window.width/2-25, Window.height-50)

    def init(self, *args):
        if save.save_dict:
            save.deserialize_save(self, save.save_dict, window=Window, exclude=[self.edit, self.close, self.grab])

    def set_shape(self, *args):
        image.draw_from_widget(save.save_dict, Window, True)
        Window.shape_image = mask
        Window.shape_mode = "colorkey"
        Clock.schedule_once(self.init)
    
    # Edit position and size of widgets
    def edit_widgets(self, *args):
        self.edit.text = "Save"
        self.edit.unbind(on_press=self.edit_widgets)
        self.edit.bind(on_press=self.save_widgets)
        self.edit_binds = []
        self.edit_binds.append((self.grab, 'on_touch_down', self.grab.fbind('on_touch_down', move_window_start)))
        self.edit_binds.append((self.grab, 'on_touch_move', self.grab.fbind('on_touch_move', move_window_move)))
        self.edit_binds.append((self.grab, 'on_touch_up', self.grab.fbind('on_touch_up', move_window_stop)))
        for widget in self.children[:-3]:
            self.edit_binds.append((widget, 'on_touch_down', widget.fbind('on_touch_down', move_widgets_start)))
            self.edit_binds.append((widget, 'on_touch_move', widget.fbind('on_touch_move', move_widgets_move)))
            self.edit_binds.append((widget, 'on_touch_up', widget.fbind('on_touch_up', move_widgets_stop)))

    def save_widgets(self, *args):
        self.edit.text = "Edit"
        self.edit.unbind(on_press=self.save_widgets)
        self.edit.bind(on_press=self.edit_widgets)
        for bind in self.edit_binds:
            widget, name, uid = bind
            widget.unbind_uid(name, uid)
        save.save(self, window=Window)

class VirtualGamepadApp(App):
    def build(self):
        self.main_window = MainWindow()
        title = "Virtual Joystick"
        Window.set_title(title)
        hwnd = win32gui.FindWindow(None, title)
        # Set WS_EX_NOACTIVATE flag
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), int(0.5 * 255), win32con.LWA_ALPHA)
        return self.main_window

if __name__ == '__main__':
    VirtualGamepadApp().run()
