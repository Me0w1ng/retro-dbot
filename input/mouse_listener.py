import win32api
import time
import win32gui
from input.window import Window


def listen_mouse_click(base_window: Window):
    state_left = win32api.GetKeyState(0x01)
    dim = base_window.get_dim()
    while True:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                pass
            else:
                flags, hcursor, (x,y) = win32gui.GetCursorInfo()
                x, y = x - dim['left'], y - dim['top']
                pixel = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x, y)
                print(f"({x}, {y}) {hex(pixel)}")

        time.sleep(0.001)


if __name__ == '__main__':
    xelit = Window.list_windows()[0]
    xelit.resize()
    listen_mouse_click(xelit.frame)