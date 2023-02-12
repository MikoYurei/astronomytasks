import numpy as np
import matplotlib.pyplot as plt


#определение функции
def f(x):
    return 0.5*np.cos(x)

a = -5  #левая граница
c = -np.pi/2
d = np.pi/2
b = 5  #правая граница

#      Для интеграла
n = 5 #число разбиений
str_cycle = [a, c, d, b]
Summ = 0
graf = []
maXim = []
for i in range(1,len(str_cycle)):
    x = (str_cycle[i]-str_cycle[i-1])/n
    fa = f(str_cycle[i-1])
    fb = f(str_cycle[i])
    if str_cycle[i] != d:
        fa = 0
        fb = 0
    j = 1
    Sum = 0
    while(j < n):
        m = str_cycle[i-1] + j*x #значение х
        Sum = Sum + 2*f(m) #значение y
        j = j + 1
        if str_cycle[i] != d:
            Sum = 0
        graf.append(x*Sum/2+Summ)
        maXim.append(m)
    Summ = (fa + Sum + fb)*x/2

plt.plot(maXim, graf, '.-')
plt.show()