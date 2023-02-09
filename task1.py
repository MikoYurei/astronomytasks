L = [5, 4, 3, 2, 1]
for i in range(0, len(L)):
    for j in range(0, len(L)-i-1):
        if L[j+1] < L[j]:
            a = L[j]
            L[j] = L[j+1]
            L[j+1] = a
print("L = ", L)