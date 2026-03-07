def print_numbers_order():
     num = 1

     while num <= 10:
        print(num)
        num +=1

def print_numbers_reverse():
     num = 10

     while num >= 1:
        print(num)
        num -=1

def print_numbers_even():
    num = 1

    while num <= 100:
        if num % 2 == 0:
            print(num)
        num +=1

def print_numbers_odd():
    num = 1

    while num <= 100:
        if num % 2 != 0:
            print(num)
        num +=1

def print_tables():
    # Taking input from the user
    n = int(input("Enter a number: "))

    # Printing the multiplication table from n × 1 to n × 10
    print(f"\n--- Multiplication Table of {n} ---\n")

    i = 1
    while i <= 10:
        print(f"{n} * {i} = {n * i}")
        i += 1

def print_sum_of_n_numbers():
    # Taking input from the user
    n = int(input("Enter a number: "))

    # Initializing sum and counter
    total_sum = 0
    i = 1

    # Calculating the sum of first n natural numbers
    while i <= n:
        total_sum += i
        i += 1

    # Displaying the result
    print(f"\nThe sum of the first {n} natural numbers is: {total_sum}")

def sum_of_n_even():
    # Taking input from the user
    n = int(input("Enter a number: "))

    # Starting from 2 and incrementing by 2 (only even numbers)
    i = 2
    sum = 0

    while i <= n:
        sum = sum + i
        i += 2    # Jump by 2 (2, 4, 6, 8, 10...)

    print(f"\nSum of even numbers from 1 to {n} = {sum}")

def sum_of_n_odd():
    # Taking input from the user
    n = int(input("Enter a number: "))

    # Starting from 1 and incrementing by 2 (only odd numbers)
    i = 1
    sum = 0

    while i <= n:
        sum = sum + i
        i += 2    # Jump by 2 (1, 3, 5, 7, 9...)

    print(f"\nSum of odd numbers from 1 to {n} = {sum}")

#print_numbers_order()
#print_numbers_reverse()
#print_numbers_even()
#print_numbers_odd()
#print_tables()
#print_sum_of_n_numbers()
#sum_of_n_even()
sum_of_n_odd()
