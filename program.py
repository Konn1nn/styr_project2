# Author: Hákon Hákonarson(hakon19)

import sys


class Process:
    def __init__(self, debug=False):
        """Create the lists needed for this program"""
        self.pm = []
        for _ in range(524288):
            self.pm.append(None)
        self.disk = []
        for _ in range(1024):
            self.disk.append([None]*512)
        self.frames = [0, 1]
        self.debug = debug

    def print_pm(self):
        """Only for debugging"""
        if self.debug:
            temp_list = []
            for i in range(len(self.pm)):
                if self.pm[i] != None:
                    temp_list.append([i, self.pm[i]])
            print(temp_list)

    def print_disk(self):
        """Only for debugging"""
        if self.debug:
            temp_list = []
            for i in self.disk:
                if i != []:
                    temp_list.append([self.disk.index(i), i])
            print(temp_list)

    def initalize(self, init_file):
        """Takes the init file and places each item in the correct possition
        in the physical memory."""
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
        """Helper function for initalize that handles the top line in the 
        document."""
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
        """Helper function for initalize that handles the lower line in the 
        document."""
        s = None
        p = None
        f = None
        for line in line_list:
            self.print_pm()
            s = line[0]
            p = line[1]
            f = line[2]
            if self.pm[s*2+1] < 0:
                self.disk[abs(self.pm[2*s+1])][p] = f
            else:
                self.pm[self.pm[s*2+1]*512+p] = f
            if f >= 0:
                self.frames.append(f)

    def line_to_list(self, line):
        """Helper function for initalize to take the strings in the document
        and converting them into integers and seperate them in a list."""
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
        """This takes the virtual addresses in a string format from the 
        document and converts them to an integer and stores them in a list."""
        self.va_list = []
        line_list = None
        for line in input_file:
            line_list = line.split()
            for i in line_list:
                self.va_list.append(int(i))
        self.derive_va()

    def derive_va(self):
        """This function derives the virtual addresses into three parts to be
        worked with later."""
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
        """This is the function that starts the translations and makes sure
        that only prints from the translation go to a document."""
        original_stdout = sys.stdout
        output = open(out_put_name, 'w+')
        sys.stdout = output
        self.va_translation()
        sys.stdout = original_stdout

    def va_translation(self):
        """This function handles the translation of the VA and can handle
        demand paging."""
        s = None
        p = None
        w = None
        pw = None
        pa = None
        for va in self.va_derived_list:
            s = va[0]
            p = va[1]
            w = va[2]
            pw = va[3]
            if pw >= self.pm[2*s]:
                print('-1', end=' ')
            else:
                if self.pm[2*s+1] < 0:
                    new_frame = self.get_new_frame()
                    for i in range(len(self.disk[abs(self.pm[2*s+1])])):
                        self.pm[new_frame*512 +
                                i] = self.disk[abs(self.pm[2*s+1])][i]
                    self.pm[2*s+1] = new_frame
                    self.frames.append(new_frame)
                if self.pm[self.pm[2*s+1]*512+p] < 0:
                    new_frame2 = self.get_new_frame()
                    self.pm[self.pm[2*s+1]*512+p] = new_frame2
                    self.frames.append(new_frame2)
                pa = self.pm[self.pm[2*s+1]*512+p]*512+w
                print(pa, end=' ')

    def get_new_frame(self):
        """This function gets a new frame when something is moved from disk to
        physical memory"""
        for i in range(1000):
            if i not in self.frames:
                return i


def console():
    print("\nThis project does run demand paging so it should also handle tests without demand paging.")
    debug = input(
        "Do you want to run in debug mode?\n(Get printout of the addresses in PM and whats at that location.) y/n: ")
    p_dp = Process()
    if debug == 'y':
        p_dp.debug = True

    init_dp_file = input("Init file name(if empty 'init-dp.txt'): ")
    if init_dp_file == '':
        init_dp_file = 'init-dp.txt'
    init_dp_file = open(init_dp_file, 'r')

    input_dp_file = input("Input file name(if empty 'input-dp.txt'): ")
    if input_dp_file == '':
        input_dp_file = 'input-dp.txt'
    input_dp_file = open(input_dp_file, 'r')

    output_name = input("Output file name(if empty 'output-dp.txt'): ")
    if output_name == '':
        output_name = 'output-dp.txt'

    p_dp.initalize(init_dp_file)
    p_dp.get_va(input_dp_file)
    p_dp.translate(output_name)
    p_dp.print_pm()
    print('Done, your results are located in a file called: ' + output_name)


if __name__ == "__main__":
    console()
