import pygame as p
import random as rnd

p.init()

screen = p.display.set_mode((1280,720))

clock = p.time.Clock()


class Player(p.Rect):

    def __init__(self, x, y):
        super().__init__(x,y, 100,25) #arbitrary values TODO tweak
        #self.vx=0
        #self.speed=8

    def draw(self):
        p.draw.rect(screen, 'grey', self, 0)#fill
        p.draw.rect(screen, 'black', self, 1)#outline

    def update(self):
        #self.x += self.vx
        if self.x < 0:
            self.x=0
        if self.x + self.width > screen.get_width():
            self.x = screen.get_width()-self.width


class Ball(p.Rect):

    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = rnd.randint(0,4) * rnd.choice([1,-1])
        self.vy = rnd.randint(3,5)

    def draw(self):
        p.draw.ellipse(screen, 'black', self, 0)
        p.draw.ellipse(screen, 'grey', self, 1)

    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        if self.x<0:
            self.x=0
            self.vx*=-1
        elif self.x + self.width > screen.get_width():
            self.x=screen.get_width()-self.width
            self.vx*=-1
        if self.y<0:
            self.y=0
            self.vy*=-1
        elif self.y > screen.get_height()+5:
            self.y = screen.get_height()//2

class Brick(p.Rect):
    WIDTH = 80
    HEIGHT = 20

    def __init__(self, x, y):
        super().__init__(x, y, Brick.WIDTH, Brick.HEIGHT)
        self.color = (20+rnd.randint(0, 235), 20+rnd.randint(0, 235), 20+rnd.randint(0, 235))

    def draw(self):
        p.draw.rect(screen, self.color, self, 0, border_radius=8)
        p.draw.rect(screen, 'black', self, 1, border_radius=8)


bricks = []
for x in range(4, screen.get_width()-Brick.WIDTH, Brick.WIDTH+4):
    for y in range(0, 300, Brick.HEIGHT+4):
        bricks.append(Brick(x, y))

player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2-10, screen.get_height()/2+20, 20)


while True:
    # Process player inputs.
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            raise SystemExit
        # elif event.type == p.KEYDOWN:
        #      if event.key == p.K_a:# or event.key == p.K_LEFT:
        #          player.vx-=player.speed
        #      if event.key == p.K_d:# or event.key == p.K_RIGHT:
        #          player.vx+=player.speed
        # elif event.type == p.KEYUP:
        #      if event.key == p.K_a:# or event.key == p.K_LEFT:
        #          player.vx+=player.speed
        #      if event.key == p.K_d:# or event.key == p.K_RIGHT:
        #          player.vx-=player.speed


    # Do logical updates here.
    player.x=p.mouse.get_pos()[0]-player.width/2
    player.update()
    ball.update()
    if player.colliderect(ball):
        ball.vy*=-1
        ball.y = player.y - ball.width # perhaps sideways collision would look bete
        ball.vx+=((ball.x+ball.width/2)-(player.x+player.width/2))//12.5


    for brick in bricks:
        if ball.colliderect(brick):
            ball.vy*=-1
            bricks.remove(brick)


    screen.fill('white')  # Fill the display with a solid color

    # Render the graphics here.
    player.draw()
    ball.draw()

    for b in bricks:
        b.draw()


    p.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)