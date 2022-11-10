import os


class Binary:
    def __init__(self, name, mode="r+b"):
        try:
            my_file = open(name, mode)
            self.my_file = my_file
            self.name = name
            my_file.seek(0, 2)
            self.size = my_file.tell() // 4
            self.ok = True
            self.closed = False
        except IOError:
            self.ok = False

    def get_int32(self, pos):
        self.my_file.seek(pos*4)
        arr = self.my_file.read(4)
        return ((arr[3]*256+arr[2])*256+arr[1])*256+arr[0]

    def get_ints32(self, pos, amount):
        self.my_file.seek(pos*4)
        arr = self.my_file.read(amount*4)
        outputs = []
        for i in range(0, len(arr), 4):
            outputs.append(((arr[i+3]*256+arr[i+2])*256+arr[i+1])*256+arr[i])
        return outputs

    def set_int32(self, pos, value):
        self.my_file.seek(pos*4)
        arr = []
        for i in range(4):
            arr.append(value % 256)
            value //= 256
        self.my_file.write(bytearray(arr))
        if pos+1 > self.size:
            self.size = pos+1

    def set_ints32(self, pos, values):
        self.my_file.seek(pos*4)
        arr = []
        for j in range(len(values)):
            value = values[j]
            for i in range(4):
                arr.append(value % 256)
                value //= 256
        self.my_file.write(bytearray(arr))

    def close(self):
        if not self.closed:
            self.my_file.close()
            self.closed = True

    def delete(self):
        if not self.closed:
            self.my_file.close()
            self.closed = True
        os.remove(self.name)


class Run:
    def __init__(self, start, length, bin_file):
        self.start = start
        self.length = length
        self.pos = 0
        self.bin_file = bin_file
        if length > 0:
            self.has_more = True
            self.value = bin_file.get_int32(start)
        else:
            self.has_more = False
            self.value = 0

    def next(self):
        self.pos += 1
        if self.pos < self.length:
            self.value = self.bin_file.get_int32(self.start + self.pos)
        else:
            self.has_more = False
