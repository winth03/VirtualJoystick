# from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
import math

class Joystick(FloatLayout):
    def __init__(self, *args, gamepad, left=True, **kwargs):
        self.gamepad = gamepad
        self.left = left
        super().__init__(*args, **kwargs)
        self.joySize = 100
        self.stick_pos = (self.center_x - self.joySize * 1.5, self.center_y - self.joySize * 1.5)
        self.base = Image(source="img/Joystick.png", size=self.size, pos_hint={"center_x":0.5,"center_y":0.5}, fit_mode="contain")
        self.stick = Image(source="img/SmallHandleFilledGrey.png", size=(self.joySize, self.joySize), pos_hint={"center_x":0.5,"center_y":0.5}, fit_mode="scale-down")
        self.add_widget(self.base)
        self.add_widget(self.stick)

        Clock.schedule_interval(self.update, 1/120)

    def update(self, *args):
        self.stick.pos = self.stick_pos

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.stick.pos_hint = {}
            touch.grab(self)
            return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            x, y = touch.pos
            center_x, center_y = self.center_x, self.center_y
            pos_x, pos_y = self.pos
            size = self.size[0]

            # Clamp the joystick to the outer circle
            if math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2) > size / 2 - self.joySize / 2:
                angle = math.atan2(center_y - y, center_x - x)
                x = center_x - (size / 2 - self.joySize / 2) * math.cos(angle)
                y = center_y - (size / 2 - self.joySize / 2) * math.sin(angle)
            
            # Draw the joystick
            self.stick_pos = (x - self.joySize * 1.5, y - self.joySize * 1.5)

            # Send the joystick position to the gamepad
            x = 2 * (x - (self.joySize / 2) - pos_x) / (size - 2*(self.joySize / 2)) - 1
            y = 2 * (y - (self.joySize / 2) - pos_y) / (size - 2*(self.joySize / 2)) - 1
            self.gamepad.left_joystick_float(x, y) if self.left else self.gamepad.right_joystick_float(x, y)
            self.gamepad.update()
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.stick.pos_hint = {"center_x":0.5,"center_y":0.5}
            self.stick_pos = (self.center_x - self.joySize * 1.5, self.center_y - self.joySize * 1.5)
            self.gamepad.left_joystick_float(0, 0) if self.left else self.gamepad.right_joystick_float(0, 0)
            self.gamepad.update()
            touch.ungrab(self)
            return True
