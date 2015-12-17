from pprint import pprint
import pickle

def toDict(filename):
    """
    Takes a local txt file output from word2vec 
    and returns it as a python dictionary
    following the convention

        { 
            WORD (str) : Vector (float)
            ...
        }

    """
    d = {}
    raw = [line for line in open(filename, 'r')]

    for line in raw:
        content = line.split()
        word = content[0]
        #ignore last char, it is a newline
        vector = [ float(val) for val in content[1: (len(content)-1) ] ]
        d[word] = vector
        
    return d

def fruitToDict(d, filename):
    """
    Opens a filename of fruit
    extracts vectors for found fruits
    """
    fruitDict = {}

    raw = [line for line in open(filename, 'r')]
    for fruitname in raw:
        lowercase = "".join((fruitname.lower() ).split())
        print("Looking up: {0}".format(lowercase))
        if lowercase in d:
            fruitDict[lowercase] = d[lowercase]
            print("Found!")
        else:
            print("Not found!")

    return fruitDict 
    
if __name__ == "__main__":
    d = toDict("./vectors_100k.txt")

    """
    with open('vectors_100k.pickle', 'wb') as outfile:
        pickle.dump(d, outfile)
    """
    fruit_file = "./fruit.txt"
    not_fruit = "./notfruit.txt"

    compost= "./compostable.txt"
    trash= "./trash.txt"
    paper= "./paper.txt"
    cans= "./cans_bottles.txt"
   
    compost_dict = fruitToDict(d,compost)
    print len(compost_dict)
    trash_dict = fruitToDict(d,trash)
    print len(trash_dict)
    paper_dict = fruitToDict(d,paper)
    print len(paper_dict)
    cans_dict = fruitToDict(d,cans)
    print len(cans_dict)


    with open('compost_VECTORS.pickle', 'wb') as outfile:
        pickle.dump(compost_dict, outfile)

    with open('trash_VECTORS.pickle', 'wb') as outfile:
        pickle.dump(trash_dict, outfile)

    with open('paper_VECTORS.pickle', 'wb') as outfile:
        pickle.dump(paper_dict, outfile)

    with open('cans_VECTORS.pickle', 'wb') as outfile:
        pickle.dump(cans_dict, outfile)

    """
    with open('vectors_100k.pickle', 'rb') as infile:
        d = pickle.load(infile)
    """
    """
    f = fruitToDict(d,fruit_file)
    print len(f)
    not_f = fruitToDict(d, not_fruit )
    print len(not_f)
    with open('fruitVectors.pickle', 'wb') as outfile:
        pickle.dump(f, outfile)
    with open('notFruitVectors.pickle', 'wb') as outfile:
        pickle.dump(not_f, outfile)
    """
