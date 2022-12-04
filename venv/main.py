
import csv
import random

songs = list()
playlists = list()


#=====================================User Class============================================#
class User():
    def __init__(self, name = "Bot"):
        self.name = name
        self.listened_songs = random.sample(songs, random.choice(range(5,10)))
        self.week1 = []
        self.week2 = []
        self.week3 = []

    def change_playlist(self, playlist, week):
        if week == 1:
            self.week1 = playlist
        elif week == 2:
            self.week2 = playlist
        elif week == 3:
            self.week3 = playlist
        self.listened_songs += playlist

    def get_song_names(self, playlist):
        song_names = list()
        for i in playlist:
            song_names.append(i["title"])
        return song_names

    def get_all_song_names(self):
        song_names = list()
        for i in self.listened_songs:
            song_names.append(i["title"])
        return song_names

class Users():
    def __init__(self):
        self.users = list()
        for i in range(100):
            self.users.append(user())

#=====================================PlayList Classes & Functions============================================#
class Playlist():
    def __init__(self):
        self.playlist = list()
        while len(self.playlist) <= 50:
            song = random.choice(songs)
            if song not in self.playlist:
                self.playlist.append(song)

def create_playlists():
    for i in range(100):
        playlists.append(Playlist())

#=====================================Discover Weekly Function Week 1============================================#
def discover_week_1(user):
    '''
    Goes through every playlist in the set of 100 playlist that were created previously.
    Goes through every song from that playlist and checks if it has been listened to by the user.
    If it has been listened to it increments the listened variable.
    At last if there has atleast been 3 songs in the playlist that has songs the user have listened to then
    return a list of 5 random songs from that list.

    :param user:
    :return: A List with 5 songs
    '''
    for playlist in playlists:
        listened = 0
        for song in playlist.playlist:
            if song in user.listened_songs:
                listened += 1
        if listened >= 3:
            return random.sample(playlist.playlist, 5), None
    print("NOTFOUND TRYING AGAIN")
    playlist = []
    create_playlists()
    return discover_week_1(user)

#=====================================Discover Weekly Function Week 2============================================#
def discover_week_2(user):
    '''
    Goes through the users listened songs and counts the genres of the songs he listened to.
    Then collects the songs from the song list with the most listened genre
    Reutrns a list of 5 random songs from the collected list

    :param user:
    :return:
    '''
    genres = dict()
    genre_list = list()

    #Collect users most listened genres
    for song in user.listened_songs:
        if song['the genre of the track'] in genres:
            genres[song['the genre of the track']] += 1
        else:
            genres[song['the genre of the track']] = 1

    #Collects songs that have the users favorite genre
    for song in songs:
        if song['the genre of the track'] == max(genres, key=genres.get):
            genre_list.append(song)

    return random.sample(genre_list, 5),max(genres, key=genres.get)

#=====================================Discover Weekly Function Week 3============================================#
def mood_calculator(song,moods):
    '''
    Calculates the mood based on attributes of the song

    :param song: A Dictionry that containts attributes of  the song
    :param moods: The Keys for the columns that contain the attributes of the song
    :return: Mood of the song
    '''
    mood = None
    # If BPM > 199
    if int(song[moods[0]]) > 119:
        # If Loudness is > -6
        if int(song[moods[3]]) > -6:
            mood = "party"
        else:
            mood = "happy"
    else:
        # If Valence is > 52
        if int(song[moods[4]]) > 52:
            mood = "lounge"
        else:
            mood = "calming"
    return mood

def discover_week_3(user):
    '''
    Collects the keys of song attributes.
    Then goes through every song in the users listened songs and checks its mood and records it in the mood_stats.
    Then we collect the songs that have similar mood traits and stoe them in a list
    From the collected list we randomly pick 5 songs and return it.
    :param user:
    :return:
    '''
    moods = list()
    mood_stats = {
        "happy": 0,
        "calming": 0,
        "party": 0,
        "lounge": 0
    }
    mood_list = list()

    # Collect keys of song attributes
    for i in range(4, 10):
        moods.append(list(user.listened_songs[0].keys())[i])

    for song in user.listened_songs:
        mood_stats[mood_calculator(song, moods)] += 1

    for song in songs:
        if mood_calculator(song,moods) == max(mood_stats, key=mood_stats.get):
            mood_list.append(song)

    return random.sample(mood_list, 5), max(mood_stats, key=mood_stats.get)

#=====================================CSV to List of Dictionaries============================================#
def convert_csv(path):
    with open(path, encoding='utf-8') as file:
        file = csv.DictReader(file)
        for row in file:
            songs.append(row)

#=====================================Main Functions============================================#

def start():
    '''
    Runs the main app with its menu.
    We are first presented with 3 options to either Discover new songs, look at pervious songs or quit
    Once the 4th week has been reached no more songs are available and the program exits autmoatically

    :return: None
    '''

    user = User(input("Set Your Name:"))
    week = 1
    while week <= 4:
        # Discover Weekly
        if menu_choice == 1:
            if week == 1:
                discover_playlist = discover_week_1(user)
            elif week == 2:
                discover_playlist = discover_week_2(user)
                print(f"You've recently been listening alot of {discover_playlist[1]}!")
            elif week == 3:
                discover_playlist = discover_week_3(user)
                print(f"You're {discover_playlist[1]} energy have been showing recently!")
            elif week == 4:
                print("Its the 4th week! We ran out of songs :(( Goodbye!!")
                break

            print("This week's songs are:")
            for i, n in enumerate(discover_playlist[0]):
                print(i + 1, n['title'])

            user.change_playlist(discover_playlist[0], week)
            print("----------------------------------------------------")
            input("Enter anything to exit and proceed to the next week")
            week += 1

        # Playlist Check
        elif menu_choice == 2:
            print("----------------------------------------------------")
            print("Choose A Playlist")
            playlist_choice = int(input(f"[1] Listened Songs ({len(user.listened_songs)}) \n"
                                        f"[2] Discover Week 1 ({len(user.week1)}) \n"
                                        f"[3] Discover Week 2 ({len(user.week2)})\n"
                                        f"[4] Discover Week 3 ({len(user.week3)}) "))
            print("----------------------------------------------------")
            if playlist_choice == 1:
                for i, n in enumerate(user.get_song_names(user.listened_songs)):
                    print(i + 1, n)
            elif playlist_choice == 2:
                for i, n in enumerate(user.get_song_names(user.week1)):
                    print(i + 1, n)
            elif playlist_choice == 3:
                for i, n in enumerate(user.get_song_names(user.week2)):
                    print(i + 1, n)
            elif playlist_choice == 4:
                for i, n in enumerate(user.get_song_names(user.week3)):
                    print(i + 1, n)
            print("----------------------------------------------------")
            input("Enter anything to return to menu")

convert_csv("spotify-dataset.csv")
create_playlists()