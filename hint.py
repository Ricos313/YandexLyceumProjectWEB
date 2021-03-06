import time
from datetime import datetime

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import clientui


dict = {":laughing:": "π", "smiley": "π", ":smile1:": "π", ":smile2:": "π", ":smile3:": "π",
        ":smile4:": "π", ":shy:": "π", ":demon:": "π", ":smile6:": "π", ":smile7:": "π",
        ":smile8:": "π", ":smile9:": "π", ":loving:": "π", ":smile11:": "π", ":smile12:": "π",
        ":smile13:": "π", ":smile14:": "π", ":smile15:": "π", ":smile16:": "π", ":smile17:": "π",
        ":kissing:": "π", ":heart:": "β€", ":dirt:": "π©", ":monkey:": "π", ":crown:": "π",
        ":snake:": "π", ":chicken:": "π", ":ghost:": "π»", ":fire:": "π₯", ":18+:": "π",
        ":prize:": "π", ":lightning:": "β‘", ":moon:": "π", ":mask:": "π·", ":angry:": "π€"}


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
                if text[first:second] in dict:
                    smile = dict[text[first:second]]
                    text = f'{text[:first]}{smile}{text[second + 1:]}'

            data = {
                "name": name,
                "text": text
            }
            responce = requests.post(f"{self.host}/send", json=data)
        except:
            self.textBrowser.append('Π‘Π΅ΡΠ²Π΅Ρ Π½Π΅Π΄ΠΎΡΡΡΠΏΠ΅Π½\nΠΠΎΠΏΡΠΎΠ±ΡΠΉΡΠ΅ ΠΏΠΎΠ·ΠΆΠ΅\n')
            return
        if responce.status_code != 200:
            self.textBrowser.append('ΠΡΠΎΠ²Π΅ΡΡΡΠ΅ ΠΈΠΌΡ ΠΈΠ»ΠΈ ΡΠ΅ΠΊΡΡ\n')
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
    window = Messenger(host="https://952d-178-176-77-77.eu.ngrok.io")
    window.show()
    app.exec()