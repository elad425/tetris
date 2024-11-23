import pygame,sys
from random import choice

import tetris.map
import tetris.shapes

block_size=25
offset=block_size*6

pygame.init()
width = len(tetris.map.shape[0])*block_size+offset
height = len(tetris.map.shape)*block_size
screen = pygame.display.set_mode((width, height))

class Game:
    def __init__(self):
        self.high_score = open("tetris highscore.txt", "r").read()
        self.font3=pygame.font.Font('assets\\space invaders\\Pixeled.ttf',int(block_size))
        self.font=pygame.font.Font('assets\\space invaders\\Pixeled.ttf',int(block_size/2))
        self.font2=pygame.font.Font('assets\\space invaders\\Pixeled.ttf',int(block_size/3))
        self.shape_color_list=['green','blue','red','brown','yellow','dark green','purple']
        self.shape = tetris.map.shape
        self.history = ''
        self.spawn_place=[]
        for i in range(3,9):self.spawn_place.append(block_size*i)
        self.lst = []
        for j in range(1, 21): self.lst.append(j *block_size)

        self.red_shape=tetris.shapes.Shape.shape_red
        self.blue_shape=tetris.shapes.Shape.shape_blue
        self.green_shape = tetris.shapes.Shape.shape_green
        self.brown_shape = tetris.shapes.Shape.shape_brown
        self.yellow_shape = tetris.shapes.Shape.shape_yellow
        self.darkgreen_shape = tetris.shapes.Shape.shape_dark_green
        self.purple_shape = tetris.shapes.Shape.shape_purple

        self.block_size=block_size
        self.walls=pygame.sprite.Group()
        self.rows = pygame.sprite.Group()
        self.cols = pygame.sprite.Group()
        self.ground=pygame.sprite.Group()
        self.limitsl=pygame.sprite.Group()
        self.limitsr=pygame.sprite.Group()
        self.limit=pygame.sprite.Group()
        self.up_next_shapes=pygame.sprite.Group()
        self.ground_shapes=pygame.sprite.Group()
        self.air_shapes=pygame.sprite.Group()
        self.prediction = pygame.sprite.Group()
        self.create_map(0,0)

        self.time=0
        self.temp_time=0
        self.down_speed = 1000
        self.time_div=self.down_speed

        self.air_left=False
        self.air_right=False
        self.check_predict=False
        self.check_speed_up=False
        self.display_shade=True
        self.check_multi=False

        self.timer_start=0
        self.air_color=''
        self.temp_place=0
        self.air_dir=0
        self.score=0
        self.up_next=[]
        for i in range(4):
            temp=choice(self.shape_color_list)
            self.up_next.append(temp)
            self.shape_color_list.remove(temp)

        self.check_game=True
        self.create_shape()

    def create_map(self, x_start, y_start):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x' or col=='r' or col=='c' or col=='l' or col=='t':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Map(self.block_size, (240, 240, 240), x, y)
                    self.walls.add(block)
                if col == 'c' or col=='l' or col=='t':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Line(1,self.block_size*22, (70, 70, 70), x, y)
                    self.cols.add(block)
                if col == 'r':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Line(self.block_size*12,1, (70, 70, 70), x, y)
                    self.rows.add(block)
                if col == 'g':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Map(self.block_size,  (210, 210, 210), x, y)
                    self.ground.add(block)
                if col == 'l':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Line(1,self.block_size*22, (70, 70, 70), x, y)
                    self.limitsl.add(block)
                if col == 't':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Line(1,self.block_size*22, (70, 70, 70), x, y)
                    self.limitsr.add(block)
                if col == 'x':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.map.Map(self.block_size, (240, 240, 240), x, y)
                    self.limit.add(block)

    def draw_shape(self,group,color,shape,x_start,y_start=1):
        for row_index, row in enumerate(shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = tetris.shapes.Shape(self.block_size,color, x, y)
                    group.add(block)

    def display_up_next(self):
        temp_x_place=10
        for i in self.up_next:
            temp_color=self.pick_shape(i)
            self.draw_shape(self.up_next_shapes, i, temp_color[0], self.block_size*14,self.block_size*temp_x_place)
            temp_x_place+=5
            if not self.check_speed_up:
                break

    def movment(self):
        self.time=int(pygame.time.get_ticks()/self.time_div)
        if self.time!=self.temp_time:
            for i in self.air_shapes: i.rect.y += self.block_size
            self.temp_time=self.time

        keys=pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.time_div=50
        else:
            self.time_div=self.down_speed

    def move_right(self):
        if not self.air_right:
            for i in self.air_shapes: i.rect.x += self.block_size
            self.temp_place+=self.block_size
            self.create_shade()

    def move_left(self):
        if not self.air_left:
            for i in self.air_shapes: i.rect.x -= self.block_size
            self.temp_place-=self.block_size
            self.create_shade()

    def rotate(self):
        temp=0
        for i in self.air_shapes:
            temp=i.get_y()
            break
        self.air_shapes.empty()
        temp_color=self.pick_shape(self.air_color)
        self.draw_shape(self.air_shapes,self.air_color, temp_color[self.air_dir], self.temp_place,temp)
        self.air_dir+=1
        if self.air_dir>3:self.air_dir=0
        self.create_shade()

    def create_shape(self):
        self.air_dir=0
        self.air_color=self.up_next.pop(0)
        self.temp_place=choice(self.spawn_place)
        temp_color=self.pick_shape(self.air_color)
        self.draw_shape(self.air_shapes,self.air_color,temp_color[0],self.temp_place)
        self.air_dir+=1
        self.create_shade()

    def check_hit_ground(self):
        for i in self.ground:
            if pygame.sprite.spritecollide(i, self.air_shapes, False):
                for x in self.air_shapes: x.rect.y -= 1
                for j in self.air_shapes:self.ground_shapes.add(j)
                self.air_shapes.empty()
                self.create_shape()
                self.up_next_shapes.empty()
                self.display_up_next()

    def check_hit_shape(self):
        for i in self.ground_shapes:
            if pygame.sprite.spritecollide(i, self.air_shapes, False):
                for x in self.air_shapes: x.rect.y -=1
                for j in self.air_shapes:self.ground_shapes.add(j)
                self.air_shapes.empty()
                self.create_shape()
                self.up_next_shapes.empty()
                self.display_up_next()

    def check_hit_limits(self):
        for i in self.limitsl:
            if pygame.sprite.spritecollide(i, self.air_shapes, False):
                self.air_left=True
            else:self.air_left=False
        for i in self.limitsr:
            if pygame.sprite.spritecollide(i, self.air_shapes, False):
                self.air_right=True
            else:self.air_right=False
        for i in self.air_shapes:
            if pygame.sprite.spritecollide(i, self.limit, False):
                for j in self.air_shapes:
                    j.rect.x-=self.block_size
                self.create_shade()

    def check_side_collision(self):
        for i in self.ground_shapes:
            for j in self.air_shapes:
                if j.get_y()==i.get_y()+1:
                    if i.get_x()-self.block_size==j.get_x():
                        self.air_right=True
                    if i.get_x()+self.block_size==j.get_x():
                        self.air_left = True

    def check_complete(self):
        multi=0
        for r in range(len(self.lst)):
            counter=0
            for i in self.ground_shapes:
                temp=i.get_y()
                if temp==self.lst[r]:
                    counter+=1
            if counter==10:
                multi+=1
                for q in self.ground_shapes:
                    temp = q.get_y()
                    if temp == self.lst[r]:
                        q.kill()
                for b in self.ground_shapes:
                    if b.get_y()<self.lst[r]:
                        b.rect.y+=self.block_size
        if multi>1:
            multi*=2
            self.check_multi=True
            self.timer_start=pygame.time.get_ticks()
            self.remove_multi()
        self.score +=100*multi

    def up_next_list(self):
        if not self.shape_color_list:
            self.shape_color_list=['green','blue','red','brown','yellow','dark green','purple']
        if len(self.up_next)!=3:
            temp = choice(self.shape_color_list)
            self.up_next.append(temp)
            self.shape_color_list.remove(temp)

    def predict_landing(self):
        if not self.check_predict:
            for i in self.prediction:
                i.rect.y+=self.block_size
        for j in self.prediction:
            if pygame.sprite.spritecollide(j,self.ground,False):self.check_predict=True
            if pygame.sprite.spritecollide(j, self.ground_shapes, False): self.check_predict = True

    def create_shade(self):
        if self.display_shade:
            self.check_predict = False
            self.prediction.empty()
            for i in self.air_shapes:
                block = tetris.shapes.Shape(self.block_size, (60, 60, 60), i.get_x(), i.get_y())
                self.prediction.add(block)
        else:self.prediction.empty()

    def speed_up(self):
        if 2000<=self.score<5000:
            self.down_speed=500
        if 5000 <= self.score < 8000:
            self.down_speed = 300
            self.check_speed_up = True
        if 8000 <= self.score < 10000:
            self.down_speed = 200
        if 10000 <= self.score:
            self.down_speed = 200
            self.display_shade=False

    def display_score(self):
        score_massage = self.font.render('score:' + str(self.score), False, (250, 250, 250))
        score_rect = score_massage.get_rect(topleft=(width - offset+block_size, 0))
        screen.blit(score_massage, score_rect)
        highscore_massage = self.font2.render('highscore:' + str(self.high_score), False, (250, 250, 250))
        highscore_rect = highscore_massage.get_rect(topleft=(width - offset+self.block_size, self.block_size))
        screen.blit(highscore_massage, highscore_rect)
        upnext_massage = self.font2.render('up next:', False, (250, 250, 250))
        upnext_rect = upnext_massage.get_rect(topleft=(self.block_size*14, self.block_size*8))
        screen.blit(upnext_massage, upnext_rect)

    def display_multi(self):
        if self.check_multi:
            victory_massage = self.font3.render('COMBO!', False, (250, 50,50))
            victory_rect = victory_massage.get_rect(topleft=(width - offset+int(self.block_size/3), self.block_size *2))
            screen.blit(victory_massage, victory_rect)

    def remove_multi(self):
        if self.check_multi:
            end_timer=pygame.time.get_ticks()
            if end_timer-self.timer_start>2500:
                self.check_multi=False

    def game_over(self):
        for i in self.ground_shapes:
            if i.rect.y<self.block_size:
                self.check_game=False

    def pick_shape(self,color):
        if color == 'red':return self.red_shape
        if color == 'blue':return self.blue_shape
        if color == 'green':return self.green_shape
        if color == 'brown':return self.brown_shape
        if color == 'yellow':return self.yellow_shape
        if color == 'dark green':return self.darkgreen_shape
        if color == 'purple':return self.purple_shape

    def check_high_score(self):
        if int(self.score) > int(self.high_score):
            t = open("tetris highscore.txt", "w")
            t.write(str(self.score))
            t.close()
            self.high_score=self.score

    def end_screen(self):
        txt = self.font3.render('game over', False, (255, 255, 255))
        txt_rect = txt.get_rect(topleft=(width / 2-txt.get_width()/2, self.block_size*3))
        screen.blit(txt, txt_rect)

        score_txt = self.font.render('score:  ' + str(self.score), False, (255, 255, 255))
        score_rect = score_txt.get_rect(center=(width / 2, height / 2))
        screen.blit(score_txt, score_rect)

        highscore_txt = self.font.render('high score:  ' + str(self.high_score), False, (255, 255, 255))
        highscore_rect = score_txt.get_rect(topleft=(width / 2-highscore_txt.get_width()/2, height / 2 + self.block_size))
        screen.blit(highscore_txt, highscore_rect)

        restart_massage = self.font.render('PRESS R TO RESTART', False, (255, 255, 255))
        restart_rect = score_txt.get_rect(topleft=(width / 2 - restart_massage.get_width() / 2, height / 2 + self.block_size*6))
        screen.blit(restart_massage, restart_rect)

    def run(self):
        if self.check_game:
            self.movment()
            self.prediction.draw(screen)
            self.ground.draw(screen)
            self.up_next_shapes.draw(screen)
            self.ground_shapes.draw(screen)
            self.air_shapes.draw(screen)
            self.walls.draw(screen)
            self.rows.draw(screen)
            self.cols.draw(screen)
            self.check_hit_limits()
            self.check_hit_ground()
            self.check_hit_shape()
            self.check_side_collision()
            self.check_complete()
            self.predict_landing()
            self.up_next_list()
            self.display_score()
            self.speed_up()
            self.remove_multi()
            self.display_multi()
            self.check_high_score()
            self.game_over()
        else:self.end_screen()

def main():
    clock = pygame.time.Clock()
    game = Game()
    run=True
    tick=60

    while run:
        clock.tick(tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    game.move_right()
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    game.move_left()
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    game.rotate()
                if event.key==pygame.K_r:
                    run=False

        screen.fill((30,30,30))
        game.run()
        pygame.display.flip()

    main()


if __name__ == '__main__':
    main()
