import astropy.io.fits as pyfits
import astropy
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import *
import pylab
from tkinter import scrolledtext
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def click():
    global scidata, fig # X=730, Y=1890
    global сoord_x, coord_y, r_of_star
    global left_x, left_y, right_x, right_y
    global Z, exp
    source = entr1.get()
    coord_x = entr2.get()
    coord_y = entr3.get()
    r_of_star = entr4.get()
    r1_back = float(entr5.get())
    r2_back = float(entr6.get())
    hdulist = pyfits.open(f"{source}")
    hdulist.info()
    scidata = hdulist[0].data
    exp = hdulist[0].header['exptime']
    print("exp=", exp)
    hdulist.close()

    left_x = int(coord_x) - int(r2_back)
    right_x = int(coord_x) + int(r2_back)
    left_y = int(coord_y) - int(r2_back)
    right_y = int(coord_y) + int(r2_back)

    def ver_plot():
        damn = [row[int(coord_x)] for row in scidata]
        ver_Y = damn[left_y:right_y]
        ver_X = [i for i in range(left_y, right_y)]

        fig = Figure(figsize=(5, 5), dpi=70)
        plot1 = fig.add_subplot(111)
        plot1.plot(ver_X, ver_Y)
        plot1.set_xlim([left_y, right_y])
        canvas = FigureCanvasTkAgg(fig, master=star_window)
        canvas.draw()
        canvas.get_tk_widget().grid(column=1, row =7)


    def hor_plot():
        hor_X = [i for i in range(left_x, right_x)]
        hor_Y = scidata[int(coord_y)][int(left_x):int(right_x)]
        fig = Figure(figsize=(5,5), dpi=70)
        plot1 = fig.add_subplot(111)
        plot1.plot(hor_X, hor_Y)
        canvas = FigureCanvasTkAgg(fig, master=star_window)
        canvas.draw()
        canvas.get_tk_widget().grid(column=2, row =7)


    z_temp, Z = [], []
    # i = left_y
    # while i < right_y:
    for i in range(left_y, right_y):
        for k in range(left_x, right_x):
            z_temp.append(scidata[i][k])  # type = list
        z_arr = np.asarray(z_temp, dtype=int)  # type = ndarray
        Z.append(z_arr)
        z_temp = []
        i = i + 1
    Z = np.asarray(Z)

    x = [i for i in range(left_x, right_x)]
    y = [i for i in range(left_y, right_y)]
    X, Y = np.meshgrid(x, y)

    def d_plot():
        fig = plt.Figure(figsize=(5,5), dpi=70)
        # ax = plt.axes(projection='3d') #scatters
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='inferno')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        canvas = FigureCanvasTkAgg(fig, master=star_window)
        canvas.draw()
        canvas.get_tk_widget().grid(column=3, row =7)


    def back_pix():
        global circle
        summ_maj, summ_min = 0, 0
        length_min, length_maj = 0, 0
        for i in range(0, len(Z)):
            for k in range(0, len(Z)):
                if ((int(r2_back)-int(i))**2+(int(r2_back)-int(k))**2) < int(r2_back)**2:
                    summ_maj += Z[i][k]
                    length_maj += 1

        ot = int(r2_back)-int(r1_back)
        do = int(r2_back)+int(r1_back)
        for i in range(ot, do):
            for k in range(ot, do):
                if ((int(r2_back)-int(i))**2+(int(r2_back)-int(k))**2) < int(r1_back)**2:
                    summ_min += Z[i][k]
                    length_min += 1
        circle = (summ_maj-summ_min)/(length_maj-length_min)
        lblzach = Label(text=f'{circle}')
        lblzach.grid(column=1, row=12)

    def flex():
        summ_star, len_star = 0, 0
        ot = int(r2_back)-int(r_of_star)
        do = int(r2_back)+int(r_of_star)
        for i in range(ot, do):
            for k in range(ot, do):
                if ((int(r2_back)-int(i))**2+(int(r2_back)-int(k))**2) < int(r_of_star)**2:
                    summ_star += Z[i][k]
                    len_star += 1
        res = summ_star - len_star*circle
        res_in_sec = res/exp
        lblflux = Label(text=f"Суммарно {res}")
        lblflux2 = Label(text=f'В секунду {res_in_sec}')
        lblflux.grid(column=2, row=12)
        lblflux2.grid(column=2, row=13)

    btn2 = Button(star_window, text='Средний фон', command = back_pix)
    btn2.grid(row=10, column=1)

    btn3 = Button(star_window, text='Flux', command=flex)
    btn3.grid(row=10, column=2)

    var1, var2, var3 = IntVar(), IntVar(), IntVar()
    var1.set(1)
    c1 = Checkbutton(star_window, text='Vertical',
                     variable=var1, onvalue=1, offvalue=0,
                     command=ver_plot)
    c1.grid(column=1, row=6)

    var2.set(2)
    c2 = Checkbutton(star_window, text='Horizontal',
                     variable=var2, onvalue=1, offvalue=0,
                     command=hor_plot)
    c2.grid(column=2, row=6)

    var3.set(3)
    c3 = Checkbutton(star_window, text='3d',
                     variable=var3, onvalue=1, offvalue=0,
                     command=d_plot)
    c3.grid(column=3, row=6)



star_window = tk.Tk()
star_window.title(f"Взлом мира")
star_window.geometry('800x800')


lbl1 = Label(text='Введите путь')
lbl1.grid(column = 1, row = 1)
entr1 = Entry(text = 'Введите путь', bg='black', fg = 'white', width = 60)
entr1.grid(column = 2, row = 1)
entr1.insert(0, "C:/Users/Miko/PycharmProjects/task3/v523cas60s-001.fit")

lbl2 = Label(text='X')
lbl2.grid(column = 1, row = 2)
entr2 = Entry(width = 25)
entr2.grid(row = 2, column = 2)
entr2.insert(0, '730')

lbl3 = Label(text='Y')
lbl3.grid(column = 1, row = 3)
entr3 = Entry(width = 25)
entr3.grid(row = 3, column = 2)
entr3.insert(0, '1892')

lbl4 = Label(text='R of star')
lbl4.grid(column = 3, row = 2)
entr4 = Entry(width = 25)
entr4.grid(row = 2, column = 4)
entr4.insert(0, '4')

lbl5 = Label(text='R of back1')
lbl5.grid(column = 3, row = 3)
entr5 = Entry(width = 25)
entr5.grid(row = 3, column = 4)
entr5.insert(0, '5')

lbl6 = Label(text='R of back2')
lbl6.grid(column = 3, row = 4)
entr6 = Entry(width = 25)
entr6.grid(row = 4, column = 4)
entr6.insert(0, '8')



btn = Button(star_window, text="Принять", command=click)
btn.grid(row = 5, column = 1)



star_window.mainloop()
