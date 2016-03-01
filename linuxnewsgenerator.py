import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

from bs4 import BeautifulSoup
import praw
import queue
import random
import re
import requests
import sys
import threading
import time
import unicodedata as ud


class checkboxes(Qw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.one_check = Qw.QCheckBox()
        self.two_check = Qw.QCheckBox()
        self.three_check = Qw.QCheckBox()
        self.four_check = Qw.QCheckBox()
        self.five_check = Qw.QCheckBox()

        vertical_lay = Qw.QVBoxLayout()
        vertical_lay.addWidget(self.one_check)
        vertical_lay.addWidget(self.two_check)
        vertical_lay.addWidget(self.three_check)
        vertical_lay.addWidget(self.four_check)
        vertical_lay.addWidget(self.five_check)

        print(vertical_lay.getContentsMargins())
        self.setLayout(vertical_lay)

        self.setFixedWidth(35)


class Form(Qw.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.reddit_data = []

    def setupUi(self, Form):
        Form.resize(700, 400)

        self.checkies = checkboxes()

        self.text_output = Qw.QTextEdit(Form)
        self.text_output.setStyleSheet('background:#D6DAF0;')

        self.source_combox = Qw.QComboBox(Form)
        self.source_combox.addItem("Reddit - /r/linux")
        self.source_combox.addItem("linux.slashdot.org")

        self.roll_button = Qw.QPushButton('Start')
        self.roll_button.clicked.connect(self.roll_the_news)

        grid = Qw.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.checkies, 0, 0, 2, 1)
        grid.addWidget(self.text_output, 0, 1, 2, 2)
        grid.addWidget(self.source_combox, 3, 1, 1, 1)
        grid.addWidget(self.roll_button, 3, 2, 1, 1)
        self.setLayout(grid)

    def roll_the_news(self):
        if not self.reddit_data:
            self.get_reddit_r_linux()
            self.roll_button.setText('Re-Roll')

        random_news = random.sample(self.reddit_data, 5)
        self.populate_list(random_news)

    def populate_list(self, news_list):
        self.text_output.clear()
        for z in news_list:
            self.text_output.append('<big><b><font color=#789922>>{}</big></b></font color>'.format(z.title))
            self.text_output.append(z.url)
            self.text_output.append('')

    def get_reddit_r_linux(self):
        yesterday = time.time() - (24*60*60)
        r = praw.Reddit(user_agent='linuxnewsgenerator')
        submissions = r.get_subreddit('linux').get_new(limit=100)
        for z in submissions:
            print(z.title)
            print(z.created_utc)
            print(yesterday)
            print(z.created_utc - yesterday)
            if z.created_utc > yesterday and not z.is_self:
                self.reddit_data.append(z)


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    screen = Form()
    screen.show()
    sys.exit(app.exec_())
