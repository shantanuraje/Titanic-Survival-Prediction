import csv as csv 
import numpy as np
import pdb
# Open up the csv file in to a Python object
train_file = csv.reader(open('./data/train.csv', 'rb')) 
train_header = train_file.next()  # The next() command just skips the 
                                 # first line which is a header
train_data=[]                          # Create a variable called 'data'.
for row in train_file:      # Run through each row in the csv file,
    train_data.append(row)             # adding each row to the data variable
train_data = np.array(train_data)              # Then convert from a list to an array
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
test_data = np.array(test_data)              # Then convert from a list to an array
                     # Be aware that each item is currently
                                 # a string in this format
# So we add a ceiling
fare_ceiling =40
# then modify the data in the Fare column to = 39, if it is greater or equal to the ceiling
train_data[ train_data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

# I know there were 1st, 2nd and 3rd classes on board
# But it's better practice to calculate this from the data directly
# Take the length of an array of unique values in column index 2
number_of_classes = len(np.unique(train_data[0::,2])) 

# Initialize the survival table with all zeros
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in xrange(number_of_classes):       #loop through each class
  for j in xrange(number_of_price_brackets):   #loop through each price bin
#    print "Class:",i,"Price bracket:",j    
    women_only_stats = train_data[(train_data[0::,4] == "female")&(train_data[0::,2].astype(np.float) == i+1)&(train_data[0:,9].astype(np.float)>= j*fare_bracket_size) &(train_data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]
    men_only_stats = train_data[(train_data[0::,4] != "female")&(train_data[0::,2].astype(np.float)== i+1)&(train_data[0:,9].astype(np.float)>= j*fare_bracket_size)&(train_data[0:,9].astype(np.float)< (j+1)*fare_bracket_size), 1] 
#    print women_only_stats,np.mean(women_only_stats.astype(np.float))
#    print men_only_stats,np.mean(men_only_stats.astype(np.float))    
    survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) 
    survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))
#    pdb.set_trace()
survival_table[ survival_table != survival_table ] = 0.

survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1 

prediction_file = open("./predictions/gender_class_tprice_model.csv", "wb")
p = csv.writer(prediction_file)
#
p.writerow(["PassengerId", "Survived"])

for row in test_data:
    for j in xrange(number_of_price_brackets):
#        print j
        try:
            row[8] = float(row[8])
#            print "@"
#            print row[8]
        except:                                   
            bin_fare = 3 - float(row[1])
#            print bin_fare
#            print "%"            
            break
        if row[8].astype(np.float) > fare_ceiling:
#            print type(row[8]),type(fare_ceiling)
#            print row[8] > fare_ceiling
            bin_fare = number_of_price_brackets-1
#            print bin_fare
#            print "^"
            break                                   
        elif row[8].astype(np.float) >= j * fare_bracket_size and row[8].astype(np.float) < (j+1) * fare_bracket_size:             
            bin_fare = j
#            print bin_fare
#            print "&"
            break
    if row[3] == 'female':
        print [row[0], "%d" % int(survival_table[0, float(row[1])-1, bin_fare])]                              #If the passenger is female
        p.writerow([row[0], "%d" % int(survival_table[0, float(row[1])-1, bin_fare])])
    else:
        print [row[0], "%d" % int(survival_table[0, float(row[1])-1, bin_fare])]                                          #else if male
        p.writerow([row[0], "%d" % int(survival_table[1, float(row[1])-1, bin_fare])])

#    pdb.set_trace() 
# Close out the files.
#test_file.close() 
prediction_file.close()
#    if row[3] == 'female':         # is it a female, if yes then                                       
#        p.writerow([row[0],'1'])    # predict 1
#    else:                              # or else if male,       
#        p.writerow([row[0],'0'])    # predict 0
##test_file.close()
#prediction_file.close()