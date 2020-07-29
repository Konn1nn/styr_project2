import sys


class Node:
    def __init__(self, cont, next_node=None):
        self.cont = cont
        self.next = next_node


class LinkedList:
    def __init__(self, first_item=None):
        self.size = 0
        if first_item != None:
            first_item = Node(first_item)
            self.size += 1
        self.head = first_item
        self.tail = first_item
        self.capacity = 16

    def append(self, new_item):
        new_item = Node(new_item)
        if self.head == None and self.tail == None:
            self.head = new_item
            self.tail = new_item
        else:
            self.tail.next = new_item
            self.tail = new_item
        self.size += 1

    def remove(self):
        if self.head == None and self.tail == None:
            pass
        elif self.head.next == None:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        self.size -= 1

    def move_back(self):
        if self.head == None and self.tail == None or self.head.next == None:
            pass
        else:
            self.tail.next = self.head
            self.tail = self.tail.next
            self.head = self.head.next
            self.tail.next = None

    def __len__(self):
        return self.size


pm = []
for i in range(524288):
    pm.append(None)
disk = []
for i in range(1024):
    disk.append([])
frames = [0, 1]


def print_pm():
    temp_list = []
    for i in range(len(pm)):
        if pm[i] != None:
            temp_list.append([i, pm[i]])
    print(temp_list)


def print_disk():
    temp_list = []
    for i in disk:
        if i != []:
            temp_list.append([disk.index(i), i])
    print(temp_list)


def initalize(init_file):
    counter = 0
    line1 = None
    line2 = None
    for line in init_file:
        if counter == 0:
            line1 = line
        elif counter == 1:
            line2 = line
        counter += 1
    line1_list = line_to_list(line1)
    init_line1(line1_list)
    line2_list = line_to_list(line2)
    init_line2(line2_list)


def init_line1(line_list):
    s = None
    z = None
    f = None
    for line in line_list:
        s = line[0]
        z = line[1]
        f = line[2]
        pm[s*2] = z
        pm[s*2+1] = f
        if f >= 0:
            frames.append(f)


def init_line2(line_list):
    s = None
    p = None
    f = None
    for line in line_list:
        print_pm()
        s = line[0]
        p = line[1]
        f = line[2]
        if pm[s*2+1] < 0:
            disk[abs(pm[2*s+1])].append(f)
        else:
            pm[pm[s*2+1]*512+p] = f
        if f >= 0:
            frames.append(f)


def line_to_list(line):
    line_list = line.split()
    val1 = None
    val2 = None
    val3 = None
    ret_list = []
    for i in range(0, len(line_list), 3):
        val1 = int(line_list[i])
        val2 = int(line_list[i+1])
        val3 = int(line_list[i+2])
        ret_list.append([val1, val2, val3])
    return ret_list


def get_va(input_file):
    my_list = []
    line_list = None
    for line in input_file:
        line_list = line.split()
        for i in line_list:
            my_list.append(int(i))
    return my_list


def derive_va(my_list):
    var1FF = int('111111111', 2)
    var3FFF = int('111111111111111111', 2)
    s = None
    p = None
    w = None
    pw = None
    ret_list = []
    for va in my_list:
        s = va >> 18
        w = va & var1FF
        p = (va >> 9) & var1FF
        pw = va & var3FFF
        ret_list.append([s, p, w, pw])
    return ret_list


def va_translation(va_list):
    s = None
    p = None
    w = None
    pw = None
    pa = None
    for va in va_list:
        print_pm()
        print_disk()
        s = va[0]
        p = va[1]
        w = va[2]
        pw = va[3]
        if pw >= pm[2*s]:
            print('-1')
            return
        test_var = pm[2*s+1]
        if pm[2*s+1] < 0:
            new_frame = get_new_frame()
            for i in range(len(disk[abs(pm[2*s+1])])):
                pm[new_frame*512+i] = disk[abs(pm[2*s+1])][i]
            pm[2*s+1] = new_frame
            frames.append(new_frame)
        test_var2 = pm[pm[2*s+1]*512+p]
        if pm[pm[2*s+1]*512+p] < 0:
            new_frame2 = get_new_frame()
            # pm[new_frame2*512] = abs(pm[pm[2*s+1]*512+p])
            pm[pm[2*s+1]*512+p] = new_frame2
            frames.append(new_frame2)
            print_pm()
        pa = pm[pm[2*s+1]*512+p]*512+w
        print(pa)


def get_new_frame():
    for i in range(1000):
        if i not in frames:
            return i


if __name__ == "__main__":
    init_file = open('init_dp.txt', 'r')
    initalize(init_file)
    input_file = open('input_dp.txt', 'r')
    va_list = get_va(input_file)
    print_pm()
    va_derived_list = derive_va(va_list)
    original_stdout = sys.stdout
    output = open('output.txt', 'w+')
    sys.stdout = output
    va_translation(va_derived_list)
    print_pm()
    for i in range(len(pm)):
        print(i, ', ', pm[i])
    sys.stdout = original_stdout
