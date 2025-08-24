import cv2
import face_recognition
import serial
import time
import os

# Connect to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

# Load known faces
known_faces = []
known_names = []

for file in os.listdir("faces"):
    img = face_recognition.load_image_file(f"faces/{file}")
    encoding = face_recognition.face_encodings(img)[0]
    known_faces.append(encoding)
    known_names.append(file.split(".")[0])

# Start camera
cap = cv2.VideoCapture(0)

print("System ready...")

while True:
    if arduino.in_waiting > 0:
        msg = arduino.readline().decode().strip()
        if msg == "P":  # presence detected
            ret, frame = cap.read()
            rgb_frame = frame[:, :, ::-1]
            faces = face_recognition.face_encodings(rgb_frame)

            for face in faces:
                matches = face_recognition.compare_faces(known_faces, face)
                if True in matches:
                    name = known_names[matches.index(True)]
                    print(f"Authorized: {name}")
                    arduino.write(b'O')  # send open signal
                    time.sleep(5)
                    break
            else:
                print("Unknown face detected.")