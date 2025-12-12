'''
# Write a program to take a user's name and print “Hello, <name>!”.
name = input("Enter your name: ")
print(f"Hello, {name}!")

#Input two numbers and print their sum.
num1 = float(input("Entyer First number: "))
num2 = float(input("Enter Second number: "))
sum = num1 + num2
print(f"The sum of {num1} and {num2} is {sum}.")


#Take a number and print whether it is positive, negative, or zero.
number = float(input("Enter a number: "))
if number>0:
    print("The number is positive.")
elif number<0:
    print("The number is negative.")  
else:
    print("The number is zero.")
    

#Ask the user for age and print “You are an adult” or “You are a minor”.

age = int(input("Enter your age: "))
if age >=18:
    print("You are an adult.")
else:
    print("You are a minor.")
'''