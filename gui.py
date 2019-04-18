from PyQt5 import QtCore, QtGui, QtWidgets
import settings


class Ui_Dialog(object):
    def startUi(self, Dialog=None):
        if Dialog is None:
            Dialog = self
        else:
            self.gridLayout = QtWidgets.QGridLayout(Dialog)
            self.gridLayout.setObjectName('gridLayout')
        Dialog.setObjectName('Dialog')
        Dialog.resize(900, 500)
        self.settings = settings
        self.labels = []
        self.spins = []
        _translate = QtCore.QCoreApplication.translate
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName('pushButton')
        self.pushButton.setText(_translate('Dialog', 'Запуск симуляции'))
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 2)
        for index, (var_name, pack) in enumerate(settings._strings.items()):
            type_v, min_v, max_v, name = pack
            label = QtWidgets.QLabel(Dialog)
            label.setObjectName('label'+str(index))
            label.setText(_translate('Dialog', name))
            self.gridLayout.addWidget(label, index+1, 0, 1, 1)
            self.labels.append(label)
            if type_v == 'I':
                spinBox = QtWidgets.QSpinBox(Dialog)
                spinBox.setObjectName('spinBox'+str(index))
                if min_v > 0:
                    spinBox.setMinimum(min_v)
                else:
                    spinBox.setMinimum(-2**30+1)
                if max_v > 0:
                    spinBox.setMaximum(max_v)
                else:
                    spinBox.setMaximum(2**30)
                spinBox.setValue(getattr(settings, var_name))
                self.gridLayout.addWidget(spinBox, index+1, 1, 1, 1)
                self.spins.append(spinBox)
            elif type_v == 'R':
                spinBox = QtWidgets.QDoubleSpinBox(Dialog)
                spinBox.setObjectName('spinBox'+str(index))
                if min_v > 0.0:
                    spinBox.setMinimum(min_v)
                else:
                    spinBox.setMinimum(-2.0**126)
                if max_v > 0.0:
                    spinBox.setMaximum(max_v)
                else:
                    spinBox.setMaximum(2.0**127)
                spinBox.setValue(getattr(settings, var_name))
                spinBox.setSingleStep(spinBox.value()*0.1)
                self.gridLayout.addWidget(spinBox, index+1, 1, 1, 1)
                self.spins.append(spinBox)
        Dialog.setWindowTitle(_translate('Dialog', 'Настройка параметров'))
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def clear(self):
        self.listWidget.close()
        self.listWidget2.close()
        self.listWidget3.close()
        self.lcdNumber.close()
        self.progressBar.close()
        self.pushButton.close()
        self.pushButton2.close()
        self.pushButton3.close()
        for label in self.label:
            label.close()

    def setupUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setObjectName('Dialog')
        Dialog.setWindowTitle(_translate('Dialog', 'Книжный магазин'))
        Dialog.resize(1600, 900)
        self.label = [QtWidgets.QLabel(Dialog) for i in range(4)]
        for index, label in enumerate(self.label):
            label.setObjectName(f'label{index}')

        # Первый столбец
        vertical = 0
        self.gridLayout.addWidget(self.label[0], 0, vertical, 1, 1)
        self.label[0].setText(_translate(
            'Dialog', 'Весь ассортимент магазина, с числом хранимых единиц'))
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setMinimumWidth(200)
        self.listWidget.setObjectName('listWidget')
        self.gridLayout.addWidget(self.listWidget, 1, vertical, 2, 1)
        self.gridLayout.addWidget(self.label[3], 3, vertical, 1, 1)
        self.label[3].setText(_translate('Dialog', f'Общий доход за отчётный период: {0}'))

        # Третий столбец
        vertical = 3
        self.gridLayout.addWidget(self.label[2], 0, vertical, 1, 1)
        self.label[2].setText(_translate(
            'Dialog', 'Список покупателей, пришедших за шаг моделирования, и их число'))
        self.lcdNumber = self.create_lcd_number()
        self.gridLayout.addWidget(self.lcdNumber, 1, vertical, 1, 1)
        self.listWidget2 = QtWidgets.QListWidget(Dialog)
        self.listWidget2.setMinimumWidth(200)
        self.listWidget2.setObjectName('listWidget2')
        self.gridLayout.addWidget(self.listWidget2, 2, vertical, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setObjectName('progressBar')
        self.gridLayout.addWidget(self.progressBar, 3, vertical, 1, 1)

        # Второй столбец
        vertical = 1
        self.pushButton2 = QtWidgets.QPushButton(Dialog)
        self.pushButton2.setObjectName('pushButton')
        self.pushButton2.setText(_translate('Dialog', 'Перезапуск'))
        self.gridLayout.addWidget(self.pushButton2, 0, vertical, 1, 1)
        self.pushButton3 = QtWidgets.QPushButton(Dialog)
        self.pushButton3.setObjectName('pushButton')
        self.pushButton3.setText(_translate('Dialog', 'Выход'))
        self.gridLayout.addWidget(self.pushButton3, 0, vertical+1, 1, 1)
        self.label[1].setText(_translate(
            'Dialog', 'Список ожидаемых в будущем заявок, отсортированный по датам'))
        self.gridLayout.addWidget(self.label[1], 1, vertical, 1, 2)
        self.listWidget3 = QtWidgets.QListWidget(Dialog)
        self.listWidget3.setMinimumWidth(200)
        self.listWidget3.setObjectName('listWidget3')
        self.gridLayout.addWidget(self.listWidget3, 2, vertical, 1, 2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName('pushButton')
        self.gridLayout.addWidget(self.pushButton, 3, vertical, 1, 2)
        self.pushButton.setText(_translate(
            'Dialog', 'Шаг моделирования (1 день)'))
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def create_lcd_number(self):
        lcdNumber = QtWidgets.QLCDNumber(self)
        lcdNumber.setFrameShape(QtWidgets.QFrame.WinPanel)
        lcdNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        lcdNumber.setSmallDecimalPoint(False)
        lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        lcdNumber.setObjectName('lcdNumber')
        return lcdNumber
