import sys
import socket
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QHBoxLayout, QVBoxLayout, QApplication, QListView, QRadioButton,
	QTextBrowser, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

class ClientWindow(QWidget):

	def __init__(self, host, port):
		super().__init__()
		connection = self.connect(host, port)
		self.initUI()


	def connect(self, host, port):
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			conn.connect((host, port))
		except:
			msg = QMessageBox.critical(self, 'Connection Error',
			'Well, it looks like server is shut down.', QMessageBox.Ok)
			sys.exit(1)
		else:
			return conn


	def initUI(self):	
		lstView = QListView()
		txtView = QTextBrowser()
		txtView.append('INFO FROM SERVER')

		left_vbox = QVBoxLayout()
		left_vbox.addWidget(lstView)
		left_vbox.addWidget(txtView)

		buttons_text = ('View All', 'Add New', 'Edit', 'Delete', 'Search')
		buttons = [QPushButton(x) for x in buttons_text]
		exec_btn = QPushButton('>>>')

		[btn.clicked.connect(self.send_query) for btn in buttons]

		right_vbox = QVBoxLayout()
		[right_vbox.addWidget(r) for r in buttons]
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

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QMessageBox.Yes |
			QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


	def send_query(self):
		self.conn.send()


if __name__ == '__main__':
	app = QApplication(sys.argv)

	HOST = '127.0.0.1'
	PORT = 1488

	w = ClientWindow(HOST, PORT)
	sys.exit(app.exec_())