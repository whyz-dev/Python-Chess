from tkinter import *
from time import *

piece_name = ["Pawn", "Knight", "Rook", "Bishop", "Queen", "King"] 
color_name = ["Black","White"] 

class Piece:
    def __init__(self, canvas, typ, color, x, y):
        self.type   = typ
        self.canvas = canvas
        self.color  = color
        self.x      = x
        self.y      = y
        self.image  = PhotoImage(file="images/"+color_name[self.color]+piece_name[self.type] +'.png')
        self.item   = canvas.create_image(self.x*80, self.y*80, image=self.image,  anchor=NW)
    
    def move(self, x, y):
        self.canvas.move(self.item, (x-self.x)*80, (y-self.y)*80)
        self.x = x
        self.y = y

class Game(Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.width  = 640
        self.height = 640
        self.canvas = Canvas(self,bg = "#996633", width=self.width, height = self.height)
        self.canvas.pack()
        self.pack()
        self.choose = 0
        self.sleect = None
        self.enemy  = None

        self.pieces = []
        self.order = [2,1,3,4,5,3,1,2]
        self.turn = 0
        self.draw()

        # set pieces
        for i in range(len(self.order)):
            self.pieces.append(Piece(self.canvas,self.order[i],0,i,0))
        for i in range(8):
            self.pieces.append(Piece(self.canvas,0,0,i,1))
        for i in range(len(self.order)):
            self.pieces.append(Piece(self.canvas,self.order[i],1,7-i,7))
        for i in range(8):
            self.pieces.append(Piece(self.canvas,0,1,i,6))
        
        self.canvas.focus_set()

        self.canvas.bind('<Button-1>',
                        self.action)

    def draw(self): 
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    self.canvas.create_rectangle((i*80,j*80,i*80+80,j*80+80),fill="#%02x%02x%02x" % (204, 153, 102))

    def moveable(self, x, y):
        sel = self.select
        t = sel.type
        if t == 0:
            if not sel.color:
                if x!=sel.x:
                    if abs(x-sel.x) == 1 and y-sel.y == 1 and self.collision(x,y) == 2:
                        return 2
                    return 0
                elif y-sel.y == 2 and sel.y == 1:
                    return 1
                elif y-sel.y == 1:
                    return 1
                else:
                    return 0
            elif sel.color :
                if x!=sel.x:
                    if abs(x-sel.x) == 1 and y-sel.y == -1 and self.collision(x,y) == 2:
                        return 2
                    else:
                        return 0
                if y-sel.y == -2 and sel.y == 6 :
                    return 1
                elif y-sel.y == -1:
                    return 1
                else:
                    return 0
            else:
                return 0
        elif t == 1:
            dx = [1, 1, 2, 2, -1, -1, -2, -2]
            dy = [2, -2, 1, -1, 2, -2, 1, -1]
            for i in range(8):
                if y-sel.y == dy[i] and x-sel.x == dx[i]:
                    return 1
            return 0
        elif t == 2:
            if x == sel.x:
                for piece in self.pieces:
                    if piece.x == x and piece.y > min(y, sel.y) and piece.y < max(y, sel.y):
                        return 0
                return 1
            if y == sel.y:
                for piece in self.pieces:
                    if piece.y == y and piece.x > min(x, sel.x) and piece.x < max(x, sel.x):
                        return 0
                return 1
        elif t == 3:
            if abs(x-sel.x) == abs(y-sel.y):
                for piece in self.pieces:
                    if piece.x > min(x,sel.x) and piece.x < max(x,sel.x) and piece.y > min(y,sel.y) and piece.y < max(y,sel.y):
                        if abs(x-piece.x) == abs(y-piece.y):
                            return 0
                return 1
            return 0
        elif t == 4:
            if x == sel.x:
                for piece in self.pieces:
                    if piece.x == x and piece.y > min(y, sel.y) and piece.y < max(y, sel.y):
                        return 0
                return 1
            if y == sel.y:
                for piece in self.pieces:
                    if piece.y == y and piece.x > min(x, sel.x) and piece.x < max(x, sel.x):
                        return 0
                return 1
            if abs(x-sel.x) == abs(y-sel.y):
                for piece in self.pieces:
                    if piece.x > min(x,sel.x) and piece.x < max(x,sel.x) and piece.y > min(y,sel.y) and piece.y < max(y,sel.y):
                        if abs(x-piece.x) == abs(y-piece.y):
                            return 0
                return 1
            return 0
        elif t == 5:
            if abs(x - sel.x) <= 1 and abs(y - sel.y) <= 1:
                return 1
            return 0

    def collision(self,x,y):
        col = 0 # empty:0, ally:1, enemy:2
        for piece in self.pieces:
            if piece.x == x and piece.y == y and piece != self.select:
                col = 1 + int(piece.color != self.select.color)
                if piece.color != self.select.color:
                    self.enemy = piece
        return col

    def action(self, event):
        x = event.x//80 
        y = event.y//80

        if not self.choose:
            for piece in self.pieces:
                if x == piece.x and y == piece.y:
                    if piece.color != self.turn % 2:
                        continue
                    self.choose = 1
                    self.select = piece
        else:
            is_collision = self.collision(x,y)
            is_moveable  = self.moveable(x,y)
            print(is_moveable,is_collision)
            if is_moveable:
                if not self.select.type and is_moveable == 2 and is_collision == 2:
                    self.select.move(x,y)
                    print(self.enemy.color, self.select.color)
                    for i in range(len(self.pieces)):
                        if self.pieces[i] == self.enemy:
                            self.canvas.delete(self.pieces[i].item)
                            del self.pieces[i]
                            break
                    self.turn+=1
                elif is_moveable == 1 and is_collision == 0:
                    self.select.move(x,y)
                    self.turn+=1
                elif self.select.type and is_moveable == 1 and is_collision == 2:
                    self.select.move(x,y)
                    print(self.enemy.color, self.select.color)
                    for i in range(len(self.pieces)):
                        if self.pieces[i] == self.enemy:
                            self.canvas.delete(self.pieces[i].item)
                            del self.pieces[i]
                            break
                    print(len(self.pieces))
                    self.turn+=1
            self.choose=0

if __name__ == "__main__":
    window = Tk()
    game = Game(window)
    game.mainloop()
 