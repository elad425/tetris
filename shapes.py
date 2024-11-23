import pygame

class Shape(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_pos(self):
        return [self.rect.x,self.rect.y]

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    shape_red=['xx','xx'],['xx','xx'],['xx','xx'],['xx','xx']

    shape_blue=['xx','x','x'],['xxx','  x'],[' x',' x','xx'],['x','xxx']

    shape_brown=['xx',' x',' x'],['  x','xxx'],['x','x','xx'],['xxx','x']

    shape_green=['x','xx',' x'],[' xx','xx '],['x','xx',' x'],[' xx','xx ']

    shape_purple=[' x','xx','x'],['xx ',' xx'],[' x','xx','x'],['xx ',' xx']

    shape_yellow=['x','xx','x'],['xxx',' x '],[' x','xx',' x'],[' x ','xxx']

    shape_dark_green=['x','x','x','x'],['xxxx'],['x','x','x','x'],['xxxx']
