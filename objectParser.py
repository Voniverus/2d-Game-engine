import numpy as np


def parseData(data):
    object = []

    try:
        objectItems = data.split(":")
    
        pointStrings = objectItems[2][2:-2].split('], [')

        points = []

        for string in pointStrings:
            point = string.split(", ")
            points.append([float(i) for i in point])

        color = eval(objectItems[3])


        object = [int(objectItems[0]), np.array([float(i) for i in objectItems[1].strip('][').split(', ')]), np.array(points), color]

    except:
        print("Failed to parse.")

    return object


def parseList(data):
    objects = []

    print("PARSE:")
    print("data: {}".format(data))
    
    if "|" not in data:
        print("empty")
        return objects

    try:
        datalist = data.split("|")
        datalist.pop()

        for object in datalist:
            objects.append(parseData(object))
            
        print("objects: {}".format(objects))

    except:
        print("Failed to parse.")


    print()

    return objects