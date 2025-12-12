#Calculate the area of a circle (radius given by user).
radius = float(input("Enter the radius of the circle: "))
area = 3.14159 * radius ** 2
print("The area of the circle is:", area)

# Convert temperature from Celsius to Fahrenheit.
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = (celsius * 9/5) + 32 
print("Temperature in Fahrenheit:", fahrenheit)

# Input the number of days and convert it into years, weeks, days.
days = int(input("Enter number of days: "))
years = days//365
weeks = (days % 365)//7
days_remaining = (days % 365) % 7
print(f"{days} days is approximately {years} years, {weeks} weeks, and {days_remaining} days.")

# Swap two numbers without using a third variable.
a = int(input("Enter first number (a): "))
b = int(input("Enter second number (b): "))
a = a + b
b = a - b  
a = a - b
print("After swapping: a =", a, ", b =", b)