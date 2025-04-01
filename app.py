from flask import Flask, render_template, request
# from flask_socketio import SocketIO
import transcrib 
from ai import chat1
from audio import speech


app=Flask(__name__,template_folder='templates')

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def sum():
    if request.method=="POST":
        url= request.form['geturl']
        if "youtube.com/watch?v=" in url:
            video_id=url.split('=')
            video_id= video_id[1]
            print(video_id)
            query= transcrib.get_transcribe(video_id)
            print('<==========Tranc==========>\n\n\n', query)
            summary=chat1(query)
            print('<==========Summary==============>', summary)
            audios=speech(summary)
            
            return render_template('youtSumm.html', video_id=video_id, summary=summary,audio=audios)#,answers=answer)
        
        else:
            print('Enter Valid url')
        
        print(url)
        return render_template('index.html', summary=summary)


if __name__== '__main__':
    app.run(debug=True)