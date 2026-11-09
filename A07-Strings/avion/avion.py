import sys


registrations = [line.strip() for line in sys.stdin]
cia_blimps = [
    str(row)
    for row, registration in enumerate(registrations, start=1)
    if "FBI" in registration
]

if cia_blimps:
    print(" ".join(cia_blimps))
else:
    print("HE GOT AWAY!")
