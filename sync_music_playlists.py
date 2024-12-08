# Automatically sync favorite music playlist from Rhythmbox (pc) and Vanilla Music (mb, mobile)
# with Syncthing

from os import getenv


# your computer username
username = getenv('USER')
home = '/home/'
music = 'Music/'
# root location of your music library for Rhythmbox (pc)
pc_music_root_directory = home + username + '/' + music
# root location of your music library for Vanilla Music (mb)
mb_music_root_directory = '/storage/3530-3564/' + music
# playlist automatically created by Vanilla Music to keep untouched by pc
mb_playlist_pc_untouched = 'Top 100'
# text file to store the changes in the playlists resulting by the sync, create it before deploy
log = home + username + '/Documents/sync-music-playlists/sync.log'

pc_playlists_root_directory = '/home/' + username + '/.local/share/rhythmbox/'
pc_playlists = 'playlists.xml'
start_playlist = '  <playlist name="'
end_playlist = '  </playlist>\n'
start_playlist_song = '    <location>file://'
end_playlist_song = '</location>\n'
pc_playlists_data = '" show-browser="true" browser-position="180" search-type="search-match" type="static">'
mb_playlists='*.m3u'


def load_pc_playlist(playlist,
                     pc_playlists_root_directory=pc_playlists_root_directory, pc_playlists=pc_playlists,
                     pc_music_root_directory=pc_music_root_directory,
                     start_playlist=start_playlist, end_playlist=end_playlist,
                     start_playlist_song=start_playlist_song, end_playlist_song=end_playlist_song):
    from urllib.parse import unquote

    start_playlist = start_playlist + playlist

    file = open(pc_playlists_root_directory + pc_playlists)
    pc = file.readlines()
    file.close()

    s = 0
    for line in pc:
        if start_playlist in line:
            break
        s = s + 1

    if s == len(pc):
        return False
    else:
        e = s
        for line in pc[s:]:
            if line == end_playlist:
                break
            e = e + 1

        pc = pc[s + 1:e]

        s = start_playlist_song + pc_music_root_directory
        e = end_playlist_song

        for i, l in enumerate(pc):
            pc[i] = unquote(l[l.find(s) + len(s):l.find(e)]).replace('&amp;', '&')

        # if playlist[:4] != 'Top ':
        #     pc.sort()

        return pc


def load_pc_playlists(pc_playlists_root_directory=pc_playlists_root_directory, pc_playlists=pc_playlists,
                      start_playlist=start_playlist):
    file = open(pc_playlists_root_directory + pc_playlists)
    pc = file.readlines()
    file.close()

    playlists = []
    for i, line in enumerate(pc):
        if start_playlist in line:
            line = line[len(start_playlist):]
            if start_playlist not in pc[i + 1]:
                playlists.append(line[:line.find('"')])

    playlists.remove('Play Queue')

    return playlists


def load_mb_playlist(mb_playlist, mb_playlists=mb_playlists,
                     pc_playlists_root_directory=pc_playlists_root_directory, mb_music_root_directory=mb_music_root_directory):
    from os.path import isfile

    extension = mb_playlists[mb_playlists.find('.'):]
    if isfile(pc_playlists_root_directory + mb_playlist + extension):
        file = open(pc_playlists_root_directory + mb_playlist + extension)
        mb = file.readlines()
        file.close()

        for i, l in enumerate(mb):
            mb[i] = l[len(mb_music_root_directory):-1]

        # if mb_playlist[:4] != 'Top ':
        #     mb.sort()

        return mb

    else:
        return False


