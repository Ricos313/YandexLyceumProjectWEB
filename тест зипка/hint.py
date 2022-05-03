import time
from datetime import datetime

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import clientui



class Messenger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, host):
        self.host = host
        super().__init__()
        self.setupUi(self)
        self.after = 0
        self.pushButton.pressed.connect(self.send_message)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_message)
        self.timer.start(1000)

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        try:
            data = {
                "name": name,
                "text": text
            }
            responce = requests.post(f"{self.host}/send", json=data)
        except:
            self.textBrowser.append('Сервер недоступен\nПопробуйте позже\n')
            return
        if responce.status_code != 200:
            self.textBrowser.append('Проверьте имя или текст\n')
            return
        self.textEdit.setText('')

    def print_message(self, message):
        t = message['time']
        dt = datetime.fromtimestamp(t)
        dt = dt.strftime('%H:%M')
        self.textBrowser.append(dt + " " + message["name"])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def get_message(self):
        try:
            response = requests.get(f"{self.host}/messages", params={'after': self.after})
        except:
            return
        messages = response.json()['messages']
        for message in messages:
            self.print_message(message)
            self.after = message['time']


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Messenger(host="https://69e1-95-140-31-114.eu.ngrok.io")
    window.show()
    app.exec()