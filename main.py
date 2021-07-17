from moviepy.tools import verbose_print
from pytube import YouTube
from moviepy.editor import *
import os
import re

banned_chars = ['"', '*', '<', '>', '?', '\\', '|', '/', ':', '#', ',']

def progress_function(stream, chunk, bytes_remaining):
    print('\r', round((1-bytes_remaining/stream.filesize)*100, 3), '% done...', end="")

def mp4_to_mp3(mp4, mp3):
    mp4_wo_frames = AudioFileClip(mp4)
    mp4_wo_frames.write_audiofile(mp3, verbose=False)
    mp4_wo_frames.close()

def DownloadVideo(link, filename, output):
    yt = YouTube(link, on_progress_callback=progress_function)
    if filename == None:
        name = yt.title
    else:
        name = filename
    print(f'Downloading {yt.title}...')
    if len(yt.streams.filter(file_extension='mp4', type='audio')) == 0:
        print("No streams found")
        return
    stream = yt.streams.filter(file_extension='mp4', type='audio')[0]
    path = stream.download(filename=name)  
    print('') 
    for char in banned_chars:
        name = name.replace(char, '')
    if name[-1] == '.' or name[-1] == ' ':
        name = name[:-1]
    mp4_to_mp3(path, path[:-3] + 'mp3')
    os.remove(path)
    os.rename(path[:-3] + 'mp3', output + '\\' + name + '.mp3')
    print("Done.")

def Main():
    with open('outputdir.txt', 'r') as cfg:
        output = cfg.read()
    while True:
        name = None
        user_in = input()
        user_in_split = re.findall("(?:\".*?\"|\S)+", user_in)
        if len(user_in_split) == 0:
            print('Exiting...')
            break
        if user_in_split[0] == 'dl':
            link_index = 1
            if '-n' in user_in_split:
                name = user_in_split[2].replace('"', '')
                link_index += 2
            DownloadVideo(user_in_split[link_index], name, output)
        elif user_in_split[0] == 'exit':
            print("Exiting...")
            break
        elif user_in_split[0] == 'o':
            with open('outputdir.txt', "w") as cfg:
                cfg.write(user_in_split[1].replace('"', ''))
        else:
            print("Correct Usage: dl <link>")

if __name__ == '__main__':
    Main()