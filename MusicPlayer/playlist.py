import random
    """For now I plan to use this to store the queue of songs"""
from collections import deque
class Playlist:
    def __init__(self):
        #Dual ended queues to remove from the front and back quickly
        self.playlist = deque()
        self.playlist_history = deque()
        self.track_history = deque()
        self.looping = False

    def get_len(self):
        return len(self.playlist)

    def add(self, track):
        self.playlist.append(track)
    
    def randomize(self):
        random.shuffle(self.playlist)
