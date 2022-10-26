import time
import os

from threading import Thread

from MovieTool.ombi_handler import ombi_requests
from MovieTool.download_torrents import download
from MovieTool.torrent_handler import torrent_handler

import configparser

# ============================================================
config_file = os.path.abspath('MovieToolConfig.ini')

config = configparser.ConfigParser()
config.read(config_file)

print(config.sections())


# Main parameters.
sleep_time = config['General']['sleep_time'] # Seconds.
file_max_size = config['General']['file_max_size'] # In MB's.
downloads_cache_path = config['General']['downloads_temp_path']
movie_db_path = config['General']['movie_db_definitive']
delete_torrents_die = config['General']['delete_torrents_die']


# Ombi parameters.
ombi_host = config['Ombi']['ombi_host']
ombi_apikey = config['Ombi']['ombi_apikey']


# jackett parameters.
jackett_host = config['Jackett']['jackett_host']
jackett_apikey = config['Jackett']['jackett_apikey']


# qBittorrent parameters.
qb_host = config['qBittorrent']['qb_host']
qb_user = config['qBittorrent']['qb_user']
qb_pass = config['qBittorrent']['qb_password']


# ============================================================



consults = []
while True:
    movies_requests = ombi_requests(ombi_host, ombi_apikey)
    print(movies_requests)
    
    for requests in movies_requests:
        consults = requests[:-1]
        request_data = requests[-1]

        # t = Thread(target lambda= ombi_delete(request_data['showId'], ombi_host, ombi_apikey, request_data['contentType'])).start()
        
        Thread(target = lambda: ombi_delete(request_data['showId'], ombi_host, ombi_apikey, request_data['contentType'])).start()
        
    t_download = ''
    for consult in consults:
        t_download = download(consult, jackett_host, jackett_apikey, qb_host, qb_user, qb_pass, downloads_cache_path, file_max_size, delete_torrents_die = delete_torrents_die)
        
        
        
        if request_data['contentType'] == 'tv':
            se = consult.split(' ')[-1]
            se = se.replace('S', '').split('E')
            
            season = se[0]
            episode = se[1]
        
        
            Thread(target = lambda: torrent_handler(t_download, request_data['title'], movie_db_path, 'tv', qb_host, qb_user, qb_pass, 10, season, episode, content_release = request_data['release'])).start()
            
        else:
            Thread(target = lambda: torrent_handler(t_download, request_data['title'], movie_db_path, 'movie', qb_host, qb_user, qb_pass, 10, content_release = request_data['release'])).start()
            
        
        
        
    consults = []
    
    #Thread(target = lambda: torrent_handler(t_download, )).start()
    
    time.sleep(sleep_time)