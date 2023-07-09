from langchain.tools import Tool

from apps.JadeApp import JadeApp

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from apps.ReqFormat.ReqFormat import ReqFormat


class MusicApp(JadeApp):
    def __init__(self, name, hub):
        super().__init__(name, hub)

        self.func_tools = [
            Tool(
                name="play_song",
                func=self.search_and_play,
                description="playing song request by user by a query consisting of the name and potentially additional "
                            "information such as the artist. respond to the user by telling them you're playing the"
                            "song they requested"
            ),
            Tool(
                name="queue_song",
                func=self.search_and_add_to_queue,
                description="queuing song request by user by a query consisting of the name and potentially additional "
                            "information such as the artist. respond to the user by telling them you're playing the"
                            "song they requested"
            )
        ]

        scope = ['streaming', 'user-read-playback-state']
        auth = SpotifyOAuth(scope=scope)
        self.sp = spotipy.Spotify(auth_manager=auth)
        # self.search_and_play("Sun Goes Down")
        print("lolz")

    def start(self):
        super().start()

    def search_and_play(self, query):
        print("searching for and playing song with query " + "'" + query + "'")
        song_uri = self.sp.search(q=query, type='track')['tracks']['items'][0]['uri']
        self.play_song(song_uri)

    def play_song(self, song_uri):
        self.sp.start_playback(uris=[song_uri])

    def search_and_add_to_queue(self, query):
        print("searching for and queuing song with query " + "'" + query + "'")
        song_uri = self.sp.search(q=query, type='track')['tracks']['items'][0]['uri']
        self.add_to_queue(song_uri)

    def add_to_queue(self, song_uri):
        # Sun goes down = 34eF4BoV8FPk0uhAAoqU7h
        self.sp.add_to_queue(song_uri)
