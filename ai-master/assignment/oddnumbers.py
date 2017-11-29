numbers = [1,2,3,4,5,6,7,8,9,10,11,12]
oddnumbers = []

for num in numbers:
    if num % 2 != 0:
        oddnumbers.append(num)

print("The odd numbers are :", oddnumbers)
