from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pyttsx3
import os
# from waitress import serve
from multiprocessing import Process

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def route():
    return "Hello"

def generate_audio(user):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Voices")
    for v in voices:
        print(v.id)

    print("End Voices")
    # engine.setProperty('voice', voices[user[4]].id)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', user[5])
    engine.setProperty('volume', user[3])
    engine.say(user[0])
    if(user[1]):
        engine.save_to_file(user[0], user[2])
    engine.runAndWait()
    engine.stop()

# def tts_process(user):
#     p = Process(target=generate_audio, args=(user,))
#     p.start()
#     p.join()

@app.route('/back', methods=['POST'])
def tts():
    user=[]
    request_data=request.get_json()
    # print(request_data)

    for val in request_data:
        user.append(request_data[val])
        print(request_data[val])

    generate_audio(user)
    # tts_process(user)

    if(user[1]):
        return send_file(user[2], as_attachment=True)
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    return jsonify({"message":"Done"},200)

if __name__ == '__main__':
    app.run(port=5000)

# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8080)