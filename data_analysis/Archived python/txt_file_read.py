import sys
import os
import matplotlib.pyplot as plt
import glob



def main():
    dirname = sys.argv[1]
    filepath = dirname + '/*'
    print(filepath)
    for name in glob.glob(filepath):
       print(name)
       ranges = []
       time = []
       counts = []
       LTA = []
       delta = []
       yaw = []
       pitch = []
       if not os.path.isfile(name):
           print("File path {} does not exist. Exiting...".format(filepath))
           sys.exit()

       with open(name) as fp:
           line = fp.readline()
           cnt = 1
           while line:
               # print("Line {}: {}".format(cnt, line.strip()))
               line = fp.readline()
               int_data = format_txt(line)
               if int_data[0] == 0:
                   time.append(int_data[1])
                   counts.append(int_data[2])
                   LTA.append(int_data[3])
                   yaw.append(int_data[4])
                   pitch.append(int_data[5])
                   delta.append(int_data[3] - int_data[2])
                   cnt += 1
       ranges = find_pour_time(time, pitch)
       plotStuff(time, counts, LTA, yaw, pitch, ranges, delta, name, cnt)
    plt.show()


def find_pour_time(time, pitch):
    ranges = []
    inRange = False
    record = False
    for i in range(len(pitch)):
        if not inRange:
            if pitch[i] < -90.0:
                start = time[i]
                inRange = True
        else:
            if pitch[i] > -90.0:
                end = time[i]
                inRange = False
                ranges.append([start, end])
    return ranges


def format_txt(line):
    sep_line = line.split("_")
    errorcode = 0
    try:
        raw_counts = sep_line[5] + sep_line[6]
        raw_LTA = sep_line[7] + sep_line[8]
        yaw = float(sep_line[26])
        pitch = float(sep_line[27])
        time = float(sep_line[28])
        counts = int(raw_counts, 16)
        LTA = int(raw_LTA, 16)

    except:
        errorcode = 1
        yaw = ""
        pitch = ""
        time = ""
        counts = ""
        LTA = ""

    finally:
        return [errorcode, time, counts, LTA, yaw, pitch]


def plotStuff(time, counts, LTA, yaw, pitch, ranges, delta, name, cnt):
    plt.figure()
    plt.suptitle(name)

    plt.subplot(311)
    plt.plot(time, delta, 'b', label='Delta')
    plt.ylabel('Counts')
    plt.axis([time[0], time[-1], 0, 1250])
    for i in range(len(ranges)):
        if i == 0:
            plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label='Bottle inverted >90 deg')
        else:
            plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label=None)
    plt.legend(loc='upper right')

    plt.subplot(312)
    plt.plot(time, counts, 'r--', label='Counts')
    plt.plot(time, LTA, 'k', label='LTA')
    plt.ylabel('Counts')
    plt.axis([time[0], time[-1], 0, 1250])
    for i in range(len(ranges)):
        if i == 0:
            plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label='Bottle inverted >90 deg')
        else:
            plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label=None)
    # plt.title('Counts and LTA')
    plt.legend(loc='upper right')

    plt.subplot(313)
    plt.plot(time, yaw, 'b', label='Yaw')
    plt.plot(time, pitch, 'r', label='Pitch')
    plt.axis([time[0], time[-1],-200, 200])
    for i in range(len(ranges)):
        if i == 0:
            plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label='Bottle inverted >90 deg')
        else:
            plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label=None)
    # plt.title('Bottle pour angle', y=1.08)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angle of bottle (degrees)')
    plt.legend(loc='upper right')




if __name__ == '__main__':
   main()