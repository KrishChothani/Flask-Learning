
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    ## read the cameraframe
    while 1 :
        success , frame = camera.read()
        if not success :
            break
        else :
            frame = cv2.flip(frame, 1)
            ret , buff= cv2.imencode('.jpg', frame)
            frame = buff.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__' :
    app.run(debug=True , port=2590)
    