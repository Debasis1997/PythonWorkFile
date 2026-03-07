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

#print_numbers_order()
#print_numbers_reverse()
#print_numbers_even()
#print_numbers_odd()
#print_tables()
print_sum_of_n_numbers()
