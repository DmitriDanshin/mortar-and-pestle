import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import webbrowser

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
    import tkMessageBox
else:
    from tkinter import *
    import tkinter as Tk
    from tkinter import messagebox
from LightPipes import *
import math

root = Tk.Tk()
root.wm_title("Резонатор Фабри — Перо")
root.wm_protocol("WM_DELETE_WINDOW", root.quit)

wavelength = 512 * nm # Длина волны
size = 5 * mm # Масштаб
N = 300  # Количество шагов интегрирования

f = 100 * mm
r = 0.7
d = 6 * mm
Dlabda = 0.0
nmedium = 1.0
k = 2 * math.pi / wavelength

D = DoubleVar()
R = DoubleVar()
DLABDA = DoubleVar()
NMEDIUM = DoubleVar()

D.set(d / mm)
R.set(r)
DLABDA.set(Dlabda / nm)
NMEDIUM.set(nmedium)

fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v = StringVar()


def TheExample(event):
    global I
    Dlabda = DLABDA.get() * nm
    nmedium = NMEDIUM.get()
    d = D.get() * mm
    r = R.get()
    k2 = 2 * math.pi / (wavelength + Dlabda)

    F = Begin(size, wavelength, N)
    I = Intensity(1, F)
    step = size / N / mm
    for i in range(1, N):
        xray = i * step
        for j in range(1, N):
            yray = j * step
            X = xray * mm - size / 2
            Y = yray * mm - size / 2
            radius = math.sqrt(X * X + Y * Y)
            theta = radius / f
            delta2 = k * nmedium * d * math.cos(theta)
            Inten = 0.5 / (1 + (4.0 * r / (1.0 - r)) * math.pow(math.sin(delta2), 2))
            delta2 = k2 * nmedium * d * math.cos(theta)
            I[i][j] = (Inten + 0.5 / (1 + (4.0 * r / (1.0 - r)) * math.pow(math.sin(delta2), 2)))
    ax1.clear()
    ax1.imshow(I, cmap='gist_heat')
    ax1.axis('off')
    ax1.axis('equal')
    str = 'Распределение интенсивности'
    ax1.set_title(str)
    canvas.draw()


def motion(event):
    x = event.xdata
    y = event.ydata
    if x and y is not None and 0 < x < N and 0 < y < N:
        v.set('x=%3.2f mm, y=%3.2f mm\n I=%3.3f [a.u.]' % (
            (-size / 2 + x * size / N) / mm, (-size / 2 + y * size / N) / mm, I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')


def _quit():
    root.quit()


Scale(root,
      takefocus=1,
      orient='horizontal',
      label='Отражение зеркал',
      length=200, from_=0.0, to=0.99,
      resolution=0.01,
      variable=R,
      cursor="hand2",
      command=TheExample).pack()

Scale(root,
      takefocus=1,
      orient='horizontal',
      label='Расстояние между стёклами [mm]',
      length=200, from_=0.0, to=10.000,
      resolution=0.001,
      variable=D,
      cursor="hand2",
      command=TheExample).pack()


def cb():
    TheExample(0)


Checkbutton(root,
            text="Вставить среду между зеркалами",
            onvalue=1.73,
            offvalue=1.0,
            variable=NMEDIUM,
            cursor="hand2",
            command=cb).pack()

Checkbutton(root,
            text="Двойная длина волны",
            onvalue=1.8,
            offvalue=0.0,
            variable=DLABDA,
            cursor="hand2",
            command=cb).pack()

Button(root,
       width=24,
       text='Quit',
       cursor="hand2",
       command=_quit).pack(pady=10)

Label(root, textvariable=v).pack(pady=50)

cid = fig.canvas.mpl_connect('motion_notify_event', motion)

TheExample(0)
root.mainloop()
root.destroy()
