import numpy as np
def reverse_matrix(mini_mas):
    #создание матрицы
    maxi_mas = np.zeros((len(mini_mas), 2*len(mini_mas)),dtype=float)
    for i in range(len(mini_mas)):
        for j in range(2*len(mini_mas)):
            if j>=len(mini_mas):
                if i == j-len(mini_mas):
                    maxi_mas[i][j]=1
            else:
                maxi_mas[i][j]=mini_mas[i][j]
    mas = maxi_mas

    #преобразование матрицы
    for i in range (0, len(mas)):
        a = mas[i][i]
        for j in range (2*len(mas)):
            mas[i][j] = mas[i][j]/a
        # print(mas)
        for k in range (i+1, len(mas)):
            b = mas[k][i]
            for j in range(2*len(mas)):
                mas[k][j]+=mas[i][j]*(-1)*b

    for i in range (len(mas)-1,0,-1):
        for k in range (i-1, -1, -1):
            b = mas[k][i]
            for j in range(2*len(mas)):
                mas[k][j]-=mas[i][j]*b #

    rev_mas = np.zeros((len(mini_mas), len(mini_mas)),dtype=float)
    for i in range (0,len(mas)):
        for j in range (0, len(mas)*2):
            if j>=len(mas):
                rev_mas[i][j-len(mas)] = mas[i][j]
    return(rev_mas)

#функция, находящая трансп матрицу
def transp_matrix(mini_mas):
    tr_mas = np.zeros((len(mini_mas), len(mini_mas)))
    for i in range(0, len(mini_mas)):
        for j in range(0, len(mini_mas)):
            tr_mas[i][j]=mini_mas[j][i]
    return(tr_mas)


#алгоритм для линейной регрессии
Y = np.array([[42000], [144000], [151000]])
print("Y = ", Y)
X = np.array([[2310, 2, 20], [2333, 2, 12], [2356, 3, 33]], dtype=float)
print("X = ", X)
rm = reverse_matrix(X)
print('X^(-1) = ', rm)
tm = transp_matrix(X)
print("X_tr = ", tm)
G = np.dot(X, rm)
temp = np.dot(tm, X)
temp_rev = reverse_matrix(temp)
meow = np.dot(temp_rev, tm)
B = np.dot(meow, Y)
print(f"Конечный результат \n B = ", B)

