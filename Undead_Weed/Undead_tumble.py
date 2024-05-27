import pyglet
from random import randint

Win_W = 1200
Win_H = 675
Win = pyglet.window.Window(Win_W, Win_H)
PlayerBatch = pyglet.graphics.Batch()
EnemyBatch = pyglet.graphics.Batch()
BackgroundBatch = pyglet.graphics.Batch()
timer = 0
score = 0
alive = True

#default enemy class
class Ent():
    def __init__(self, x=400, y=200, spritesheet="Zombie.png", rows=1, columns=1, h=30, w=30):
        self.Vx = 0
        self.Vy = 0
        self.H = h
        self.W = w
        self.sprite_sheet = pyglet.resource.image(spritesheet)
        self.image_grid = pyglet.image.ImageGrid(self.sprite_sheet, rows=rows, columns=columns)
        self.ani = pyglet.image.Animation.from_image_sequence(self.image_grid, duration=0.3)
        self.sprite = pyglet.sprite.Sprite(self.ani, x,y, batch=EnemyBatch)
        self.sprite.scale = 1.7
        self.aabb = [self.sprite.x, self.sprite.x + self.W, self.sprite.y, self.sprite.y + self.H]

    def move(self):
        """Updates Ent.Form to new x,y position"""
        self.sprite.x += self.Vx
        self.sprite.y += self.Vy
        self.aabb = [self.sprite.x, self.sprite.x + self.W, self.sprite.y, self.sprite.y + self.H]

    def chase(self, targetx, targety, frames=40):
        source = pyglet.math.Vec2(self.sprite.x, self.sprite.y)
        target = pyglet.math.Vec2(targetx, targety)
        direction = target - source
        direction = direction.normalize() *frames
        self.Vx, self.Vy = direction

    def collide(self, other):
        xcol = False
        ycol = False
        """check if self aabb overlaps with other aabb"""
        if (other.aabb[0] <= self.aabb[0] <= other.aabb[1] or
                other.aabb[0] <= self.aabb[1] <= other.aabb[1]):
            xcol = True
            if (other.aabb[2] <= self.aabb[2] <= other.aabb[3] or
                    other.aabb[2] <= self.aabb[3] <= other.aabb[3]):
                ycol = True
        return xcol and ycol

#default Player class
class EntPlayer(Ent):
    def __init__(self, x=200, y=200, spritesheet="Tumbleweed.png", rows=1, columns=1, h=30, w=30):
        self.Vx = 0
        self.Vy = 0
        self.H = h
        self.W = w
        self.sprite_sheet = pyglet.resource.image(spritesheet)
        self.image_grid = pyglet.image.ImageGrid(self.sprite_sheet, rows=rows, columns=columns)
        self.ani = pyglet.image.Animation.from_image_sequence(self.image_grid, duration=0.3)
        self.sprite = pyglet.sprite.Sprite(self.ani, x,y, batch=PlayerBatch)
        self.sprite.scale = 1.3
        self.aabb = [self.sprite.x, self.sprite.x + self.W, self.sprite.y, self.sprite.y + self.H]
    

#enemy controller class
class EntController():
    def __init__(self):
        self.memberlist = []
        self.destructlist = []

    def createEnt(self, x=200, y=200, spritesheet="Zombie.png", rows=1, columns=1, h=35, w=40, vx=0, vy=0, scale=1.7):
        newEnt=Ent(x=x, y=y, spritesheet=spritesheet, rows=rows, columns=columns, h=h, w=w)
        newEnt.scale=scale
        newEnt.Vx = vx
        newEnt.Vy = vy
        self.memberlist.append(newEnt)

    def move(self):
        for i in self.memberlist:
            i.move()
            if i.sprite.x<0 or i.sprite.x>1200:
                self.destructlist.append(i)
            if i.sprite.y<0 or i.sprite.y>675:
                self.destructlist.append(i)
            

    def die(self):
        while self.destructlist:
            try:
                deadguy = self.destructlist.pop(0)
                self.memberlist.remove(deadguy)
                deadguy.sprite.delete()
                del deadguy
                pass
            except:
                pass

    def chase(self, x, y, frames=40):
        self.memberlist[-1].chase(x, y, frames)

    def collidePlayer(self, other):
        global alive
        global timer
        global score
        for i in self.memberlist:
            if i.collide(other):
                alive=False
                print(timer + score)

    def collideLine(self, other):
        global score
        """die when colliding with bullet"""
        for i in self.memberlist:
            for j in other.memberlist:
                #print(self.selfdestructlist, i.collide(j), j.collide(i))
                if j.collide(i):
                    self.destructlist.append(i)
                    score+=1
                


