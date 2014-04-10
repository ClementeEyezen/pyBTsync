import subprocess
import os.path
import shutil
import json
from io import BytesIO
import pycurl

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
    address = ''
    port = ''
    return [address, port]
    
def get_folders(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret):
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
        if isinstance(folder_secret,basestring):
            # if there is a folder secret
            c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_folders&secret='+folder_secret)
        else:
            c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_folders')
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        folder_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return folder_info
    
def add_folder(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_path, folder_secret, selective_sync):
    '''
    Adds a folder to Sync. If a secret is not specified, it will be generated automatically. 
    The folder will have to pre-exist on the disk and Sync will add it into a list of syncing folders.
    Returns '0' if no errors, error code and error message otherwise.
    
    http://[address]:[port]/api?method=add_folder&dir=(folderPath)[&secret=(secret)&selective_sync=1]
    
    dir (required) - specify path to the sync folder
    secret (optional) - specify folder secret
    selective_sync (optional) - specify sync mode, selective - 1, all files (default) - 0
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        url = 'http://'+address+':'+port+'/api?method=add_folder&dir='+folder_path
        if isinstance(folder_secret,basestring):
            # if there is a secret, add that info to the url
            url = url+'&secret='+folder_secret
        if isinstance(selective_sync, (int)):
            # if there is a selective_sync option passed as an integer
            url = url+'&selective_sync='+str(selective_sync%2)
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        error_info = json.loads(data.getvalue()) # the json info
        error = error_info["error"]
        #return the json info, format as follows
        return error

def remove_folder(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret):
    '''
    Removes folder from Sync while leaving actual folder and files on disk. 
    It will remove a folder from the Sync list of folders and does not touch any files or folders on disk. 
    Returns '0' if no error, '1' if there’s no folder with specified secret.

    http://[address]:[port]/api?method=remove_folder&secret=(secret)

    secret (required) - specify folder secret
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret ,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=remove_folder&secret='+folder_secret)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        error_info = json.loads(data.getvalue()) # the json info
        error = error_info["error"]
        #return the json info, format as follows
        return error
    
def get_files(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret, sub_path):
    '''
    Returns list of files within the specified directory. 
    If a directory is not specified, will return list of files and folders within the root folder. 
    Note that the Selective Sync function is only available in the API at this time.
    [
        {
            "name": "images",
            "state": "created",
            "type": "folder"
        },
        {
            "have_pieces": 1,
            "name": "index.html",
            "size": 2726,
            "state": "created",
            "total_pieces": 1,
            "type": "file",
            "download": 1 // only for selective sync folders
        }
    ]
    http://[address]:[port]/api?method=get_files&secret=(secret)[&path=(path)]
    secret (required) - must specify folder secret
    path (optional) - specify path to a subfolder of the sync folder.
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring):
        if isinstance(sub_path,basestring):
            # if there is a folder secret
            c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_files&secret='+folder_secret+'&path='+sub_path)
        else:
            c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_files&secret='+folder_secret)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        file_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return file_info
    
def set_file_preferences(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret, sub_path, download):
    '''
    Selects file for download for selective sync folders. 
    Returns file information with applied preferences.

    http://[address]:[port]/api?method=set_file_prefs&secret=(secret)&path=(path)&download=1

    secret (required) - must specify folder secret
    path (required) - specify path to a subfolder of the sync folder.
    download (required) - specify if file should be downloaded (yes - 1, no - 0)
    '''
    c = curl_obj
    data = BytesIO
    if (isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring) 
        and isinstance(folder_secret,basestring) and isinstance(download, (int))):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_files&secret='+folder_secret+
                 '&path='+sub_path+'&download='+str(download%2))
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        file_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return file_info
    
def get_folder_peers(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret):
    '''
    Returns list of peers connected to the specified folder.
    [
        {
            "id": "ARRdk5XANMb7RmQqEDfEZE-k5aI=",
            "connection": "direct", // direct or relay
            "name": "GT-I9500",
            "synced": 0, // timestamp when last sync completed
            "download": 0,
            "upload": 22455367417
        }
    ]
    
    http://[address]:[port]/api?method=get_folder_peers&secret=(secret)
    
    secret (required) - must specify folder secret
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_folder_peers&secret='+folder_secret)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        folder_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return folder_info
    
