from flask import Flask, request, render_template
import json

app = Flask(__name__)

def load_people():
    with open('people.json', 'r') as file:
        return json.load(file)

def save_people(people):
    with open('people.json', 'w') as file:
        json.dump(people, file)

@app.route("/", methods=["GET", "POST"])
def check_dob():
    result = ""
    people = load_people()
    if request.method == "POST":
        name_to_check = request.form.get("name")
        dob_to_check = request.form.get("dob")
        
        # Find all people with the same date of birth
        duplicates = [person["name"] for person in people if person["dob"] == dob_to_check]
         
        if duplicates:
            # Include the user's name if they are also in the duplicates
            if name_to_check not in duplicates:
                duplicates.append(name_to_check)
            result = f"People who share the same date of birth ({dob_to_check}): {', '.join(duplicates)}."
        else:
            new_person = {"name": name_to_check, "dob": dob_to_check}
            people.append(new_person)
            save_people(people) 
            
            result = f"{name_to_check} has been added with the date of birth {dob_to_check}."
            
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)