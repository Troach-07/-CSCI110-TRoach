s = input().strip()
pos = 1
for ch in s:
    if ch == 'A':
        if pos == 1:
            pos = 2
        elif pos == 2:
            pos = 1
    elif ch == 'B':
        if pos == 2:
            pos = 3
        elif pos == 3:
            pos = 2
    elif ch == 'C':
        if pos == 1:
            pos = 3
        elif pos == 3:
            pos = 1
print(pos)