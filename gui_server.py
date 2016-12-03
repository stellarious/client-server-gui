import os
import sys
import pickle
from PyQt5.QtWidgets import (QWidget, QPushButton, 
	QVBoxLayout, QApplication,	QTextBrowser, QMessageBox)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QTcpServer, QHostAddress

class ServerWindow(QWidget):
	def __init__(self):
		super().__init__()
		
		self.initUI()

		self.host = ''
		self.port = 1488
		self.dbfilename = 'db.dat'

		self.open_db(self.dbfilename)

		server = QTcpServer(self)
		server.listen(QHostAddress('0.0.0.0'), self.port)

		server.newConnection.connect(self.new_client_handler)


	def initUI(self):	
		self.txt_view = QTextBrowser()
		quit_button = QPushButton("Stop'n'quit")
		quit_button.clicked.connect(QCoreApplication.instance().quit)

		vbox = QVBoxLayout()
		vbox.addWidget(self.txt_view)
		vbox.addWidget(quit_button)

		self.setLayout(vbox)

		self.setWindowTitle('Server')
		self.setGeometry(700, 300, 350, 400)

		self.show()


	def new_client_handler(self):
		socket = self.sender().nextPendingConnection()
		self.txt_view.append('<font color="green">New connection {}:{}</font>'.format(
			socket.peerAddress().toString(),
			socket.peerPort()))
		
		socket.disconnected.connect(self.client_disconnected)


	def client_disconnected(self):
		self.txt_view.append('<font color="red">{}:{} was disconnected</font>'.format(
			self.sender().peerAddress().toString(),
			self.sender().peerPort()))


	def open_db(self, dbfilename):
		if os.path.isfile(dbfilename):
			with open(dbfilename, 'rb') as f:
				data = f.read()
				db = pickle.loads(data)
				self.txt_view.append('File was loaded.')
				return db
		else:
			return []


	# def closeEvent(self, event):
	# 	reply = QMessageBox.question(self, 'Message',
	# 		"Are you sure to quit?", QMessageBox.Yes |
	# 		QMessageBox.No, QMessageBox.No)

	# 	if reply == QMessageBox.Yes:
	# 		event.accept()
	# 	else:
	# 		event.ignore()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = ServerWindow()
	sys.exit(app.exec_())