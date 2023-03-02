import tkinter as tk
from tkinter import messagebox
from selector import *

class Sudoku:
    board_width = 450
    board_height = 450
    bar_height = 50

    def __init__(self, difficuly = Difficuly.EASY) -> None:
        self.selector = Selector(difficuly)
        self.current_number = None
        self.canvas_items = {} #id list 
        self.board : dict = {}  #items : (id, editable)

        win= tk.Tk()
        win.title("Sudoku")
        win.resizable(False, False)
        #win.geometry(f"{Sudoku.board_width}x{Sudoku.board_height + Sudoku.bar_height}")
        self.canvas= tk.Canvas(win, 
            width=Sudoku.board_width,
            height=Sudoku.board_height+Sudoku.bar_height,
            background="white")
        self.canvas.bind("<Button-1>", self.update)
        self.canvas.bind("<Button-3>", self.delete_numbers)
        self.canvas.pack()

        self.setup_canvas()
        self.setup_board()
        win.mainloop()

    def delete_numbers(self, event):
        canvas, click_x, click_y = self.canvas, event.x, event.y
        width, height = Sudoku.board_width, Sudoku.board_height
        x, y = click_x // (width // 9), click_y // (height // 9)
        item_id = x + y * 9

        if y > 8: return

        if item_id in self.board and self.board[item_id][1]:
            val = self.canvas_items.pop(item_id, None)
            if val != None : canvas.delete(val)
            self.board.pop(item_id, None)

    def setup_canvas(self):
        """Create the sudoku outlines"""
        canvas = self.canvas      
        width, height, bar_height = Sudoku.board_width, Sudoku.board_height, Sudoku.bar_height

        #board
        for i in range(1, 9):
            line_width = 3 if i % 3 == 0 else 1 
            canvas.create_line(width / 9 * i, 0, width / 9 * i, height, width=line_width)
            canvas.create_line(0, height / 9 * i, width, height / 9 * i, width=line_width)

        #selecting bar
        for i in range(0, 9):
            pos_x = width // 9 * (i + 0.5)
            pos_y = height + bar_height * 0.5
            canvas.create_line(width / 9 * i, height, width / 9 * i, height + bar_height, width=3)
            canvas.create_text(pos_x, pos_y, text=str(i + 1), font=('Calibri 18'))
        canvas.create_rectangle(3, height, width, height + bar_height, width=3)

    def setup_board(self):
        """Load and draw a sudoku game"""
        board = self.selector.get_board().strip('\n')
        width, height = Sudoku.board_width, Sudoku.board_height

        #delete old items
        for key, value in self.canvas_items.items():
            self.canvas.delete(value)
        self.canvas_items.clear()
        self.board.clear()

        #add new items
        for i, x in enumerate(board):
            if x == '0': continue
            pos_x = width // 9 * (i % 9 + 0.5)
            pos_y = height // 9 * (i // 9 + 0.5)
            self.canvas_items[i] = self.canvas.create_text(
                pos_x, pos_y, text=x, font=('Calibri 18'), fill='green')
            self.board[i] = (int(x), False)

    def check_win(self):
        #check if board is filled
        for i in range(0, 81):
            if not self.canvas_items.get(i, None): return False

        #copy board to list
        b : list[list[str]] = []
        for i in range(0,9):
            b.append([])
            for j in range(0,9):
                b[i].append(self.board[i + 9 * j][0])

        for i in range(0,9):
            #check row
            if b[i].count(i + 1) != 1:
                return False
            
            #check column
            temp = set({})
            for j in range(0,9):
                temp.add(b[i][j])
            if len(temp) != 9:
                return False
            
            #check 3x3 grids
            grid_x = i % 3
            grid_y = i // 3
            temp.clear()
            for j in range(0, 3): 
                for k in range(0, 3):
                    temp.add(b[grid_x * 3 + j][grid_y * 3 + k])
            if len(temp) != 9:
                return False

        return True

    def update(self, event):
        canvas, click_x, click_y = self.canvas, event.x, event.y
        width, height = Sudoku.board_width, Sudoku.board_height
        x, y = click_x // (width // 9), click_y // (height // 9)
        item_id = x + y * 9

        if y <= 8:
            #print new numbers to screen
            pos_x = width // 9 * (x + 0.5)
            pos_y = height // 9 * (y + 0.5)
            if not self.current_number:# delete
                if item_id in self.board and self.board[item_id][1] == True:
                    val = self.canvas_items.pop(item_id, None)
                    if val != None : canvas.delete(val)
                    self.board.pop(item_id, None)
            elif item_id not in self.canvas_items: #add
                self.canvas_items[item_id] = canvas.create_text(
                    pos_x, pos_y, text=self.current_number, font=('Calibri 18'), fill='red')
                self.board[item_id] = (self.current_number, True)
        else:
            #update current number
            if self.current_number == x + 1:
                self.current_number = None
            else:
                self.current_number = x + 1
            for i in range(0, 81):  
                if self.board.get(i, None) == None: continue
                if self.board.get(i)[0] == self.current_number:
                    self.canvas.itemconfig(self.canvas_items[i], fill='red')
                elif self.board.get(i)[1] != False:
                    self.canvas.itemconfig(self.canvas_items[i], fill='black')
                else:
                    self.canvas.itemconfig(self.canvas_items[i], fill='green')


        if self.check_win():
            messagebox.showinfo("winner!", "Congrats on solving the puzzle!")
            self.setup_board()