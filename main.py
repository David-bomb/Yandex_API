import sys
import keyboard

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox

SCREEN_SIZE = [600, 450]
PEREVOD = {'схема': 'map',
           'спутник': 'sat',
           'гибрид': 'sat,skl'}


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        keyboard.add_hotkey("PageUP", lambda: self.change_view(0))
        keyboard.add_hotkey("PageDOWN", lambda: self.change_view(1))
        keyboard.add_hotkey("UP", lambda: self.change_view(2))
        keyboard.add_hotkey("DOWN", lambda: self.change_view(3))
        keyboard.add_hotkey("LEFT", lambda: self.change_view(4))
        keyboard.add_hotkey("RIGHT", lambda: self.change_view(5))
        self.delta = 16
        self.setFixedSize(*SCREEN_SIZE)
        self.shema.currentTextChanged.connect(lambda: self.change_view(6))
        self.lon = "37.618879"
        self.lat = "55.751426"
        self.map = PEREVOD[self.shema.currentText()]
        self.initUI()
        self.setWindowTitle('Кафты')

    def get_requests(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([self.lon, self.lat]),
            "z": str(self.delta),
            "l": self.map
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            quit()
        return response

    def initUI(self):
        ## Изображение
        response = self.get_requests()
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.image.setGeometry(0, 0, *SCREEN_SIZE)


    def change_view(self, k):
        if k == 0:
            self.delta += 1
        elif k == 1:
            self.delta -= 1
        if self.delta < 0:
            self.delta = 0
        if self.delta > 21:
            self.delta = 21
        elif k == 2:
            self.lat = str(round((float(self.lat) + 0.00045), 6))
        elif k == 3:
            self.lat = str(round((float(self.lat) - 0.00045), 6))
        elif k == 4:
            self.lon = str(round((float(self.lon) - 0.00045), 6))
        elif k == 5:
            self.lon = str(round((float(self.lon) + 0.00045), 6))
        elif k == 6:
            self.map = PEREVOD[self.shema.currentText()]
        self.delta = round(self.delta, 3)
        response = self.get_requests()
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

