
import numpy as np
import scipy
import matplotlib.pyplot as plt
with open ('task2_data.dat', 'r') as f:
    old_data = f.read()
    new_data = old_data.replace('su hor', 'SU_Hor')
    new_data = old_data.replace('SU Hor', 'SU_Hor')
    new_data = old_data.replace("RZ Lyr", 'RZ_Lyr')
    new_data = old_data.replace("rzlyr", 'RZ_Lyr')
    new_data = old_data.replace("RZLyr", 'RZ_Lyr')
    new_data = old_data.replace('b', 'B')
    new_data = old_data.replace('v', 'V')
with open ('task2_data.dat', 'w') as f:
  f.write(new_data)


f = open('task2_data.dat', 'r')
line_table = f.readlines() #чтение из файла

column_obj = [] #новый список для названий
column_filt, column_hjd, column_magn = [], [], []
for line in line_table:
    column_obj.append(line.split("   ")[0])

    column_hjd.append(line.split("    ")[1])
    column_filt.append(line.split("    ")[2])
    column_magn.append(line.split("     ")[2])

del column_filt[0], column_obj[0], column_hjd[0], column_magn[0]
column_filt = [x.strip(' ') for x in column_filt]
column_magn = [x.strip('\n') for x in column_magn]
column_magn = [x.strip(' ') for x in column_magn]
f.close()
print('objects:', column_obj)
print('filters:', column_filt)
print("magn", column_magn)

column_obj_norm = []
for i in column_obj:
    if i not in column_obj_norm:
        column_obj_norm.append(i)
print("Названия без дубликатов = ", column_obj_norm)

k = 0
for w in range (0, len(column_obj)):
    if column_obj[w] == "SU_Hor":
        k = k + 1
print(f"последний элемент SU_Hor находится на {k} позиции. С позиции {k+1} идут RZ_Lyr")

su_hor_filters = list(set(column_filt[:k]))
rz_lyr_filters = sorted(list(set(column_filt[k:])), key=str.lower)

catalog = column_obj_norm, [su_hor_filters, rz_lyr_filters]
for i in range(0, len(column_obj_norm)):
    print(f"В данной базе данных представлен объект {catalog[0][i]} в фильтрах {catalog[1][i]}")


for i in range (0, len(column_hjd)):
    w = float(column_hjd[i])
    w += 2400000
    column_hjd[i] = str(w)
print("hjd:", column_hjd)


date = []
  #перевод дат
for j in range (0, len(column_hjd)):
    # hjd = float(input('Введите юлианскую дату')) + 0.5
    hjd = float(column_hjd[j])+0.5
    jdn = int(hjd)
    time = hjd - jdn
    a = jdn + 32044
    b = (4*a + 3) // 146097
    c = a - (146097*b // 4)
    d = (4*c + 3)//1461
    e = c - (1461*d)//4
    m = (5*e + 2)//153
    day = e - (153*m + 2)//5 + 1
    month = m + 3 - 12 * (m//10)
    year = 100*b + d - 4800 + (m//10)

    h = time*24
    mins = (h-int(h))*60
    sec = (mins-int(mins))*60
    gd = f'{day}.{month}.{year} {int(h)}:{int(mins)}:{int(sec)}'
    date.append(gd)
print("date", date)


obj_name = input("Введите имя объекта: SU_Hor или RZ_Lyr")
new_file = open(f'{obj_name}.dat', 'w')
obj_filt = input("Введите фильтры: V, B, Ic")
fiils = obj_filt.split()
f0, f1, f2 = None, None, None
if len(fiils)==1:
    f0 = obj_filt
    new_file.write(f"Date\t\t\t\t HJD\t\t\t Magn in {f0}\n")
elif len(fiils) == 2:
    f0, f1 = fiils[0], fiils[1]
    new_file.write(f"Date\t\t\t\t HJD\t\t\t Magn in {f0}\t Magn in {f1}\n")
elif len(fiils)==3:
    f0, f1, f2 = fiils[0], fiils[1], fiils[2]
    new_file.write(f"Date\t\t\t\t HJD\t\t\t Magn in {f0}\t Magn in {f1}\t Magn in {f2}\n")
m0, m1, m2, jd, da = [], [], [], [], []

for i in range(0, len(column_obj)):
    if str(obj_name) == column_obj[i]:
        if column_filt[i] == f0:
            jd.append(column_hjd[i])
            m0.append(column_magn[i])
            da.append(date[i])
            m1.append(f'\t\t')
            m2.append(f'\t\t')
        elif column_filt[i] == f1:
            jd.append(column_hjd[i])
            m0.append(f'\t\t')
            da.append(date[i])
            m1.append(column_magn[i])
            m2.append(f'\t\t')
        elif column_filt[i] == f2:
            jd.append(column_hjd[i])
            m0.append(f'\t\t')
            da.append(date[i])
            m1.append(f'\t\t')
            m2.append(column_magn[i])

eins, zwei = [], []

for k in range (0, len(jd)):
    min_jd = min(jd)
    ind = jd.index(min_jd)
    new_file.write(f"{da[ind]}\t {min_jd}\t {m0[ind]}\t {m1[ind]}\t {m2[ind]}\n")
    eins.append(float(min_jd))
    zwei.append(float(m0[ind]))
    del jd[ind], da[ind], m0[ind], m1[ind], m2[ind]

new_file.close()
# mas = np.array([eins, zwei], dtype=float)


plt.plot(eins, zwei)
plt.show()