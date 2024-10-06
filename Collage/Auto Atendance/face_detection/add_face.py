import cv2
import face_recognition
import cx_Oracle
import numpy as np
import os
from datetime import datetime

def get_db_connection():
    return cx_Oracle.connect('system/yash123@localhost:1521/xe')

def close_db_connection(conn, cursor):
    cursor.close()
    conn.close()

def display_student_details(usn, cursor):
    cursor.execute("SELECT * FROM student WHERE USN = :usn", {'usn': usn})
    student = cursor.fetchone()
    
    if student:
        print(f"\nUSN: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Department: {student[2]}")
        print(f"Semester: {student[3]}")
        print(f"Date of Birth: {student[4]}")
        if student[6]:
            print("Face ID: Exists")
        else:
            print("Face ID: Not Available")
    else:
        print("Student not found.")

def add_student(usn, conn, cursor):
    name = input("Enter student name: ").strip()
    dept = input("Enter department: ").strip()
    sem = input("Enter semester: ").strip()
    dob = input("Enter date of birth (YYYY-MM-DD): ").strip()
    
    try:
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")
        return
    
    cursor.execute("INSERT INTO student (USN, NAME, DEPT, SEM, DOB) VALUES (:usn, :name, :dept, :sem, :dob)",
                   {'usn': usn, 'name': name, 'dept': dept, 'sem': sem, 'dob': dob_date})
    conn.commit()
    print("Student added successfully.")

def edit_student(usn, conn, cursor):
    display_student_details(usn, cursor)
    
    name = input("Enter new name (leave blank to keep current): ").strip()
    dept = input("Enter new department (leave blank to keep current): ").strip()
    sem = input("Enter new semester (leave blank to keep current): ").strip()
    dob = input("Enter new date of birth (YYYY-MM-DD, leave blank to keep current): ").strip()
    
    if name:
        cursor.execute("UPDATE student SET NAME = :name WHERE USN = :usn", {'name': name, 'usn': usn})
    if dept:
        cursor.execute("UPDATE student SET DEPT = :dept WHERE USN = :usn", {'dept': dept, 'usn': usn})
    if sem:
        cursor.execute("UPDATE student SET SEM = :sem WHERE USN = :usn", {'sem': sem, 'usn': usn})
    if dob:
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            cursor.execute("UPDATE student SET DOB = :dob WHERE USN = :usn", {'dob': dob_date, 'usn': usn})
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
    
    conn.commit()
    print("Student details updated successfully.")

def delete_related_records(usn, conn, cursor):
    # Replace 'child_table1' and 'child_table2' with your actual child table names
    cursor.execute("DELETE FROM child_table1 WHERE USN = :usn", {'usn': usn})
    cursor.execute("DELETE FROM child_table2 WHERE USN = :usn", {'usn': usn})
    conn.commit()

def delete_student(usn, conn, cursor):
    display_student_details(usn, cursor)
    confirm = input("Are you sure you want to delete this student and all related records? (yes/no): ").strip().lower()
    if confirm == 'yes':
        delete_related_records(usn, conn, cursor)
        cursor.execute("DELETE FROM student WHERE USN = :usn", {'usn': usn})
        conn.commit()
        print("Student and related records deleted successfully.")
    else:
        print("Deletion canceled.")

def add_face_from_path(usn, image_path, conn, cursor):
    if not os.path.isfile(image_path):
        print(f"Error: File '{image_path}' does not exist. Please check the file path and try again.")
        return
    
    # Load image
    image = cv2.imread(image_path)
    
    # Convert image from BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect face in the image
    face_locations = face_recognition.face_locations(rgb_image)
    
    if len(face_locations) == 1:
        # Encode the face
        face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        
        # Convert face encoding to binary format
        face_encoding_binary = face_encoding.tobytes()
        
        # Update database with face encoding
        cursor.execute("UPDATE student SET face_id = :face_id WHERE USN = :usn", {'face_id': face_encoding_binary, 'usn': usn})
        conn.commit()
        
        print("Face stored successfully.")
    else:
        print("Error: Unable to detect a single face in the image.")

def main_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    while True:
        print("\nMain Menu:")
        print("1. Add Student")
        print("2. Edit Student")
        print("3. Delete Student")
        print("4. Add Face from Image Path")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            usn = input("Enter USN of the student: ").strip()
            cursor.execute("SELECT * FROM student WHERE USN = :usn", {'usn': usn})
            if cursor.fetchone():
                print("Student already exists. Here are the details:")
                display_student_details(usn, cursor)
            else:
                add_student(usn, conn, cursor)
        elif choice == '2':
            usn = input("Enter USN of the student: ").strip()
            cursor.execute("SELECT * FROM student WHERE USN = :usn", {'usn': usn})
            if cursor.fetchone():
                edit_student(usn, conn, cursor)
            else:
                print("Student not found.")
        elif choice == '3':
            usn = input("Enter USN of the student: ").strip()
            cursor.execute("SELECT * FROM student WHERE USN = :usn", {'usn': usn})
            if cursor.fetchone():
                delete_student(usn, conn, cursor)
            else:
                print("Student not found.")
        elif choice == '4':
            usn = input("Enter USN of the student: ").strip()
            cursor.execute("SELECT * FROM student WHERE USN = :usn", {'usn': usn})
            if cursor.fetchone():
                display_student_details(usn, cursor)
                image_path = input("Enter the path to the image: ").strip()
                add_face_from_path(usn, image_path, conn, cursor)
            else:
                print("Student not found.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
    close_db_connection(conn, cursor)

if __name__ == "__main__":
    main_menu()
