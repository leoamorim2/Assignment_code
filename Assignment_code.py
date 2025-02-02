import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


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
        messagebox.showerror("Error", "File not found. Please check the path and try again.")
        return None
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "File is empty.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error loading the file: {e}")
        return None


def calculate_average(column):
    return column.mean() if not column.empty else 0


def count_grades(data):
    fails = len(data[data['grade'] < 40])
    passes = len(data[data['grade'] >= 40])
    grades_distribution = {
        'A': len(data[data['grade'] >= 70]),
        'B': len(data[(data['grade'] >= 50) & (data['grade'] < 70)]),
        'C': len(data[(data['grade'] >= 40) & (data['grade'] < 50)])
    }
    return fails, passes, grades_distribution


def display_results():
    avg_grade = calculate_average(data['grade'])
    avg_attendance = calculate_average(data['attendance'])
    fails, passes, grades_distribution = count_grades(data)

    for row in tree.get_children():
        tree.delete(row)

    tree.insert("", "end", values=("Average Grade", f"{avg_grade:.2f}"))
    tree.insert("", "end", values=("Average Attendance", f"{avg_attendance:.2f}%"))
    tree.insert("", "end", values=("Fails", fails))
    tree.insert("", "end", values=("Passes", passes))

    for grade, count in grades_distribution.items():
        tree.insert("", "end", values=(f"Grade {grade}", count))


def search_student():
    search_term = entry_search.get().strip()
    if search_term.isdigit():
        result = data[data['student_id'] == int(search_term)]
    else:
        result = data[(data['first_name'].str.contains(search_term, case=False, na=False)) |
                      (data['last_name'].str.contains(search_term, case=False, na=False))]
    for row in search_tree.get_children():
        search_tree.delete(row)
    if result.empty:
        search_tree.insert("", "end", values=("No results found", "", "", "", ""))
    else:
        for _, row in result.iterrows():
            search_tree.insert("", "end", values=(
            row['student_id'], row['first_name'], row['last_name'], row['country'], row['grade']))


def plot_average_grade_by_country():
    avg_grade_by_country = data.groupby('country')['grade'].mean().sort_values()
    avg_grade_by_country.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title('Average Grades by Country')
    plt.xlabel('Country')
    plt.ylabel('Average Grade')
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.tight_layout()
    plt.show()


file_path = "student_grades.csv"
data = load_data(file_path)
if data is None or data.empty:
    exit()

root = tk.Tk()
root.title("Student Grades Application")

frame = tk.Frame(root)
frame.pack(pady=10)

tree = ttk.Treeview(frame, columns=("Metric", "Value"), show="headings")
tree.heading("Metric", text="Metric")
tree.heading("Value", text="Value")
tree.pack()

tk.Button(root, text="Display Results", command=display_results).pack(pady=5)

frame_search = tk.Frame(root)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Search Student:").pack(side=tk.LEFT)
entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT, padx=5)
tk.Button(frame_search, text="Search", command=search_student).pack(side=tk.LEFT)

search_tree = ttk.Treeview(root, columns=("ID", "First Name", "Last Name", "Country", "Grade"), show="headings")
for col in ["ID", "First Name", "Last Name", "Country", "Grade"]:
    search_tree.heading(col, text=col)
search_tree.pack()

tk.Button(root, text="Show Grade Chart", command=plot_average_grade_by_country).pack(pady=5)

root.mainloop()
