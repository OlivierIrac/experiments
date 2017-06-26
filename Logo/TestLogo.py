'''
Created on 8 juin 2017

@author: irac1
'''
import turtle
import random
maxAngle=45
minAngle=10
nbSteps=100
random.seed()
bob = turtle.Turtle()
wn = turtle.Screen()
bob.color("black")
#bob.speed(1000000000000000000000000)
wn.bgcolor("white")
while True:
    angle=random.randint(minAngle,maxAngle)
    bob.pencolor(random.random(),random.random(),random.random())
    for _ in range (0,nbSteps):
        bob.forward(1)
        bob.left(random.randint(-angle, angle))