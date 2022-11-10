from classes import Binary, Run
import time


def sort(file_count):
	start = time.time()
	binf = Binary("numbers", "r+b")

	# Створення файлів

	input_files = []
	input_file_runs = []
	output_file = Binary("file0", "w+b")
	output_file_runs = []
	for i in range(1, file_count):
		input_files.append(Binary("file"+str(i), "w+b"))
		input_file_runs.append([])
	print("Створено "+str(file_count)+" тимчасових файлів.")
	print("-"*60)

	# Розрахунок розподілу
	current_size = len(input_files)
	distributions = [1] * current_size
	target_size = binf.size
	total_switches = 0
	while current_size < target_size:
		print(distributions)
		total_switches += 1
		max_val = -1
		max_i = 0
		for i in range(len(distributions)):  # Знайти найбільше
			if distributions[i] > max_val:
				max_val = distributions[i]
				max_i = i
		for i in range(len(distributions)):  # Додати до всіх інших
			if i != max_i:
				distributions[i] += max_val
				current_size += max_val
	print("-"*40)
	print("Розподіл: "+str(distributions))
	print("Всього серій: "+str(current_size))
	print("Пустих серій: "+str(current_size - target_size))
	print("-"*40)
	total_runs = current_size

	# Розбиття вхідного файлу в серії та розкладання їх по файлам

	write_file_pos = [0] * len(input_files)
	write_to_files = [x for x in range(len(input_files))]
	distr = [distributions[x] for x in range(len(input_files))]
	write_to_file = 0
	write_to_file_idx = 0
	read_pos = 0
	runs_written = 0
	while read_pos < binf.size:
		int = binf.get_int32(read_pos)
		input_files[write_to_file].set_int32(write_file_pos[write_to_file], int)
		input_file_runs[write_to_file].append(Run(write_file_pos[write_to_file], 1, input_files[write_to_file]))
		distr[write_to_file_idx] -= 1
		if distr[write_to_file_idx] < 1:
			write_to_files.pop(write_to_file_idx)
			distr.pop(write_to_file_idx)
			write_to_file_idx -= 1

		read_pos += 1
		write_file_pos[write_to_file] += 1
		write_to_file_idx = (write_to_file_idx + 1) % len(write_to_files)
		write_to_file = write_to_files[write_to_file_idx]
		runs_written += 1

	while runs_written < total_runs:
		input_file_runs[write_to_file].append(Run(write_file_pos[write_to_file], 0, input_files[write_to_file]))
		distr[write_to_file_idx] -= 1
		if distr[write_to_file_idx] < 1:
			write_to_files.pop(write_to_file_idx)
			distr.pop(write_to_file_idx)
			write_to_file_idx -= 1

		if len(write_to_files) > 0:
			write_to_file_idx = (write_to_file_idx + 1) % len(write_to_files)
			write_to_file = write_to_files[write_to_file_idx]
		runs_written += 1

	# Злиття
	sorting = True
	output_pos = 0
	switches = 0
	while sorting:
		has_more = True
		output_start = output_pos
		while has_more:
			min_i = -1
			min_val = 9999999
			for i in range(len(input_files)):
				if len(input_file_runs[i]) > 0 and input_file_runs[i][0].has_more:
					value = input_file_runs[i][0].value
					# print(" Перевіряємо значення: "+str(value))
					if value < min_val:
						min_val = value
						min_i = i
			if min_i > -1:
				# print("Мінімум: "+str(minVal))
				output_file.set_int32(output_pos, min_val)
				output_pos += 1
				input_file_runs[min_i][0].next()
				has_more = True
			else:
				has_more = False
		# print("Немає нічого")
		output_length = output_pos - output_start
		output_file_runs.append(Run(output_start, output_length, output_file))
		switch_to = -1
		switch_to_count = 0
		for i in range(len(input_files)):
			if len(input_file_runs[i]) > 0:
				input_file_runs[i].pop(0)
				if len(input_file_runs[i]) == 0:
					switch_to = i
					switch_to_count += 1

		if switch_to_count == len(input_files):  # Всі файли пусті - вийти
			sorting = False
		elif switch_to > -1:  # Один з файлів пустий - переключитись на нього
			switches += 1
			print("Переключення файлу ["+str(switches)+"/"+str(total_switches)+"]")
			output_file, input_files[switch_to] = input_files[switch_to], output_file
			output_file_runs, input_file_runs[switch_to] = input_file_runs[switch_to], output_file_runs
			output_pos = 0

	for i in range(output_file_runs[0].length):
		binf.set_int32(i, output_file.get_int32(i))
	for inf in input_files:
		inf.delete()
	output_file.delete()

	print("На виконання пійшло "+str(time.time() - start)+" секунд")


def main():
	file_count = int(input("Кількість файлів: "))
	sort(file_count)


main()
