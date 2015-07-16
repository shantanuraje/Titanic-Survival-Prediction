import csv as csv 
import numpy as np

# Open up the csv file in to a Python object
train_file = csv.reader(open('./data/train.csv', 'rb')) 
train_header = train_file.next()  # The next() command just skips the 
                                 # first line which is a header
train_data=[]                          # Create a variable called 'data'.
for row in train_file:      # Run through each row in the csv file,
    train_data.append(row)             # adding each row to the data variable
train_data = np.array(train_data) 	         # Then convert from a list to an array
			         # Be aware that each item is currently
                                 # a string in this format
number_passengers = np.size(train_data[0::,1].astype(np.float))
number_survived = np.sum(train_data[0::,1].astype(np.float))
proportion_survivors = number_survived / number_passengers

women_only_stats = train_data[0::,4] == "female" # This finds where all 
                                           # the elements in the gender
                                           # column that equals “female”
men_only_stats = train_data[0::,4] != "female"   # This finds where all the 
                                           # elements do not equal 
                                           # female (i.e. male)
women_onboard = train_data[women_only_stats,1].astype(np.float)  
men_onboard = train_data[men_only_stats,1].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)  
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard) 


test_file = csv.reader(open('./data/test.csv', 'rb')) 
test_header = test_file.next()  # The next() command just skips the 
                                 # first line which is a header
test_data=[]                          # Create a variable called 'data'.
for row in test_file:      # Run through each row in the csv file,
    test_data.append(row)             # adding each row to the data variable
test_data = np.array(test_data) 	         # Then convert from a list to an array
			         # Be aware that each item is currently
                                 # a string in this format
prediction_file = open("./predictions/genderbasedmodel.csv", "wb")
prediction_file_object = csv.writer(prediction_file)

prediction_file_object.writerow(["PassengerId", "Survived"])
for row in test_data:       # For each row in test.csv
    if row[3] == 'female':         # is it a female, if yes then                                       
        prediction_file_object.writerow([row[0],'1'])    # predict 1
    else:                              # or else if male,       
        prediction_file_object.writerow([row[0],'0'])    # predict 0
#test_file.close()
prediction_file.close()