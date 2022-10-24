import time
from threading import Thread

from MovieTool.ombi_handler import ombi_requests, ombi_delete
from MovieTool.download_torrents import download
from MovieTool.torrent_handler import torrent_handler

# ============================================================

# Main parameters.
sleep_time = 20 # Seconds.
file_max_size = 3000 # In MB's.
discard_low_content = False
downloads_cache_path = ''
movie_db_path = ''

# Ombi parameters.
ombi_host = ''
ombi_apikey = ''


# jackett parameters.
jackett_host = ''
jackett_apikey = ''


# qBittorrent parameters.
qb_host = ''
qb_user = ''
qb_pass = ''


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
        t_download = download(consult, jackett_host, jackett_apikey, qb_host, qb_user, qb_pass, downloads_cache_path, file_max_size, discard_low_content)
        
        
        
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