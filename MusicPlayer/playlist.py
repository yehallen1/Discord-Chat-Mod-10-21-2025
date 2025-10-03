import random
from collections import deque
class Playlist:
    def __init__(self):
        #Dual ended queues to remove from the front and back quickly
        self.playlist = deque()
        self.playlist_history = deque() 
        self.track_history = deque() #Seperate queue for the names of the tracks
        self.max_track_len = 50 #temp value
        self.looping = False

    def get_len(self):
        return len(self.playlist)
    
    def add(self, track):
        self.playlist.append(track)
    
    def randomize(self):
        random.shuffle(self.playlist)

    def clear_playlist(self):
        self.playlist.clear()
        self.playlist_history.clear()

    def add_name(self, name):
        self.trackname_history.append(name)
        if len(self.trackname_history) > self.max_track_len:
            self.trackname_history.popleft()
    
    def play_next(self):
        if self.get_len() == 0:
            return None
        return None
    
    def play_prev(self):
        if self.get_len() == 0:
            return None
        return None

