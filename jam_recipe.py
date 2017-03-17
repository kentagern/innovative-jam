import requests
import sys
from random import randrange



# generate a name
# pull synonyms of main ingredient and select one randomly
# we don't care about language here - we are exporting, after all
def getJamName(seed):
    synonyms = (requests.get("http://api.conceptnet.io/query?rel=/r/Synonym&node=/c/en/" + seed).json())['edges']
    if len(synonyms) == 0:
        return 0

    rint = randrange(len(synonyms))
    return synonyms[rint]['start']['label']


def getDescriptor():
    return ' a rather innovative jam'


def readFileLines():
    filename = open(sys.argv[1], "r")
    f = filename.readlines()
    filename.close
