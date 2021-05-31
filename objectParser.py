import numpy as np

def parseFloatArray(string):
    return np.array([float(i) for i in string.strip('][').split(', ')])

def parseColor(string):
    return eval(string)


def parseArrayOfFloatArrays(string):
    arrays = []
    for subString in string:
            arrays.append([float(i) for i in subString.split(", ")])

    return arrays


def parseData(data):
    object = []


    try:
        objectItems = data.split(":")
    
        pointStrings = objectItems[2][2:-2].split('], [')

        points = []

        for string in pointStrings:
            points.append([float(i) for i in string.split(", ")])


        color = eval(objectItems[3])


        object = [int(objectItems[0]), np.array([float(i) for i in objectItems[1].strip('][').split(', ')]), np.array(points), color]

    except:
        print("Failed to parse.")

    return object


def parseClientData(data):
    object = []

    try:
        objectItems = data.split(":")

        object = [int(objectItems[0]), 
                  np.array([float(i) for i in objectItems[1].strip('][').split(', ')]), 
                  np.array([float(i) for i in objectItems[2].strip('][').split(', ')]), 
                  bool(int(objectItems[3]))]

    except:
        print("Failed to parse.")

    return object


def parseObject(data):
    objects = []
    
    if "|" not in data:
        print("empty")
        return objects

    try:
        datalist = data.split("|")
        datalist.pop()

        for object in datalist:
            objects.append(parseData(object))
            

    except:
        print("Failed to parse.")


    return objects