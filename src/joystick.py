from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse
import math

class Joystick(FloatLayout):
    def __init__(self, *args, gamepad, left=True, **kwargs):
        self.gamepad = gamepad
        self.left = left
        super().__init__(*args, **kwargs)
        self.joySize = 100
        self.joyPos = (self.center_x - self.joySize / 2, self.center_y - self.joySize / 2)

        # Draw the joystick
        self.bind(pos=self.update_pos)
        self.draw()

    def update_pos(self, *args):
        self.joyPos = (self.center_x - self.joySize / 2, self.center_y - self.joySize / 2)
        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            self.base = Ellipse(pos=self.pos, size=self.size)
            Color(0, 0, 0)
            self.joystick = Ellipse(pos=self.joyPos, size=(self.joySize, self.joySize))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
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
            self.joyPos = (x - self.joySize / 2, y - self.joySize / 2)
            self.draw()

            # Send the joystick position to the gamepad
            x = 2 * (x - (self.joySize / 2) - pos_x) / (size - 2*(self.joySize / 2)) - 1
            y = 2 * (y - (self.joySize / 2) - pos_y) / (size - 2*(self.joySize / 2)) - 1
            self.gamepad.left_joystick_float(x, y) if self.left else self.gamepad.right_joystick_float(x, y)
            self.gamepad.update()
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.joyPos = (self.center_x - self.joySize / 2, self.center_y - self.joySize / 2)
            self.draw()
            self.gamepad.left_joystick_float(0, 0) if self.left else self.gamepad.right_joystick_float(0, 0)
            self.gamepad.update()
            touch.ungrab(self)
            return True
