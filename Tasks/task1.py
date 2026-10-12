n=10
x=3
y=2
for i in range(n):
 if i%(x*y) == 0:
     print("A")
    elif i%x == 0:
     print("B")
    elif i%y == 0:
        print("C")
    else:
    print(i)
