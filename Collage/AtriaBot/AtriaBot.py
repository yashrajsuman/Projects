import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Data for places, teachers, and principal/HOD names
place_data = {
    "atriainstituteoftechnology": "Atria Institute of Technology is in Anandnagar, Hebble, Bangalore, India.",
    "seminarhall": "It is on the second floor, near the admin block.",
    "library": "The library is located on the first floor, adjacent to the IT block.",
    "canteen": "The canteen is on the ground floor, beside the auditorium.",
    "gym": "The gym is in the sports complex on the west side of campus.",
    "bc615": "BC615 is in the fourth floor corner room.",
    "hod cabin": "HOD cabin is in the 4th floor beside stairs.",
}

teacher_data = {
    "software engineering": "Prof. Asma Begum",
    "project management": "Prof. Asma Begum",
    "se": "Prof. Asma Begum",
    "computer networks": "Prof. Manjunath Khatokar",
    "cn": "Prof. Manjunath Khatokar",
    "theory of computation": "Prof. Kavita GL",
    "toc": "Prof. Kavita GL",
    "mini project": "Dr. Deepak NR",
    "iot": "Om Prakash",
    "idt": "Prof. Asma Begum",
    "english": "Prof. Jeslin",
    "kannada": "Prof. Jeslin",
}

principal_name = "Dr. Principle"  
hod_names = {
    "ise": "Dr. Deepak NR", 
    "cse": "Dr. Devi Kannan"   
}
print("Hi, I am Atria Bot")
def get_response():
    user_input = input("You: ")
    user_input = user_input.lower().strip().replace("?", "").replace(",", "").replace(".", "")
    
    # Check for greetings first
    if "hi" in user_input or "hello" in user_input:
        print("Bot: Hello!")
        return True
    if "good morning" in user_input:
        print("Bot: Good Morning!")
        return True
    if "good afternoon" in user_input:
        print("Bot: Good Afternoon!")
        return True
    if "bye" in user_input:
        print("Bot: Bye! Have a great day!")
        return False  # Exit the loop

    # Named Entity Recognition to understand the question
    doc = nlp(user_input)

    # Check for location-related queries
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity
            if ent.text.lower() in place_data:
                print(f"Bot: {place_data[ent.text.lower()]}")
                return True

    # Check for specific location queries that might not be recognized as entities
    for place in place_data.keys():
        if place in user_input:
            print(f"Bot: {place_data[place]}")
            return True

    # HOD queries should be prioritized here
    if "who" in user_input and "hod" in user_input:
        if "of" in user_input:
            branch = user_input.split("of")[-1].strip()
        else:
            branch = user_input.split("hod")[-1].strip()
        branch = branch.lower()  # Convert to lower case for comparison
        if branch in hod_names:
            print(f"Bot: The HOD of {branch.upper()} is {hod_names[branch]}.")
        elif not branch:
            print("Bot: Please specify the department. For example, 'Who is HOD of ISE?'")
        else:
            print(f"Bot: Sorry, I don't have information about the HOD of {branch.upper()}.")
        return True

    # Check for specific teacher queries
    if ("who" in user_input and "teaching" in user_input) or ("who" in user_input and "teach" in user_input):
        subject = user_input.split("teaching")[-1].strip() if "teaching" in user_input else user_input.split("teach")[-1].strip()
        subject = subject.lower()  # Convert to lower case for comparison
        if subject in teacher_data:
            print(f"Bot: {teacher_data[subject]} teaches {subject}.")
        else:
            print("Bot: Sorry, I don't know who teaches that subject.")
        return True

    # Check for specific subject queries
    if "who is" in user_input:
        subject = user_input.split("who is")[-1].strip()
        subject = subject.lower()  # Convert to lower case for comparison
        for key, value in teacher_data.items():
            if subject in (key, value.lower()):
                print(f"Bot: {value} teaches {key}.")
                return True

    # Check for general teacher queries by subject
    for subject in teacher_data.keys():
        if subject in user_input:
            print(f"Bot: {teacher_data[subject]} teaches {subject}.")
            return True

    # Principal queries
    if "principal" in user_input:
        print(f"Bot: The principal is {principal_name}.")
        return True

    print("Bot: Sorry, I don't know the answer to that.")
    return True  # Continue the loop

while True:
    if not get_response():
        break
