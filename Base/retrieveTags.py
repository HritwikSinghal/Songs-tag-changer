import json

from Base import tools
from Base import jioSaavnApi


def getCertainKeys(song_info):
    rel_keys = [
        'title',
        'album',
        'singers',
        'music',

        'year',
        'label',
        'duration',

        'e_songid',
        'image_url',
    ]

    json_data = json.loads(song_info)
    rinfo = {}

    # for k, v in json_data.items():
    #     print(k, ':', v)

    for key in json_data:

        if key in rel_keys:
            if key == 'singers':
                rinfo['artist'] = json_data[key]
            elif key == 'music':
                rinfo['composer'] = json_data[key]
            elif key == 'year':
                rinfo['date'] = json_data[key]
            elif key == 'duration':
                rinfo['length'] = json_data[key]
            elif key == 'label':
                rinfo['organization'] = json_data[key]
            elif key == 'image_url':
                rinfo['image_url'] = tools.fixImageUrl(json_data[key])
            else:
                rinfo[key] = json_data[key]

    return rinfo


def getSong(song_list, song_name):
    for song in song_list:
        data = json.loads(song)
        if data['title'] == song_name:
            return song

    # This Asks user to select Song since no song was matched using title and name
    i = 0
    for song in song_list:
        rel_keys = getCertainKeys(song)
        print(i + 1, end=' ) \n')
        for key in rel_keys:
            print('\t', key, ':', rel_keys[key])
        print()
        i += 1
    song_number = int(input("Enter your song number from above list, "
                            "if none matches, enter 'none': ")) - 1

    return song_list[song_number]


def getTags(tags, song_name):
    baseUrl = "https://www.jiosaavn.com/search/"

    if tools.isTagPresent(tags, 'album') and tools.removeYear(tags['album'][0]) != song_name:
        url = baseUrl + song_name + ' ' + tags['album'][0]
    elif tools.isTagPresent(tags, 'artist'):
        url = baseUrl + song_name + ' ' + tools.removeGibberish(tags['artist'][0])
    else:
        url = baseUrl + song_name

    list_of_songs_with_info = jioSaavnApi.fetchList(url)

    song = str(getSong(list_of_songs_with_info, song_name))
    song_info = getCertainKeys(song)

    return song_info


def start(tags, song_name):
    return getTags(tags, song_name)
