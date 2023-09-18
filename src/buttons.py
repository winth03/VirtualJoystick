from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
import vgamepad as vg

class Buttons(GridLayout):
    def __init__(self, *args, gamepad, dpad=False, **kwargs):
        self.gamepad = gamepad
        self.dpad = dpad
        super().__init__(*args, **kwargs)
        """
        Button in layout
        | |Y| |
        |X|S|B|
        | |A| |
        """
        self.button_dict = {
            "A":vg.XUSB_BUTTON.XUSB_GAMEPAD_A, 
            "B":vg.XUSB_BUTTON.XUSB_GAMEPAD_B, 
            "X":vg.XUSB_BUTTON.XUSB_GAMEPAD_X, 
            "Y":vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            "START":vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            }
        self.dpad_dict = {
            "X":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            "Y":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            "B":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            "A":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            "START":vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            }
        self.cols = 3
        self.rows = 3
        self.buttons = {}
        self.spacers = [Image(), Image(), Image(), Image()]
        self.buttons["A"] = Button(text="DOWN" if self.dpad else "A")
        self.buttons["B"] = Button(text="RIGHT" if self.dpad else "B")
        self.buttons["X"] = Button(text="LEFT" if self.dpad else "X")
        self.buttons["Y"] = Button(text="UP" if self.dpad else "Y")
        self.buttons["START"] = Button(text="SELECT" if self.dpad else "START")

        self.buttons["A"].bind(on_press=lambda *args:self.press("A", *args))
        self.buttons["A"].bind(on_release=lambda *args:self.release("A", *args))
        self.buttons["B"].bind(on_press=lambda *args:self.press("B", *args))
        self.buttons["B"].bind(on_release=lambda *args:self.release("B", *args))
        self.buttons["X"].bind(on_press=lambda *args:self.press("X", *args))
        self.buttons["X"].bind(on_release=lambda *args:self.release("X", *args))
        self.buttons["Y"].bind(on_press=lambda *args:self.press("Y", *args))
        self.buttons["Y"].bind(on_release=lambda *args:self.release("Y", *args))
        self.buttons["START"].bind(on_press=lambda *args:self.press("START", *args))
        self.buttons["START"].bind(on_release=lambda *args:self.release("START", *args))
        
        self.add_widget(self.spacers[0])
        self.add_widget(self.buttons["Y"])
        self.add_widget(self.spacers[1])
        self.add_widget(self.buttons["X"])
        self.add_widget(self.buttons["START"])
        self.add_widget(self.buttons["B"])
        self.add_widget(self.spacers[2])
        self.add_widget(self.buttons["A"])
        self.add_widget(self.spacers[3])

    def press(self, button, *args):
        self.gamepad.press_button(button=self.dpad_dict[button] if self.dpad else self.button_dict[button])
        self.gamepad.update()

    def release(self, button, *args):
        self.gamepad.release_button(button=self.dpad_dict[button] if self.dpad else self.button_dict[button])
        self.gamepad.update()