#!/usr/bin/env python
'''
--------------------------------------------------------------------------------------------
| __FILE__:            caseTrendInRange.pyplot                                             |  
| __AUTHORS__:         Anthony Vidovic (1130891), John Denbutter (1056466)                 |
|                      Or Brener (1140102), Tony Ngo (1142414)                             |
|                                                                                          |
| __PROJECT__:         COVID-19 Data Analysis and Visualization                            |
| __LAST UPDATED__:    Sunday, March 28th, 2021                                            |
--------------------------------------------------------------------------------------------
| __SUMMARY__:         Obtain total cases for each month in the given                      |
|                      date range.                                                         |
|                      Visualized on line graph.                                           |
|                                                                                          |
| __DATA__:            dateCounts.csv                                                      |
|                                                                                          |
| __RUN WITH__:        File will be run from gui.py.                                       |
|                      To individually run:                                                |
|                      python plot.PyFiles/caseTrendInRange.py 'start_date' 'end_date'     |
--------------------------------------------------------------------------------------------
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

# --------------------#
#       Methods       #
# --------------------#
def to_date_to_string(to_date):
    '''Modifies the to_date to allow the date comparison to compare to (and including) the final month. Increments the to_date month by 1 and returns it as a string.

    param - to_date: (List[int]) 

    return: str_to_date (string)
    '''
    # Checks the second unit of the month
    date_character = int(to_date[6]) 
    # If it is not September
    if date_character != 9: 
        date_character += 1
        str(date_character)
        to_date[6] = date_character
        # List of int changed to list of str
        to_date = [str(int) for int in to_date] 
        str_to_date = ""
        for element in to_date:
            # New string is combination of elements in List of string
            str_to_date += element 
    # If it is September
    else: 
        # Month is changed to 0, so it increments to 10
        date_character = 0 
        str(date_character)
        to_date[6] = date_character
        # Checks the first unit of the month
        date_character = int(to_date[5]) 
        date_character += 1
        str(date_character)
        to_date[5] = date_character
        # List of int changed to list of str
        to_date = [str(int) for int in to_date] 
        str_to_date = ""
        for element in to_date:
            # New string is combination of elements in List of string
            str_to_date += element 

    return str_to_date


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

    data = open_file_CSV('data/dateCounts.csv')

    # Arguments are passed from gui.py
    from_date = str(argv[1])
    to_date = list(argv[2])
    
    str_to_date = to_date_to_string(to_date) # Increments the month of to_date by one and converts it to a string
    

    condensed_list = [] # Will store all counts needed withing the given months


    start_date = 0
    for i in range(0, len(data)): 
        # If the date in the csv is greater than the given from_date, then the previous date is needed
        if (data[i][0] > from_date): 
            start_date = i-1
            # In the case date is not listed
            if (data[i-1][0] != from_date): 
                start_date = i
            for j in range(start_date, len(data)):
            # If the date in the csv is greater than the given to_date, then the previous date is needed
                if (data[j][0] > str_to_date): 
                    break
                else:
                    condensed_list.append([data[j][0], data[j][1]])
            break


    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    month_range = [] # Month range will hold all the months in between the start and end date

    for i in range(1, len(condensed_list)):
        # This is current index date
        date_string = condensed_list[i][0] 
        # This is previous index date
        prev_date = condensed_list[i-1][0] 
        # If the current date is same as previous
        if date_string[5:-3] == prev_date[5:-3]: 
            # Move onto next date
            i += 1          
        # If they aren't the same                 
        elif date_string[5:-3] != prev_date[5:-3]: 
            month_range.append(prev_date[5:-3])
        else: 
            month_range.append(prev_date[5:-3])
    # Appends the last month since the loop doesn't record it
    month_range.append(prev_date[5:-3]) 


    month_counter = [0] * 24 # Month_counter will track all the cases per month

    # Nested loop to check each month and if they match
    for i in range (0, len(month_list)): 
        # Within each condensed_list date
        for k in range (0, len(condensed_list)-1):   
            date_string = condensed_list[k][0]
            if date_string[:-6] == '2020': 
                # If the month matches, then increase counter by the amount at current condensed_list
                if month_list[i] == date_string[5:-3]: 
                    month_counter[i] += int(condensed_list[k][1]) 
            elif date_string[:-6] == '2021':
                if month_list[i] == date_string[5:-3]:
                    month_counter[i+12] += int(condensed_list[k][1])

    counted_list = [] # 2D list that holds the month (along with year) and the cases found in that month

    # This loop will append the values into the list using the if statements
    for z in range (0, len(month_counter)): 
        # This will append for 2020
        if (z >= 0 and z <= 11): 
            counted_list.append(["2020-"+month_list[z], month_counter[z]])
        # This will append for 2021
        elif (z >= 12 and z <= 23): 
            counted_list.append(["2021-"+month_list[z-12], month_counter[z]])
    # counted_list will now have all the values stored for each month from 2020 to 2021 regardless of the month range


    new_list = [] # Holds only the months that are in the month_range


    for i in range (0, len(counted_list)):
        if counted_list[i][1] != 0:
            new_list.append(counted_list[i])



    #----Start of Line Plot----#

    # Split into two separate lists
    months, cases_per_month = map(list, zip(*new_list))


    plt.figure(figsize=(10, 5))
    plt.plot(months, cases_per_month, 'o-', color='#265597')

    # Rotate xticks is there are over 5
    if len(months) > 5:
        plt.xticks(rotation=30)
    else:
        plt.xticks(rotation=0)

    # Properties and labels of plot
    plt.yticks(weight='bold')
    plt.fill_between(months, cases_per_month, color='#B6CCE0')
    plt.grid(True)
    plt.xlabel('Month',weight = 'bold')
    plt.ylabel('Cases',weight = 'bold')
    plt.title('Rate of confirmed cases from the chosen period', weight='bold')

    plt.savefig("plots/caseTrendInRange_plot.png")


    # Report printed to terminal for verification of output
    print(OKCYAN+"#-----------REPORT-----------#"+ENDC)
    print(OKBLUE+"SUCCESSFULLY REACHED Q2.py"+ENDC)
    print(OKBLUE+"Start Date = " + months[0] + ENDC)
    print(OKBLUE+"To Date = " + months[len(months)-1] + ENDC)
    print(OKBLUE+"Plot Successfully made"+ENDC)
    print(OKCYAN+"#------------End-------------#"+ENDC)


main(sys.argv)

# --------------------#
#    End of program   #
# --------------------#