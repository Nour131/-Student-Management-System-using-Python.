import json
import os

FILENAME = "students.json"


def load_students():
    if not os.path.exists(FILENAME):
        return {}
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Could not read the data file. Starting with an empty list.")
        return {}


def save_students(students_dict):
    with open(FILENAME, "w") as f:
        json.dump(students_dict, f, indent=2)


def get_int_input(prompt, default=None):
    """Keeps asking until a valid integer is entered.
    If default is not None, an empty input returns the default instead of looping."""
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            return int(val)
        except ValueError:
            print("Please enter a valid number.")


def add_student(students_dict):
    new_student = {}

    name = input("Enter student's name: ").strip()
    while not name:
        name = input("Name cannot be empty. Enter student's name: ").strip()
    new_student["name"] = name

    new_id = get_int_input("Enter student's id: ")

    # Check for duplicate ID before doing anything else
    for student in students_dict.values():
        if student["id"] == new_id:
            print("A student with this ID already exists. Student not added.")
            return

    new_student["id"] = new_id
    new_student["age"] = get_int_input("Enter student's age: ")
    new_student["major"] = input("Enter student's major: ").strip()
    new_student["email"] = input("Enter student's email: ").strip()

    # Use the ID itself as the key so keys never collide, even after deletions
    students_dict[f"student{new_id}"] = new_student
    save_students(students_dict)
    print("Student added successfully.")


def view_students(students_dict):
    if not students_dict:
        print("No students found.")
        return
    print(json.dumps(students_dict, indent=2))


def search_by_id(students_dict, student_id):
    for key in students_dict:
        if students_dict[key]["id"] == student_id:
            return students_dict[key]
    return None


def update_student(students_dict, student_id):
    for key in students_dict:
        if students_dict[key]["id"] == student_id:
            print("Current info:", students_dict[key])
            field = input("Which field do you want to update (name/age/major/email)? ").strip()

            if field not in ("name", "age", "major", "email"):
                print("Invalid field.")
                return

            if field == "age":
                new_val = get_int_input("Enter new age: ")
            else:
                new_val = input(f"Enter new {field}: ").strip()

            students_dict[key][field] = new_val
            save_students(students_dict)
            print("Student updated successfully.")
            return

    print("No student found with this ID.")


def delete_student(students_dict, student_id):
    key_to_delete = None
    for key in students_dict:
        if students_dict[key]["id"] == student_id:
            key_to_delete = key
            break

    if key_to_delete:
        confirm = input(f"Are you sure you want to delete student {student_id}? (y/n): ").strip().lower()
        if confirm == "y":
            del students_dict[key_to_delete]
            save_students(students_dict)
            print("Student deleted successfully.")
        else:
            print("Delete cancelled.")
    else:
        print("No student found with this ID.")



def main():
    students_dict = load_students()

    menu = """
==== Student Management System ====
1. Add a student
2. View all students
3. Search for a student by ID
4. Update student information
5. Delete a student
6. Exit
=====================================
"""

    while True:
        print(menu)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_student(students_dict)

        elif choice == "2":
            view_students(students_dict)

        elif choice == "3":
            student_id = get_int_input("Enter student ID to search: ")
            result = search_by_id(students_dict, student_id)
            if result:
                print("Student found:", result)
            else:
                print("No student found with this ID.")

        elif choice == "4":
            student_id = get_int_input("Enter student ID to update: ")
            update_student(students_dict, student_id)

        elif choice == "5":
            student_id = get_int_input("Enter student ID to delete: ")
            delete_student(students_dict, student_id)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please choose between 1 and 6.")


if __name__ == "__main__":
    main()
