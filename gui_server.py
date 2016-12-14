import os
import sys
import pickle
import operator
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from storageModel import StorageSystem


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
			'Add New': self.add_record,
			'Delete': self.delete_record,
			'Search': self.search,
			'Sort': self.sort,
			'Edit': self.edit_record
		}

	def initUI(self):
		self.txt_view = QTextBrowser()

		vbox = QVBoxLayout()
		vbox.addWidget(self.txt_view)

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
		cmd_name, cmd_params = request
		self.txt_view.append('{}: {}'.format(cmd_name, cmd_params))

		try:
			self.send_message(s, self.options[cmd_name](cmd_params))
		except Exception as e:
			self.txt_view.append(str(e))


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
				try:
					db = pickle.loads(data)
					self.txt_view.append('File was loaded.')
					return db
				except:
					return []
		else:
			return []

	def show_all(self, p):
		if not self.db: return (False, '<<< DB is empty')
		return (True, self.db)

	def add_record(self, args):
		try:
			new_record = StorageSystem(args)
			self.db.append(new_record)
			return (True, self.db)
		except Exception as e:
			return (False, '<<< Bad data')

	def edit_record(self, args):
		try:
			obj_id = int(args[0])
		except:
			return (False, '<<< Wrong param')

		field, new_value = args[1], args[2]

		try:
			new_value = int(new_value)
		except:
			pass

		for item in self.db:
			if item.id == obj_id:
				try:
					setattr(item, field, new_value)
					return (True, self.db)
				except:
					return (False, '<<< Bad data')


	def delete_record(self, obj_id):
		if not self.db: return '<<< DB is empty'

		obj_id = int(obj_id)

		for item in self.db:
			if item.id == obj_id:
				self.db.remove(item)
				return (True, self.db)

	def search(self, args):
		field, value = args
		try:
			value = int(value) #convert if int
		except:
			pass

		field_vals = list(map(operator.attrgetter(field), self.db))
		items_vals = list(zip(self.db, field_vals))
		items = [x[0] for x in items_vals if x[1] == value]
		if items: return (True, items)
		return (False, '<<< Nothing found')

	def sort(self, args):
		sorted_items = list(sorted(self.db, key=operator.attrgetter(args)))
		return (True, sorted_items)

	def closeEvent(self, event):
		with open('db.dat', 'wb') as f:
			data = pickle.dumps(self.db)
			f.write(data)
			self.txt_view.append('Data saved.')

		if self.db:
			with open('last_id', 'w') as tf:
				tf.write(str(self.db[-1].id))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = ServerWindow()
	sys.exit(app.exec_())
