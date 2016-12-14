import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        labels = ('Model', 'System Cache', 'Max Controllers',
            'Protocols', 'Ports', 'Max Disks', 'Price')

        rxs = ('\w{1,10}', '\d{1,4}', '\d{1,2}', '\w{1,20}',
            '\w{1,20}', '\d{1,4}', '\d{1,5}')

        self.qlabels = [QLabel(x) for x in labels]
        self.hboxes = [QHBoxLayout() for _ in self.qlabels]

        for hb, ql, rx in zip(self.hboxes, self.qlabels, rxs):
            hb.addWidget(ql)
            hb.addStretch()
            tmp_line = QLineEdit()
            rx_validator = QRegExpValidator(QRegExp(rx), tmp_line)
            tmp_line.setValidator(rx_validator)
            tmp_line.textChanged.connect(self.text_edited)
            hb.addWidget(tmp_line)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        [vbox.addLayout(x) for x in self.hboxes]
        vbox.addWidget(self.buttons)

        self.setLayout(vbox)
        self.setModal(True)
        self.setGeometry(300, 300, 270, 270)
        self.setFixedSize(270, 270)
        self.setWindowTitle('Add new record')
        self.show()


    def text_edited(self):
        qlineedit_pos = 2
        for x in self.hboxes:
            if not x.itemAt(qlineedit_pos).widget().text():
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
                return
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)


    def data_from_form(self):
        qlineedit_pos = 2
        return [x.itemAt(qlineedit_pos).widget().text() for x in self.hboxes]


    @staticmethod
    def get_data():
        dialog = AddDialog()
        result = dialog.exec_()
        data = dialog.data_from_form()
        return result == QDialog.Accepted, data


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        attr_names = ('id', 'model', 'system_cache', 'max_controllers',
        'protocols', 'port_types', 'max_disks', 'price')
        self.rxs = ('\d{1,4}', '\w{1,10}', '\d{1,4}', '\d{1,2}', '\w{1,20}',
            '\w{1,20}', '\d{1,4}', '\d{1,5}')

        self.attr_box = QComboBox()
        self.searchline = QLineEdit()

        rx_validator = QRegExpValidator(QRegExp(self.rxs[0]), self.searchline)
        self.searchline.setValidator(rx_validator)

        self.attr_box.currentIndexChanged.connect(self.attr_changed)
        self.searchline.textChanged.connect(self.text_edited)

        [self.attr_box.addItem(x) for x in attr_names]

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(self.attr_box)
        hbox.addWidget(self.searchline)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch()
        vbox.addWidget(self.buttons)

        self.setLayout(vbox)
        self.setModal(True)
        self.setWindowTitle('Search record')
        self.show()


    def attr_changed(self):
        self.searchline.clear()
        index = self.attr_box.currentIndex()
        rx_validator = QRegExpValidator(QRegExp(self.rxs[index]), self.searchline)
        self.searchline.setValidator(rx_validator)


    def text_edited(self):
        if not self.searchline.text():
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
                return
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)


    def data_from_form(self):
        attr = self.attr_box.currentText()
        search_q = self.searchline.text()
        return attr, search_q

    @staticmethod
    def get_data():
        dialog = SearchDialog()
        result = dialog.exec_()
        data = dialog.data_from_form()
        return result == QDialog.Accepted, data


class SortDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        attr_names = ('id', 'model', 'system_cache', 'max_controllers',
        'protocols', 'port_types', 'max_disks', 'price')

        self.attr_box = QComboBox()
        [self.attr_box.addItem(x) for x in attr_names]

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(self.attr_box)
        vbox.addWidget(self.buttons)

        self.setLayout(vbox)
        self.setModal(True)
        self.setWindowTitle('Sort by')
        self.show()


    def data_from_form(self):
        attr = self.attr_box.currentText()
        return attr


    @staticmethod
    def get_data():
        dialog = SortDialog()
        result = dialog.exec_()
        data = dialog.data_from_form()
        return result == QDialog.Accepted, data
