import g2d
from boardgame import BoardGame
from time import time

W, H = 40, 40
LONG_PRESS = 0.5

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._downtime = 0
        self.update_buttons()
        self._guide_open = False


    def tick(self):
        if self._guide_open == False:         # all this methods can be called only when the menu is closed
            if g2d.key_pressed("h"):
                self._game.hint("AUTOMATIC_CIRCLES")
                self.update_buttons()
            elif g2d.key_pressed("c"):
                self._game.hint("CLEAR_ALL")
                self.update_buttons()
            elif g2d.key_pressed("u"):
                self._game.hint("SET_CIRCLES_BLACK")
                self.update_buttons()
            elif g2d.key_pressed("s"):
                self._game.hint("NEXT_MOVE")
                self.update_buttons()
            elif g2d.key_pressed("w"):
                self._game.hint("SOLVE")
                self.update_buttons()
            elif g2d.key_pressed("?"):
                self.guide()
            elif g2d.key_pressed("LeftButton"):
                self._downtime = time()
            elif g2d.key_released("LeftButton"):
                mouse = g2d.mouse_position()
                if (0 <= mouse[0] <= self._game.cols() * W) and (0 <= mouse[1] <= self._game.rows() * H):  
                    x, y = mouse[0] // W, mouse[1] // H
                    if time() - self._downtime > LONG_PRESS:
                        self._game.flag_at(x, y)
                    else:
                        self._game.play_at(x, y)
                    self.update_buttons()
        else:
            if g2d.key_pressed("q"):
                self._guide_open = False
                g2d.init_canvas((self._game.cols() * W , self._game.rows() * H))
                self.update_buttons()


    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()

        '''DRAWING MATRIX LINES'''
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))

        '''MANAGING EACH MATRIX CELL'''
        for y in range(rows):
            for x in range(cols):
                value = self._game.value_at(x, y)
                center = x * W + W//2, y * H + H//2

                '''CHECKING THE STATUS OF THE CELL'''
                if self._game.status_at(x, y) == "BLACK":
                    g2d.fill_rect((x * W, y * H, W, H))
                elif self._game.status_at(x, y) == "CIRCLE":
                    image = g2d.load_image("Circle_Hitori.png")
                    g2d.draw_image(image, (x * W, y * H))
                    g2d.draw_text_centered(value, center, H//2) 
                    
                else:
                    g2d.draw_text_centered(value, center, H//2)    


        g2d.update_canvas()
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()

    def guide(self):               # showing all details about the game 
        self._guide_open = True
        size_x = 1400
        size_y = 400

        g2d.init_canvas((size_x,size_y))
        g2d.set_color((0,0,0))
        g2d.draw_text_centered("HITORI", (size_x / 2, 40),30)
        g2d.draw_text_centered("KEYS", (size_x / 4, 80), 25)
        g2d.draw_text("h ➤ draw automatic circles adjacent to black cells", (20, 110), 20)
        g2d.draw_text("c ➤ clear all matrix", (20, 140), 20)
        g2d.draw_text("u ➤ if two circles have the same value, one is set to black ", (20, 170), 20)
        g2d.draw_text("s ➤ make an automatic move (include keeping a cell not circled nor black)", (20, 200), 20)
        g2d.draw_text("w ➤ solve automatically the puzzle", (20, 230), 20)
        g2d.draw_text("q ➤ quit the menù", (size_x / 9, size_y - 35), 20)

        g2d.draw_text_centered("RULES", ((size_x / 4)*3, 80), 25)
        g2d.draw_text("1) Color cells so no number appears more than once in a row or column.", (((size_x / 2) + 20), 110), 20)
        g2d.draw_text("2) The sides of black cells never touch", (((size_x / 2) + 20), 140), 20)
        g2d.draw_text("3) White cells form a continuous network", (((size_x / 2) + 20), 170), 20)
        g2d.update_canvas()
        


def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W , game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)
