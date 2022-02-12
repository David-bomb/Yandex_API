import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setFixedSize(*SCREEN_SIZE)
        self.getImage()
        self.initUI()
        self.setWindowTitle('Кафты')

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = "37.618879"
        lat = "55.751426"
        delta = "0.002"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.setGeometry(0, 0, *SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())