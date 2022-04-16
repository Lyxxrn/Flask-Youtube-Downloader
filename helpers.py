from pytube import YouTube, Playlist
import os
import shutil

def download_vid(url):

    video = YouTube(url)
    video = video.streams.get_audio_only()
    out = video.download(output_path="music")

    base, ext = os.path.splitext(out)
    new_file = base + '.mp3'
    os.rename(out, new_file)

    # result of success
    print(video.title + " has been successfully downloaded.")

def list_playlist(url):
    p = Playlist(url)
    titles = []
    thumbnails = []
    urls = []
    for video in p.videos:
        vname = video.title
        thumbnail = video.thumbnail_url
        print(vname)
        print(thumbnail)
        titles.append(vname)
        thumbnails.append(thumbnail)
    for url in p.video_urls:
        print(url)
        urls.append(url)
    return titles, thumbnails, urls

def download_playlist(selected_songs):
    for i in range(0, len(selected_songs)):
        download_vid(selected_songs[i])

def clear_temp():
    if os.path.exists("music"):
        shutil.rmtree('music', ignore_errors=True)
    if os.path.exists("music.zip"):
        os.remove("music.zip")



