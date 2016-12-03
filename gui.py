import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QListView, QRadioButton,
	QTextBrowser)
from PyQt5.QtGui import QIcon

class ClientWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()


	def initUI(self):
		lstView = QListView()
		txtView = QTextBrowser()
		txtView.append('INFO FROM SERVER')

		left_vbox = QVBoxLayout()
		left_vbox.addWidget(lstView)
		left_vbox.addWidget(txtView)

		radio_text = ('View All', 'Add New', 'Edit', 'Delete', 'Search')
		radio_buttons = [QPushButton(x) for x in radio_text]
		exec_btn = QPushButton('>>>')

		right_vbox = QVBoxLayout()
		[right_vbox.addWidget(r) for r in radio_buttons]
		right_vbox.addStretch()
		right_vbox.addWidget(exec_btn)

		hbox = QHBoxLayout()
		hbox.addLayout(left_vbox)
		hbox.addLayout(right_vbox)

		self.setLayout(hbox)

		self.setWindowTitle('Client')
		self.setGeometry(300, 300, 350, 400)
		self.setWindowIcon(QIcon('icon.png'))

		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = ClientWindow()
	sys.exit(app.exec_())