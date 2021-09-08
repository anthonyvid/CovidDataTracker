#!/usr/bin/env python
'''
------------------------------------------------------------------------------
| __FILE__:            ageRange.py                                           |  
| __AUTHORS__:         Anthony Vidovic (1130891), John Denbutter (1056466)   |
|                      Or Brener (1140102), Tony Ngo (1142414)               |
|                                                                            |
| __PROJECT__:         COVID-19 Data Analysis and Visualization              |
| __LAST UPDATED__:    Sunday, March 28th, 2021                              |
------------------------------------------------------------------------------
| __SUMMARY__:         Obtain total cases in age range given for each city.  |
|                      Visualized on bar graph.                              |
|                                                                            |
| __DATA__:            ageRange.csv                                          |
|                                                                            |
| __RUN WITH__:        File will be run from gui.py.                         |
|                      To individually run:                                  |
|                      python plot.PyFiles/ageRange.py 'from_age' 'to_age'   |
------------------------------------------------------------------------------
'''

# --------------------#
#      Libraries      #
# --------------------#
import os
os.environ["MPLCONFIGDIR"] = "/home/runner/PROJECTL01-CIS2250-3/plot.PyFiles"
import sys
import csv
import matplotlib.pyplot as plt

# --------------------#
#   Global Variables  #
# --------------------#
OKCYAN = '\033[96m'
OKBLUE = '\033[94m'
ENDC = '\033[0m'
phu_names = [
            'Algoma', 'Brant', 'Durham', 'Grey Bruce',
            'Haldimand-Norfolk', 'Haliburton', 'Halton',
            'Hamilton', 'Hastings and Prince Edward', 'Chatham-Kent',
            'Kingston', 'Lambton', 'Leeds, Greenville',
            'Middlesex-London', 'Niagra Region', 'North Bay',
            'Northwestern', 'Ottawa', 'Peel', 'Peterborough', 'Porcupine',
            'Renfrew County', 'Eastern Ontario', 'Simcoe Muskoka', 'Sudbury',
            'Thundery Bay', 'Timiskaming', 'Waterloo', 'Guelph', 'Windsor', 'York', 'Toronto', 'Southwestern', 'Huron Perth']

# --------------------#
#       Methods       #
# --------------------#
def open_file_CSV(filename):
    '''Opens a csv file and reads the contents into a list.

    param - filename: name of the file to open

    return: A list with the file contents
    '''
    try:
        with open(filename, newline='') as csvfile:
            data = list(csv.reader(csvfile))
        return data
    except:
       print("Error opening file, please run again")
       sys.exit(1)

# --------------------#
#     Main program    #
# --------------------#
def main(argv):
    
    data = open_file_CSV('data/ageRange.csv')

    # Arguments are passed from gui.py
    from_age = argv[1]
    to_age = argv[2]

    # List of all ages we are checking in file
    range_list = list(range(int(from_age), int(to_age) + 10, 10))  

    # Loop through range list and change values match file values
    for i in range(0, len(range_list)):
        if range_list[i] == 10:
            range_list[i] = 20
            range_list[i] = '<' + str(range_list[i])
        elif range_list[i] == 90 or range_list[i] == 100:
            range_list[i] = '90+'
        else:
            range_list[i] = str(range_list[i]) + 's'

    # Holds total cases for an age in the range, for each PHU
    count_in_range = [] 

    # Populate count_in_range
    for i in range(0, len(data)):  
        if data[i][1] in range_list:
            count_in_range.append([data[i][0],data[i][2]])
           
    total_counter = 0

    # Account for 0th index since were looping from 1st
    total_counter += int(count_in_range[0][1]) 

    # 2d list holding phu with total count for give nrang
    total_list = []

    # Appends [0,0] last PHU at end of list so that loop will record the last count at the end of the list 
    count_in_range.append([0, 0])  
    
    # Loops for every valid count between age range and populates total_list
    for k in range(1, len(count_in_range)):
        if count_in_range[k][0] == count_in_range[k - 1][0]: 
            total_counter += int(count_in_range[k][1])
        elif (count_in_range[k][0] != count_in_range[k - 1][0]): 
            total_list.append([count_in_range[k - 1][0], total_counter])
            total_counter = 0
            total_counter = int(count_in_range[k][1]) 
        else:  
            total_counter = 0  
            total_counter = int(count_in_range[k][1]) 


    # Sort the 2dlist from lowest to highest cases
    total_list = sorted(total_list,key=lambda l:l[1])

    # Split into 2 lists
    phu_codes, cases_per_PHU = map(list, zip(*total_list))


    #-----Start of bar Plot-----#

    plt.figure(figsize=(10,6.5))

    # properties of the bars
    barh_dict = {
        'color':'#476DCA',
        'edgecolor':'#0C0910',
        'capstyle':'butt',
        'joinstyle':'round',
        'linewidth':'0.2',
        'linestyle':'-'
    }

    plt.title("Covid cases from outbreaks in age range "+from_age+" to "+to_age, weight='bold')
    plt.xlabel("Number of cases", weight = 'bold')
    plt.barh(phu_names,cases_per_PHU,height=0.6, **barh_dict)
    maxXValue = max(cases_per_PHU) 
    plt.xlim([0, maxXValue+5000])
    
    # Axis properties
    plt.yticks(
        c='#383838',
        fontsize=8,
        fontstretch='normal',
        fontweight='regular',
        weight='bold'
    )
    plt.xticks(weight='bold')

    # Text beside each bar
    text_dict = {
        'color':'#383838',
        'fontweight':'book',
        'fontsize':'small',
        'fontfamily':'monospace',
        'fontstretch':'condensed',
        'weight':'bold'
    }

    # Print number of cases at end of each bar graph
    for i, v in enumerate(cases_per_PHU):
        plt.text(v + 100, i - 0.25 , ' '+str(v),**text_dict)

    plt.savefig("plots/ageRange_plot.png")


    # Report printed to terminal for verification of output
    print(OKCYAN+"#-----------REPORT-----------#"+ENDC)
    print(OKBLUE+"SUCCESSFULLY REACHED Q2.py"+ENDC)
    print(OKBLUE+"from_age = " + from_age + ENDC)
    print(OKBLUE+"to_age = " + to_age + ENDC)
    print(OKBLUE+"Plot Successfully made"+ENDC)
    print(OKCYAN+"#------------End-------------#"+ENDC)


main(sys.argv)
# --------------------#
#    End of program   #
# --------------------#
