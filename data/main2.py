import pandas as pd
#read drug file
import numpy as np
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt

excel_file = 'Drugs-demo1.xlsx'
drug_file = pd.read_excel(excel_file)

list_num_hours = []
list_num_row = []
already_taking_drugs = 0
i=2

# list of list that keep all cvri for 15 hours before taking drug
value_of_cvri = []
# keep the row that id is change
row_num_cvri = []

'''
This function including all the patients that 
dosent recive drugs at the begining, and later on
they recive drugs.
'''
def dont_get_then_get():
    start_take_drug = 0
    hour_of_take_drug = 0
    patient_id = ""
    for i in range(len(drug_file['patient_id'])):
        hour_of_take_drug += 1
        # if the id is change start new counting
        if patient_id != drug_file['patient_id'][i]:
            patient_id = drug_file['patient_id'][i]
            start_take_drug = 0
            hour_of_take_drug = 1

        # if is the first time he is take drug
        if start_take_drug == 0:
            if drug_file['Drug1'][i] > 0:
                start_take_drug = 1
                #we want at least 12 clean of drugs hours for check the cvri method
                if hour_of_take_drug - 1 > 15:
                    # keep how much hours he is taking drugs
                    list_num_hours.append(hour_of_take_drug - 1)
                    # keep the row from the drugs table
                    list_num_row.append(i + 2)


    # read cvri filr
    CVRI_file = pd.ExcelFile('CVRI - demo1.xlsx')
    cvri = pd.read_excel(CVRI_file, 'Sheet2')


    # run on the hour list
    list_pos = 0
    for i in range(len(cvri['id_demo'])):
        # becuse the row number in drug and cvri filr ia now the same for each is, needed to check is its the same person
        # if not the loop run until he get the same id in the cvri file
        # (in cvri file each id start allways after from drug id)
        if (cvri['id_demo'][i] == drug_file['patient_id'][list_num_row[list_pos]]):
            row_num_cvri.append(i + 2)
            ################## make this function
            sub_list_of_cvri = []
            # we want to run for only 15 hours before start to take drug
            # row number + excel file tart from 2 + hours that take until take drug + 15 hors that we check
            number_row_to_take = i + 2 + list_num_hours[list_pos] - 15
            deadline = i + list_num_hours[list_pos]
            print(number_row_to_take, " ", deadline)

            # keep value of cvri for 15 vours
            for j in range(15):
                sub_list_of_cvri.append(cvri['CVRI'][number_row_to_take + (j - 2)])
            print(sub_list_of_cvri)
            value_of_cvri.append(sub_list_of_cvri)
            ##################
            if (list_pos == len(list_num_row) - 1):
                break
            list_pos += 1

    print(list_num_hours)
    print(list_num_row)
    print(row_num_cvri)
    return 1

'''
This function including all the patients that 
RECIVED drugs from the start, then stop, and then
start recive drugs again.
'''
def get_drug_stop_and_get_again():
    start_take_drug = 0
    hour_of_take_drug = 0
    patient_id = ""
    counter = 0
    already_taking_drugs = 0
    second_hour_drugs_taking = 0
    for i in range(len(drug_file['patient_id'])):
        hour_of_take_drug += 1
        # if the id is change start new counting
        if patient_id != drug_file['patient_id'][i]:
            patient_id = drug_file['patient_id'][i]
            start_take_drug = 0
            hour_of_take_drug = 1
            already_taking_drugs = 0
            second_hour_drugs_taking = 0
            counter = 0
        # if is the first time he is take drug
        if start_take_drug == 0:
            counter += 1
            if drug_file['Drug1'][i] > 0:
                start_take_drug = 1
                flag = True
                already_taking_drugs = 1

        else:
            if already_taking_drugs == 1 and counter == 1:
                if drug_file['Drug1'][i] > 0:
                    continue
                else:
                    # stop taking drugs
                    second_hour_drugs_taking += 1
                    if drug_file['Drug1'][i + 1] > 0 and drug_file['patient_id'][i+1] == patient_id:
                        #start again taking drugs
                        already_taking_drugs = 2
                        if second_hour_drugs_taking - 1 > 15:
                            list_num_hours.append(hour_of_take_drug)
                            list_num_row.append(i + 2)


    # read cvri filr
    CVRI_file = pd.ExcelFile('CVRI - demo1.xlsx')
    cvri = pd.read_excel(CVRI_file, 'Sheet2')


    # run on the hour list
    list_pos = 0
    for i in range(len(cvri['id_demo'])):
        # becuse the row number in drug and cvri filr ia now the same for each is, needed to check is its the same person
        # if not the loop run until he get the same id in the cvri file
        # (in cvri file each id start allways after from drug id)
        if (cvri['id_demo'][i] == drug_file['patient_id'][list_num_row[list_pos]]):
            row_num_cvri.append(i + 2)
            ################## make this function
            sub_list_of_cvri = []
            # we want to run for only 15 hours before start to take drug
            # row number + excel file tart from 2 + hours that take until take drug + 15 hours that we check
            number_row_to_take = i + 2 + list_num_hours[list_pos] - 15
            deadline = i + list_num_hours[list_pos]
            print(number_row_to_take, " ", deadline)

            # keep value of cvri for 15 vours
            for j in range(15):
                sub_list_of_cvri.append(cvri['CVRI'][number_row_to_take + (j - 2)])
            print(sub_list_of_cvri)
            value_of_cvri.append(sub_list_of_cvri)
            ##################
            if (list_pos == len(list_num_row) - 1):
                break
            list_pos += 1

    print(list_num_hours)
    print(list_num_row)
    print(row_num_cvri)
    return 0

'''!!!!! @@@@@@ ACTIVE FUNCTIONS HERE   @@@@@@@@!!!!
'''

#x = dont_get_then_get()
x= get_drug_stop_and_get_again()


############### data visualization #########################


#On move function to show the current value of hour and CVRI while moving mouse over the graph.
def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y
    if event.inaxes:
        ax = event.inaxes  # the axes instance
        print('Hour: %f, CVRI: %f' % (event.xdata, event.ydata))


from scipy.interpolate import make_interp_spline

plt.subplots(figsize=(13,5))
for i in range(len(value_of_cvri)):
    #x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    x1 =np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    y1 = np.array(value_of_cvri[i])
    y1 = np.nan_to_num(y1)
    x_y_Line = make_interp_spline(x1,y1)
    X_ = np.linspace(x1.min(),x1.max(),1000)
    Y_ = x_y_Line(X_)
    temp = i+1
    plt.plot(X_, Y_, label='$Patient = %i$'%temp)

# naming the x axis
plt.xlabel('hours')
# naming the y axis
plt.ylabel('CVRI')
# giving a title to my graph
if(x == 1):
    plt.title('Before event happen')
else:
    plt.title('Second event happen')
# show a legend on the plot

plt.legend(loc='center left', bbox_to_anchor=(0.95, 0.5))

#To show the currnet value when mouse move over the graph.
#To cancel/active the mouse move value put/release Binding_id under comment.
#binding_id = plt.connect('motion_notify_event', on_move)

plt.show()
