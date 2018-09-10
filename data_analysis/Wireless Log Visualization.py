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
               print("File path {} does not exist. Exiting...".format(filepath))#
       ranges = []
       time = []
       counts = []
       LTA = []
       delta = []
       yaw = []
       pitch = []
       if(name[-4:] == ".txt"):
           with open(name) as fp:
               line = fp.readline()
               cnt = 1
               while line:
                   line = fp.readline()
                   int_data = format_txt(line)
                   if int_data[0] == 0:
                       time.append(int_data[1]/1000)
                       counts.append(int_data[2])
                       LTA.append(int_data[3])
                       yaw.append(int_data[4])
                       pitch.append(int_data[5])
                       delta.append(int_data[3] - int_data[2])
                       cnt += 1
           ranges = find_pour_time(time, pitch)
           plotStuff(time, counts, LTA, yaw, pitch, ranges, delta, name)
    plt.show()



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 8/18                                                                                               
# Original Author: Renata Smith
# Last Editor: Renata Smith
#                                                                                                                     
# Function: find_pour_time()                                                                               	   
# Description: takes in the time and pitch array, and generates "range" data. This helps to serve as an aide for
# when we are looking for when the bottle should be detecting liquid, and when it shouldn't be detecting liquid.
# Parameters 0: [int?/flt?...]times in a time array, and a pitch(angle) array.
# Parameter 1:
# Return: 2d array that includes every range to highlight(all numbers) 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_pour_time(time, pitch):
    ranges = []
    inRange = False
    record = False
    for i in range(len(pitch)):
        if not inRange:
            if pitch[i] < -90.0:    #when the pitch is less than -90 degrees, then you generate the begining of the range
                start = time[i]     #sets start of the range. 
                inRange = True      #in range is true
        else:
            if pitch[i] > -90.0:
                end = time[i]
                inRange = False
                ranges.append([start, end])     #appends an array to an array(effectively a 2D array handling things)
    return ranges       #returns this newly minted array of data back into whatever called this function. 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 8/18                                                                                               
# Original Author: Renata Smith
# Last Editor: Renata Smith
#                                                                                                                     
# Function: format_txt()                                                                               	   
# Description:takes in a line(as a string) that is supposed to be extracted from a text file,
# and then outputs an array that separates and parses all the information
# Parameters: a line(string)
# Returns: Array that includes an error code(number), time(number), counts(number), LTA(number), yaw(number)
# and pitch(number)data, all the selected string file.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
        return [errorcode, time, counts, LTA, yaw, pitch]  #returns all the data back as an array.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 8/18                                                                                               
# Original Author: Renata Smith
# Last Editor: Renata Smith
#                                                                                                                     
# Function: plotStuff()                                                                               	   
# Description: graphs out data based off the time, counts, LTA< yaw and pitch graph data.  Saves png graph files, and generates interactive graph programs to allow us to analyze and process the data.
# Parameters: time array(number), counts array(number), LTA array(number), pitch array(number), ranges array(number), delta array(number), name of graph title.(String)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def plotStuff(time, counts, LTA, yaw, pitch, ranges, delta, name):
    nameBuff = processName(name)
    left = 0.06  # the left side of the subplots of the figure
    right = 0.96  # the right side of the subplots of the figure
    bottom = 0.1  # the bottom of the subplots of the figure
    top = 0.9  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for space between subplots,
    # expressed as a fraction of the average axis width
    hspace = 0.07  # the amount of height reserved for space between subplots,
    # expressed as a fraction of the average axis height
    thresholds = [32, 64, 256, 320]
    try:
        plt.figure()    #generates a new matplotlib figure object

        plt.suptitle(nameBuff)  #titles the grpah
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())

        plt1 = plt.subplot(311)
        plt.plot(time, delta, 'b', label='Delta')   #plots out the deltas onto a subplot, labels it as Delta
        plt.axhline(y=thresholds[0], color='g', linestyle='-', label="Programmable Thresholds")
        plt.axhline(y=thresholds[1], color='g', linestyle='-')
        plt.axhline(y=thresholds[2], color='g', linestyle='-')
        plt.axhline(y=thresholds[3], color='g', linestyle='-')
        for i in range(len(ranges)):    #goes through all the ranges, so it knows what to shade.
            if i == 0:
                plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label='Bottle inverted >90 deg')
            else:
                plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label=None)
        plt.axhline(y=thresholds[0], color='g', linestyle='-', label="Programmable Thresholds")
        plt.axhline(y=thresholds[1], color='g', linestyle='-')
        plt.axhline(y=thresholds[2], color='g', linestyle='-')
        plt.axhline(y=thresholds[3], color='g', linestyle='-')
        plt.ylabel('Counts')  # Labels the y axis as counts.
        plt.axis([time[0], time[-1], 0, 1250])
        plt.setp(plt1.get_xticklabels(), visible=False)
        plt.legend(loc='upper right')

        ############
        plt2 = plt.subplot(312)
        plt.plot(time, counts, 'r--', label='Counts')
        plt.plot(time, LTA, 'k', label='LTA')
        plt.ylabel('Counts')
        plt.axis([time[0], time[-1], 0, 1500])
        plt.setp(plt2.get_xticklabels(), visible=False)
        for i in range(len(ranges)):
            if i == 0:
                plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label='Bottle inverted >90 deg')
            else:
                plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label=None)
        # plt.title('Counts and LTA')
        plt.legend(loc='upper right')

        #############
        plt3 = plt.subplot(313)
        plt.axis([time[0], time[-1], -200, 200])
        plt.plot(time, yaw, 'b', label='Yaw')
        plt.plot(time, pitch, 'r', label='Pitch')
        for i in range(len(ranges)):
            if i == 0:
                plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label='Bottle inverted >90 deg')
            else:
                plt.axvspan(ranges[i][0], ranges[i][1], facecolor='b', alpha=0.2, label=None)
        # plt.title('Bottle pour angle', y=1.08)
        plt.xlabel('Time (seconds)')#
        plt.ylabel('Angle of bottle (degrees)')
        plt.legend(loc='upper right')
        plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top,
                        wspace=wspace, hspace=hspace)
        plt.tight_layout()
        plt.savefig(name[:-3] +"png")
        print("figure made")

    finally:
        print(name)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Date last modified: 8/18                                                                                               
# Original Author: Renata Smith
# Last Editor: Renata Smith
#                                                                                                                     
# Function: processName(name)                                                                           	   
# Description: takes in the file path, and output the name of the file. 
# Parameters: takes in the file path(string)
# Returns: Outputs the name of the file(string)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def processName(path):  
    temp =  path.split('\\')
    subpath = ""
    
    for i in range (0, len(temp)-1):
        subpath = subpath + temp[i] + '/'
    print(subpath)
    filename = temp[len(temp)-1]
    return filename[:-4]



if __name__ == '__main__':
   main()