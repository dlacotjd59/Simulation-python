import math
import random
import time
import tkinter
import tkinter.ttk as ttk
from tkinter import *
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from drone import Drone

N_DRONES = 4
CANVAS_WIDTH = 850
CANVAS_HEIGHT = 751

PATH_IMG_DRONE = 'rsc/images/drone.png'
PATH_IMG_BUTTON = 'rsc/images/Button.png'
PATH_IMG_MAPTITLE = 'rsc/images/simulation_map_title.png'
PATH_IMG_MAP = 'rsc/images/MAP.png'


def load_resources(canvas: tkinter.Canvas):
    resources = {}
    resources['IMG_DRONE'] = tkinter.PhotoImage(file=PATH_IMG_DRONE)
    return resources


def create_drones(n_drones: int) -> List[Drone]:
    drones: List[Drone] = []
    for _ in range(n_drones):
        x = random.randint(0, CANVAS_WIDTH - 1)
        y = random.randint(0, CANVAS_HEIGHT - 1)
        drone = Drone(x, y, 4)
        drones.append(drone)

    return drones


#-----------------------------------------------------GUI 창 제작---------------------------------------------------------------
root = Tk()  #root = main창
root.title("Modeling Simulator")  # GUI 제목
root.geometry("1700x950+0+15") # 가로 * 세로 + 가로좌표 + 세로좌표 (화면에 띄울 크기 및 위치)
root.configure(bg='black')
#GUI 배경에 내가 원하는 이미지 넣어서 꾸며주기 

#입력칸 제작
label1 = Label(root, font=(13), fg="yellow", bg="black", text="map x direction : ")
label1.place(x=20, y=80)
text = Text(root, font=(13), fg="yellow", width=18, height=1, bg="black")  #글자를 적을수 있는 공간을 생성 : enter를 써서 여러줄 입력을해야할 때 쓰임
text.place(x=20, y=110)

label1 = Label(root, font=(13), fg="yellow", bg="black", text="map y direction : ")
label1.place(x=20, y=140)
text = Text(root, font=(13), fg="yellow", width=18, height=1, bg="black")  #글자를 적을수 있는 공간을 생성 : enter를 써서 여러줄 입력을해야할 때 쓰임
text.place(x=20, y=170)

values = [str(i) + "대" for i in range(1,6)]   #2. values에 넣어줄 항목들
combobox = ttk.Combobox(root, height=5, values=values, state="readonly")  #1. combobox를 만들고 values에 넣어줄 항목을 위에서 설정, state(상태)에서 readonly를 하면 항목작성x
combobox.set("dron의 수")  #3. combobox이름지정
combobox.place(x=20, y=220)

_is_charting_requested = False
def toggle_realtime_charting():
    global _is_charting_requested
    _is_charting_requested = not _is_charting_requested

_is_drone_simulation_requested = False
def toggle_drone_simulation():
    global canvas2
    global drones
    global _is_drone_simulation_requested
    
    state = 'normal' if not _is_drone_simulation_requested else 'hidden'
        
    for drone_img_id, _ in drones:
        canvas2.itemconfigure(drone_img_id, state=state)
        
    _is_drone_simulation_requested = not _is_drone_simulation_requested

#GUI 배경위에 버튼이나 label 씌워지는지 test한거
label3 = Label(root, font=(13), fg="yellow", bg="black", text="Realtime Chart Activate")
label3.place(x=20, y=360)
photo = PhotoImage(file=PATH_IMG_BUTTON) #이미지를 버튼으로 설정 ("파일저장한 폴더명/이미지의 이름.저장형식")
btn3 = Button(root, image=photo, command=toggle_realtime_charting)
btn3.place(x=20, y=400)  # 이 또한 grid, pack은 error나서 위치 지정이 안됨으로 place사용

label4 = Label(root, font=(13), fg="yellow", bg="black", text="Drone Simulation Activate")
label4.place(x=20, y=460)
btn4 = Button(root, image=photo, command=toggle_drone_simulation)
btn4.place(x=20, y=500)  #이 또한 grid, pack은 error나서 위치 지정이 안됨으로 place사용






