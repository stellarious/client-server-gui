import itertools

class StorageSystem:
	class_counter = itertools.count(0)


	def __init__(self, args):
		self.id = int(next(self.class_counter))
		self.model = args[0]
		self.system_cache = int(args[1])
		self.max_controllers = int(args[2])
		self.protocols = args[3]
		self.port_types = args[4]
		self.max_disks = int(args[5])
		self.price = int(args[6])


	def __str__(self):
		return '{}.{}, {} MiB, {} disks, ${}'.format(
			self.id, self.model, self.system_cache,
			self.max_disks, self.price)
