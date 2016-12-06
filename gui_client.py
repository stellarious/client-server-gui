import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QTcpSocket, QHostAddress

class ClientWindow(QWidget):
	def __init__(self, host, port):
		super().__init__()
		self.connect(host, port)
		self.initUI()


	def connect(self, host, port):
		self.socket = QTcpSocket()
		self.socket.connectToHost(host, port)

		self.socket.connected.connect(self.handle_connection)
		self.socket.error.connect(self.sock_error)
		self.socket.readyRead.connect(self.read_from_server)


	def handle_connection(self):
		self.txt_view.append('Connected to {}:{}'.format(
			self.socket.peerAddress().toString(),
			self.socket.peerPort()))


	def send_query(self):
		action = self.sender().text()

		self.request = QByteArray()
		stream = QDataStream(self.request, QIODevice.WriteOnly)
		stream.writeQString(action)
		self.socket.write(self.request)


	def sock_error(self):
		msg = QMessageBox.critical(self, 'Connection Error',
		self.sender().errorString(), QMessageBox.Ok)
		sys.exit(1)


	def initUI(self):
		self.lst_view = QListView()
		self.txt_view = QTextBrowser()

		left_vbox = QVBoxLayout()
		left_vbox.addWidget(self.lst_view)
		left_vbox.addWidget(self.txt_view)

		buttons_text = ('View All', 'Add New', 'Edit', 'Delete', 'Search')
		buttons = [QPushButton(x) for x in buttons_text]

		[btn.clicked.connect(self.send_query) for btn in buttons]

		right_vbox = QVBoxLayout()
		[right_vbox.addWidget(r) for r in buttons]
		right_vbox.addStretch()

		hbox = QHBoxLayout()
		hbox.addLayout(left_vbox)
		hbox.addLayout(right_vbox)

		self.setLayout(hbox)

		self.setWindowTitle('Client')
		self.setGeometry(300, 300, 350, 400)
		self.setWindowIcon(QIcon('icon.png'))

		self.show()


	def read_from_server(self):
		s = self.sender()
		if s.bytesAvailable() > 0:
			stream = QDataStream(s)
			client_data = stream.readQString()
			self.txt_view.append(client_data)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	HOST = '127.0.0.1'
	PORT = 1488

	w = ClientWindow(HOST, PORT)
	sys.exit(app.exec_())
