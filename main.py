class Student:
    def __init__(self, name: str, age: int, student_id: str) -> None:
        self.name = name.strip()
        self.age = age
        self.student_id = student_id.strip()

    def __repr__(self) -> str:
        return f"Student(name={self.name!r}, age={self.age}, student_id={self.student_id!r})"


def get_valid_age(prompt: str) -> int:
    while True:
        age_input = input(prompt).strip()
        if not age_input:
            print("Age cannot be empty. Please try again.")
            continue
        if not age_input.isdigit():
            print("Please enter a valid number for age.")
            continue

        age = int(age_input)
        if age <= 0:
            print("Age must be greater than zero.")
            continue

        return age


def collect_student_data(count: int = 3) -> list[Student]:
    students: list[Student] = []

    print(f"Please enter information for {count} students.")
    for index in range(1, count + 1):
        print(f"\nStudent {index}")
        name = input("  Name: ").strip()
        while not name:
            print("  Name cannot be empty.")
            name = input("  Name: ").strip()

        age = get_valid_age("  Age666: ")

        student_id = input("  Student ID: ").strip()
        while not student_id:
            print("  Student ID cannot be empty.")
            student_id = input("  Student ID: ").strip()

        students.append(Student(name, age, student_id))

    return students


def print_students_sorted(students: list[Student]) -> None:
    print("\nStudent names and ages in order:")
    for student in sorted(students, key=lambda s: s.name.lower()):
        print(f"- {student.name}, {student.age} years old")


if __name__ == "__main__":
    student_list = collect_student_data(3)
    print_students_sorted(student_list)