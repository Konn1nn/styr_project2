import sys


class Process:
    def __init__(self):
        self.pm = []
        for i in range(524288):
            self.pm.append(None)
        self.disk = []
        for i in range(1024):
            self.disk.append([])
        self.frames = [0, 1]

    def print_pm(self):
        temp_list = []
        for i in range(len(self.pm)):
            if self.pm[i] != None:
                temp_list.append([i, self.pm[i]])
        print(temp_list)

    def print_disk(self):
        temp_list = []
        for i in self.disk:
            if i != []:
                temp_list.append([self.disk.index(i), i])
        print(temp_list)

    def initalize(self, init_file):
        counter = 0
        line1 = None
        line2 = None
        for line in init_file:
            if counter == 0:
                line1 = line
            elif counter == 1:
                line2 = line
            counter += 1
        line1_list = self.line_to_list(line1)
        self.init_line1(line1_list)
        line2_list = self.line_to_list(line2)
        self.init_line2(line2_list)

    def init_line1(self, line_list):
        s = None
        z = None
        f = None
        for line in line_list:
            s = line[0]
            z = line[1]
            f = line[2]
            self.pm[s*2] = z
            self.pm[s*2+1] = f
            if f >= 0:
                self.frames.append(f)

    def init_line2(self, line_list):
        s = None
        p = None
        f = None
        for line in line_list:
            self.print_pm()
            s = line[0]
            p = line[1]
            f = line[2]
            if self.pm[s*2+1] < 0:
                self.disk[abs(self.pm[2*s+1])].append(f)
            else:
                self.pm[self.pm[s*2+1]*512+p] = f
            if f >= 0:
                self.frames.append(f)

    def line_to_list(self, line):
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

    def get_va(self, input_file):
        self.va_list = []
        line_list = None
        for line in input_file:
            line_list = line.split()
            for i in line_list:
                self.va_list.append(int(i))
        self.derive_va()

    def derive_va(self):
        var1FF = int('111111111', 2)
        var3FFF = int('111111111111111111', 2)
        s = None
        p = None
        w = None
        pw = None
        self.va_derived_list = []
        for va in self.va_list:
            s = va >> 18
            w = va & var1FF
            p = (va >> 9) & var1FF
            pw = va & var3FFF
            self.va_derived_list.append([s, p, w, pw])

    def translate(self, out_put_name):
        original_stdout = sys.stdout
        output = open(out_put_name, 'w+')
        sys.stdout = output
        self.va_translation()
        sys.stdout = original_stdout

    def va_translation(self):
        s = None
        p = None
        w = None
        pw = None
        pa = None
        for va in self.va_derived_list:
            # self.print_pm()
            # self.print_disk()
            s = va[0]
            p = va[1]
            w = va[2]
            pw = va[3]
            if pw >= self.pm[2*s]:
                print('-1', end=' ')
            else:
                test_var = self.pm[2*s+1]
                if self.pm[2*s+1] < 0:
                    new_frame = self.get_new_frame()
                    for i in range(len(self.disk[abs(self.pm[2*s+1])])):
                        self.pm[new_frame*512 +
                                i] = self.disk[abs(self.pm[2*s+1])][i]
                    self.pm[2*s+1] = new_frame
                    self.frames.append(new_frame)
                test_var2 = self.pm[self.pm[2*s+1]*512+p]
                if self.pm[self.pm[2*s+1]*512+p] < 0:
                    new_frame2 = self.get_new_frame()
                    # pm[new_frame2*512] = abs(pm[pm[2*s+1]*512+p])
                    self.pm[self.pm[2*s+1]*512+p] = new_frame2
                    self.frames.append(new_frame2)
                    # self.print_pm()
                pa = self.pm[self.pm[2*s+1]*512+p]*512+w
                # self.print_pm()
                print(pa, end=' ')

    def get_new_frame(self):
        for i in range(1000):
            if i not in self.frames:
                return i


def console():
    use_ans = input(
        "Do you want to run with(w), without(wo) demand paging or both(b)?: ")
    init_and_input_files = input(
        "Do you want to use init and input files? y/n: ")
    if init_and_input_files == 'y':
        if use_ans in ['wo', 'b']:
            p = Process()
            init_file = open(
                input("Init file name(without demand paging): "), 'r')
            input_file = open(
                input("Input file name(without demand paging): "), 'r')
            p.initalize(init_file)
            p.get_va(input_file)
            p.translate('output.txt')
        if use_ans in ['w', 'b']:
            p_dp = Process()
            init_dp_file = open(
                input("Init file name(with demand paging): "), 'r')
            input_dp_file = open(
                input("Input file name(with demand paging): "), 'r')
            p_dp.initalize(init_dp_file)
            p_dp.get_va(input_dp_file)
            p_dp.translate('output_dp.txt')


if __name__ == "__main__":
    console()
    # init_file = open('init_dp.txt', 'r')
    # initalize(init_file)
    # input_file = open('input_dp.txt', 'r')
    # va_list = get_va(input_file)
    # print_pm()
    # va_derived_list = derive_va(va_list)
    # original_stdout = sys.stdout
    # output = open('output.txt', 'w+')
    # sys.stdout = output
    # va_translation(va_derived_list)
    # print_pm()
    # for i in range(len(pm)):
    #     print(i, ', ', pm[i])
    # sys.stdout = original_stdout
