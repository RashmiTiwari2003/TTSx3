from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
# from pygame import mixer
import os
import time
import threading

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def route():
    return "Hello"

def generate_audio():
    text="What are you doing?"
    tts=gTTS(text,lang='en')
    tts.save('output.mp3')

def delete_file(filename):
    time.sleep(2)
    try:
        os.remove(filename)
        print(f"{filename} has been deleted.")
    except Exception as e:
        print(f"Error deleting file {filename}: {str(e)}")

@app.route('/back', methods=['POST'])
def tts():
    user=[]
    request_data=request.get_json()

    for val in request_data:
        user.append(request_data[val])
        print(request_data[val])

    try:
        generate_audio()

        audio = AudioSegment.from_mp3("output.mp3")

        play(audio)

        # mixer.init()
        # mixer.music.load("output.mp3")
        # mixer.music.play()

        # while mixer.music.get_busy():
        #     continue

        # mixer.music.stop()
        # mixer.quit()

        # if(user[4]):
        threading.Thread(target=delete_file, args=('output.mp3',)).start()
        return send_file('output.mp3', as_attachment=True)
        # else:
        #     return jsonify({"message":"Done"},200)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def cleanup(response):
    try:
        os.remove("output.mp3")
    except Exception as e:
        app.logger.error(f"Error deleting file: {str(e)}")
    return response

if __name__ == '__main__':
    app.run(debug=True)