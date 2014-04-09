import subprocess
import os.path
import shutil
import json
from io import BytesIO

def main():
    #run this
    pass
    

def start(btsync_location, config_storage_path):
    #start up the BitTorrent Client
    fname = os.path.join(config_storage_path,r"btsync_config.txt")
    if os.path.isfile(fname):
        # if the config file is there
        pass
    else:
        # else copy to the proper place a new config file with the correct settings
        shutil.copyfile(fname,r"example_config.txt")
    
    # now the config file should be in the correct place, so now we can launch the program
    # call the btsync process, with --config flag, pointing to the config file
    subprocess(os.path.join(btsync_location,"btsync"),"--config",os.path.join(config_storage_path,r"btsync_config.txt"))
    
def get_folders(address, port, secret, curl_obj):
    '''
    Returns an array with folders info. If a secret is specified, will return info about the folder with this secret.
    
    [
        {
            "dir": "\\\\?\\D:\\share",
            "secret": "A54HDDMPN4T4BTBT7SPBWXDB7JVYZ2K6D",
            "size": 23762511569,
            "type": "read_write",
            "files": 3206,
            "error": 0,
            "indexing": 0
        }
    ]
    
    http://[address]:[port]/api?method=get_folders[&secret=(secret)]
    
    secret (optional) - if a secret is specified, will return info about the folder with this secret
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_folders[&secret='+secret+']')
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        folder_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        #[ list of...
        '''
        {
            "dir":"\\\\?\\D:\\share",
            "secret": "(secret)",
            "size": "(size)",
            "type": "read_write", //example
            "files": (num_files),
            "error": 0,
            "indexing": 0,
        }
        '''
        # ] 
        
        return folder_info
    
def add_folder(address, port, folder_path, folder_secret, selective_sync, curl_obj):
    '''
    Adds a folder to Sync. If a secret is not specified, it will be generated automatically. The folder will have to pre-exist on the disk and Sync will add it into a list of syncing folders.
    Returns '0' if no errors, error code and error message otherwise.
    
    { "error": 0 }
    
    http://[address]:[port]/api?method=add_folder&dir=(folderPath)[&secret=(secret)&selective_sync=1]
    
    dir (required) - specify path to the sync folder
    secret (optional) - specify folder secret
    selective_sync (optional) - specify sync mode, selective - 1, all files (default) - 0
    '''