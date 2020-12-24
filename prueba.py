import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Invacion Zombie")
wn.setup(615,630)
wn.tracer(0)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        v=self.getscreen()
        self.color("white")
        self.penup()
        self.speed(0)


class Player(turtle.Turtle):

    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.sobreviviente = 0
        self.zombie = 2
        self.goto(x,y)
        self.direction = random.choice(["up","down","left","right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        #Checar si es una pared
        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        else:
            self.direction = random.choice(["up","down","left","right"])

        turtle.ontimer(self.move, t=random.randint(100,300))

    def is_collision(self,other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 5:
            return True
        else:
            return False


class Sobreviviente(turtle.Turtle):
    """docstring for obreviviente."""

    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.sobreviviente = 1
        self.goto(x,y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Zombie(turtle.Turtle):

    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("green")
        self.penup()
        self.speed(0)
        self.zombie = 1
        self.goto(x,y)
        self.direction = random.choice(["up","down","left","right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        #Checar si el personaje esta cerca
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        #Checar si es una pared
        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        else:
            self.direction = random.choice(["up","down","left","right"])

        turtle.ontimer(self.move, t=random.randint(100,300))

    def is_collision(self,other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 5:
            return True
        else:
            return False

    def is_close(self,other):
        a = self.xcor()-other.xcor()
        b = self.ycor()- other.ycor()
        distance = math.sqrt((a ** 2 )+(b **2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()



levels = [""]
level_1 = [
"XXXXXXXXXXXXXXXXXXXXX",
"XXX  Z XXXXXX  Z XXXX",
"X        P         XX",
"X                  XX",
"X  P  P    P   P   XX",
"X XXXXXX  XXXXXXX  XX",
"X   P         X    XX",
"X             X P  XX",
"X P    P      X    XX",
"X  P             P XX",
"X          P       XX",
"XXXXXXXXX   XXXXXXXXX",
"X                  XX",
"X XXXXXX    XP  X  XX",
"X  P        X   XP XX",
"X      P    X   X  XX",
"X         P X   X   S",
"X XXXXXX            S",
"X P   P     P       S",
"X                   S",
"XXXXXXXXXXXXXXXXXXXXX",
]

sobrevivientes = []
zombies = []
players = []

levels.append(level_1)

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level [y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x,screen_y)
                pen.stamp()
                #Agregar cordenadas de la paredes
                walls.append((screen_x,screen_y))

            if character == "P":
                players.append(Player(screen_x,screen_y))

            if character == "S":
                sobrevivientes.append(Sobreviviente(screen_x, screen_y))

            if character == "Z":
                zombies.append(Zombie(screen_x, screen_y))

pen = Pen()
#]player = Player()

# Lista de cordenadas de paredes
walls = []


setup_maze(levels[1])
#print (walls)

#turtle.listen()
#turtle.onkey(player.go_left,"Left")
#turtle.onkey(player.go_right,"Right")
#turtle.onkey(player.go_up,"Up")
#turtle.onkey(player.go_down,"Down")

wn.tracer(0)

for zombie in zombies:
    turtle.ontimer(zombie.move, t=250)

for player in players:
    turtle.ontimer(player.move, t=10)



while True:
    for sobreviviente in sobrevivientes:
        if player.is_collision(sobreviviente):
                player.sobreviviente += sobreviviente.sobreviviente
                print ("Sobreviviente: {}".format(player.sobreviviente))
                sobreviviente.destroy()


    for zombie in zombies:
        if player.is_collision(zombie):
            player.zombie += zombie.zombie
            print ("Zombie: {}".format(player.zombie))

            #wn.update()
    wn.update()
