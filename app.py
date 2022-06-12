import pafy


def roundoff(x):
    if x> 1073741824:
        y = round(x/1073741824, 1)
        return str(y) + 'GB'
    elif x > 1048576:
        y = round(x/1048576, 1)
        return str(y) + "MB"
    elif x > 1024:
        y = round(x/1024, 1)
        return str(y) + "KB"



def get_audio(url):
    video = pafy.new(url)
    title = video.allstreams
    title = title[1]
    title = title.title
    audiostreams = video.audiostreams
    bitrates =[]
    extensions =[]
    file_sizes =[]
    AS = []
    for i in audiostreams:
        bitrates.append(i.bitrate)
        extensions.append(i.extension)
        file_sizes.append(roundoff(i.get_filesize()))

    return bitrates, extensions, file_sizes, title, audiostreams


def get_idx(itag):
    url = session['link']
    audio = get_audio(url)[1]
    for index, size in enumerate(audio):
        if size == itag:
            return index


def modified_name(name):
    paths = name.split('\\')
    del paths[-2]
    path = '\\'.join(paths)
    return path



from flask import Flask, render_template, request, url_for, session

# This is my home page
app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"

@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == 'POST':
        session['link'] = request.form.get("url")
        try:
            audio = get_audio(session['link'])
        except:
            return render_template('error.html')
        return render_template('download_page.html',audio = audio)

    return render_template('index.html')

#this page will give you the download options



from flask import redirect, send_file
from io import BytesIO

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        url = session['link']
        aud = get_audio(url)[4]
        itag = request.form.get("itag")
        itag = get_idx(itag)
        file = aud[itag]
        #ext = get_audio(url)[1][itag]
        name = file.filename
        file = file.download()
        return send_file(modified_name, as_attachment=True,download_name = name , mimetype = 'audio/mp3')
    return redirect(url_for("home"))





if __name__ == '__main__':
    app.run(debug = True)





