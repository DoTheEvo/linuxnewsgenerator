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


class Form(Qw.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.reddit_data = []

    def setupUi(self, Form):
        Form.resize(400, 270)

        self.list_widget = Qw.QListWidget(Form)
        item = Qw.QListWidgetItem()
        self.list_widget.addItem(item)

        self.source_combox = Qw.QComboBox(Form)
        self.source_combox.addItem("Reddit - /r/linux")
        self.source_combox.addItem("linux.slashdot.org")

        self.roll_button = Qw.QPushButton('Start')
        self.roll_button.clicked.connect(self.roll_the_news)

        grid = Qw.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.list_widget, 1, 1, 2, 2)
        grid.addWidget(self.source_combox, 3, 1)
        grid.addWidget(self.roll_button, 3, 2)
        self.setLayout(grid)

    def roll_the_news(self):
        if not self.reddit_data:
            self.get_reddit_r_linux()
            self.roll_button.setText('Re-Roll')

        random_news = random.sample(self.reddit_data, 5)
        self.populate_list(random_news)

    def populate_list(self, news_list):
        self.list_widget.clear()
        for z in news_list:
            self.list_widget.addItem('>{}'.format(z.title))
            self.list_widget.addItem(z.url)

    def get_reddit_r_linux(self):
        yesterday = time.time() - (24*60*60)
        r = praw.Reddit(user_agent='linuxnewsgenerator')
        submissions = r.get_subreddit('linux').get_new(limit=100)
        for z in submissions:
            print(z.title)
            print(z.is_self)
            if z.created_utc < yesterday and not z.is_self:
                self.reddit_data.append(z)


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    screen = Form()
    screen.show()
    sys.exit(app.exec_())
