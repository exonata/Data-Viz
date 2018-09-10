#libraries to import are setup here
import sys#main librarie for python
import os
import matplotlib.pyplot as plt#graphing library(matplotlib) link: https://matplotlib.org/
import glob #library used to search through files in a folder.


def main():
    dirname = sys.argv[1]
    filepath = dirname + '/*'
    for name in glob.glob(filepath):
        if not os.path.isfile(name):
            print("File path {} does not exist. Exiting...".format(filepath))  #
        outputdata = ""
        print("file name: ")
        print(name)
        if (name[-4:] == ".txt"):
            cnt = 0
            with open(name) as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    line = fp.readline()
                    int_data = format_txt(line)
                    if int_data[0] == 0:
                        outputdata = outputdata + str(int_data[1]) + "," + str(int_data[2]) + "," + str(int_data[3]) \
                                     + "," + str(int_data[3] - int_data[2]) + "," + str(int_data[4]) + "," +\
                                     str(int_data[4]) + "\n"
                        cnt += 1
            write_to_file(outputdata, name, filepath)


def init_log_file(filename, fileheader):
    f = open(filename, 'w')
    try:
        f.write(fileheader)
        print(filename)
    except Exception as e:
        print("Could not init log file error: ", e)
    finally:
        f.close()


def write_to_file(outputdata, name, filepath):
    errorCode = 0
    fileheader = "Time, Counts, LTA, Delta, Yaw, Pitch\n"
    nameBuff = processName(name)
    filename = filepath[:-1] + "binary_" + nameBuff + ".csv"
    init_log_file(filename, fileheader)
    file = open(filename, 'a')
    try:
        print("Writing to file")
        print(outputdata)
        for i in range(len(outputdata)):
            file.write(outputdata[i])
    except Exception as e:
        errorCode = 1
        print("Could not init log file error: ", e)
    finally:
        file.close()
    return errorCode

def format_txt(line):
    sep_line = line.split("_")
    errorcode = 0
    try:
        counts = int(sep_line[5]) * 256 + int(sep_line[6], 16)
        LTA = int(sep_line[7]) * 256 + int(sep_line[8], 16)
        yaw = float(sep_line[26])
        pitch = float(sep_line[27])
        time = float(sep_line[28])
    except:
        errorcode = 1

        yaw = ""
        pitch = ""
        time = ""
        counts = ""
        LTA = ""
    finally:
        return [errorcode, time, counts, LTA, yaw, pitch]


def processName(path):
    temp = path.split('\\')
    subpath = ""
    for i in range(0, len(temp) - 1):
        subpath = subpath + temp[i] + '/'
    print(subpath)
    filename = temp[len(temp) - 1]
    return filename[:-4]


if __name__ == '__main__':
   main()