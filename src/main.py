from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from joystick import Joystick
from buttons import Buttons
from kivy.app import App
import vgamepad as vg
import win32gui
import win32api
import win32con

class MainWindow(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gamepad = vg.VX360Gamepad()
        self.leftjoy = Joystick(gamepad=self.gamepad, size_hint=(None,None), size=(300, 300), pos=(0, 0))
        self.rightjoy = Joystick(gamepad=self.gamepad, left=False, size_hint=(None,None), size=(300, 300), pos=(Window.width-300, 0))
        self.buttons = Buttons(gamepad=self.gamepad, size_hint=(None,None), size=(300, 300), pos=(Window.width-300, Window.height/2-150))
        self.dpads = Buttons(gamepad=self.gamepad, dpad=True, size_hint=(None,None), size=(300, 300), pos=(0, Window.height/2-150))

        self.add_widget(self.leftjoy)
        self.add_widget(self.rightjoy)
        self.add_widget(self.buttons)
        self.add_widget(self.dpads)

        self.bind(size=self.update_widgets)

    def update_widgets(self, *args):
        self.leftjoy.pos = (0, 0)
        self.rightjoy.pos = (self.width-300, 0)
        self.buttons.pos = (self.width-300, self.height/2-150)
        self.dpads.pos = (0, self.height/2-150)

class VirtualGamepadApp(App):
    def build(self):
        self.main_window = MainWindow()
        title = "Virtual Gamepad"
        Window.set_title(title)
        Window.always_on_top = True
        Window.maximize()
        hwnd = win32gui.FindWindow(None, title)
        # Set WS_EX_NOACTIVATE flag
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), int(0.5 * 255), win32con.LWA_ALPHA)
        return self.main_window

if __name__ == '__main__':
    VirtualGamepadApp().run()
