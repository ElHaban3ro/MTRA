import time
import os
from datetime import datetime

from threading import Thread

from MovieTool.ombi_handler import ombi_requests, ombi_delete
from MovieTool.download_torrents import download
from MovieTool.torrent_handler import torrent_handler

import configparser

import requests

f = open('logerrors.txt', 'w')



# ============================================================
config_file = os.path.abspath('./MovieToolConfig.ini')

config = configparser.ConfigParser()
config.read(config_file)



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


def download_nofound_torrents(content_type, consult, request_obj):
    status = 'no found'

    while status != 'found':

        print('\n\nIntentando descargar torrent que no se pudo.')


        try:
            t_download = download(consult, jackett_host, jackett_apikey, qb_host, qb_user, qb_pass, downloads_cache_path, int(file_max_size), delete_torrents_die = delete_torrents_die)

            print(f'Lo intentaremos descargar cada 3 horas, si quiere que no se haga de nuevo las peticiones, reinicie el servidor...')


            if t_download[1] == 'found':
                status = 'found'

            else:
                pass


        except KeyError as error:
            f.write(f'[{str(datetime.now())[:-7]}] Jacket Host o API Key erronea.\n\n')
        

        time.sleep(18000)

            
        
    
    if content_type == 'tv':
        se = consult.split(' ')[-1]
        se = se.replace('S', '').split('E')
        
        season = se[0]
        episode = se[1]
    
        Thread(target = lambda: torrent_handler(t_download[0], request_obj['title'], movie_db_path, 'tv', qb_host, qb_user, qb_pass, 10, season, episode, content_release = request_data['release'])).start()

        
    else:
        Thread(target = lambda: torrent_handler(t_download[0], request_obj['title'], movie_db_path, 'movie', qb_host, qb_user, qb_pass, 10, content_release = request_obj['release'])).start()
        
        





consults = []
while True:
    try:
        movies_requests = ombi_requests(ombi_host, ombi_apikey)
        print(f' ------------------ {movies_requests} -----------------------')
        
    
    except requests.exceptions.ConnectionError as error:
        movies_requests = []
        f.write(f'[{str(datetime.now())[:-7]}] {error}\n\n')
        print(f'=================== {error} ============================')


    for requests in movies_requests:
        consults = requests[:-1]
        request_data = requests[-1]

        
        try:
            Thread(target = lambda: ombi_delete(request_data['showId'], ombi_host, ombi_apikey, request_data['contentType'])).start()
        
        except requests.exceptions.ConnectionError as error:
            f.write(f'[{str(datetime.now())[:-7]}] {error}\n\n')
        
    t_download = []


    for consult in consults:
        try:
            t_download = download(consult, jackett_host, jackett_apikey, qb_host, qb_user, qb_pass, downloads_cache_path, int(file_max_size), delete_torrents_die = delete_torrents_die)

            print(t_download)

            if t_download[1] == 'no found':
                Thread(target = lambda: download_nofound_torrents(request_data['contentType'], consult, request_data)).start()


        except KeyError as error:
            f.write(f'[{str(datetime.now())[:-7]}] Jacket Host o API Key erronea.\n\n')
            
        

        
        
        
        if request_data['contentType'] == 'tv':
            se = consult.split(' ')[-1]
            se = se.replace('S', '').split('E')
            
            season = se[0]
            episode = se[1]
        
            Thread(target = lambda: torrent_handler(t_download[0], request_data['title'], movie_db_path, 'tv', qb_host, qb_user, qb_pass, 10, season, episode, content_release = request_data['release'])).start()

            
        else:
            Thread(target = lambda: torrent_handler(t_download[0], request_data['title'], movie_db_path, 'movie', qb_host, qb_user, qb_pass, 10, content_release = request_data['release'])).start()
            
        
    consults = []
    
    time.sleep(int(sleep_time))