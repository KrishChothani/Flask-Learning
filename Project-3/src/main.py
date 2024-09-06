import face_recognition
import cv2
import numpy as np
from flask import Flask, render_template, Response 

app = Flask(__name__)
camera = cv2.VideoCapture(0)

Krish_Image = face_recognition.load_image_file('Images/Krish/Krish.jpg')
krish_face_encoding = face_recognition.face_encodings(Krish_Image)[0]

Akshit_Image = face_recognition.load_image_file('Images/Akshit/Akshit.jpg')
Akshit_face_encoding = face_recognition.face_encodings(Akshit_Image)[0]

known_face_encodings = [
    krish_face_encoding,
    Akshit_face_encoding   
]
known_face_names = [
    "Krish",
    "Akshit"
]

process_this_frame = True

def generate_frames():
    global process_this_frame

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                
                face_names.append(name)
        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2590)

camera.release()
cv2.destroyAllWindows()
