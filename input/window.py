import win32api
import win32gui
import win32ui
import win32.lib.win32con as win32con
import time
from PIL import Image
import cv2
import numpy as np

TICK = 0.1
DEFAULT_SIZE_X = 758
DEFAULT_SIZE_Y = 615
CELL_Y_OFFSET = 10
CELL_GAP_X = 54
CELL_GAP_Y = 27
PLAYER_MENU_OFFSETS = (490, 454)
PLAYER_MENU_GAP_X = 29.25
PLAYER_MENU_ORDER = {'player': 0, 'spells': 1, 'inventory': 2}


class Window:
    def __init__(self, hwnd, name):
        self.hwnd = hwnd
        self.name = name
        self.frame: Window = None  # main frame of the game
        self.children = []

    @staticmethod
    def _window_enumeration_handler(hwnd, top_windows):
        name = win32gui.GetWindowText(hwnd)
        top_windows.append(Window(hwnd, name))

    @staticmethod
    def list_windows():
        windows = []
        win32gui.EnumWindows(Window._window_enumeration_handler, windows)
        windows = list(filter(lambda x: 'Dofus Retro' in x.name, windows))
        for w in windows:
            children = w.get_children()
            if children:
                w.frame = children[0]
        return windows

    def get_children(self):
        children = []
        win32gui.EnumChildWindows(self.hwnd, Window._window_enumeration_handler, children)
        return children

    def resize(self, minimize=False):
        if minimize:
            y = win32api.GetSystemMetrics(1) - 30
            win32gui.MoveWindow(self.hwnd, 0, y, DEFAULT_SIZE_X, DEFAULT_SIZE_Y, True)
        else:
            win32gui.MoveWindow(self.hwnd, 0, 0, DEFAULT_SIZE_X, DEFAULT_SIZE_Y, True)

    def get_dim(self):
        dim = win32gui.GetWindowRect(self.hwnd)
        size_x = dim[2] - dim[0]
        size_y = dim[3] - dim[1]
        return {"left": dim[0], "top": dim[1], "right": dim[2], "bottom": dim[3], "size_x": size_x, "size_y": size_y}

    def focus(self):
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(TICK)

    def click(self, x=0, y=0, wParam=0):
        hwnd = self.hwnd
        time.sleep(TICK)
        lp = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, wParam, lp)
        time.sleep(TICK)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, wParam, lp)

    def double_click(self, x=0, y=0, wParam=0):
        lp = win32api.MAKELONG(x, y)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDBLCLK, wParam, lp)
        time.sleep(TICK)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, wParam, lp)

    def click_cell(self, cell):
        y, x = divmod(cell, 14.5)
        _x = int(x * CELL_GAP_X)
        _y = int(y * (CELL_GAP_Y / 2))
        self.click(_x, _y + CELL_Y_OFFSET)

    def toggle_menu(self, index):
        x, y = PLAYER_MENU_OFFSETS
        x += int(index * PLAYER_MENU_GAP_X)
        self.click(x, y)
        time.sleep(TICK * 5)

    def get_pixels(self, rect=None):
        # win32gui.GetPixel(self.hwnd, )
        pass


    def capture(self, debug=False):
        self.focus()
        # dimensions = win32gui.GetWindowRect(self.hwnd)
        # image = ImageGrab.grab(dimensions)
        # image.show()
        hwnd = self.hwnd
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        # hwndDC = win32gui.GetDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        open_cv_image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        del im
        if debug:
            cv2.imshow("Debug capture", open_cv_image)
            cv2.waitKey()

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        return open_cv_image

if __name__ == "__main__":
    xelit = Window.list_windows()[0]
    xelit.focus()
    xelit.frame.capture()
    # xelit.click_cell(30)
    # xelit.toggle_menu(2)