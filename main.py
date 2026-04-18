class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

def collect_student_data():
    students = []
    for _ in range(3):
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        student_id = input("Enter student ID: ")
        students.append(Student(name, age, student_id))
    return students

def print_student_list(students):
    sorted_students = sorted(students, key=lambda student: student.name)
    for student in sorted_students:
        print(f"Name: {student.name}, Age: {student.age}")

if __name__ == "__main__":
    student_data = collect_student_data()
    print_student_list(student_data)