def get_secrets(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret, type_encrypted="encryption"):
    '''
    Generates read-write, read-only and encryption read-only secrets. 
    If ‘secret’ parameter is specified, will return secrets available for sharing under this secret.
    The Encryption Secret is new functionality. 
    This is a secret for a read-only peer with encrypted content (the peer can sync files but can not see their content). One example use is if a user wanted to backup files to an untrusted, unsecure, or public location. This is set to disabled by default for all users but included in the API.
    
    {
        "read_only": "ECK2S6MDDD7EOKKJZOQNOWDTJBEEUKGME",
        "read_write": "DPFABC4IZX33WBDRXRPPCVYA353WSC3Q6",
        "encryption": "G3PNU7KTYM63VNQZFPP3Q3GAMTPRWDEZ”
    }
    
    http://[address]:[port]/api?method=get_secrets[&secret=(secret)&type=encryption]
    
    secret (required) - must specify folder secret
    type (optional) - if type=encrypted, generate secret with support of encrypted peer
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        url = 'http://'+address+':'+port+'/api?method=get_secrets'
        if isinstance(folder_secret,basestring):
            url = url+'&secret='+folder_secret
        if isinstance(type_encrypted,basestring):
            url = url+'&type='+type_encrypted
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        secrets_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return secrets_info
    
def get_folder_preferences(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret):
    '''
    Returns preferences for the specified sync folder.
    
    {
        "search_lan":1,
        "use_dht":0,
        "use_hosts":0,
        "use_relay_server":1,
        "use_sync_trash":1,
        "use_tracker":1
    }
    
    http://[address]:[port]/api?method=get_folder_prefs&secret(secret)
    
    secret (required) - must specify folder secret
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_folder_prefs&secret='+folder_secret)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        folder_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return folder_info
    
def set_folder_preferences(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret,
                           use_dht=0,use_hosts=0,search_lan=1,use_relay_server=0,use_tracker=0,use_sync_trash=0):
    '''
    Sets preferences for the specified sync folder. Parameters are the same as in ‘Get folder preferences’. Returns current settings.
    
    http://[address]:[port]/api?method=set_folder_prefs&secret=(secret)&param1=value1&param2=value2,...
    
    secret (required) - must specify folder secret
    params - { use_dht, use_hosts, search_lan, use_relay_server, use_tracker, use_sync_trash }
    
    1: DHT - Use DHT (Distributed "Sloppy" Hash Table) to connect to different peers 
        (if ticked, the instance stores details of other clients it’s connected to and 
        shares this with any other clients that connect to it)
        All DHT users store a complete list, and act as pseudo trackers
    2: Hosts - If you don’t want to use the Bittorrent servers to help connect to other clients, 
        you can add either an IP or domain here. For example, for instances outside my network, 
        I could turn off tracker and relay servers and specify a (dynamic) domain name of a 
        Raspberry Pi here for the client to automatically connect to that client.
    3: Search LAN - searches the LAN for instances of BTSync
    4: Relay Server - This uses the bittorrent sync server as an intermediary server 
        to help direct clients to find each other. Disable this if you want no communication 
        with the Bittorrent server for any reason.
    5: Tracker - This option means that the Bittorrent server is used to direct connections 
        to individual instances
    6: Sync Trash - store deleted files
    
    Ignore 3rd parties: set 4,5 to 0 (false)
    Single server networks: set 1 (DHT) to 1 (true), set 2 (Hosts) to the dynamic domain name for the one server
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring):
        url = 'http://'+address+':'+port+'/api?method=set_folder_prefs&secret='+folder_secret
        if isinstance(use_dht,(int)):
            url = url + '&param1='+str(use_dht%2)
        if isinstance(use_hosts,basestring):
            url = url + '&param2='+str(use_hosts)
        if isinstance(search_lan,(int)):
            url = url + '&param3='+str(search_lan%2)
        if isinstance(use_relay_server,(int)):
            url = url + '&param4='+str(use_relay_server%2)
        if isinstance(use_tracker,(int)):
            url = url + '&param5='+str(use_tracker%2)
        if isinstance(use_sync_trash,(int)):
            url = url + '&param6='+str(use_sync_trash%2)
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        folder_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return folder_info
    
def get_folder_hosts(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret):
    '''
    Returns list of predefined hosts for the folder, or error code if a secret is not specified.
    
    {
        "hosts" : ["192.168.1.1:4567",
        "example.com:8975"]
    }
    
    http://[address]:[port]/api?method=get_folder_hosts&secret=(secret)
    
    secret (required) - must specify folder secret
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_folder_hosts&secret='+folder_secret)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        host_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return host_info
    
