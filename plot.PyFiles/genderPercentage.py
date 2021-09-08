#!/usr/bin/env python
'''
------------------------------------------------------------------------------
| __FILE__:            genderPercentage.py                                   |  
| __AUTHORS__:         Anthony Vidovic (1130891), John Denbutter (1056466)   |
|                      Or Brener (1140102), Tony Ngo (1142414)               |
|                                                                            |
| __PROJECT__:         COVID-19 Data Analysis and Visualization              |
| __LAST UPDATED__:    Sunday, March 28th, 2021                              |
------------------------------------------------------------------------------
| __SUMMARY__:         Obtain total cases related to an outbreak for each    |
|                      gender, for the given city. Visualized on a pie chart |
|                      showing the percentage of cases for each gender.      |
|                                                                            |
| __DATA__:            genderPercentage.csv                                  |
|                                                                            |
| __RUN WITH__:        File will be run from gui.py.                         |
|                      To individually run:                                  |
|                      python plot.PyFiles/q1.py 'phu_id'                    |
|                                                                            |
| __REFERENCES__:      below comments marked with 'Reference'                |
|                      have been used from an external source.               |
|                      Details will be provided in the comment.              |
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

    # Arguments are passed from gui.py
    PHU_code = argv[1]
    PHU_name = argv[2]

    data = open_file_CSV('data/genderPercentage.csv')

    counts_per_gender = [0,0,0,0] # [female, male, gender_diverse, unspecified]

    # Populate counts_per_gender for each gender
    for i in range(0, len(data)):
        if (data[i][0] == PHU_code):
            counts_per_gender[0] += int(data[i][2])
            counts_per_gender[1] += int(data[i + 1][2])
            counts_per_gender[2] += int(data[i + 2][2])
            counts_per_gender[3] += int(data[i + 3][2])
            break


    # Convert num cases per gender into percentages out of 100%
    sum_counts = sum(counts_per_gender)
    i = 0
    for num in counts_per_gender:
        counts_per_gender[i] = round(num / sum_counts * 100, 2)
        i += 1


    #--------Start of Pie Graph-------#

    colors = ['#FFC2B4', '#4C9F70', '#F6E27F', '#C6DDF0']
    wedgeprops = {"linewidth": 1.5, 'width': 1, "edgecolor": "#0C0910"}

    # Figure that the chart lays on
    fig1, ax1 = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect="equal"))

    # Pie chart
    wedges, texts = ax1.pie(counts_per_gender,
                            colors=colors,
                            wedgeprops=wedgeprops,
                            shadow=True,
                            startangle=100)


    #---Referenced code below---#
    '''
    _TITLE_:     Labeling a pie and a donut
    _LINK_:      https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
    _SECTION_:   Second code block
    _AUTHORS_:   The Matplotlib Development Team
    _DATE_:      Mar 26, 2021
    '''
    bbox_props = dict(boxstyle="square,pad=0.3",fc="#0D101D",ec="#0D101D",lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-|>"),bbox=bbox_props,zorder=0,va="center")

    coord_list = []
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))

        # Following two if statements not referenced
        coord_list.append([x, y])
        if i == 3:
            if abs(coord_list[3][1] - coord_list[2][1]) <= 0.09:
                y -= 0.12

        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax1.annotate(str(counts_per_gender[i]) + '%',
                     xy=(x, y),
                     xytext=(1.35 * np.sign(x), 1.4 * y),
                     horizontalalignment=horizontalalignment,
                     color=colors[i],
                     **kw)
    # End of referenced code


    ax1.legend(labels=['Female', 'Male', 'Gender Diverse', 'Unspecified'],
               loc=4,
               title='PHU: ' + PHU_name)
        
    ax1.axis('equal')
    plt.tight_layout()
    fig1.savefig("plots/genderPercentage_plot.png")

    #-----End of pie chart-----#


    # Report printed to terminal for verification of output
    print(OKCYAN+"#-----------REPORT-----------#"+ENDC)
    print(OKBLUE+"SUCCESSFULLY REACHED Q1.py"+ENDC)
    print(OKBLUE+"PHU-ID = " + PHU_code + ENDC)
    print(OKBLUE+"PHU-NAME = " + PHU_name + ENDC)
    print(OKBLUE+"Plot Successfully made"+ENDC)
    print(OKCYAN+"#------------End-------------#"+ENDC)


main(sys.argv)

#
#   End of Script
#
