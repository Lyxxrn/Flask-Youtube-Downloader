import flask
import zipfile
import os
from helpers import list_playlist, download_vid, download_playlist, clear_temp

app = flask.Flask(__name__)

selected_songs = []

@app.route('/', methods=['Get', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')
    else:
        url = flask.request.form.get('url')
        # delete old files if there + errorhandling
        clear_temp()
        if not "http" in url:
            messege = 'Please enter a valid URL.'
            return flask.render_template('index.html', messege=messege)
        if not "youtube.com" in url:
            messege = "Please enter a valid URL from YouTube."
            return flask.render_template('index.html', messege=messege)

        # download playlist
        if "list=" in url:
            print("playlist")
            titles, thumbnails, urls = list_playlist(url)
            print(titles)
            return flask.render_template('playlist.html', titles=titles, thumbnails=thumbnails, urls=urls, len=len(titles))
        # download video
        else:
            print("video")
            download_vid(url)
            return flask.render_template("download.html")

@app.route('/playlist', methods=['Get','POST'])
def playlistdownload():
    if flask.request.method == 'POST':
        global selected_songs
        selected_songs = flask.request.values.getlist("select")
        return flask.render_template('loaddownload.html')
    

@app.route('/loaddownload', methods=['Get','POST'])
def loaddownload():
    print(selected_songs)
    download_playlist(selected_songs)
    return flask.render_template('download.html')
    
@app.route('/download', methods=['Get','POST'])
def download():
    zipf = zipfile.ZipFile('music.zip','w', zipfile.ZIP_DEFLATED)
    for root,dirs, files in os.walk('music/'):
        for file in files:
            zipf.write('music/'+file)
    zipf.close()
    return flask.send_file('music.zip',
            mimetype = 'zip',
            attachment_filename= 'music.zip',
            as_attachment = True)

if __name__ == "__main__":
    app.run(host="0.0.0.0")