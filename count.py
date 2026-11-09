print("need numbers")
user_input = input("Enter a number, or type 'quit': ").strip().lower()

if user_input == "quit":
    print("Goodbye!")
else:
    try:
        number = int(user_input)
    except ValueError:
        print("Please enter a valid number or 'quit'.")
    else:
        if number >= 1_000_000_000:
            formatted_number = number / 1_000_000_000
            suffix = "b"
        elif number >= 1_000_000:
            formatted_number = number / 1_000_000
            suffix = "m"
        elif number >= 1_000:
            formatted_number = number / 1_000
            suffix = "k"
        elif number >= 1:
            print(number)
        else:
            print("Number is out of range.")

        if number >= 1_000:
            rounded_number = f"{formatted_number:.1f}".rstrip("0").rstrip(".")
            print(f"{rounded_number}{suffix}")