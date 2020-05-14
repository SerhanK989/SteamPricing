import ast

def transformRow(line):
    #function that takes in a list of values corresponding to the columns
    #and parses them in the way that we want
    splitted = line.split('#serhan#')
    result = []
    result.append(splitted[0])
    for val in splitted[1:-1]:
        if val != '':
            if val[0] == '{':
                backI = len(val) - val[::-1].index('}')
                val = val[0:backI]
            result.append((ast.literal_eval(val)))
        else:
            result.append('')
    if splitted[-1] == '':
        result.append('')
    else:
        result.append((ast.literal_eval(splitted[-1])))
            
    return result

def clean_data(rdd):
    #format data
    
    cleaned = rdd.map(transformRow)
    #remove invalid prices
    #priced = cleaned.filter(lambda x: x[-1] != '')
    
    return cleaned
    