#class of lines for bullets
class line():
    def __init__(self, x1=100, y1=100, h=20, w=20):
        self.form = pyglet.shapes.Line(x1,y1,x1+w,y1+h, width=4, batch=PlayerBatch)
        self.Vx = 0
        self.Vy = 0
        self.aabb = [self.form.x, self.form.x + w, self.form.y, self.form.y + h]

    def move(self):
        self.form.x += self.Vx
        self.form.x2 = self.form.x + (self.Vx*2)

        self.form.y += self.Vy 
        self.form.y2 = self.form.y + (self.Vy*2)

        self.aabb = [self.form.x, self.form.x2,  self.form.y, self.form.y2]


    def chase(self, sourcex, sourcey, targetx, targety, frames=40):
        source = pyglet.math.Vec2(sourcex, sourcey)
        target = pyglet.math.Vec2(targetx, targety)
        direction = target - source
        direction = direction.normalize() *frames
        self.Vx, self.Vy = direction


    def collide(self, other):
        xcol = False
        ycol = False
        """check if self aabb overlaps with other aabb"""
        if (other.aabb[0] <= self.aabb[0] <= other.aabb[1] or
                other.aabb[0] <= self.aabb[1] <= other.aabb[1]):
            xcol = True
            if (other.aabb[2] <= self.aabb[2] <= other.aabb[3] or
                    other.aabb[2] <= self.aabb[3] <= other.aabb[3]):
                ycol = True
        return xcol and ycol





class lineController():
    def __init__(self):
        self.memberlist = []
        self.destructlist = []


    def create_line(self, x1=100, y1=100, x2=200, y2=200):
        new_line = line(x1, y1, x2, y2)
        self.memberlist.append(new_line)
        

    def move(self):
        for i in self.memberlist:
            i.move()
            if i.form.x<0:
                del i

    def chase(self, sourcex, sourcey, targetx, targety):
        self.memberlist[-1].chase(sourcex, sourcey, targetx, targety, 40)

    


#Creation of entities
        

player=EntPlayer(spritesheet="Tumbleweed.png")
gun = lineController()
horde = EntController()


#when key is pressed move player ent
@Win.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.A or symbol == pyglet.window.key.LEFT:
        player.Vx -= 3
    if symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
        player.Vx += 3
    if symbol == pyglet.window.key.W or symbol == pyglet.window.key.UP:
        player.Vy += 3
    if symbol == pyglet.window.key.S or symbol == pyglet.window.key.DOWN:
        player.Vy -= 3
        

@Win.event
def on_mouse_press(x, y, button, modifiers):
    gun.create_line(player.sprite.x + 15, player.sprite.y + 15, 0,0)
    gun.chase(player.sprite.x + 15, player.sprite.y + 15, x , y)


#when key is released stop moving player ent
@Win.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.A or symbol == pyglet.window.key.LEFT:
        player.Vx += 3
    if symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
        player.Vx -= 3
    if symbol == pyglet.window.key.W or symbol == pyglet.window.key.UP:
        player.Vy -= 3
    if symbol == pyglet.window.key.S or symbol == pyglet.window.key.DOWN:
        player.Vy += 3


def main_loop(dt):
    Win.clear()
    BackgroundBatch.draw()

    global timer
    timer += 1
    if alive:
        PlayerBatch.draw()
        player.move()
        gun.move()

        EnemyBatch.draw()
        horde.move()
        horde.collidePlayer(player)
        horde.collideLine(gun)
        horde.die()


    if timer % 60 == 0:
        # zombies walk to the left or right of the screem
        yrng = randint(0,2)
        ypos = 100 + (yrng * 225)
        xrng = randint(0,1)
        if xrng == False:
            xpos = 0
            xvel = 3
        if xrng == True:
            xpos = 1200
            xvel = -3
        horde.createEnt(x=xpos, y=ypos,vx=xvel, rows=2)

    if timer % 120 == 0:
        # Bones walk down from the top of the screen 
        xrng = randint(0,3)
        ypos = 675
        xpos = 100 + (300 * xrng)
        horde.createEnt(spritesheet="Bones.png", x=xpos, y=ypos, vy=-2, rows=2, h=40)

    if timer % 240 == 0:
        tpos = randint(1,4)
        if tpos == 1:
            xpos = 100
            ypos = 620
        elif tpos == 2:
            xpos = 1100
            ypos = 620
        elif tpos == 3:
            xpos = 100
            ypos = 0
        else:
            xpos = 1100
            ypos = 0

        horde.createEnt(spritesheet="Spook.png", x=xpos, y=ypos, w=30)
        horde.chase(player.sprite.x, player.sprite.y, 10)


pyglet.clock.schedule_interval(main_loop, 1 / 60)
pyglet.app.run()
