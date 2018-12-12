
# coding: utf-8
import sys
sys.path.append('trie')
#print(sys.path)
import encoding 
#from db import DB as db 

import pickle
from hashlib import sha256

END = 16
class MerklePatriciaTrie:
    def __init__(self,dbname,_root_hash=""):
        self.db = dbname
        self.root = ""
        self.id = self.getCurrentNum()
        self.initial_root_hash(_root_hash)
        
    def initial_root_hash(self,root):
        if root == "":
            return ""
        print('root:', root)
        node = self.db.get(root)
        self.root = pickle.loads(node)

    def getCurrentNum(self):
        try:
            idx = int(self.db.get(b'currentNum').decode())
            #print('s', idx)
            return idx
        except:
            return 0

    def root_hash(self):
        if self.root == "":
            return ""
        hash_key = self.update_db(self.root)
        #print("Call root_hash and the current root hash is", hash_key)
        return hash_key
    
    def node_type(self, node):
        if len(node) == 17:
            return "Branch"
        elif len(node) == 2:
            nib = encoding.hp_to_hex(node[0])
            #print("nib",nib)
            if nib[-1] == END:
                return "Leaf"
            else:
                return "Extension"
        elif node == "":
            return "Blank"
        else:
            raise TypeError("There is no this node type!")
    
    def update_db(self, node):
        if node == "":
            return ""
        assert isinstance(node, list)
        value = pickle.dumps(node)
        key = sha256(value).digest()
        self.db.put(key, value)
        return key

    def decode(self, key):
        if key == "":
            return ""
        return pickle.loads(self.db.get(key))

    def delete_db(self,node):
        if node == "":
            return 
        key = sha256(pickle.dumps(node)).digest()
        self.db.delete(key)


    def update_node(self, node, key, value):
        _node_type = self.node_type(node)
        #print("Node Type:", _node_type)
        if _node_type == 'Branch':
            #key空，直接將value 存在branch node 的最後
            if not key:
                node[-1] = value
            #沿著branch node繼續往下找
            else:   
                new_node = self.update_and_delete(self.decode(node[key[0]]), key[1:], value)
                node[key[0]] = self.update_db(new_node)
            return node
        
        elif _node_type == 'Leaf' or _node_type == 'Extension':
            original_key = ori_key = encoding.terminator(encoding.hp_to_hex(node[0]),False)
            prefix = 0
            for i in range(min(len(ori_key), len(key))):
                if key[i] != ori_key[i]:
                    break
                prefix = i + 1
            key = key[prefix:]
            ori_key = ori_key[prefix:]
            #與現在node's key一樣
            if key == ori_key == []:

                if _node_type == 'Leaf':
                    return [node[0], value]
                new_node = self.update_and_delete(self.decode(node[1]), key, value)
            
            elif ori_key == []:
                #查此extension node的child
                if _node_type == 'Extension':
                    
                    new_node = self.update_and_delete(self.decode(node[1]), key, value)
                #如果是leaf node 開一個branch node 將原本node和new node放進新的branch
                else:
                    new_node = [""]*17
                    new_node[-1] = node[1]
                    new_node[key[0]] = self.update_db([encoding.hex_to_hp(encoding.terminator(key[1:],True)), value])
            
            else:
                new_node = [""]*17
                if len(ori_key) == 1 and _node_type == "Extension":
                    new_node[ori_key[0]] = node[1]
                else:
                    if _node_type == "Extension":
                        ter = False
                    else:
                        ter = True
                    new_node[ori_key[0]] = self.update_db([encoding.hex_to_hp(encoding.terminator(ori_key[1:],ter)),node[1]])
                #if key空 value直接放進branch，else 把剩下的key value存入branch
                if key == []:
                    new_node[-1] = value
                else:
                    new_node[key[0]] = self.update_db([encoding.hex_to_hp(encoding.terminator(key[1:],True)), value])
            #change current node to a extension node which connected with the branch node we create above
            if prefix > 0:
                new_node = [encoding.hex_to_hp(original_key[:prefix]), self.update_db(new_node)]
            return new_node
                
        elif _node_type == "Blank":
            return [encoding.hex_to_hp(encoding.terminator(key,True)), value]

    def delete_node(self, node, key):
        _node_type = self.node_type(node)
        if _node_type == "Blank":
            return ""

        elif _node_type == "Branch":
            #key empty, find it
            if not key:
                node[-1] = ""
                #print("Node after delete",node)
            else:
                new_node = self.delete_and_delete(self.decode(node[key[0]]), key[1:])
                new_node = self.update_db(new_node)
                if new_node == node[key[0]]:
                    return node
                else:
                    node[key[0]] = new_node
            #after deleting, if the branch node has only one child, change it into extension/leaf node
            count = 0
            not_blank = []
            for idx in range(17):
                if node[idx] != "":
                    count += 1
                    not_blank.append(idx)
            if count > 1:
                return node
            else:
                #return leaf node
                if not_blank[0] == END:
                    return [encoding.hex_to_hp(encoding.terminator([], True)), node[-1]]
                else:
                    child_node = self.decode(node[not_blank[0]])
                    child_node_type = self.node_type(child_node)
                    if child_node_type == "Branch":
                        return [encoding.hex_to_hp(not_blank), self.update_db(child_node)]
                    elif child_node_type == "Leaf" or child_node_type == "Extension":
                        new_key = not_blank + encoding.hp_to_hex(child_node[0])
                        return [encoding.hex_to_hp(new_key), child_node[1]]
                    
        else:
            original_key = encoding.terminator(encoding.hp_to_hex(node[0]),False)
            if _node_type == "Leaf":
                if original_key == key:
                    return ""
                else:
                    return node
            if len(original_key) > len(key) or key[:len(original_key)] != original_key:
                return node
            new_node = self.delete_and_delete(self.decode(node[1]), key[len(original_key):])
            #child is not found
            if new_node == self.decode(node[1]):
                return node
            if new_node == "":
                return ""
            #some nodes have been changed
            else:
                new_node_type = self.node_type(new_node)
                if new_node_type == "Branch":
                    return [encoding.hex_to_hp(original_key), self.update_db(new_node)]
                else:
                    original_key = original_key + encoding.hp_to_hex(new_node[0])
                    return [encoding.hex_to_hp(original_key), new_node[1]]

        
    def update_and_delete(self, node, key, value):
        original_node = node
        new_node = self.update_node(node, key, value)
        #print("New node:",new_node)
        if original_node != new_node:
            self.delete_db(original_node)
        return new_node

    def delete_and_delete(self, node, key):
        original_node = node
        new_node = self.delete_node(node, key)
        if original_node != new_node:
            self.delete_db(original_node)
        return new_node
        
    def get_node_value(self, node, key):
        _node_type = self.node_type(node)
        if _node_type == 'Branch':
            #key="", find
            if not key:
                return node[-1]
            child = node[key[0]]
            return self.get_node_value(self.decode(child), key[1:])
        if _node_type == 'Blank':
            return ""
        #leaf node or extension node
        original_key = encoding.terminator(encoding.hp_to_hex(node[0]), False)

        if _node_type == "Leaf":
            if key == original_key:
                return node[1] 
            else:
                return ""
        
        if _node_type == "Extension":
            #check new_key is in the prefix of key
            if len(original_key) > len(key) or key[:len(original_key)] != original_key:
                return ""
            else:
                return self.get_node_value(self.decode(node[1]), key[len(original_key):])

    def search(self, key):
        value = self.get_node_value(self.root, encoding.raw_to_hex(str(key)))
        return value

    def update(self, key, value):
        if value == "":
            return self.delete_db(key)
        #print("Update", key, value)
        #print("Current root:", self.root)
        self.root = self.update_and_delete(self.root, encoding.raw_to_hex(str(key)), value)
        #print(type(str(self.id).encode()))
        self.db.put(str(self.id).encode(), pickle.dumps(value))
        self.id += 1
        self.db.put(b'currentNum', str(self.id).encode())
        #print("Root after update:", self.root)
        
    def delete(self, key):
        self.root = self.delete_and_delete(self.root, encoding.raw_to_hex(str(key)))
        self.id -= 1
        self.db.put(b'currentNum', str(self.id).encode())
        #print("Root after delete:", self.root)
        self.root_hash()

    def delete_children(self, node):
        _node_type = self.node_type(node)
        if _node_type == "Blank":
            return 
        elif _node_type == "Branch":

            for i in range(END): 
                if node[i] != "":
                    self.delete_children(self.decode(node[i]))
            self.delete_db(node)
        elif _node_type == "Extension":
            self.delete_children(self.decode(node[1]))
            self.delete_db(node)    
        else:
            self.delete_db(node)

    def delete_all(self):
        self.delete_children(self.root)
        self.delete_db(self.root)
        self.root = ""
        self.id = 0
        self.db.put(b'currentNum', str(self.id).encode())

    def _count_key_num(self, node):
        _node_type = self.node_type(node)

        if _node_type == "Blank":
            return 0

        elif _node_type == "Extension":
            return self._count_key_num(self.decode(node[1])) + 1

        elif _node_type == "Leaf":
            return 1

        else:
            count = [self._count_key_num(self.decode(node[i])) for i in range(16)]
            return sum(count)+1

    def count_key_num(self):
        return self._count_key_num(self.root)

    def _iter_subtree(self, node):
        _node_type = self.node_type(node)
        if _node_type == "Blank":
            return {}

        if _node_type == "Branch":
            result = {}
            for i in range(16):
                res = self._iter_subtree(self.decode(node[i]))
                for key, value in res.items():
                    #print("key:",key)
                    original_key = str(i) + "," + key
                    #print("ori:",original_key)
                    result[original_key] = value
                if node[-1]:
                    result["16"] = node[-1]
            return result

        tmp = encoding.terminator(encoding.hp_to_hex(node[0]), False)
        key = ",".join([str(t) for t in tmp])
        if _node_type == "Extension":
            res = self._iter_subtree(self.decode(node[1]))
        if _node_type == "Leaf":
            res = {"16":node[1]}

        result = {}
        for key2, value in res.items():
            print('key:', key, "key2:", key2, "value:", value)
            original_key = key + "," + key2
            result[original_key] = value
        return result

    def search_prefix(self, node, prefix, curr_prefix):
        _node_type = self.node_type(node)
        print("type:", _node_type)
        #check this type
        #print("prefix:",prefix)
        if not prefix:
            return node, curr_prefix
        if _node_type == "Blank":
            return "", curr_prefix

        if _node_type == "Branch":
            if not prefix:
                return node, curr_prefix
            child = node[prefix[0]]
            curr_prefix += [prefix[0]]
            #print(self.decode(child))
            node, curr_prefix = self.search_prefix(self.decode(child), prefix[1:], curr_prefix)
            return node, curr_prefix

        #leaf node or extension node
        key = encoding.terminator(encoding.hp_to_hex(node[0]), False)
        if _node_type == "Leaf":
            #print("prefix:", prefix, "key:", key)
            if len(prefix) < len(key) and prefix == key[:len(prefix)]:
                return node, curr_prefix
            else:
                return "", curr_prefix

        if _node_type == "Extension":
            print("extendsion node:", node, "key:", key, "prefix:", prefix)
            if len(prefix) < len(key) and prefix == key[:len(prefix)]:
                return node, curr_prefix
            elif prefix not in key and len(prefix) < len(key):
                return "", curr_prefix
            elif len(prefix) > len(key) and prefix[:len(key)] != key:
                return "", curr_prefix
            else:
                curr_prefix += key
                node, curr_prefix = self.search_prefix(self.decode(node[1]), prefix[len(key):], curr_prefix)
                return node, curr_prefix

    def iter_subtree(self, prefix):
        #get all key, value start with the same prefix
        node, curr_prefix = self.search_prefix(self.root, encoding.raw_to_hex(prefix), [])
        print("node:", node)
        if node == "":
            return {}
        res = self._iter_subtree(node)
        #encoding_prefix = encoding.raw_to_hex(prefix)
        #print("encoding_prefix:", encoding_prefix)
        print(node)
        result = {}
        for key, value in res.items():
            key = [int(k) for k in key.split(',')]
            total_key = curr_prefix + key
            print("total:",total_key)
            print(encoding.raw_to_hex('h7777'))
            total_key = encoding.hex_to_raw(encoding.terminator(total_key, False))
            result[total_key] = value

        return result



