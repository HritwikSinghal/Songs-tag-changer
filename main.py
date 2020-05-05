import os
import re
import traceback
from mutagen.easyid3 import EasyID3 as easyid3

import tools
import albumName
import artistName
import composerName
import songName
import songTitle
import retrieveTags


def inputSongDir():
    # songDir = input("Enter song dir:  ")
    songDir = r'C:\Users\hritwik\Pictures\Camera Roll'

    print("Song dir is: ", songDir)
    return songDir


def getFullPathOfSongsInDir(songDir):
    files_in_dir = tools.os.listdir(songDir)

    full_path_of_songs = []
    for song_name in files_in_dir:
        song_name = tools.re.findall(r'(.+\.mp3)', song_name)
        if len(song_name) != 0:
            name = tools.os.path.join(songDir, song_name[0])
            full_path_of_songs.append(name)
    return full_path_of_songs


def changeSongName(songDir, full_path_of_songs):
    for songNameWithPath in full_path_of_songs:
        songName.start(songDir, full_path_of_songs, songNameWithPath)
    print()


def changeSongTags(full_path_of_songs):
    for songNameWithPath in full_path_of_songs:
        tags = easyid3(songNameWithPath)

        song_name = tools.getSongNameWithoutPath(songNameWithPath)
        song_name = song_name.replace('.mp3', '')

        print("Song Name: ", song_name)

        artistName.start(tags, song_name)
        # albumName.start(tags, song_name)
        # composerName.start(tags, song_name)
        # songTitle.start(tags, song_name)

        # retrieveTags.start(tags, song_name)
        # break

        print()


def handleSongs(songDir):
    full_path_of_songs = getFullPathOfSongsInDir(songDir)
    print('Now in ', songDir)

    # changeSongName(songDir, full_path_of_songs)
    changeSongTags(full_path_of_songs)


def start():
    # taking songs directory
    all_song_dir = inputSongDir()

    # walk_down_curr_dir = input("\nDo you want walk down?\n1 == Yes, 0 == No\n") == '1'
    walk_down_curr_dir = False
    if walk_down_curr_dir:
        print("Walking down ", all_song_dir, "...")
        for dirPath, subDirName, fileNames in (tools.os.walk(all_song_dir, topdown=True)):
            curr_songs_dir = dirPath
            handleSongs(curr_songs_dir)
    else:
        print("Only changing attributes in: ", all_song_dir, "...\n")
        handleSongs(all_song_dir)
