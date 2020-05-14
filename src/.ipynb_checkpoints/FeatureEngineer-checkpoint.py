import datetime
import string
import numpy as np

def mkdict(L):
    d = {}
    for n in L:
        d[n] = 1
    return d

def combineDict(d1, d2):
    d = d1.copy()
    for key in d2.keys():
        if key in d1:
            d[key] += 1
        else:
            d[key] = 1
    return d

def getGenres(L):
    result = []
    for d in L:
        if 'id' in d:
            result.append(d['id'])
    return result

def get_name(line):
    return line[0]

def get_age(line):
    if line[1] == 0:
        return 0
    else:
        return (1)
        


def feature_engineer(line, devCounts, pubCounts, genres):
    '''header = ['name', 'required_age', 'windows', 'mac', 'linux', 'release_date', 
                
    
                'price']'''
    #future features: company, genre, 
    result = []
    
    #name
    result.append(get_name(line))
    
    #required_age
    result.append(get_age(line))
    
    #which platforms
    platforms = line[5]
    result.append(int(platforms['windows']))
    result.append(int(platforms['mac']))
    result.append(int(platforms['linux']))
    
    #release_date
    '''
    date = line[8]
    if 'date' in date: 
        release_date = datetime.datetime.strptime(date['date'], '%b %d, %Y').date()
        result.append(release_date)
    else:
        result.append(None)
    '''
    
    #min_reqs
    reqs = line[7]
    #min_mem
    if reqs and isinstance(reqs, dict) and 'minimum' in reqs:
        min_reqs = reqs['minimum']
        if 'Memory' in min_reqs:
            start = min_reqs.index('Memory')
            past = min_reqs[start:].split(' ')
            for i in range(len(past)-1):
                word = past[i]
                if word.isdigit():
                    nextword = past[i+1]
                    if nextword == 'MB':
                        result.append(int(word)/1024.0)
                        break
                    else:
                        result.append(int(word))
                        break

        else:
            result.append(0)

        #min_storage        
        if 'Storage' in min_reqs:
            start = min_reqs.index('Storage')
            past = min_reqs[start:].split(' ')
            for i in range(len(past)-1):
                word = past[i]
                if word.isdigit():
                    nextword = past[i+1]
                    if nextword == 'MB':
                        result.append(int(word)/1024.0)
                        break
                    else:
                        result.append(int(word))
                        break
        else:
            result.append(0)
    
    else:
        result.append(0)
        result.append(0)

    #devs
    devVals = [0]*10
    maxdev = -1
    for dev in line[3]:
        if devCounts[dev] > maxdev:
            maxdev = devCounts[dev]
        
    if maxdev > 9:
        devVals[-1] = 1
    else:
        devVals[maxdev-1] = 1
        
    result = result + devVals
    
    if len(line[3]) > 1:
        result.append(1)
    else:
        result.append(0)
        
    result.append(maxdev)
        
    #pubs
    pubVals = [0]*12
    maxpub = -1
    for pub in line[4]:
        if pubCounts[pub] > maxpub:
            maxpub = pubCounts[pub]

    if maxpub > 11:
        pubVals[-1] = 1
    else:
        pubVals[maxpub-1] = 1
    result = result + pubVals
    
    if len(line[4]) > 1:
        result.append(1)
    else:
        result.append(0)
        
    result.append(maxpub)
        
    #Genres:
    genreList = list(genres.keys())
    numGenres = len(genres)+1
    hotGenres = [0]*numGenres
    for genre in line[6]:
        genreid = genre['id']
        genreIndex = genreList.index(genreid)
        hotGenres[genreIndex] = 1
    
    if line[6] == []:
        hotGenres[-1] = 1
        
    result = result + hotGenres
        
        
    #price
    prices = line[9]
    if line[2]:
        result.append(0)
    elif prices != '':
        #might have to do work w/ currencies
        result.append(prices['final']/100.0)
    else:
        result.append(None)

    return result


        
def feature_engineer_wrapper(rdd):
    developers = rdd.map(lambda x: x[3])
    publishers = rdd.map(lambda x: x[4])
    devCounts = developers.map(mkdict).reduce(combineDict)
    pubCounts = publishers.map(mkdict).reduce(combineDict)
    genres = rdd.map(lambda x: getGenres(x[6])).map(mkdict).reduce(combineDict)
    return rdd.map(lambda x: feature_engineer(x, devCounts, pubCounts, genres))

