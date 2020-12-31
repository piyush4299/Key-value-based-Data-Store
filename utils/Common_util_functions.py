import os
import sys
import time
import uuid

import utils.Constants as const


class utils:
    # This function is for checking if key is present in data_store.
    def is_key_present(self,key,store):
        for item,value in store.items():
            if key == item:
                return True
        return False
    
    '''
    This function checks if key value are valid or not. If the rules doesn't follow for the given key value pairs then
    it will raise an eception.
    '''
    def is_valid_data(self,key,value,ttl):
        if not isinstance(key, str):
            raise ValueError(f"Key [{key}] must be string type.")
        else:
            if len(key) <= const.MAX_KEY_LEN:
                if not isinstance(value,dict):
                    raise ValueError(f"Value [{value}] must be dictionary(JSON) type.")
                else:
                    if sys.getsizeof(value) <= const.MAX_VALUE_SIZE:
                        # If user enters negative values other than "-1" for ttl it will automatically set it to "-1"
                        if ttl.isdigit() and int(ttl) < 0:
                            ttl = str(-1)

                        return True
        return False
    
    # This function helps in checking the entire data_storage file size.
    def is_filesize_limited(self,file_detail):
        return os.stat(file_detail).st_size <= const.MAX_FILE_SIZE

    # This function is helpful in initializing the datastorage with folder_path mentioned by user or not.
    def initialize_data_storage(self,folder_path,filename):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path,filename), 'w'):
            pass
    
    # This function generated the filename with name and time-stamp.
    def get_file_name(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return "data_storage_" + timestr + ".json"
    