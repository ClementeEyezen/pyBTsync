import subprocess
import os.path

def main():
    #run this
    pass
    

def start(btsync_location, config_storage_path):
    #start up the BitTorrent Client
    fname = os.path.join(config_storage_path,'btsync_config.txt')
    if os.path.isfile(fname):
        # if the config file is there
    else:
        # else create a new config file with the correct settings
        
        
    