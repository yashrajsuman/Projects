import cv2
import face_recognition
import cx_Oracle
import numpy as np
from collections import deque, Counter

# Function to fetch all face encodings and names from the database
def fetch_all_face_encodings_and_names():
    connection = cx_Oracle.connect('system', 'yash123', 'localhost/xe')
    cursor = connection.cursor()
    cursor.execute("SELECT face_id, name FROM student WHERE face_id IS NOT NULL")
    
    face_encodings = []
    names = []
    
    for row in cursor:
        face_data = row[0].read()
        if face_data and len(face_data) == 128 * 8:  # Check if data is non-empty and the correct length
            face_encoding = np.frombuffer(face_data, dtype=np.float64).reshape(128)
            face_encodings.append(face_encoding)
            names.append(row[1])
        else:
            print(f"Skipping invalid or empty face encoding for {row[1]}")
    
    cursor.close()
    connection.close()
    return face_encodings, names

# Fetch all face encodings and names from the database
known_face_encodings, known_face_names = fetch_all_face_encodings_and_names()

if not known_face_encodings:
    print("Error: No valid face encodings found in the database.")
else:
    # Initialize the webcam
    video_capture = cv2.VideoCapture(1)

    # A deque to store the recognized names in the last N frames
    N = 10
    recent_names = deque(maxlen=N)

    while True:
        # Capture a single frame of video
        ret, frame = video_capture.read()
        
        if not ret:
            print("Error: Failed to capture image from webcam.")
            break
        
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert the frame from BGR to RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces and encode them
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # Compare each detected face with the known face encodings
        frame_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            frame_names.append(name)
        
        # Add the names detected in the current frame to the deque
        recent_names.extend(frame_names)
        
        # Determine the most common name in the deque
        if recent_names:
            most_common_name = Counter(recent_names).most_common(1)[0][0]
        else:
            most_common_name = "Unknown"

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, frame_names):
            # Scale the face locations back to the original frame size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, most_common_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # Display the frame
        cv2.imshow('Video', frame)
        
        # Press 'q' to quit the video stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    video_capture.release()
    cv2.destroyAllWindows()
