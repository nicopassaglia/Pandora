import os
import time
import random
import string
import shutil
import re
from pandora.config import CAPTURE_FILTER_EXPRESSION, DISPLAY_FILTER_EXPRESSION, TSHARK_FIELDS, USE_VICTIM_IP_FROM_MAC
from pandora.utils.program import ProgramBase
#from pandora.utils import utils
from pandora.definitions import TEMP_PATH, HTTPREQS_PATH

class Tshark(ProgramBase):
    program = 'tshark'
    def __init__(self, tempath=TEMP_PATH, dirpath=HTTPREQS_PATH):
        super().__init__()
        self.tempath = tempath
        self.dirpath = dirpath
        self.name = 'actividad'
        self.extension = '.csv'
        self.filename = self.name + self.extension
        self.proc = None
        self.filehandler = None

    def create_tshark_command(self, interface, victim_ip):
        command = [self.program, "-i", interface]

        if CAPTURE_FILTER_EXPRESSION != "":
            command.append("-f")
            if USE_VICTIM_IP_FROM_MAC:
                filter_with_victim_ip = CAPTURE_FILTER_EXPRESSION + " and host " + victim_ip + ""
                command.append(filter_with_victim_ip)
            else:
                command.append(CAPTURE_FILTER_EXPRESSION)

        if DISPLAY_FILTER_EXPRESSION != "":
            command.append("-Y")
            command.append(DISPLAY_FILTER_EXPRESSION)

        command.append("-E")
        command.append("separator=,")
        command.append("-E")
        command.append("quote=d")
        command.append("-T")
        command.append("fields")
        for field in TSHARK_FIELDS:
            command.append("-e")
            command.append(field)

        return command

    def execute_command(self, interface, victim_ip):
        filepath = os.path.join(self.tempath, self.filename)
        command = self.create_tshark_command(interface, victim_ip)
        #command.extend(['>', filepath])
        #self.proc = self.pcaller.executeret(command)
        self.filehandler = open(filepath, "w")
        self.proc = self.pcaller.executeret(command, stdout=self.filehandler)
        #self.proc = self.pcaller.executeret(command, stdout=filepath)

    def restart_tshark(self, interface, victim_ip):
        self.kill_proc()
        self.close_file()
        #self.non_destructive_move()
        self.copy_fix()
        self.execute_command(interface, victim_ip)

    def kill_proc(self):
        self.proc.terminate()
        #self.proc.kill()
        self.proc.wait()

    def close_file(self):
        self.filehandler.close()

    def copy_fix(self):
        srcfilepath = os.path.join(self.tempath, self.filename)
        dstfilepath = os.path.join(self.dirpath, self.filename)
        while os.path.isfile(dstfilepath):
            randstr = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            dstfilepath = os.path.join(self.dirpath, self.name + randstr + self.extension)
        try:
            print(f"Copy and fix from {srcfilepath} to {dstfilepath}")
            with open(srcfilepath, 'r') as fhsrc:
                count = 0
                for line in fhsrc:
                    count +=1
                count -= 3
            if count > 0:
                with open(srcfilepath, 'r') as fhsrc:
                    with open(dstfilepath, 'w') as fhdst:
                        for line in fhsrc:
                            if line.find(" packets captured") == -1:
                                fhdst.write(line)
                            else:
                                wrongline = line
                                break
                        try:
                            line = fhsrc.readline()
                            wrongline = ''.join([wrongline, line])
                            replace_string = str(count) + " packets captured\n"
                            newline = wrongline.replace(replace_string, "")
                            fhdst.write(newline)
                        except AttributeError:
                            pass
                        for line in fhsrc:
                            fhdst.write(line)

        except OSError:
            pass

    def non_destructive_move(self):
        srcfilepath = os.path.join(self.tempath, self.filename)
        dstfilepath = os.path.join(self.dirpath, self.filename)
        if self.filehandler.closed:
            while os.path.isfile(dstfilepath):
                randstr = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                dstfilepath = os.path.join(self.dirpath, self.name + randstr + self.extension)
            for _ in range(1, 10):
                try:
                    shutil.move(srcfilepath, dstfilepath)
                    print(f"File {srcfilepath} moved successfully")
                    break
                except OSError:
                    time.sleep(1)




    # def execute_command(self, interface, victim_ip, timeout):
    #     file_path = os.path.join(self.dirpath, 'actividad.csv')

    #     command = self.create_tshark_command(interface, victim_ip)

    #     out = self.pcaller.runread(command, timeout)

    #     # Used to parse output and remove PACKETS CAPTURED string from it
    #     cant_paquetes = (out[0].count("\n")) - 3

    #     clean_output = out[0].replace(str(cant_paquetes) + " packets captured\n", "")

    #     output_splited = clean_output.split("\n")

    #     utils.array_to_csv(output_splited[3:], file_path)

    #     return out
  