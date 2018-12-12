
# coding: utf-8

# In[1]:


#import leveldb
import plyvel
import time
# In[ ]:


class DB:
    def get(db, key):
        """
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            print("wait")
            time.sleep(1)
            v = DB.get(name, key)
            return vi
        """
        value = db.get(key)
        if value == None:
            value = ""
        #print("key:",key)
        return value
    
    def put(db, key, value):
        """
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            time.sleep(1)
            DB.put(name, key, value)
            return 0
        """
        db.put(key, value)
            
    def delete(db, key):
        """
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            DB.delete(name, key)
        """
        db.delete(key)

    def deleteAll(db):
        """
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            DB.deleteAll(name)
        """
        for key, value in db:
            db.delete(key)

    def close(db):
        db.close()
        assert db.closed
        
