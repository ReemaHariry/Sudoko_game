import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("500x550")
root.config(bg="#f0f0f0")

# Define the Sudoku grid (9x9) as a 2D list of Entry widgets
entries = []

# Example Sudoku puzzle (0 represents empty cells)
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def create_grid():
    global entries
    entries = [[None for _ in range(9)] for _ in range(9)]

    for row in range(9):
        for col in range(9):
            entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center', bd=1, relief="solid")
            entry.grid(row=row, column=col, padx=(0 if col % 3 else 3), pady=(0 if row % 3 else 3),
                       ipadx=5, ipady=5)
            entry.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
            entries[row][col] = entry

    set_initial_values()

def set_initial_values():
    for row in range(9):
        for col in range(9):
            if initial_board[row][col] != 0:
                entries[row][col].insert(0, str(initial_board[row][col]))
                entries[row][col].config(state='disabled')  # Disable editing of initial values

# Function to clear the grid
def clear_grid():
    for row in range(9):
        for col in range(9):
            entries[row][col].config(state='normal')  # Enable editing
            entries[row][col].delete(0, tk.END)

# Function to validate if a number can be placed at board[row][col]
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# Function to find an empty cell in the grid
def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# Function to solve the Sudoku using backtracking
def solve_sudoku(board):
    empty_location = find_empty_location(board)

    if not empty_location:
        return True  # Puzzle solved

    row, col = empty_location

    for num in range(1, 10):  # Try numbers 1 to 9
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0  # Backtrack

    return False

# Function to retrieve the current state of the board
def get_board():
    return [[int(entries[row][col].get() or 0) for col in range(9)] for row in range(9)]

# Function to check the validity of the current board
def check_sudoku():
    board = get_board()
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0  # Temporarily set the current cell to 0 to avoid conflict with itself
                if not is_valid(board, row, col, num):
                    messagebox.showerror("Error", "Sudoku is not valid.")
                    return False
                board[row][col] = num  # Restore the number after checking
    messagebox.showinfo("Success", "Sudoku is valid!")
    return True

# Function to solve the Sudoku and update the GUI
def solve_sudoku_button():
    board = get_board()
    if solve_sudoku(board):
        for row in range(9):
            for col in range(9):
                entries[row][col].delete(0, tk.END)
                entries[row][col].insert(0, str(board[row][col]))
        messagebox.showinfo("Success", "Sudoku solved!")
    else:
        messagebox.showerror("Error", "No solution exists.")

# Create the grid
create_grid()

# Add buttons for actions
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=9, column=0, columnspan=9, pady=20)

check_button = tk.Button(button_frame, text="Check", command=check_sudoku, font=('Arial', 12), width=10, bg="#dff0d8")
check_button.pack(side=tk.LEFT, padx=10)

solve_button = tk.Button(button_frame, text="Solve", command=solve_sudoku_button, font=('Arial', 12), width=10, bg="#d9edf7")
solve_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_grid, font=('Arial', 12), width=10, bg="#f2dede")
clear_button.pack(side=tk.LEFT, padx=10)

# Start the GUI loop
root.mainloop()
