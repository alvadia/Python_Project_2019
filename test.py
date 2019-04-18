import random
import string
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import gui
import settings
from bookStore import BookStore
class Example(QDialog, gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.start = 1
        self.startUi(self)
        self.pushButton.clicked.connect(self.buttonClicked)
    def start_simulation(self):
        self.setupUi(self)
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton2.clicked.connect(self.restart)
        self.pushButton3.clicked.connect(self.exit)
        self.mainStore = BookStore()
        for book in self.mainStore.book_index:
            self.listWidget.addItem(str(book))
        self.progressBar.value = self.mainStore.current_day
        self.lcdNumber.value = 0
    def restart(self):
        self.clear()
        self.start = 1
        self.startUi()
        self.pushButton.clicked.connect(self.buttonClicked)
    def exit(self):
        self.close()
    def buttonClicked(self):
        if self.start == 1:
            self.start = 0
            import settings
            lst = [s for s in dir(settings) if not s.startswith('_')]
            for index, var_name in enumerate(settings._strings):
                setattr(settings, var_name, self.spins[index].value())
                self.spins[index].close()
                self.labels[index].close()
            del self.spins
            del self.labels
            self.pushButton.close()
            self.gridLayout.update()
            self.start_simulation()
        else:
            income = int(self.mainStore.params['income'])
            self.label[3].setText(f"Общий доход за весь период:{income}")
            if self.mainStore.current_day == self.settings.finalDay:
                self.listWidget.clear()
                for index, label in enumerate(self.label):
                    if index==0:
                        self.label[index].setText(f"Статистика проданных книг.")
                    elif index==1:
                        self.label[index].setText(f"Список заявок, которые придут после горизонта событий моделирования:")
                    elif index==2:
                        self.label[index].setText(f"Список всех покупателей, приходивших в магазин, с их данными")
                    elif index==3:
                        self.label[index].setText(f"Общий доход за всё время моделирования составил {income}.")
                    else:
                        self.label[index].setText('')
                self.lcdNumber.display(len(self.mainStore.buyer_index))
                for book in self.mainStore.book_statistic():
                    temp = QListWidgetItem(book)
                    self.listWidget.addItem(temp)
                self.listWidget2.clear()
                for buyer in self.mainStore.buyer_statistic():
                    temp = QListWidgetItem(buyer)
                    self.listWidget2.addItem(temp)
                self.listWidget3.clear()
                for bid in self.mainStore.get_bids():
                    temp = QListWidgetItem(bid)
                    self.listWidget3.addItem(temp)
                Dialog.setWindowTitle(_translate("Dialog", "Статистика"))
            else:
                if self.settings._const_DEBUG:
                    print(str(self.mainStore.tick()))
                else:
                    mainStore.tick()
                self.listWidget2.clear()
                for order, flag in self.mainStore.orderlog:
                    temp = QListWidgetItem(order)
                    if not flag:
                        temp.setForeground(QColor(255,0,0))
                    self.listWidget2.addItem(temp)
                self.listWidget.clear()
                for book in self.mainStore.book_index:
                    temp = QListWidgetItem(str(book))
                    if book.is_low_count():
                        temp.setForeground(QColor(255,0,0))
                    self.listWidget.addItem(temp)
                self.listWidget3.clear()
                for bid in self.mainStore.get_bids():
                    temp = QListWidgetItem(bid)
                    self.listWidget3.addItem(temp)
                self.lcdNumber.display(len(self.mainStore.orderlog))
                self.progressBar.setProperty('value', self.mainStore.current_day * 100 / self.settings.finalDay)
                self.progressBar.setFormat('Day '+str(self.mainStore.current_day))
def run():
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    app.exec()
if __name__ == '__main__':
    run()
