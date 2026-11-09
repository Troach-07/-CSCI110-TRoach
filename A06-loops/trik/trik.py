# Read the sequence of cup swaps.
s = input().strip()

# The ball starts under cup 1.
pos = 1

# Follow each swap and update which cup hides the ball.
for ch in s:
    # Swap cups 1 and 2.
    if ch == 'A':
        if pos == 1:
            pos = 2
        elif pos == 2:
            pos = 1
    # Swap cups 2 and 3.
    elif ch == 'B':
        if pos == 2:
            pos = 3
        elif pos == 3:
            pos = 2
    # Swap cups 1 and 3.
    elif ch == 'C':
        if pos == 1:
            pos = 3
        elif pos == 3:
            pos = 1

# Print the cup that contains the ball.
print(pos)