import math 
import random 
import csv
from math import sqrt

# class labels encoded to 0 , 1 , 2 , 3 
def encode_class(mydata): 
    classes = [] 
    for i in range(len(mydata)): 
        if mydata[i][-1] not in classes: 
            classes.append(mydata[i][-1])
    labelSize=len(classes)
    for i in range(len(classes)): 
        for j in range(len(mydata)): 
            if mydata[j][-1] == classes[i]: 
                mydata[j][-1] = i 
    return mydata ,classes 


def splitting(mydata, ratio): 
    train_num = int(len(mydata) * ratio) 
    train = [] 
    test = list(mydata) 
    while len(train) < train_num: 
        index = random.randrange(len(test))
        train.append(test.pop(index)) 
    return train, test


# Group data rows under each class dict[unacc], dict[acc], dict[vgood] & dict[good]
def groupUnderClass(mydata): 
      dict = {} 
      for i in range(len(mydata)): 
          if (mydata[i][-1] not in dict): 
              dict[mydata[i][-1]] = [] 
          dict[mydata[i][-1]].append(mydata[i]) 
      return dict

def accuracy_rate(test, predictions): 
    correct = 0
    for i in range(len(test)): 
        if test[i][-1] == predictions[i]: 
            correct += 1
    return (correct / float(len(test))) * 100.0  


#----------------------code----------------------

filename = 'car.data.csv'
mydata = csv.reader(open(filename, "rt")) 
mydata = list(mydata) 
mydata , classes = encode_class(mydata) 

ratio = 0.75
train_data, test_data = splitting(mydata, ratio) 

#*****************************-Learn Phase-******************************

groupClass=dict()
groupClass=groupUnderClass(train_data)    
pC=dict()

for i in range (len(groupClass)):
    for key in groupClass:
        pC[key]=(len(groupClass[key])/len(train_data))


clist=dict()
predictions=[]
while(True):
    for i in range(len(train_data[0])-1):
        valueRange = [] 
        for j in range(len(train_data)):
            if train_data[j][i] not in valueRange: 
                valueRange.append(train_data[j][i])    
        for key in groupClass:
                 for x in range(0,len(valueRange)):
                     ctr=0
                     cString = ''
                     for j in range(0,len(groupClass[key])):
                         if(valueRange[x]==groupClass[key][j][i]):
                             ctr+=1                 
                     cString = str(key)+'-'+str(i)+'-'+valueRange[x]
                     clist[cString]= ctr/len(groupClass[key])

#_____________________ if probability = 0 ________________________

    N=0
    for key in clist:
        if (clist[key]==0):
            classLabel=key[0]
            if(int(classLabel) < 3):num=4 
            else:num=3
            clist[key]=1/(len(groupClass[int(classLabel)])+num)
            for key in clist:                
                if (key[0]==(classLabel)):
                    clist[key]=((clist[key]*len(groupClass[int(classLabel)]))+1)/(len(groupClass[int(classLabel)])+num)
    for key in clist:
        if (clist[key]==0):N=1
    if (N==0):break


#*****************************-Test Phase-******************************


for i in range(len(test_data)):
    prob=dict()
    for key in groupClass:
       p=pC[key]
       for j in range(len(test_data[0])-1):
            string=str(key)+'-'+str(j)+'-'+test_data[i][j]
            p*=clist[string]
       prob[key]=p
    
    #print('Test Case',test_data[i],'is' ,max(prob, key=prob.get))           
    predictions.append(max(prob,key=prob.get))

#--------accuracey-------------

accuracy = accuracy_rate(test_data, predictions) 
print("Accuracy is: ", accuracy)


print('************************k-nearest************************')
#______________________________K-nearst_______________________________

# Convert string columns to integer
def encode_data(mydata): 
    
    for i in range(len(test_data[0])-1):
        classes = [] 
        for j in range(len(mydata)):
            if mydata[j][i] not in classes: 
                classes.append(mydata[j][i])
        for x in range(len(classes)): 
            for j in range(len(mydata)): 
                if mydata[j][i] == classes[x]: 
                    mydata[j][i] = x
    return mydata


def euclidean_distance(row1, row2):
	distance = 0.0
	for i in range(len(row1)-1):
		distance += (row1[i] - row2[i])**2
	return sqrt(distance)

    
print('Enter k:')
k = input()
k=int(k)

predictions=[]
#k=5

ratio = 0.75
train_data, test_data = splitting(encode_data(mydata), ratio) 

for j in range(len(test_data)):
    dis=[]
    nearst=[]
    for i in range(len(train_data)):
        dis.append((euclidean_distance(train_data[i], test_data[j])))
        nearst.append(train_data[i])
    Min=[]
    for i in range(k):
        Min.append(nearst[dis.index(min(dis))])
        dis.remove(min(dis))
        nearst.remove(nearst[dis.index(min(dis))])

    #print(k,' nearest classes of' , test_data[j])
    
    label=[]
    ctrlist=[]
    for i in range(len(Min)):
        x=0
        ctr=0   
        for n in range(len(Min)):
            if(Min[i][-1]== Min[n][-1]):
               ctr+=1
               if(Min[i][-1] not in label):
                   label.append(Min[i][-1])
                   x=1
                   
        if(x==1):ctrlist.append(ctr)              
    
    #print('class label is ' , label[ctrlist.index(max(ctrlist))])
    predictions.append(label[ctrlist.index(max(ctrlist))])
    #print('classes',classes[label[ctrlist.index(max(ctrlist))]])
            
#----------------- accuracey -------------------

accuracy = accuracy_rate(test_data, predictions) 
print("Accuracy is: ", accuracy)

