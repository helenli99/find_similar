#
# Seng 474
# A1 LSH Finding similar items

# question_4k Apprx 1mins:30s

import pandas as pd

def main():
    file_name = './question_4k.tsv'

    df = pd.read_csv(file_name, sep='\t')

    lines = [line.rstrip('\n') for line in open(file_name)]

    words = []
    indexArray = []

    # split the sentence to word by words
    for i in lines:
        tempWords = []
        if len(i.split('\t')) == 2:
            indexArray.append(i.split('\t')[0])
            for j in i.split('\t')[1].split(' '):
                tempWords.append(j)
            words.append(tempWords)

    result = {}
    index = 1
    index2 = 2


    # use the the formula to calculate the similarity
    for i1 in range(1, len(words)):
        temp = {str(indexArray[i1]):[]}
        result.update(temp)
        for i2 in range(1, len(words)):
            num_u = getu(words[i1], words[i2])
            num_n = getn(words[i1], words[i2])
            if sim(num_u, num_n) is True and i1 != i2:
                result[str(indexArray[i1])].append(indexArray[i2])
        index = index + 1
        index2 = index2 + 1


    formatResult = ["qid similar-qids\n"]

    # use the writer to output as a tsv file before output store in to the arrary
    for item in result:
        tempString = str(item) + ' '
        index = 0
        if len(result[str(item)]) == 0:
            tempString = tempString + '\n'
        else:
            for i in result[str(item)]:
                if index == len(result[str(item)]) - 1:
                    tempString = tempString + str(i) + '\n'
                else:
                    tempString = tempString + str(i) + ','
                index = index + 1
        formatResult.append(tempString)


        # open a file and write out.
        f = open("question_sim_4k.tsv", "w+")
        for items in formatResult:
            f.write(items)
        f.close()


# to get the intersection
def getu(i1, i2):
    count = []
    for item in i1:
        if item in i2:
            if item not in count:
                count.append(item)

    return len(count)

# to get the union
def getn(i1, i2):
    count = []
    for item in i1:
        if item not in count:
            count.append(item)
    for item in i2:
        if item not in count:
            count.append(item)

    return len(count)


# to calculate the similarity
def sim(i1, i2):
    if i1 == 0 or i2 == 0:
        return False

    if float(i1)/float(i2) >= 0.6:
        return True
    else:
        return False

# main function
if __name__=="__main__":
    main()
