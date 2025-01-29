import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


def create_db():
    
    conn = sqlite3.connect('student_grades.db')  
    cursor = conn.cursor()

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        country TEXT,
        grade REAL,
        attendance REAL
    )
    ''')

    conn.commit()  
    conn.close()


def load_data(file_path):
    
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("Error: File not found. Please check the path and try again.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return None
    except Exception as e:
        print(f"Error loading the file: {e}")
        return None


def calculate_average(column):
    
    if column.empty:
        return 0
    return column.mean()


def count_grades(data):
    
    fails = len(data[data['grade'] < 40])
    passes = len(data[data['grade'] >= 40])

    grades_distribution = {
        'A': len(data[data['grade'] >= 70]),
        'B': len(data[(data['grade'] >= 50) & (data['grade'] < 70)]),
        'C': len(data[(data['grade'] >= 40) & (data['grade'] < 50)])
    }

    return fails, passes, grades_distribution


def display_results(avg_grade, avg_attendance, fails, passes, grades_distribution):
    
    print("Mandatory Results:")
    print(f"Average grade: {avg_grade:.2f}")
    print(f"Average attendance: {avg_attendance:.2f}%")
    print(f"Number of fails: {fails}")
    print(f"Number of passes: {passes}")
    print("Grade distribution:")
    for grade, count in grades_distribution.items():
        print(f"  {grade}: {count}")


def search_student(data):
    
    search_term = input("Enter the student's name or ID: ").strip()
    if search_term.isdigit():
        result = data[data['student_id'] == int(search_term)]
    else:
        result = data[(data['first_name'].str.contains(search_term, case=False, na=False)) |
                      (data['last_name'].str.contains(search_term, case=False, na=False))]

    if result.empty:
        print("Student not found.")
    else:
        print("Search results:")
        print(result)


def plot_average_grade_by_country(data):
    
    avg_grade_by_country = data.groupby('country')['grade'].mean().sort_values()
    avg_grade_by_country.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title('Average Grades by Country')
    plt.xlabel('Country')
    plt.ylabel('Average Grade')
    plt.xticks(rotation=45, fontsize=8, ha='right') 
    plt.tight_layout()
    plt.show()


def main_menu():
    
    
    create_db()

    file_path = "student_grades.csv"
    data = load_data(file_path)

    data = load_data(file_path)

    if data is None or data.empty:
        print("Error: No data available for processing.")
        return

    while True:
        print("\nMain Menu:")
        print("1. Display mandatory results")
        print("2. Search for student information")
        print("3. Generate average grade by country chart")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            avg_grade = calculate_average(data['grade'])
            avg_attendance = calculate_average(data['attendance'])
            fails, passes, grades_distribution = count_grades(data)
            display_results(avg_grade, avg_attendance, fails, passes, grades_distribution)
        elif choice == '2':
            search_student(data)
        elif choice == '3':
            plot_average_grade_by_country(data)
        elif choice == '4':
            print("Exiting the programme. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main_menu()