def update_pc_playlist(playlist, mb,
                       pc_playlists_root_directory=pc_playlists_root_directory, pc_playlists=pc_playlists,
                       pc_music_root_directory=pc_music_root_directory,
                       start_playlist=start_playlist, end_playlist=end_playlist,
                       start_playlist_song=start_playlist_song, end_playlist_song=end_playlist_song):
    from urllib.parse import quote

    file = open(pc_playlists_root_directory + pc_playlists)
    pc = file.readlines()
    file.close()

    start_playlist = start_playlist + playlist

    s = 0
    for line in pc:
        if start_playlist in line:
            break
        s = s + 1

    e = s
    for line in pc[s:]:
        if line == end_playlist:
            break
        e = e + 1

    pcs = pc[:s + 1]
    pce = pc[e:]

    s = start_playlist_song + pc_music_root_directory
    e = end_playlist_song

    with open(pc_playlists_root_directory + pc_playlists, 'w') as file:
        for line in pcs:
            file.write(line)
        for f in mb:
            file.write(s + quote(f, safe="()'/!,&+").replace('&', '&amp;') + e)
        for line in pce:
            file.write(line)
    file.close()


def create_pc_playlist(playlist, mb,
                       pc_playlists_root_directory=pc_playlists_root_directory, pc_playlists=pc_playlists,
                       pc_music_root_directory=pc_music_root_directory,
                       start_playlist=start_playlist, end_playlist=end_playlist,
                       start_playlist_song=start_playlist_song, end_playlist_song=end_playlist_song,
                       pc_playlists_data=pc_playlists_data):
    from urllib.parse import quote

    file = open(pc_playlists_root_directory + pc_playlists)
    pc = file.readlines()
    file.close()

    i = len(pc)
    for line in pc[::-1]:
        if line == end_playlist:
            break
        i = i - 1

    s = start_playlist_song + pc_music_root_directory
    e = end_playlist_song

    with open(pc_playlists_root_directory + pc_playlists, 'w') as file:
        for line in pc[:i]:
            file.write(line)
        file.write(start_playlist + playlist + pc_playlists_data)
        for f in mb:
            file.write(s + quote(f, safe="()'/!,&+").replace('&', '&amp;') + e)
        file.write(end_playlist)
        for line in pc[i:]:
            file.write(line)


def delete_pc_playlist(playlist,
                       pc_playlists_root_directory=pc_playlists_root_directory, pc_playlists=pc_playlists,
                       start_playlist=start_playlist, end_playlist=end_playlist):
    from urllib.parse import quote

    file = open(pc_playlists_root_directory + pc_playlists)
    pc = file.readlines()
    file.close()

    start_playlist = start_playlist + playlist

    s = 0
    for line in pc:
        if start_playlist in line:
            break
        s = s + 1

    e = s
    for line in pc[s:]:
        if line == end_playlist:
            break
        e = e + 1

    with open(pc_playlists_root_directory + pc_playlists, 'w') as file:
        file.writelines(pc[:s] + pc[e + 1:])


def update_mb_playlist(playlist, pc, mb_playlists=mb_playlists,
                       pc_playlists_root_directory=pc_playlists_root_directory,
                       mb_music_root_directory=mb_music_root_directory):
    with open(pc_playlists_root_directory + playlist + mb_playlists[mb_playlists.find('.'):], 'w') as file:
        for line in pc:
            file.write(mb_music_root_directory + line + '\n')


def logging(printout, log=log):
    file = open(log, 'a')
    print(printout)
    file.write(printout + '\n')
    file.close()


