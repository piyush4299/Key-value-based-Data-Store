import json
import os
import sys
import threading
import time
from collections import OrderedDict

from filelock import FileLock

import utils.Constants as const
from Key_value_datastore.datastore_library import DataStore
from utils.Common_util_functions import utils

if __name__ == '__main__':
    # initialize an object of utils class 
    utility = utils()

    '''
        Below section is for taking the folder_path from user and if it's not mentioned by user then setting the default
        storage path and using it for further purpose.
    '''
    file_detail = ''
    try:
        try:
            print('Enter the folder path: ')
            folder_path = input()
            filename = utility.get_file_name()
            print(filename)
            if len(folder_path) == 0:
                raise ValueError
        except ValueError as value_error:
            # This is the section which will be executed if user doesn't mention the folder_path of file.
            print("Since file path is not provided considering default path from us")
            
            folder_path = const.DEFAULT_STORAGE_PATH
            utility.initialize_data_storage(folder_path,filename)
            file_detail = folder_path + "/" + filename
            
            if not utility.is_filesize_limited(file_detail): #This is for checking if file we considered is in limit as per condition
                raise Exception("File Limit to 1 GB is not satisfied")
        else:
            # This is the section which will be executed if user mention the folder_path of file.
            utility.initialize_data_storage(folder_path,filename)
            file_detail = folder_path + "/" + filename

            if not utility.is_filesize_limited(file_detail):
                raise Exception("File Limit to 1 GB is not satisfied")
    
    except Exception as e:
        print("Something went wrong ",e)
    

    # Input is taken in below format by passing the key value in given two lists.
    input_key = ["sample_key0","sample_key1","smaple_key2"]
    input_values = [{'name':'Ram','age':'22'},{'name':'Piyush','age':'21'},{'name':'victor','age':'23'}] 
    
    obj_store = DataStore(file_detail)
    
    key_ptr,value_ptr = 0,0 
    while key_ptr < len(input_key) and value_ptr < len(input_values):
        key = input_key[key_ptr]
        value = input_values[value_ptr]    
        # TTL input is optional
        print("Enter time to leave for given key:")
        try:
            ttl = input()
            if len(ttl) == 0:
                ttl = "-1"
                raise ValueError
        except ValueError as value_error:
            print("TTL is not provided for this key")
        finally:
            try: 
                status = utility.is_valid_data(key,value,ttl)
            except ValueError as value_error:
                print("Something went wrong with input provided ",value_error)
            else:
                if status:
                    # This methods could be called using multiple threads thus increasing the performance of code.
                    # any operation we need to perform we need to pass it through here.
                    obj_store.create(key,value,ttl) 
                    # If want to see the effect of TTL values then uncomment sleep and adjust duration and insert one more key. 
                    #time.sleep(4)
                    obj_store.read(key)
            key_ptr += 1
            value_ptr += 1
        
        obj_store.delete(input_key[1])