#Realtime chart 제작
frame = LabelFrame(root, font=(20), bg="black", fg="white", text="model simulation result graph")
frame.place(x=300, y=91, width=370, height=760)

text1 = Label(frame, width=5, height=1, fg="yellow", bg="black", text="Run : ", relief="solid")
text1.place(x=80, y=350)
text2 = Label(frame, width=12, height=1, fg="yellow", bg="black", text="Current time : ", relief="solid")
text2.place(x=30, y=410)
text3 = Label(frame, width=17, height=1, fg="yellow", bg="black", text="Inter-visiting Time : ", relief="solid")
text3.place(x=6, y=470)
text4 = Label(frame, width=17, height=1, fg="yellow", bg="black", text="Cumulative Extent : ", relief="solid")
text4.place(x=5, y=530)
#fig = Figure(figsize = (5, 5), dpi = 55)

fig, ax = plt.subplots(figsize = (6, 6), facecolor='black', dpi = 55)  #하나의 ax를 가지는 하나의 figure 생성(ax의 색깔 지정 못함)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.2, 1.2)

plt.tick_params(axis='y', labelcolor='yellow')      #y축 색상
plt.tick_params(axis='x', labelcolor='yellow')      #x축 색상
ax.grid(color='lawngreen')                                   #그래프 눈금색상
ax.set_facecolor('black')                          #그래프 배경 색상

x, y = [], []
line, = ax.plot([], [], 'yellow')                  #선그래프 색상

canvas = FigureCanvasTkAgg(fig, master = frame)  
canvas.draw()
canvas.get_tk_widget().pack()


      



#가운데 지도 표시
photo3 = PhotoImage(file = PATH_IMG_MAPTITLE) #이미지도 할당 가능
label3 = Label(root, image=photo3)
label3.place(x=1000, y=45)
img1 = PhotoImage(file = PATH_IMG_MAP)
canvas2 = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,  bg="black")
canvas2.place(x=700, y=95)
canvas2.create_image(1, 1, anchor = "nw", image=img1)



root.resizable(False, False)  # GUI 창의 크기 변경 불가 (x축, y축)
#-------------------------------------------------------------------------------------------------------------------------------
rscs = load_resources(canvas2)

drones = create_drones(N_DRONES)
drones = [(canvas2.create_image(drone.x, drone.y, image=rscs['IMG_DRONE']), drone)
           for drone in drones]
for drone_img_id, _ in drones:
    canvas2.itemconfigure(drone_img_id, state='hidden')

frame_index = 0
prev_frame_time = time.time()
total_running_time = 0.
while True:
    dt = time.time() - prev_frame_time
    prev_frame_time += dt
    total_running_time += dt

    if _is_charting_requested:
        x_bound = int(total_running_time * 10)
        if 0 < frame_index:
            x = np.linspace(0., x_bound, frame_index)
            y = np.sin(x * (np.pi / 180))
            ax.set_xlim([0, x[-1]])
            ax.set_ylim([min(y), max(y)])
            line.set_data(x, y)
            fig.canvas.draw()
            fig.canvas.flush_events()

    if _is_drone_simulation_requested:
        for drone_img_id, drone in drones:
            theta = 2 * math.pi * random.random()
            v = [math.cos(theta), math.sin(theta)]
            v[0] *= drone.speed
            v[1] *= drone.speed
            drone.x += v[0]
            drone.y += v[1]
            canvas2.moveto(drone_img_id, drone.x, drone.y)
            # (x, y) 좌표에 사각형 그리기 
            rectangle = canvas2.create_rectangle(0,0,45,45,fill="lightgreen", outline="lightgreen")
            canvas2.moveto(rectangle, drone.x, drone.y)
            canvas2.moveto(drone_img_id, drone.x, drone.y)
            rectangle = canvas2.tag_raise(rectangle)
            drone = canvas2.tag_raise(drone_img_id)
    root.update()
    time.sleep(0.01)
    frame_index += 1