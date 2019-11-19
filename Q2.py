#
# Seng 474
# A1 LSH Finding similar items
# question_4k Apprx 10s
# question_50k Apprx 2mins:05s
# question_sim_150k Apprx 7mins:55s

import pandas as pd
import numpy as np
from fnv import *
import uuid


def main():

    file_name = './question_150k.tsv'

    df = pd.read_csv(file_name, sep='\t')
    lines = [line.rstrip('\n') for line in open(file_name)]
    data = np.char.split(lines)
    data2 = np.asarray(data)

    sentence_words = []
    indexArray = []
    dic = {}
    count = 0

    # to split the qid and body texts
    for i in range(1, len(data2)):
        if data2[i] != []:
            qid = data2[i].pop(0)
            indexArray.append(qid)
            sentence_words.append(data2[i])
            dic.update({qid:count})
            count = count + 1


    # D use to store the permutation with 6 minhash values
    D = []
    h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14 = {},{},{},{},{},{},{},{},{},{},{},{},{},{}
    D2 = [h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14]

    hashAB = []
    tableIndex = 0

    # use r * b different hash function to compute the random permutation
    for table in range(0, 14):
        hashTable = {}
        for i in range(0, 6):
            index = 0
            a = uuid.uuid4().int & (1<<64)-1
            b = uuid.uuid4().int & (1<<64)-1
            for sentence in sentence_words:
                signatures = []
                for word in sentence:
                    # hash the whole sentence words by words and store the mini value(minhash)
                    hashindex = word.encode('utf-8')
                    hashcode = hash(hashindex, bits=64)
                    hashint = hashF(hashcode, a, b)
                    # select the minhash
                    signatures.append(hashint)
                if str(indexArray[index]) not in hashTable:
                    hashTable.update({str(indexArray[index]):[]})
                hashTable[str(indexArray[index])].append(min(signatures))
                index = index + 1
        # append to the  hashTable
        D.append(hashTable)

        index = 0
        indexA = 0
        a1 = uuid.uuid4().int & (1<<64)-1
        b1 = uuid.uuid4().int & (1<<64)-1
        hashAB.append(a1)
        hashAB.append(b1)
        for i in range(0, len(indexArray)):
            # add the sum of the 6 minhash value and put into the corresponding hash function
            sumAll = sum(hashTable[indexArray[i]])
            hashint = (a1 * sumAll + b1) % 15373875993579943603
            if str(hashint) not in D2[tableIndex]:
                D2[tableIndex].update({str(hashint):[indexArray[i]]})
            else:
                # store into the new dictionary
                if str(indexArray[i]) not in D2[tableIndex][str(hashint)]:
                    D2[tableIndex][str(hashint)].append(indexArray[i])
        tableIndex = tableIndex + 1


    D3 = {}
    indexA = 0
    indexB = 1
    tableIndex = 0

    # find similar hash back into the table and travesel the hashtable to find the similar items
    for table in D2:
        a = hashAB[indexA]
        b = hashAB[indexB]
        for index in range(0, len(indexArray)):
            # add the sum of the 6 minhash value and hash back into corresponding hash function
            sumAll = sum(D[tableIndex][str(indexArray[index])])
            hashint = (a * sumAll + b) % 15373875993579943603
            if str(indexArray[index]) not in D3:
                D3.update({indexArray[index]:[]})
            if str(hashint) in table:
                tempTable = table[str(hashint)]
                # store all data and put it into a similar set
                for j in tempTable:
                    if j not in D3[str(indexArray[index])]:
                        D3[str(indexArray[index])].append(j)
        indexA = indexA + 2
        indexB = indexB + 2
        tableIndex = tableIndex + 1


    result = {}
    index = 0


    f = open("question_sim_150k.tsv", "w+")
    f.write("qid similar-qids\n")

    # linear search the similar set to delete the false positive similar set and also output as a tsv file.
    for item in D3:
        #result.update({str(indexArray[index]):[]})
        f.write(str(indexArray[index]) + ' ')
        if D3[item] != []:
            #I1 = sentence_words[indexArray.index(item)]
            I1 = sentence_words[int(dic[str(item)])]
            itemCount = 0
            for i in D3[item]:
                #I2 = sentence_words[indexArray.index(i)]
                I2 = sentence_words[int(dic[str(i)])]
                if I1 != I2:
                    u = getu(I1, I2)
                    n = getn(I1, I2)
                    if sim(u, n) is True:
                        if itemCount == len(D3[item]) - 1:
                            f.write(str(i))
                        else:
                            f.write(str(i) + ',')
                        #result[str(indexArray[index])].append(i)
                itemCount = itemCount + 1
            f.write('\n')
        index = index + 1
    f.close()


# to get the union
def getu(i1, i2):
    count = []
    for item in i1:
        if item in i2:
            if item not in count:
                count.append(item)

    return len(count)


# to get the intersection
def getn(i1, i2):
    count = []
    for item in i1:
        if item not in count:
            count.append(item)
    for item in i2:
        if item not in count:
            count.append(item)

    return len(count)


# calculate the similarity
def sim(i1, i2):
    if i1 == 0 or i2 == 0:
        return False

    if float(i1)/float(i2) >= 0.6:
        return True
    else:
        return False


# hash function use to hash the string.
def hashF(x,a,b):
    p = 15373875993579943603
    return (a * x + b) % p


# main function
if __name__=="__main__":
    main()
