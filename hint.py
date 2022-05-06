import time
from datetime import datetime

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import clientui
import emojiinfo


dict = {":laughing:": "😂", "smiley": "😁", ":smile1:": "😃", ":smile2:": "😄", ":smile3:": "😅",
        ":smile4:": "😆", ":shy:": "😇", ":demon:": "😈", ":smile6:": "😉", ":smile7:": "😊",
        ":smile8:": "😋", ":smile9:": "😌", ":loving:": "😍", ":smile11:": "😎", ":smile12:": "😏",
        ":smile13:": "😐", ":smile14:": "😒", ":smile15:": "😓", ":smile16:": "😔", ":smile17:": "😖",
        ":kissing:": "😘", ":heart:": "❤", ":dirt:": "💩", ":monkey:": "🙈", ":crown:": "👑",
        ":snake:": "🐍", ":chicken:": "🐔", ":ghost:": "👻", ":fire:": "🔥", ":18+:": "🔞",
        ":prize:": "🏆", ":lightning:": "⚡", ":moon:": "🌙", ":mask:": "😷", ":angry:": "😤"}


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
            if text.count(":") >= 2:
                first = text.find(":")
                second = text[first + 1:].find(":") + first + 2
                count = text.count(":")
                while count >= 2 and count % 2 == 0:
                    if text[first:second] in dict:
                        smile = dict[text[first:second]]
                        text = f'{text[:first]}{smile}{text[second + 1:]}'
                        count -= 2
                    try:
                        first = text[second:].find(":") + first + second + 2
                        second = text[first + 1:].find(":") + first + 2
                    except:
                        break

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


class Info(emojiinfo.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Messenger(host="https://952d-178-176-77-77.eu.ngrok.io")
    window.show()
    app.exec()