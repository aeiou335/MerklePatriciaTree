import random
import unittest
import MerklePatriciaTrie as MPT
import time
from hashlib import sha256
import string
import plyvel
import pickle
class TestingClass(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestingClass, self).__init__(*args, **kwargs)
		testdb = plyvel.DB("test", create_if_missing = True)
		self.test = MPT.MerklePatriciaTrie(testdb,"")
		self.db = plyvel.DB("rootDB", create_if_missing = True)
	def test_all(self):
		
		start = time.time()
		values = ["aaaaaaaa", "bbbbbbbb", "cccccccc", "dddddddd", "eeeeeeee"]
		keys = ["h7766", "h7777", "hoios", "h7234", "hnvuw"]
		for j in range(5):
			#s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
			
			#val = ''.join(random.choice(string.digits) for _ in range(8))
			#key = sha256(s.encode('utf-8')).hexdigest()
			#key = s[j]
			#keys.append(key)
			#values.append(val)
			self.test.update(keys[j], values[j])
			#print("Insert {} datas with time {}".format((j+1)*250000,time.time()))
			for i in range(25):
				s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
				val = ''.join(random.choice(string.digits) for _ in range(8))
				key = sha256(s.encode('utf-8')).hexdigest()
				self.test.update(key, val)
		end = time.time()
		print("Insert time:", end-start)
		print(self.test.id)
		"""
		for i in range(10):
			start = time.time()
			self.assertEqual(self.test.search(keys[i]), values[i])
			end = time.time()
			print("Search time:", end-start)
		"""
		#print("Key count:", self.test.count_key_num())
		print("Current root:", self.test.root_hash())
		self.db.put(b"BlockTrie", self.test.root_hash())
		print(self.db.get(b"BlockTrie"))
		#print(self.db.Get(b"BlockTrie")[0:])
		print(keys[0], values[0])
		print(keys[1], values[1])
		print(self.test.iter_subtree('hoo'))
		"""
Aa98w43xfu
llAOyh5rrs
DbvtXrhkPk
NI1WE03dio
yjo0ZeJlzS
opD5GQKfwN
qsZLKUpjwK
tC2nmSnTPg
COYEsba1Ff
SF8HzHMFiP
		self.assertTrue(self.test.node_type(self.test.root), "Blank")
		self.test.update('\x01\x02\x57',"dog")
		k, v = self.test.root
		self.assertEqual(v, "dog")
		self.test.update('\x01\x02\x58', "dig")
		self.assertTrue(self.test.node_type(self.test.root), "Extension")
		k, v = self.test.root
		node = self.test.decode(v)
		self.assertTrue(self.test.node_type(node), "Branch")
		k, v = self.test.decode(node[7])
		self.assertEqual(v,"dog")
		k, v = self.test.decode(node[8])
		self.assertEqual(v,"dig")
		print(node)
		self.test.update('\x01\x02', "dag")
		
		k, v = self.test.root
		node = self.test.decode(v)
		print(node)
		self.assertEqual(node[-1], "dag")
		node = self.test.decode(node[5])
		self.assertTrue(self.test.node_type(node), "Branch")
		self.test.update('\x01\x02', "dagg")
		k, v = self.test.root
		node = self.test.decode(v)
		self.assertEqual(node[-1], "dagg")
		self.test.update('\x01\x02\x57\x57', "dogg")
		self.test.update('\x01\x02\x57\x57', "doggg")
		k, v = self.test.root
		node = self.test.decode(v)
		k, v = self.test.decode(self.test.decode(self.test.decode(node[5])[7])[5])
		self.assertEqual(v, "doggg")
		print("-------------------------------------------------------")
		self.assertEqual(self.test.search('\x01\x02\x57'), "dog")
		self.assertEqual(self.test.search('\x01\x02\x58'), "dig")
		self.assertEqual(self.test.search('\x01\x02\x57\x57'), "doggg")
		self.assertEqual(self.test.search('\x01\x02'), "dagg")
		print("-------------------------------------------------------")
		self.test.delete('\x01\x02')
		k, v = self.test.root
		node = self.test.decode(v)
		self.test.delete('\x01\x02\x58')
		k,v = self.test.root
		node = self.test.decode(v)
		self.test.delete('\x01\x02\x57')
		k,v = self.test.root
		self.assertEqual(v, "doggg")
		self.test.delete('\x01\x02\x57\x57')
		print("-----------------------------------------------------")
		self.test.update('\x01\x02\x57',"dog")
		self.test.update('\x01\x02\x58', "dig")
		self.test.update('\x01\x02', "dag")
		self.test.update('\x01\x02\x57\x57', "dogg")
		print("Root before delete all:", self.test.root)
		self.test.delete_all()
		print("Root after delete all:",self.test.root)
		self.assertEqual(self.test.search('\x01\x02\x57'), "")
		self.assertEqual(self.test.search('\x01\x02\x58'), "")
		self.assertEqual(self.test.search('\x01\x02\x57\x57'), "")
		self.assertEqual(self.test.search('\x01\x02'), "")
		"""
	#def test_delete_all(self):


if __name__ == '__main__':
	unittest.main()