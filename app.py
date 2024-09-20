from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import os
import time
import threading

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def route():
    return "Hello"

def generate_audio(user):
    tts=gTTS(user[0],lang=user[1] ,tld=user[2])
    tts.save(user[6])

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
        generate_audio(user)

        threading.Thread(target=delete_file, args=(user[6],)).start()
        return send_file(user[6], as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)