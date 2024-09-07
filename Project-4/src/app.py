from flask import Flask, render_template, Response, redirect, url_for
import cv2
import face_recognition
import os

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

image_folder = 'D:/VSCODE/CODES/Flask-Learning/Project-4/src/Images'
for person_name in os.listdir(image_folder):
    person_folder = os.path.join(image_folder, person_name)
    if os.path.isdir(person_folder):
        for image_file in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_file)
            if image_file.endswith(('png', 'jpg', 'jpeg')):
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(person_name)


def generate_frames():
    while True:
        try:
            success, frame = video_capture.read()
            if not success:
                break

            rgb_frame = frame[:, :, ::-1]
            
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
              
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw a label with a name below the face
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error during frame processing: {e}")
            continue

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    video_capture.release()  # Only release the camera when explicitly stopping
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
