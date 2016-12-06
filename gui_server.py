import os
import sys
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QTcpServer, QHostAddress

class ServerWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

		self.server = QTcpServer(self)
		self.server.listen(QHostAddress('0.0.0.0'), 1488)

		self.server.newConnection.connect(self.new_connection_handler)


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


	def new_connection_handler(self):
		socket = self.server.nextPendingConnection()
		socket.nextBlockSize = 0
		self.txt_view.append('<font color="green">New connection {}:{}</font>'.format(
			socket.peerAddress().toString(),
			socket.peerPort()))

		socket.readyRead.connect(self.receive_message)
		socket.disconnected.connect(self.client_disconnected)


	def receive_message(self):
		s = self.sender()
		if s.bytesAvailable() > 0:
			stream = QDataStream(s)
			client_data = stream.readQString()
			self.txt_view.append(client_data)

			# options = {
			# 	'View All': self.show_all,
			# }

			self.send_message(s, 'test')


	def send_message(self, socket, msg):
		reply = QByteArray()
		stream = QDataStream(reply, QIODevice.WriteOnly)
		stream.writeQString(msg)
		socket.write(reply)


	def client_disconnected(self):
		self.txt_view.append('<font color="red">{}:{} has disconnected</font>'.format(
			self.sender().peerAddress().toString(),
			self.sender().peerPort()))

#--------------------------------------

	def open_db(self, dbfilename):
		if os.path.isfile(dbfilename):
			with open(dbfilename, 'rb') as f:
				data = f.read()
				db = pickle.loads(data)
				self.txt_view.append('File was loaded.')
				return db
		else:
			return []

	def show_all(self):
		if not self.db: return '<<< DB is empty'
		items = [str(x) for x in self.db]
		res = '\n'.join(items)
		return res


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = ServerWindow()
	sys.exit(app.exec_())
