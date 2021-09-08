#!/usr/bin/env python
'''
-----------------------------------------------------------------------------------------------------
| __FILE__:            LTCHRatio.py                                                                 |  
| __AUTHORS__:         Anthony Vidovic (1130891), John Denbutter (1056466)                          |
|                      Or Brener (1140102), Tony Ngo (1142414)                                      |
|                                                                                                   |
| __PROJECT__:         COVID-19 Data Analysis and Visualization                                     |
| __LAST UPDATED__:    Monday, March 29th, 2021                                                     |
-----------------------------------------------------------------------------------------------------
| __SUMMARY__:          Obtain cases for Ontario and for LTC in Ontario for                         |
|                       each month found between the 2 datasets. Visualized                         |
|                       on a double bar graph comparing the 2 counts for each                       |
|                       month.                                                                      |
|                                                                                                   |
| __DATA__:            dateCounts.csv   and   raw_dataset2.csv                                      |
|                                                                                                   |
| __RUN WITH__:        File will be run from gui.py.                                                |
|                      To individually run:                                                         |
|                      python plot.PyFiles/LTCHRatio.py                                             |
|                                                                                                   |
| __REFERENCES__:       raw_dataset2.csv                                                            |  
|                       _TITLE_:  Long-Term Care Home COVID-19 Data                                 |
|                       _LINK_: https://data.ontario.ca/dataset/long-term-care-home-covid-19-data   |
|                       _SECTION_: Data                                                             |
|                       _AUTHORS_: The Ontario Government of Canada Data Catalouge Team             |
|                       _DATE_:    Mar 20th, 2021                                                   |
-----------------------------------------------------------------------------------------------------
'''

# --------------------#
#      Libraries      #
# --------------------#
import os
os.environ["MPLCONFIGDIR"] = "/home/runner/PROJECTL01-CIS2250-3/plot.PyFiles"
import sys
import csv
import matplotlib.pyplot as plt
import math
import numpy as np

# --------------------#
#   Global Variables  #
# --------------------#
OKCYAN = '\033[96m'
OKBLUE = '\033[94m'
ENDC = '\033[0m'

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
    data_1 = open_file_CSV('data/dateCounts.csv')
    data_2 = open_file_CSV('data/raw_dataset2.csv')

    # Loops through dataset 1 to line up the starting date with dataset 2.
    for i in range(1, len(data_1)):
        # If the date in the csv is greater than the first entry in data_2
        if (data_1[i][0] > data_2[1][0]): 
            start_number_data_1 = i - 1
            # In the case the date is not listed in data_1
            if (data_1[i-1][0] != data_2[1][0]):
                start_number_data_1 = i
            # Date of last entry in data2
            end_date = data_2[len(data_2)-1][0] 

            # Loops through dataset 1 to line up the ending date with dataset 2.
            for j in range(i, len(data_1)):
                # If the date in the csv is greater than the last entry in data_2
                if (data_1[j][0] > data_2[len(data_2)-1][0]): 
                    end_date = data_1[j - 1][0]
                    end_number_data_1 = j - 1
                    # In the case the date is not listed in data_1
                    if (data_1[j-1][0] != end_date): 
                        end_date = data_1[j][0]
                        end_number_data_1 = j
                    break
                # If dataset 1 ends before dataset 2 (often not the case)
                if (j == (len(data_1)-1)): 
                    end_number_data_1 = j
            break

    condensed_list_1 = [] # List of all cases in dataset 1 within the date range 
    for i in range(start_number_data_1,  end_number_data_1):
        condensed_list_1.append([data_1[i][0], int(data_1[i][1])])
    

    condensed_list_2 = [] # List of all cases in dataset 2 within the date range 
    for i in range(1, len(data_2)):
        condensed_list_2.append([data_2[i][0], data_2[i][3]])
        
    case_counter = 0
    case_counter += int(condensed_list_2[0][1])
    iteration_counter = 0
    LTCcase_per_month = []
    condensed_list_2.append(["0",0])

    # Finding the total counts for each month for data set #2 (LTC homes)
    for i in range(1, len(condensed_list_2)):
        date_string = condensed_list_2[i][0]
        prev_string = condensed_list_2[i-1][0]
        # If months match, keep looping
        if date_string[5:-3] == prev_string[5:-3]: 
            case_counter += int(condensed_list_2[i][1])
            iteration_counter += 1
        # If months don't match, then add to list
        elif (date_string[5:-3] != prev_string[5:-3]):
            LTCcase_per_month.append([prev_string[:-3], math.ceil(case_counter/(iteration_counter + 1))])
            case_counter = 0
            case_counter = int(condensed_list_2[i][1])
            iteration_counter = 0
        else:
            case_counter = 0
            case_counter = int(condensed_list_2[i][1])

    case_counter = 0
    case_counter += int(condensed_list_1[0][1])
    iteration_counter = 0
    ontario_case_per_month = []
    condensed_list_1.append(["0", 0])

    # Finding the total counts for each month for data set #1 (All Ontario cases)
    for i in range (1, len(condensed_list_1)):
        date_string = condensed_list_1[i][0]
        prev_string = condensed_list_1[i-1][0]
        # If months match, keep looping
        if date_string[5:-3] == prev_string[5:-3]: 
            case_counter += int(condensed_list_1[i][1])
            iteration_counter += 1
        # If months don't match, then add to list
        elif (date_string[5:-3] != prev_string[5:-3]): 
            ontario_case_per_month.append([prev_string[:-3], math.ceil(case_counter/iteration_counter + 1)])
            case_counter = 0
            case_counter = int(condensed_list_1[i][1])
            iteration_counter = 0  
        else:
            case_counter = 0
            case_counter = int(condensed_list_1[i][1])


    #---Start of Plot---#
    plt.figure(figsize=(10, 5))
    width=0.2

    dates_ontario, cases_ontario = map(list, zip(*ontario_case_per_month))
    dates_LTC, cases_LTC = map(list, zip(*LTCcase_per_month))
    maxYValue = max(max(cases_LTC), max(cases_ontario))
    minYValue = min(min(cases_LTC), min(cases_ontario))

    bar1loc = np.arange(len(dates_ontario))
    bar2loc = [n+width for n in bar1loc]

    plt.bar(bar1loc,cases_LTC,label='Long term care homes',width=width, color='#00203F')
    plt.bar(bar2loc,cases_ontario,label='All of Ontario',width=width,color='#DF9589')

    plt.xticks(bar1loc+width/2, dates_ontario, rotation=30)
    plt.xlabel("Date")
    plt.ylabel("Average Cases")
    plt.legend()
    plt.ylim([0, maxYValue+700])
    plt.title(' Average Ongoing LTC home cases vs Average New Confirmed Covid Cases in Ontario')

    plt.savefig("plots/LTCHRatio_plot.png")    
    #---End of Plot---#


    # Report printed to terminal for verification of output
    print(OKCYAN+"#-----------REPORT-----------#"+ENDC)
    print(OKBLUE+"SUCCESSFULLY REACHED Q1.py"+ENDC)
    print(OKBLUE+"Max value on plot = " + str(maxYValue) + ENDC)
    print(OKBLUE+"Min value on plot = " + str(minYValue) + ENDC)
    print(OKBLUE+"Plot Successfully made"+ENDC)
    print(OKCYAN+"#------------End-------------#"+ENDC)


main(sys.argv)

# --------------------#
#    End of program   #
# --------------------#