def sync(pc_playlists_root_directory=pc_playlists_root_directory,
         pc_playlists=pc_playlists, mb_playlists=mb_playlists,
         mb_playlist_pc_untouched=mb_playlist_pc_untouched):
    from os import listdir, remove
    from time import sleep
    from datetime import datetime
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler

    my_event_handler = PatternMatchingEventHandler(patterns=[pc_playlists, mb_playlists], ignore_directories=True)

    # Update pc
    def on_modified(event):
        playlist = event.src_path[len(pc_playlists_root_directory):]
        if playlist != pc_playlists:
            playlist = playlist[:playlist.find('.')]
            pc = load_pc_playlist(playlist)
            mb = load_mb_playlist(playlist)

            if pc:
                added = list(set(mb) - set(pc))
                deleted = list(set(pc) - set(mb))
                if bool(added) | bool(deleted):
                    update_pc_playlist(playlist, mb)
                    if playlist != mb_playlist_pc_untouched:
                        printout = datetime.now().strftime('%H:%M:%S') + ' pc updated'
                        logging(printout)
                if bool(added) & (playlist != mb_playlist_pc_untouched):
                    printout = 'added in ' + playlist + ':\n' + '\n'.join(added) + '\n'
                    logging(printout)
                if bool(deleted) & (playlist != mb_playlist_pc_untouched):
                    printout = 'deleted in ' + playlist + ':\n' + '\n'.join(deleted) + '\n'
                    logging(printout)

            else:
                create_pc_playlist(playlist, mb)
                printout = datetime.now().strftime('%H:%M:%S') + ' created new playlist in mb: ' + playlist + \
                           '\n' + '\n'.join(mb) + '\n'
                logging(printout)

    def on_created(event):
        playlist = event.src_path[len(pc_playlists_root_directory):]
        if playlist != pc_playlists:
            playlist = playlist[:playlist.find('.')]
            mb = load_mb_playlist(playlist)
            pc = load_pc_playlist(playlist)
            if not bool(pc):
                create_pc_playlist(playlist, mb)
                printout = datetime.now().strftime('%H:%M:%S') + ' created new playlist in mb: ' + playlist + \
                           '\n' + '\n'.join(mb) + '\n'
                logging(printout)

    def on_deleted(event):
        playlist = event.src_path[len(pc_playlists_root_directory):]
        sleep(5)
        if (playlist != pc_playlists) & (playlist[-4:] == mb_playlists[1:]) & \
                (playlist not in listdir(pc_playlists_root_directory)):
            pc = load_pc_playlist(playlist)
            if pc:
                delete_pc_playlist(playlist)
                printout = datetime.now().strftime('%H:%M:%S') + ' deleted playlist in mb: ' + playlist[:-4] + '\n' + \
                           '\n'.join(pc) + '\n'
                logging(printout)

    # Update mb
    def on_moved(event):
        if (event.src_path == pc_playlists_root_directory + pc_playlists + '.tmp') & \
                (event.dest_path == pc_playlists_root_directory + pc_playlists):
            playlists = load_pc_playlists(pc_playlists_root_directory, pc_playlists, start_playlist)
            for playlist in listdir(pc_playlists_root_directory):
                playlist = playlist[:playlist.find('.')]
                if (playlist == mb_playlists[1:]) & (playlist not in playlists) & \
                        (playlist != mb_playlist_pc_untouched):
                    printout = datetime.now().strftime('%H:%M:%S') + ' deleted playlist in pc: ' + playlist[:-4]
                    logging(printout)
                    mb = load_mb_playlist(playlist)
                    if mb:
                        printout = '\n'.join(mb) + '\n'
                    else:
                        printout = ''
                    logging(printout)
                    remove(pc_playlists_root_directory + playlist)
            if mb_playlist_pc_untouched in playlists:
                playlists.remove(mb_playlist_pc_untouched)
            for playlist in playlists:
                pc = load_pc_playlist(playlist)
                mb = load_mb_playlist(playlist)
                if mb:
                    added = list(set(pc) - set(mb))
                    deleted = list(set(mb) - set(pc))
                    if bool(added) | bool(deleted):
                        update_mb_playlist(playlist, pc)
                        printout = datetime.now().strftime('%H:%M:%S') + ' phone updated'
                        logging(printout)
                    if added:
                        printout = 'added in ' + playlist + ':\n' + '\n'.join(added) + '\n'
                        logging(printout)
                    if deleted:
                        printout = 'deleted in ' + playlist + ':\n' + '\n'.join(deleted) + '\n'
                        logging(printout)

                else:
                    update_mb_playlist(playlist, pc)
                    printout = datetime.now().strftime('%H:%M:%S') + ' created new playlist in pc: ' + playlist + \
                               '\n' + '\n'.join(pc) + '\n'
                    logging(printout)

    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted

    my_observer = Observer()
    my_observer.schedule(my_event_handler, path=pc_playlists_root_directory, recursive=False)

    info = datetime.now().strftime('%d %b %H:%M:%S') + ' syncing\n'
    logging(info)

    my_observer.start()
    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

