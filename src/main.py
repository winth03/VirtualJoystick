from kivy.config import Config
import win32gui
import win32api
import win32con
import ctypes
import save

ctypes.windll.user32.SetProcessDPIAware()
save.load_save()
padding = (1, 0)
size = (win32api.GetSystemMetrics(0) - padding[0], win32api.GetSystemMetrics(1) - padding[1])
Config.set('graphics', 'width', size[0])
Config.set('graphics', 'height', size[1])
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'shaped', 1)
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'always_on_top', 1)


from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from joystick import Joystick
from kivy.clock import Clock
from buttons import Buttons
from kivy.app import App
import vgamepad as vg

from kivy.resources import resource_find
import image
image.new_image(size)
image.save_image()
mask = resource_find('img/mask.png')

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
        btn_size = (100, 50)
        widget_size = (300, 300)
        self.padding = (100, 0)
        self.offset = (Window.size[0] - size[0], Window.size[1] - size[1])
        self.edit = Button(text="Edit", size_hint=(None,None), size=btn_size, pos=(0,Window.height-btn_size[1]))
        self.close = Button(text="Close", size_hint=(None,None), size=btn_size, pos=(size[0]-btn_size[0],Window.height-btn_size[1]))
        self.leftjoy = Joystick(gamepad=self.gamepad, size_hint=(None,None), size=widget_size, pos=(0,self.offset[1]))
        self.rightjoy = Joystick(gamepad=self.gamepad, left=False, size_hint=(None,None), size=widget_size, pos=(size[0]-widget_size[0],self.offset[1]))
        self.buttons = Buttons(gamepad=self.gamepad, size_hint=(None,None), size=widget_size, pos=(size[0]-widget_size[0],(size[1]/2-widget_size[1]/2)+self.offset[1]))
        self.dpads = Buttons(gamepad=self.gamepad, dpad=True, size_hint=(None,None), size=widget_size, pos=(0,(size[1]/2-widget_size[1]/2)+self.offset[1]))

        self.exclude = [self.edit, self.close]
        self.movable = len(self.children) - len(self.exclude)
        # Static widgets
        self.add_widget(self.edit)
        self.add_widget(self.close)
        # Movable widgets
        self.add_widget(self.dpads)
        self.add_widget(self.buttons)
        self.add_widget(self.leftjoy)
        self.add_widget(self.rightjoy)
        
        self.edit.bind(on_press=self.edit_widgets)
        self.close.bind(on_press=App.get_running_app().stop)
        Clock.schedule_once(self.init)

    def init(self, *args):
        if not save.save_dict:
            save.save(self, window=Window)
        save.deserialize_save(self, save.save_dict, window=Window, exclude=self.exclude)
        Clock.schedule_once(self.set_shape)

    def set_shape(self, *args):
        image.draw_from_widget(self, Window, parent=True)
        image.save_image()
        Window.shape_image = mask
        Window.shape_mode = "binalpha"
        Window.top = 0
        Window.left = 0
    
    # Edit position and size of widgets
    def edit_widgets(self, *args):
        image.fill_all()
        image.save_image()
        Window.shape_mode = "binalpha"
        self.edit.text = "Save"
        self.edit.unbind(on_press=self.edit_widgets)
        self.edit.bind(on_press=self.save_widgets)
        self.edit_binds = []
        for widget in self.children[:self.movable]:
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
        image.new_image(size)
        image.draw_from_widget(self, Window, parent=True)
        image.save_image()
        Window.shape_mode = "binalpha"

class VirtualGamepadApp(App):
    def build(self):
        self.main_window = MainWindow()
        title = "Virtual Joystick"
        Window.set_title(title)
        print(Window.size)
        hwnd = win32gui.FindWindow(None, title)
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), int(0.5 * 255), win32con.LWA_ALPHA)
        return self.main_window

if __name__ == '__main__':
    VirtualGamepadApp().run()