def set_folder_hosts(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret, host_list, port_list):
    '''
    Sets one or several predefined hosts for the specified sync folder. 
    Existing list of hosts will be replaced. 
    Hosts should be added as values of the ‘host’ parameter and separated by commas. 
    Returns current hosts if set successfully, error code otherwise.
    
    http://[address]:[port]/api?method=set_folder_hosts&secret=(secret)&hosts=host1:port1,host2:port2,...
    
    secret (required) - must specify folder secret
    hosts (required) - enter list of hosts separated by comma. Host should be represented as “[address]:[port]”
    '''
    c = curl_obj
    data = BytesIO
    if (isinstance(address,basestring) and isinstance(port,basestring) and isinstance(folder_secret,basestring) 
        and isinstance(host_list, (list)) and isinstance(port_list,(list)) 
        and len(host_list)==len(port_list) and len(host_list)>=1):
        url = 'http://'+address+':'+port+'/api?method=set_folder_hosts&secret='+folder_secret+'&hosts='
        length = len(host_list)
        for index, host in enumerate(host_list):
            url = url+host+':'+port_list[index]
            if index <= length-1:
                url = url+','
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        host_info = data.getvalue() # the json info
    
        #return the json info, format as follows
        return host_info
    
    
def get_preferences(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), folder_secret, host_list, port_list):
    '''
    Returns BitTorrent Sync preferences. 
    Contains dictionary with advanced preferences. 
    Please see Sync user guide for description of each option.
    {
        "device_name" : "iMac",
        "disk_low_priority": "true",
        "download_limit": 0,
        "folder_rescan_interval": "600",
        "lan_encrypt_data": "true",
        "lan_use_tcp": "false",
        "lang": -1,
        "listening_port": 11589,
        "max_file_size_diff_for_patching": "1000",
        "max_file_size_for_versioning": "1000",
        "rate_limit_local_peers": "false",
        "send_buf_size": "5",
        "sync_max_time_diff": "600",
        "sync_trash_ttl": "30",
        "upload_limit": 0,
        "use_upnp": 0,
        "recv_buf_size": "5"
    }
    
    http://[address]:[port]/api?method=get_prefs
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_prefs')
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
        host_info = data.getvalue() # the json info
        #return the json info, format as follows
        return host_info
    
def set_preferences(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl(), 
                    device_name, download_limit, lang, listening_port, upload_limit, use_upnp):
    '''
    Sets BitTorrent Sync preferences. Parameters are the same as in ‘Get preferences’. 
    Advanced preferences are set as general settings. 
    Returns current settings.
    
    http://[address]:[port]/api?method=set_prefs&param1=value1&param2=value2,...
    
    params - { device_name, download_limit, lang, listening_port, upload_limit, use_upnp } and advanced settings. 
    You can find more information about advanced settings in user guide.
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        url = 'http://'+address+':'+port+'/api?method=set_prefs'
        if isinstance(device_name,basestring):
            url = url + '&param1='+device_name
        if isinstance(download_limit,(int)):
            url = url + '&param2='+str(download_limit)
        if isinstance(lang,basestring):
            url = url + '&param3='+str(lang)
        if isinstance(listening_port,(int)):
            url = url + '&param4='+str(listening_port)
        if isinstance(upload_limit,(int)):
            url = url + '&param5='+str(upload_limit)
        if isinstance(use_upnp,(int)):
            url = url + '&param6='+str(use_upnp%2)
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
        preferences = data.getvalue() # the json info
        #return the json info, format as follows
        return preferences
    
def get_os_name(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl()):
    '''
    Returns OS name where BitTorrent Sync is running.
    
    { "os": "win32" }
    
    http://[address]:[port]/api?method=get_os
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_os')
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
        os_info = data.getvalue() # the json info
        #return the json info, format as follows
        return os_info
    
def get_version(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl()):
    '''
    Returns BitTorrent Sync version.
    
    { "version": "1.2.48" }
    
    http://[address]:[port]/api?method=get_version
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_version')
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
        version_info = data.getvalue() # the json info
        #return the json info, format as follows
        return version_info
    
def get_speed(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl()):
    '''
    Returns current upload and download speed.
    
    {
        "download": 61007,
        "upload": 0
    }
    
    http://[address]:[port]/api?method=get_speed
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        c.setopt(c.URL, 'http://'+address+':'+port+'/api?method=get_speed')
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
        speed_info = data.getvalue() # the json info
        #return the json info, format as follows
        return speed_info
    
def shutdown(address='127.0.0.1', port='8888', curl_obj = pycurl.Curl()):
    '''
    Gracefully stops Sync.
    
    { "error" : 0 }
    
    http://[address]:[port]/api?method=shutdown
    '''
    c = curl_obj
    data = BytesIO
    if isinstance(address,basestring) and isinstance(port,basestring):
        url = 'http://'+address+':'+port+'/api?method=shutdown'
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,data.write)
        c.perform()
    
        error_info = json.loads(data.getvalue()) # the json info
        error = error_info["error"]
        #return the json info, format as follows
        return error
    
    