from classes import Binary
import math
import time

cache_size = 4096

class Run:
    def __init__(self, start, length, bin_file):
        self.start = start
        self.length = length
        self.pos = 0
        self.bin_file = bin_file

    def prepare(self):
        if self.length > 0:
            self.has_more = True
            self.cache = self.bin_file.get_ints32(self.start, min(cache_size, self.length))
            self.cache_pos = 0
            self.value = self.cache[0]
        else:
            self.has_more = False
            self.cache = []
            self.cache_pos = 0
            self.value = 0

    def next(self):
        self.pos += 1
        self.cache_pos += 1
        if self.pos < self.length:
            if self.cache_pos >= cache_size:
                self.cache = self.bin_file.get_ints32(self.start + self.pos, min(cache_size, self.length))
                self.cache_pos = 0
            self.value = self.cache[self.cache_pos]
            return self.value
        else:
            self.has_more = False
            return 0


def sort(file_count, run_size):
    binf = Binary("numbers", "r+b")
    start = time.time()

    input_files = []
    input_file_runs = []
    output_file = Binary("file0", "w+b")
    output_file_runs = []
    for i in range(1, file_count):
        input_files.append(Binary("file"+str(i), "w+b"))
        input_file_runs.append([])

    distributions = [1] * len(input_files)
    current_size = len(input_files)
    target_size = math.ceil(binf.size / run_size)
    total_switches = 0
    while current_size < target_size:
        print(distributions)
        total_switches += 1
        max_val = -1
        max_i = 0
        for i in range(len(distributions)):
            if distributions[i] > max_val:
                max_val = distributions[i]
                max_i = i
        for i in range(len(distributions)):
            if i != max_i:
                distributions[i] += max_val
                current_size += max_val
    print("\nРозподіл: "+str(distributions))
    print("Пустих серій: "+str(current_size - target_size))

    write_file_pos = [0] * len(input_files)
    write_to_files = [x for x in range(len(input_files))]
    distr = [distributions[x] for x in range(len(input_files))]
    write_to_file = 0
    write_to_file_idx = 0
    read_pos = 0
    runs_written = 0

    while read_pos < binf.size:
        ints = binf.get_ints32(read_pos, run_size)
        ints.sort()
        input_files[write_to_file].set_ints32(write_file_pos[write_to_file], ints)
        input_file_runs[write_to_file].append(Run(write_file_pos[write_to_file], len(ints), input_files[write_to_file]))
        distr[write_to_file_idx] -= 1
        if distr[write_to_file_idx] < 1:
            write_to_files.pop(write_to_file_idx)
            distr.pop(write_to_file_idx)
            write_to_file_idx -= 1
        read_pos += run_size
        write_file_pos[write_to_file] += run_size
        if len(write_to_files) > 0:
            write_to_file_idx = (write_to_file_idx + 1) % len(write_to_files)
            write_to_file = write_to_files[write_to_file_idx]
        runs_written += 1

    for i in range(current_size - target_size):
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

    sorting = True
    output_pos = 0
    switches = 0
    while sorting:
        output_start = output_pos
        cache = []
        cache_pos = output_pos
        files = []
        values = []
        for i in range(len(input_files)):
            if len(input_file_runs[i]) > 0:
                input_file_runs[i][0].prepare()
                if input_file_runs[i][0].has_more:
                    files.append(input_file_runs[i][0])
                    values.append(input_file_runs[i][0].value)
        while len(values) > 1:
            min_val = min(values)
            min_i = values.index(min_val)
            cache.append(min_val)
            if len(cache) == cache_size:
                output_file.set_ints32(cache_pos, cache)
                cache = []
                cache_pos = cache_pos + cache_size
            run = files[min_i]
            run.pos += 1
            run.cache_pos += 1
            if run.pos < run.length:
                if run.cache_pos >= cache_size:
                    run.cache = run.bin_file.get_ints32(run.start + run.pos, min(cache_size, run.length - run.pos))
                    run.cache_pos = 0
                values[min_i] = run.value = run.cache[run.cache_pos]
            else:
                values.pop(min_i)
                files.pop(min_i)

        if len(cache) > 0:
            output_file.set_ints32(cache_pos, cache)
            cache_pos += len(cache)

        if len(values) == 1:
            run = files[0]
            run.pos += 1
            while run.length - run.pos > 0:
                ints = run.bin_file.get_ints32(run.start + run.pos, min(cache_size, run.length - run.pos))
                run.pos += cache_size
                output_file.set_ints32(cache_pos, ints)
                cache_pos += len(ints)
        output_pos = cache_pos

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

        if switch_to_count == len(input_files):
            sorting = False
        elif switch_to > -1:
            switches += 1
            print("["+str(switches)+"/"+str(total_switches)+"]")
            output_file, input_files[switch_to] = input_files[switch_to], output_file
            output_file_runs, input_file_runs[switch_to] = input_file_runs[switch_to], output_file_runs
            output_pos = 0


    for i in range(output_file_runs[0].length):
        binf.set_int32(i, output_file.get_int32(i))
    for inf in input_files:
        inf.delete()
    output_file.delete()

    print(f"Час виконання: {str(time.time() - start)}")


def main():
    global cache_size
    file_count = int(input("Кількість файлів: "))
    sort(file_count, 100)


main()
