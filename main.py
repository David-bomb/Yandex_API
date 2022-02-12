import sys
import keyboard

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        keyboard.add_hotkey("PageUP", lambda: self.change_view(0))
        keyboard.add_hotkey("PageDOWN", lambda: self.change_view(1))
        self.delta = 0.002
        self.setFixedSize(*SCREEN_SIZE)
        self.initUI()
        self.setWindowTitle('Кафты')

    def get_requests(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = "37.618879"
        lat = "55.751426"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": "map"
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
            self.delta += 0.001
        elif k == 1:
            self.delta -= 0.001
        if self.delta < 0:
            self.delta = 0
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

