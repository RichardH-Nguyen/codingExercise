import csv
import urllib.request
import io

url = "https://s3.us-east-2.amazonaws.com/cc-eng/2018-coding-excercise/cablecast-cdn-costs.csv"
customersUrl = "https://s3.us-east-2.amazonaws.com/cc-eng/2018-coding-excercise/cablecast-customers.csv"
response = urllib.request.urlopen(url)
responseCustomer = urllib.request.urlopen(customersUrl)
cr = csv.reader(response)
datareader = csv.reader(io.TextIOWrapper(response))
dataCustomer = csv.reader(io.TextIOWrapper(responseCustomer))
rows = []
customerRows = []


for row in datareader:
    rows.append(row)

for row in dataCustomer:
    customerRows.append(row)


# index 106 total cost
#total length 213
totalIndex = rows[0].index("Total cost ($)")
gbIndex = rows[0].index("Total usage (GB)")



def GetSeperate(numOfArrays, startIndex, endIndex):
    array = []
    for i in range(numOfArrays):
        midArray = []
        for x in range(startIndex, endIndex + 1):
            midArray.append(rows[i][x])
        array.append(midArray)
    return array

def getAverageCost(array, endIndex):
    for customer in range(1, endIndex):
        average = float(array[1][customer]) / 2
        id = array[0][customer].split("(")
        name = getCustomerName(id[0])
        print("Average cost for "+str(name) + ": " + str(average))

def getAverageGB(array, endIndex):
    for customer in range(0, endIndex):
        average = float(array[1][customer]) / 2
        id = array[0][customer].split("(")
        name = getCustomerName(id[0])
        print("Average GB for "+ str(name) + ": " + str(average))


def getCustomerName(ID):
    for i in range(len(customerRows)):
        check = customerRows[i][0]
        if ID == check:
            return customerRows[i][1]


def MostData(array):
    customerID = str(array[0][0]).split("(")
    customerName = getCustomerName(customerID[0])
    print("The customer using the most data: " + str(customerName))
    

def LeastData(array):
    customerID = str(array[0][len(array[0]) - 2]).split("(")
    customerName = getCustomerName(customerID[0])
    print("The customer using the least data: " + str(customerName))

def FiveHighestID(array, startIndex):
    fiveIDArray = []
    fiveNameArray = []
    for i in range(startIndex, startIndex + 5):
        fiveIDArray.append(array[0][i])
    for id in fiveIDArray:
        idSplit = id.split("(")
        name = getCustomerName(idSplit[0])
        fiveNameArray.append(name)
    return fiveIDArray

def FiveLowest(array):
    fiveIDArray = []
    for i in range(len(array[0]) - 6, len(array[0]) - 1):
        fiveIDArray.append(array[0][i])
    return fiveIDArray

def getAveCostByID(ID, ArrayWithData):
    index = ArrayWithData[0].index(ID)
    totalCost = ArrayWithData[1][index]
    return float(totalCost) / 2


def ConvertToMoneyID(id):
    stringList = list(id)
    if "$" in stringList:
        print("ID already a moneyID")
    else:
        index = stringList.index('G')
        stringList[index] = "$"
        stringList.pop(index + 1)
        moneyString = "".join(stringList)
        return moneyString

money = GetSeperate(63, 0, totalIndex)
data = GetSeperate(63, totalIndex + 1, gbIndex)


num = 0
for i in range(62):
    newNum = data[1][i]
    if float(newNum) > num:
        num = float(newNum)

print("Average number of cost transferred per customer per month.")
totalData = money[1][len(money[0]) - 1]
AvePerCustomer = float(totalData) / float(len(data[0]) - 1)
AvePerMonth = AvePerCustomer / 2
print(AvePerMonth)
print("\n")


print("Average number of GBs transferred per customer per month.")
totalData = data[1][len(data[0]) - 1]
AvePerCustomer = float(totalData) / float(len(data[0]) - 1)
AvePerMonth = AvePerCustomer / 2
print(AvePerMonth)
print("\n")


MostData(data)
print("\n---------------------------------------------------")

LeastData(data)
print("\n---------------------------------------------------")

print("\nAverage cost per customer from highest to least")
print("-------------------------------------")
getAverageCost(money, totalIndex)

print("\nAverage GB cost per customer from highest to least")
print("-------------------------------------")
getAverageGB(data, totalIndex - 1)

fiveID = FiveHighestID(money, 1)
lowFiveID = FiveLowest(money)
dataFiveHigh = FiveHighestID(data, 0)
dataFiveLow = FiveLowest(data)
print("\nFive highest users of data and their Average cost and data usage per month:")
print("---------------------------------------------------")
for id in dataFiveHigh:
    mID = ConvertToMoneyID(id)
    AveMoney = getAveCostByID(mID, money)
    aveData = getAveCostByID(id, data)
    idSplit = id.split("(")
    name = getCustomerName(idSplit[0])
    print(name + " - Average Cost: " + str(AveMoney) + "| Average Data: " + str(aveData) + "\n")

print("\nFive lowest users of data and their Average cost and data usage per month:")
print("---------------------------------------------------")
for id in dataFiveLow:
    mID = ConvertToMoneyID(id)
    AveMoney = getAveCostByID(mID, money)
    aveData = getAveCostByID(id, data)
    idSplit = id.split("(")
    name = getCustomerName(idSplit[0])
    print(name + " - Average Cost: " + str(AveMoney) + "| Average Data: " + str(aveData) + "\n")

print("Cost and data usage for untagged customers")
print("-------------------------------------------------")
unTagIndex = money[0].index("No Tagkey: NetsuiteID($)")
print("Money: " + str(money[1][unTagIndex]))
unTagIndex = data[0].index("No Tagkey: NetsuiteID(GB)")
print("Data: " + str(data[1][unTagIndex]))

print("\nID's from CDN that also appear in EDN")
print("-------------------------------------------------")
for i in range(len(data[0]) - 1):
    Id = data[0][i]
    idArray = Id.split("(")
    ID = idArray[0]
    for x in range(len(customerRows)):
        check = customerRows[x][0]
        if ID == check:
            print(customerRows[x][0])

