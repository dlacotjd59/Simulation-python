import math
import pyautogui
import random
import time
import tkinter
from collections import namedtuple
from typing import List
import pyautogui as pg

N_DRONES = 10                       #생성할 드론의 수
CANVAS_WIDTH = 800                  #창의 가로 길이
CANVAS_HEIGHT = 800                 #창의 세로 길이


class Drone:

    def __init__(self, x, y, speed):        # x 위치, y 위치, spped
        self.x = x                          # self.x로 x를 할당
        self.y = y                          # self.y로 y를 할당
        self.speed = speed                  # self.speed로 speed를 할당

def load_resources(canvas: tkinter.Canvas):   #canvas를 tkinter.Canvas의 형태로 표현
    resources = {}                          #resource라는 dictionary에  resources['IMG_BACKGROUND']와 resources['IMG_DRONE'] 배열을 넣어줌
    resources['IMG_BACKGROUND'] = tkinter.PhotoImage(file="rsc/images/MAP.png")
    resources['IMG_DRONE'] = tkinter.PhotoImage(file="rsc/images/drone.png")
    return resources

def create_drones(n_drones: int) -> List[Drone]:   #인수 n_drones을 int타입으로 풀이, 함수create_drones의 반환값을 List[Drone]라는 것으로 풀이
    drones: List[Drone] = []   
    for _ in range(n_drones):
        x = random.randint(0, CANVAS_WIDTH - 1)
        y = random.randint(0, CANVAS_HEIGHT - 1)
        drone = Drone(x, y, 3)
        drones.append(drone)

    return drones


def main():
    root = tkinter.Tk()
    root.title("simulation")

    canvas = tkinter.Canvas(root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH,  bg="black")
    canvas.pack()

    resources = load_resources(canvas)

    canvas.create_image(0, 0, anchor = "nw",
                        image=resources['IMG_BACKGROUND'])
    root.update()
    
    drones = create_drones(N_DRONES)
    drones = [(canvas.create_image(drone.x, drone.y, image=resources['IMG_DRONE']), drone)
              for drone in drones]

    while True:
        for drone_img_id, drone in drones:
            
            theta = 2 * math.pi * random.random()
            v = [math.cos(theta), math.sin(theta)]
            v[0] *= drone.speed
            v[1] *= drone.speed
            drone.x += v[0]
            drone.y += v[1]
            rectangle = canvas.create_rectangle(0,0,45,45,fill="lightgreen", outline="lightgreen")
            canvas.moveto(rectangle, drone.x, drone.y)
            canvas.moveto(drone_img_id, drone.x, drone.y)
            rectangle = canvas.tag_raise(rectangle)
            drone = canvas.tag_raise(drone_img_id)

            
        root.update()
        time.sleep(0.01)

if __name__ == '__main__':
    main()
