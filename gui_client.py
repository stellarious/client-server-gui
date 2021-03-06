import sys
import pickle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from dialogs import AddDialog, SearchDialog, SortDialog, EditDialog


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

	def query_manager(self):
		action = self.sender().text()

		if action == 'View All':
			q = (action, 0)
			self.send_query(q)

		elif action == 'Add New':
			ok, data = AddDialog.get_data()
			if ok:
				q = (action, data)
				self.send_query(q)

		elif action == 'Edit':
			try:
				current_id = self.lst_view.currentItem().text().split('.')[0]
			except:
				self.show_message('Choose a record.')
				return

			ok, (attr, new_val) = EditDialog.get_data()
			data = (current_id, attr, new_val)

			if ok:
				q = (action, data)
				self.send_query(q)

		elif action == 'Delete':
			try:
				data = self.lst_view.currentItem().text().split('.')[0]
			except:
				self.show_message('Choose a record.')
				return

			q = (action, data)
			self.send_query(q)

		elif action == 'Sort':
			if self.lst_view.count():
				ok, data = SortDialog.get_data()
				if ok:
					q = (action, data)
					self.send_query(q)

		elif action == 'Search':
			if self.lst_view.count():
				ok, data = SearchDialog.get_data()
				if ok:
					q = (action, data)
					self.send_query(q)


	def show_message(self, message):
		reply = QMessageBox.question(self, 'Message', message, QMessageBox.Ok)


	def send_query(self, data):
		bytes_data = pickle.dumps(data)
		self.request = QByteArray(bytes_data)
		self.socket.write(self.request)


	def sock_error(self):
		msg = QMessageBox.critical(self, 'Connection Error',
		self.sender().errorString(), QMessageBox.Ok)
		sys.exit(1)


	def initUI(self):
		self.lst_view = QListWidget()
		self.txt_view = QTextBrowser()

		left_vbox = QVBoxLayout()
		left_vbox.addWidget(self.lst_view)
		left_vbox.addWidget(self.txt_view)

		buttons_text = ('View All', 'Add New', 'Edit',
			'Delete', 'Sort', 'Search')
		buttons = [QPushButton(x) for x in buttons_text]

		[btn.clicked.connect(self.query_manager) for btn in buttons]

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
			server_reply = s.read(4096)

		reply = pickle.loads(server_reply)

		ok, data = reply
		if ok:
			self.txt_view.append('<<< OK')
			self.lst_view.clear()
			[self.lst_view.addItem(QListWidgetItem(str(x))) for x in data]
		else:
			self.txt_view.append(str(data))


if __name__ == '__main__':
	app = QApplication(sys.argv)

	HOST = '127.0.0.1'
	PORT = 1488

	w = ClientWindow(HOST, PORT)
	sys.exit(app.exec_())
