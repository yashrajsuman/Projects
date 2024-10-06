import cv2
import face_recognition
import cx_Oracle
import numpy as np
from collections import deque, Counter
from datetime import datetime

# Function to fetch all face encodings and names from the database
def fetch_all_face_encodings_and_names():
    connection = cx_Oracle.connect('system', 'yash123', 'localhost/xe')
    cursor = connection.cursor()
    cursor.execute("SELECT USN, NAME, FACE_ID FROM student WHERE FACE_ID IS NOT NULL")
    
    face_encodings = []
    usns = []
    names = []
    
    for row in cursor:
        face_data = row[2].read()
        if face_data and len(face_data) == 128 * 8:  # Check if data is non-empty and the correct length
            face_encoding = np.frombuffer(face_data, dtype=np.float64).reshape(128)
            face_encodings.append(face_encoding)
            usns.append(row[0])
            names.append(row[1])
        else:
            print(f"Skipping invalid or empty face encoding for {row[1]}")
    
    cursor.close()
    connection.close()
    return usns, names, face_encodings

# Function to mark attendance in the database
def mark_attendance(usn, subject):
    connection = cx_Oracle.connect('system', 'yash123', 'localhost/xe')
    cursor = connection.cursor()
    
    # Check if attendance for today already exists
    today = datetime.today().date()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE USN = :usn AND ATTENDANCE_DATE = :today", {'usn': usn, 'today': today})
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert a new attendance record for today
        cursor.execute("INSERT INTO attendance (USN, ATTENDANCE_DATE) VALUES (:usn, :today)", {'usn': usn, 'today': today})
    
    # Update the attendance for the specific subject
    cursor.execute(f"UPDATE attendance SET {subject} = 'P' WHERE USN = :usn AND ATTENDANCE_DATE = :today", {'usn': usn, 'today': today})
    
    connection.commit()
    cursor.close()
    connection.close()

# Determine the current subject based on the time
def get_current_subject():
    now = datetime.now().time()
    if now >= datetime.strptime("08:30:00", "%H:%M:%S").time() and now < datetime.strptime("09:30:00", "%H:%M:%S").time():
        return "MATH"
    elif now >= datetime.strptime("17:30:00", "%H:%M:%S").time() and now < datetime.strptime("18:30:00", "%H:%M:%S").time():
        return "DBMS"
    elif now >= datetime.strptime("10:45:00", "%H:%M:%S").time() and now < datetime.strptime("11:45:00", "%H:%M:%S").time():
        return "DAA"
    elif now >= datetime.strptime("11:45:00", "%H:%M:%S").time() and now < datetime.strptime("12:45:00", "%H:%M:%S").time():
        return "JAVA"
    elif now >= datetime.strptime("13:30:00", "%H:%M:%S").time() and now < datetime.strptime("14:30:00", "%H:%M:%S").time():
        return "BIO"
    else:
        return None

# Fetch all face encodings and names from the database
known_usns, known_face_names, known_face_encodings = fetch_all_face_encodings_and_names()

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
        frame_usns = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            usn = None

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                usn = known_usns[best_match_index]

            frame_names.append(name)
            frame_usns.append(usn)
        
        # Add the names detected in the current frame to the deque
        recent_names.extend(frame_names)
        
        # Determine the most common name in the deque
        if recent_names:
            most_common_name = Counter(recent_names).most_common(1)[0][0]
        else:
            most_common_name = "Unknown"

        # Get the current subject
        current_subject = get_current_subject()

        # List to keep track of names for which attendance is marked
        attendance_marked_names = []

        # Mark attendance if a known face is recognized and within class time
        if current_subject:
            for usn, name in zip(frame_usns, frame_names):
                if usn:
                    mark_attendance(usn, current_subject)
                    attendance_marked_names.append(name)

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
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # Display the names for which attendance was marked
        for idx, name in enumerate(attendance_marked_names):
            cv2.putText(frame, f"Attendance marked for: {name}", (10, 30 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Display the frame
        cv2.imshow('Video', frame)
        
        # Press 'q' to quit the video stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    video_capture.release()
    cv2.destroyAllWindows()
