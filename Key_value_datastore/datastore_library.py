import json
import threading
import time
from collections import OrderedDict

from utils.Common_util_functions import utils

'''
    DataStore is the class supporting 4 functions create(),read(),delete() and delete_ttl_elapsed_keys(). The required private valriables are initialized with constructor.
'''
class DataStore:
    def __init__(self,fileDetail):
        self.__utility = utils()
        self.__fileDetail = fileDetail
        self.__store = OrderedDict()
        self.__time_bound = OrderedDict()
        self.__lock = threading.Lock()
        '''
        time_bound => {"createdAt": " ", "time_to_leave": " " } This is the structure of hashmap(Ordereddict) for maintaining the record
        for keys and their TTL duration.

        lock => It is used for maintaining a synchronization between threads

        store => {"key" : "value" } This is the structure for hashmap(Ordereddict) for maintaining the key value pairs required and 
        updating in data_storage file.

        utility => It is the object required for calling the utility(helper) functions required.

        fileDetail => It is the complete filepath for called instance.

        '''
        
    def create(self,key,data,ttl):
        '''
            To make the function thread safe locking method is used with which unless one thread completes the task 
            of creating(inserting data) into data_storage no other thread interrupts.

            The added feature is deleting TTL(Time To Leave) elapsed keys at the start of create() function so that
            the goal of memory optimization with time would be achieved.  
        '''
        with self.__lock:
            # Deleting TTL elapsed keys
            self.delete_ttl_elapsed_keys()
            try:
                if self.__utility.is_key_present(key,self.__store): # If key is already present then exception is thrown
                    raise Exception("The key you wish to insert is already present in DataStore")
                else:
                    self.__time_bound[key] = {"createdAt":time.time(),"time_to_leave":ttl}

                    # Inserting the data into store
                    self.__store[key] = data
                    
                    # After every insert/create operation check if file limit is above 1GB or not and if it is above 
                    # then delete entries in data_store till file's size is not under 1 GB.
                    while not self.__utility.is_filesize_limited(self.__fileDetail):
                        self.__store.popitem(last=False)
                        print("here")
                        write_desc = open(self.__fileDetail,'w')
                        json.dump(self.__store,write_desc)
                        write_desc.close()
                        
                    # Since store is OrderedDict it would have sorted the keys in their insertion sequence so it has 
                    # less probability that the item inserted recent is being deleted.

                    try:
                        write_desc = open(self.__fileDetail,'w')
                        # Dumping the data into data_storage file
                        json.dump(self.__store,write_desc)
                    except FileNotFoundError:
                        raise Exception("File not found to write while insertion or creating the data")
                    else:
                        write_desc.close()
            except Exception as e:
                print("Something went wrong ",e)

    def read(self,key):
        '''
        Here lock is provided only for deleting TTL elapsed keys not for entire read function since multiple threads 
        can read data without making any inconsistency in Data Store. 
        ''' 
        with self.__lock:
            # Deleting TTL elapsed keys
            self.delete_ttl_elapsed_keys()

        try:
            if len(self.__store) == 0:
                raise Exception("The data store is already empty Can't read anything ")
            else:
                if not self.__utility.is_key_present(key,self.__store):
                    raise KeyError
                
                # Read operation is successful and displaying it on console.
                print("The data asked for given key : " + str(key) + " => ",end = "")
                print(self.__store[key])
        
        except KeyError as keyerror:
            print("The key you are wishing to read is not present ",keyerror)
        except Exception as e:
            print("Something went wrong ",e)

    def delete(self,key):
        '''
        The Delete operation requires locking mechanism since it could rise the problems of inconsistency in case of 
        multiple threads.
        '''
        with self.__lock:
            self.delete_ttl_elapsed_keys()

            try:
                if len(self.__store) == 0:
                    raise Exception("The data store is already empty Can't delete further")
                else:
                    if not self.__utility.is_key_present(key,self.__store):
                        raise KeyError(self.__store[key])
                    
                    # Deleting the key from store
                    self.__store.pop(key)
            
                    try:
                        write_desc = open(self.__fileDetail,'w')
                        # Dumping the update store into data_storage file
                        json.dump(self.__store,write_desc)
                    except FileNotFoundError:
                        raise Exception("File not found to write while updating the deleted key")
                    else:
                        write_desc.close()
            except KeyError as keyerror:
                print("The key you are wishing to delete is not present ",keyerror)
            except Exception as e:
                print("Something went wrong ",e)

    def delete_ttl_elapsed_keys(self):
        keys_to_delete = []
        # Default value of TTL is considered to be "-1" if user don't provide TTL. 
        for key in self.__time_bound:
            if self.__time_bound[key]["time_to_leave"] != "-1": # Skipping deletion process if TTL is "-1"
                if abs(self.__time_bound[key]["createdAt"] - time.time()) >= float(self.__time_bound[key]["time_to_leave"]):
                    keys_to_delete.append(key)
        
        # All keys which are required to be deleted accumulated in keys_to_delete array.

        for key in keys_to_delete:
            self.__time_bound.pop(key)
            self.__store.pop(key)
            print("Key: ",key," is deleted from store since time is elapsed")        
        
        try:
            write_desc = open(self.__fileDetail,'w')
            # Dumping the updated store into data_storage file.
            json.dump(self.__store,write_desc)
        except FileNotFoundError:
            print("File not found to write while updating the deleted key")
        else:
            write_desc.close()

        




