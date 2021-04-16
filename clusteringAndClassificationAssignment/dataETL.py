"""Extraction, transformation and loading of data.
"""

def extractData(filename: str) -> tuple:
    """Extract data from file.
    """
    
    with open(filename) as inf:
        lines = inf.readlines()
    
    # 244 genes
    # 148 cell lines
    
    titles = lines.pop(0)
    genenames = titles.split(',')
    genenames.pop(0)
    
    celllinenames = []
    celllines = []
    for line in lines:
        cellline = line.split(',')
        celllinename = cellline.pop(0)
        for i, thing in enumerate(cellline):
            cellline[i] = float(thing)
        
        celllinenames.append([celllinename])
        celllines.append(cellline)
    
    return celllines, celllinenames, genenames
    

def selectData(data: list) -> list:
    """Select the desired data.
    """
    # Desired data
    listOfCellLineNumbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147]
    
    selected = []
    for number in listOfCellLineNumbers:
        selected.append(data[number-1])
    
    return selected

def extractLabels(file:str) -> list:
    """Extract labels from csv file where names are in 2nd column and labels in the 4th.
    """
    with open(file) as inf:
        lines = inf.readlines()

    titles = lines.pop(0)
    
    celllinenames = []
    labels = []
    d = {}
    for line in lines:
        cellline = line.split(',')
        celllinename = cellline[1]
        label = cellline[3].rstrip()
        d[celllinename] = label
    #     celllinenames.append(celllinename)
    #     labels.append(label)
    # 
    # selectedCelllines = selectData(celllinenames)
    # selectedLabels = selectData(labels)
    # 
    # d = {}
    # for i, cell in enumerate(selectedCelllines):
    #     d[cell] = selectedLabels[i]
    return d
        
