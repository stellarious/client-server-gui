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

		self.db = self.open_db('db.dat')

		self.server = QTcpServer(self)
		self.server.listen(QHostAddress('0.0.0.0'), 1488)

		self.server.newConnection.connect(self.new_connection_handler)

		self.options = {
			'View All': self.show_all,
			# 'Add New': pass,
		}

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
		self.setWindowIcon(QIcon('server_icon.png'))
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
			client_data = s.read(4096)

		request = pickle.loads(client_data)
		cmd_name = request[0]
		cmd_params = request[1]

		self.txt_view.append('{}: {}'.format(cmd_name, cmd_params))

		try:
			cmd_name = request[0]
			cmd_params = request[1]
			self.send_message(s, self.options[cmd_name](cmd_params))
		except:
			self.txt_view.append('Coming soon')


	def send_message(self, socket, data):
		bytes_data = pickle.dumps(data)
		reply = QByteArray(bytes_data)
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

	def show_all(self, p):
		if not self.db: return '<<< DB is empty'
		items = [str(x) for x in self.db]
		res = '\n'.join(items)
		return res


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = ServerWindow()
	sys.exit(app.exec_())
