# Check if a number is even or odd.
number = int(input("Enter the number: "))
if number % 2 == 0:
    print(f"{number} is even.")
else:
    print(f"{number} is odd.")
# Find the largest of three numbers.
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
num3 = int(input("Enter third number: "))
if num1 >= num2 and num1 >= num3:
    print(f"{num1} is the largest.")
elif num2 >= num1 and num2 >= num3:
    print(f"{num2} is the largest.")
else:
    print(f"{num3} is the largest.")

# Check if a year is a leap year.
year = int(input("Enter a year: "))
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")    




# Write a program to check if a person is eligible to vote (age ≥ 18).