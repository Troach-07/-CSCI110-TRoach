import sys


# Convert all whitespace-separated input values to integers.
values = iter(map(int, sys.stdin.read().split()))
# Read the number of classes to process.
test_cases = next(values)
results = []

for _ in range(test_cases):
    # Read the class size and all of the students' grades.
    class_size = next(values)
    grades = [next(values) for _ in range(class_size)]

    # Calculate the class average and count grades strictly above it.
    average = sum(grades) / class_size
    above_average = sum(grade > average for grade in grades)

    # Convert the count to a percentage and keep exactly three decimals.
    percentage = above_average * 100 / class_size
    results.append(f"{percentage:.3f}%")

# Print one result per class.
print("\n".join(results))