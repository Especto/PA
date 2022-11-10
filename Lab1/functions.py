from classes import Binary
import random


def generate(amount):
    file = Binary("numbers", "w+b")
    full = amount // 65536
    for i in range(full):
        file.set_ints32(i * 65536, [random.randint(0, 10000000) for i in range(65536)])
    for i in range(full * 65536, amount):
        file.set_int32(i, random.randint(0, 10000000))
    print("Готово")


def reader():
    file = Binary("numbers", "r+b")
    print("Кількість чисел в файлі: " + str(file.size))
    amount = int(input("Прочитати кількість чисел: \n"))
    nums = file.get_ints32(0, amount)
    for i in range(len(nums)):
        j = i
        print(f"{j}: {str(nums[i])}")

#generate(250000)
reader()