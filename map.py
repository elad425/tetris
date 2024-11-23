import pygame

class Map(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x,y))

class Line(pygame.sprite.Sprite):
    def __init__(self,width,height,color,x,y):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x,y))


shape=[
    'clcccccccctc',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'r          x',
    'rggggggggggx'
]
