import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

from bs4 import BeautifulSoup
from copy import copy
import feedparser
import praw
import queue
import random
import re
import requests
import sys
import threading
import time
import unicodedata as ud


class Rss_object:
    def __init__(self, title, url, locked_by_checkbox=False):
        self.title = title
        self.url = url
        self.locked_by_checkbox = locked_by_checkbox


class Checkboxes(Qw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.checkies = []
        vertical_lay = Qw.QVBoxLayout()

        for x in range(5):
            self.checkies.append(Qw.QCheckBox())

        for x in self.checkies:
            vertical_lay.addWidget(x)

        self.setLayout(vertical_lay)
        self.setFixedWidth(35)


class Form(Qw.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.news_data = []
        self.reddit_data = []
        self.slashdot_data = []
        self.random_news = []
        self.accepted_stories = {}

    def setupUi(self, Form):
        Form.resize(700, 400)

        self.cb = Checkboxes()
        self.cb.setDisabled(True)

        self.text_output = Qw.QTextEdit(Form)
        self.text_output.setStyleSheet('background:#D6DAF0;')

        self.source_combox = Qw.QComboBox(Form)
        self.source_combox.addItem("linux.slashdot.org")
        self.source_combox.addItem("Reddit - /r/linux")

        self.roll_button = Qw.QPushButton('Start')
        self.roll_button.clicked.connect(self.roll_the_news)

        grid = Qw.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.cb, 0, 0, 2, 1)
        grid.addWidget(self.text_output, 0, 1, 2, 2)
        grid.addWidget(self.source_combox, 3, 1, 1, 1)
        grid.addWidget(self.roll_button, 3, 2, 1, 1)
        self.setLayout(grid)

        for x in self.cb.checkies:
            x.stateChanged.connect(self.checkbox_got_checked)

    def roll_the_news(self):
        combo_val = self.source_combox.currentIndex()

        if combo_val == 0:
            self.news_data = self.slashdot_data
        if combo_val == 1:
            self.news_data = self.reddit_data

        if not self.news_data:
            if combo_val == 0:
                self.slashdot_data = self.get_shashdot_linux()
                self.news_data = self.slashdot_data
            if combo_val == 1:
                self.reddit_data = self.get_reddit_r_linux()
                self.news_data = self.reddit_data

            self.cb.setDisabled(False)
            self.roll_button.setText('Re-Roll')

            for z in range(5 - len(self.random_news)):
                self.random_news.append(copy(random.choice(self.news_data)))

        self.text_output.clear()

        for x in range(5):
            if not self.random_news[x].locked_by_checkbox:
                r = random.choice(self.news_data)
                while True:
                    should_break = True
                    for z in self.random_news:
                        if r.title == z.title:
                            r = random.choice(self.news_data)
                            should_break = False
                    if should_break:
                        break
                self.random_news[x] = copy(r)

        for z in self.random_news:
            self.text_output.append('<big><b><font color=#789922>>{}</big></b></font color>'.format(z.title))
            self.text_output.append(z.url)
            self.text_output.append('')

    def checkbox_got_checked(self):
        for i in range(5):
            if self.cb.checkies[i].isChecked():
                self.random_news[i].locked_by_checkbox = True
            else:
                self.random_news[i].locked_by_checkbox = False

    def get_reddit_r_linux(self):
        result = []
        yesterday = time.time() - (24*60*60)
        r = praw.Reddit(user_agent='linuxnewsgenerator')
        submissions = r.get_subreddit('linux').get_new(limit=100)
        for z in submissions:
            if z.created_utc > yesterday and not z.is_self:
                z.locked_by_checkbox = False
                result.append(z)
        return result

    def get_shashdot_linux(self):
        result = []
        rss_url = 'http://rss.slashdot.org/Slashdot/slashdotLinux'
        f = feedparser.parse(rss_url)
        for p in f.entries:
            url = p.feedburner_origlink.split('?')[0]
            z = Rss_object(p.title, url)
            result.append(z)
        return result

if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    screen = Form()
    screen.show()
    sys.exit(app.exec_())
