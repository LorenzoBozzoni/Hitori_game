import g2d
from boardgame import BoardGame
from boardgamegui import BoardGameGui, gui_play
import random

BLACK = "BLACK"
CLEAR = "CLEAR"
CIRCLE = "CIRCLE"

''' STARTING EXECUTION FROM THIS FILE '''
''' PRESS "?" FOR SHOWING HINT & RULES OF THE GAME '''

class Hitori(BoardGame):
    '''my methods'''
    def __init__(self, cols: int, rows: int):
        self._cols = cols 
        self._rows = rows 
        self._values_matrix = [] * (self._cols * self._rows)     # this list contains number inside the cells    
        self._status_matrix = [CLEAR] * (self._cols * self._rows)        # this list contains the status of the cells    
        self._flag_finished = True
        self._flag_continuity = False
        self._flag_same_circled_value = False
        self.fill_matrix()
        self._blank_matrix = [False] * (self._cols * self._rows)     # used for checking the continuity of the blank cells
        self._last_element = ""

    def fill_matrix(self):
        with open(str(self.cols()) + "x" + str(self.cols()) + ".txt", "r") as f:           # a different file is opened depending on the size the user chose
            for line in f:
                l = line.strip()
                self._values_matrix.extend(l.split("\t"))
                
    def status_at(self, x: int, y: int) -> str:                  # return the status of a cell
        return self._status_matrix[y * self.cols() + x] 

    def play_at(self, x: int, y: int):     
        if self._status_matrix[y * self.cols() + x] == CLEAR:
            self._status_matrix[y * self.cols() + x] = BLACK          # if a cell is clear, becomes black and vice versa
        elif self._status_matrix[y * self.cols() + x] == BLACK:
            self._status_matrix[y * self.cols() + x] = CLEAR

    def flag_at(self, x: int, y: int): 
        if self._status_matrix[y * self.cols() + x] == CLEAR:
            self._status_matrix[y * self.cols() + x] = CIRCLE         # the cell is circled
        elif self._status_matrix[y * self.cols() + x] == CIRCLE:
            self._status_matrix[y * self.cols() + x] = CLEAR

    def value_at(self, x: int, y: int) -> str:
        return self._values_matrix[y * self.cols() + x]      # return the value of a cell

    def cols(self) -> int: 
        return self._cols

    def rows(self) -> int: 
        return self._rows

    def finished(self) -> bool:          # checking wheter the game is finished or not
        cols, rows = self.cols(), self.rows()
        self._flag_finished = True

        for y in range(rows):
            for x in range(cols):
                if self.status_at(x, y) == BLACK:      # checking the adjacent cells of the black ones
                    if self.check_neighbours(x, y, "CHECK_BLACKS"):
                        return False
                else:           # if the cell is not black, we have to check its value
                    self.check_its_column_row(x, y)
        
        self.check_white_connection()

        if self._flag_finished and self._flag_continuity:
            return True

    def wrong(self):         # checking wheter any constrait is violated
        self._flag_continuity = False
        self._flag_same_circled_value = False

        cols, rows = self.cols(), self.rows()

        for y in range(rows):
            for x in range(cols):
                if self.status_at(x, y) == BLACK:      # checking the adjacent cells of the black ones
                    if self.check_neighbours(x, y, "CHECK_BLACKS"):
                        return True
                elif self.status_at(x, y) == CIRCLE:
                    self.set_circles_black(x, y, False)
        
        self.check_white_connection()
        
        if self._flag_same_circled_value or not self._flag_continuity:
            return True
        else:
            return False

    def check_neighbours(self, x: int, y: int, command: str) -> bool:      # return a list containing the indexes of the adjacent cells
        index_list = []
        
        if x == 0 and y == 0:         # top-left corner
            index_list.append((x + 1, y))
            index_list.append((x, y + 1))
        elif x == self.cols() - 1 and y == 0:      # top-right corner
            index_list.append((x - 1, y))
            index_list.append((x, y + 1))
        elif x == 0 and y == self.rows() - 1:       # bottom-left corner
            index_list.append((x + 1, y))
            index_list.append((x, y - 1)) 
        elif x == self.cols() - 1 and y == self.rows() - 1:      # bottom-right corner
            index_list.append((x - 1, y))
            index_list.append((x, y - 1)) 
        elif x == 0:         # left side
            index_list.append((x + 1, y))
            index_list.append((x, y + 1))
            index_list.append((x, y - 1)) 
        elif x == self.cols() - 1:      # right side
            index_list.append((x - 1, y))
            index_list.append((x, y + 1))
            index_list.append((x, y - 1)) 
        elif y == self.rows() - 1:       # bottom side
            index_list.append((x + 1, y))
            index_list.append((x, y - 1))
            index_list.append((x - 1, y)) 
        elif y == 0:      # bottom-right corner
            index_list.append((x + 1, y))
            index_list.append((x, y + 1))
            index_list.append((x - 1, y)) 
        else:               # intern cells
            index_list.append((x - 1, y))
            index_list.append((x, y + 1))
            index_list.append((x + 1, y))
            index_list.append((x, y - 1)) 
        
        # every method of the followings is used for checking constraits 
        if command == "CHECK_BLACKS":           
           return self.check_black(index_list)
        elif command == "CONNECT_WHITE":
           return self.white_connection(index_list, x, y)
        elif command == "AUTOMATIC_CIRCLES": 
           return self.insert_automatic_circles(index_list, self.status_at(x, y))

    def check_black(self, i_list):             # checking that there are not two black cells near
        for element in i_list:
            if self.status_at(element[0],element[1]) == BLACK:
                return True
        
        return False        # once the for control has checked status foreach index of the near cells, if there isn't any black, return true, so it's ok
            
    def white_connection(self, i_list, x, y):        # checking that all white cells are connected each other
        for element in i_list:
            if self.status_at(element[0],element[1]) != BLACK:
                if self._blank_matrix[element[0] + self.cols() * element[1]] == False:
                    self._blank_matrix[element[0] + self.cols() * element[1]] = True
                    self.check_neighbours(element[0],element[1], "CONNECT_WHITE")
                else:
                    pass
        return True

    def insert_automatic_circles(self, i_list, cell_status):        # the adjacent cells to the black ones are circled because there must not be two black cells near 
        updated = False
        if cell_status == BLACK:
            for element in i_list:
                if self.status_at(element[0],element[1]) != BLACK:
                    self._status_matrix[element[0] + self.cols() * element[1]] = CIRCLE           
                    updated = True

        return updated

    def check_white_connection(self):                  
        white_cell_founded = False
        self._flag_continuity = False
        for element in range(len(self._blank_matrix)):            # set every cell of blank_matrix to false. Needed to check the continuity
            self._blank_matrix[element] = False 

        b_m_white_cells = 0                      # number of white cells counted from the blank matrix
        s_m_white_cells = 0                      # number of white cells counted from the status matrix



        for y in range(self.rows()):
            for x in range(self.cols()):
                if self.status_at(x, y) != BLACK:      # checking the adjacent cells of the black ones
                    self._blank_matrix[x + self.cols() * y] = True
                    if self.check_neighbours(x, y, "CONNECT_WHITE"):
                        white_cell_founded = True                           # finding the first white cell 
                        break
                    break
                if white_cell_founded == True:
                    break
                else:
                    continue
            break
                          


        for i in self._blank_matrix:
            if i == True:
                b_m_white_cells += 1
        
        for j in self._status_matrix:
            if j != BLACK:
                s_m_white_cells += 1

        if s_m_white_cells == b_m_white_cells:         # if this two numbers are equivalent, all white cells are connected
            self._flag_continuity = True   

    def check_its_column_row(self, x: int, y: int) -> bool:         # checking clear cell status that are on the same row and column 
        k = 0
        value = self.value_at(x, y)

        first_flag = False
        second_flag = False 
        

        for k in range(self.rows()):
            if k != y and self.status_at(x,k) != BLACK:
                if value == self.value_at(x, k):
                    first_flag = True
        
        for k in range(self.cols()):
            if k != x and self.status_at(k, y) != BLACK:
                if value == self.value_at(k, y):
                    second_flag = True

        if first_flag == True or second_flag == True:      # if we find at least one equal value, the game is not finished yet
            self._flag_finished = False

    def message(self) -> str:
        return "Congratulations! You won!"

    def hint(self, command: str):
        for y in range(self.rows()):
            for x in range(self.cols()):
                if command == "AUTOMATIC_CIRCLES":
                    if self.status_at(x, y) == BLACK:      # checking the adjacent cells of the black ones
                        if self.check_neighbours(x, y, "AUTOMATIC_CIRCLES"):
                            pass
                elif command == "CLEAR_ALL":
                    self._status_matrix[x + y*self.cols()] = CLEAR
                elif command == "SOLVE":
                        #self.solve_recursive(x + self.cols() * y)
                        g2d.update_canvas()
                        for element in range(len(self._status_matrix)): 
                            self._status_matrix[element] = CLEAR 
                        if not self.solve_recursive(x + self.cols() * y):
                            g2d.prompt("Impossibile risolvere questa matrice")
                        return
                elif command == "SET_CIRCLES_BLACK":
                    if self.status_at(x, y) == CIRCLE:
                        self.set_circles_black(x,y, True)     # qua non manca un controllo sulla cella, per fare in modo che sia CIRCLE?
                elif command == "NEXT_MOVE":
                    self.next_move()
                    return

    def set_circles_black(self, x ,y, change):               # if two cells are both circled, have the same value and are on the same row/column
        k = 0
        value = self.value_at(x, y)

        first_flag = False
        second_flag = False 

        for k in range(self.rows()):
            if k != y and self.status_at(x,k) == CIRCLE:
                if value == self.value_at(x, k):
                    first_flag = True
        
        for k in range(self.cols()):
            if k != x and self.status_at(k, y) == CIRCLE:
                if value == self.value_at(k, y):
                    second_flag = True
        
        if first_flag == True or second_flag == True:     
            if change == True:
                self._status_matrix[x + self.cols() * y] = BLACK 
            else:
                self._flag_same_circled_value = True

    def next_move(self):                                   # making an automatic move that does not violate any constrait. This does not assure the game is going to be solved using only this automatic moves
        x = random.randrange(self.cols())
        y = random.randrange(self.rows())

        while self.status_at(x, y) != CLEAR:
            x = random.randrange(self.cols())
            y = random.randrange(self.rows())
            

        self._status_matrix[x + self.cols() * y] = BLACK       # try to set to black a random set
        if self.wrong():
            self._status_matrix[x + self.cols() * y] = CIRCLE      # try to set to circle the same cell because it could not be set to black
            if self.wrong(): 
                self._status_matrix[x + self.cols() * y] = CLEAR     # this cell cannot be set to black neither to circle    

        return self.status_at(x, y)

    def solve_recursive(self,i) -> bool:        # solve automatically the game
        global n
        self.hint("AUTOMATIC_CIRCLES")
        if self.wrong(): 
            return False  # unsolvable
        while i < len(self._status_matrix) and self._status_matrix[i] != CLEAR:
            i += 1
            
        if i < len(self._status_matrix):
            saved = self._status_matrix[:]  # save current status
            for a in (BLACK, CIRCLE):
                self._status_matrix[i] = a
                if self.solve_recursive(i + 1):
                    return True
                self._status_matrix = saved  # backtracking
        return self.finished()


def main():
    g2d.init_canvas((0,0))      
    side = 0
    while side != 15 and side != 12 and side != 9 and side != 8 and side != 6 and side != 5:       # user can choose one of those configurations
        side = int(g2d.prompt("Number of cols & rows? (available options: 15,12,9,8,6,5)"))
    
    h = Hitori(side, side)
    print(h._values_matrix)

    gui_play(h)
    bb = BoardGameGui(h)
    


main()
