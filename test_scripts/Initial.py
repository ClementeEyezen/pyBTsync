import pyBTsync

def main():
    btsync_folder = '/home/buck/Downloads/'
    config_location = '/home/buck/Github/pyBTsync/'
    [address,port] = pyBTsync.start(btsync_folder,config_location)
    print('address '+address)
    print('port    '+port)
    pyBTsync.shutdown()
    
if __name__ == "__main__":
    main()