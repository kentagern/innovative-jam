import requests
import sys
from sets import Set
from random import randrange

food_types = []
jam_types = []
non_latin_langs = []
ingredients = []
countries = []
adjectives = []
starter_adjectives = [] # as above but includes adjectives that can only go at the start
hashtags = []
meals = []


def file_to_array(the_file):
    filename = open(the_file, "r")
    the_array = []
    
    for line in filename:
        the_array.append(line.strip())
    filename.close
    
    return the_array


# strip indefinite articles and convert to lowercase
def sanitise_label(label):
    if label[:3] == "an " or label[:3] == "An ":
        label = label[3:]
                
    if label[:2] == "a " or label[:2] == "A ":
        label = label[2:]
    
    return label.lower()


def get_edge_labels(apistring):
    res = (requests.get(apistring).json())['edges']
    
    labels = []
    
    for i in range(0, len(res)):
        newlabel = res[i]['start']['label']
        if newlabel is not None:
            labels.append(sanitise_label(newlabel))
            
    return labels


def set_up_vars():
    global food_types
    global jam_types
    global non_latin_langs
    global ingredients
    global countries
    global adjectives
    global starter_adjectives
    global hashtags
    global meals
    
    # we create sets and then turn into lists to easily remove duplicates
    set_food_types = Set(file_to_array('res/foodtypes.txt'))
    food_types = list(set_food_types)
    
    set_jam_types = Set(file_to_array('res/jamtypes.txt'))
    jam_types = list(set_jam_types)

    set_non_latin_langs = Set(file_to_array('res/nonlatinlangs.txt'))
    non_latin_langs = list(set_non_latin_langs)

    set_countries = Set(file_to_array('res/countries.txt'))
    countries = list(set_countries)

    set_adjectives = Set(file_to_array('res/adjectives.txt'))
    adjectives = list(set_adjectives)

    # also use the above list as a basis for our starter adjectives
    set_adjectives.update(Set(file_to_array('res/starter_adjectives.txt')))    
    starter_adjectives = list(set_adjectives)
    
    set_hashtags = Set(file_to_array('res/hashtags.txt'))
    hashtags = list(set_hashtags)
    
    set_meals = Set(file_to_array('res/meals.txt'))
    meals = list(set_meals)

    set_ingredients = Set([])
    # pull types of food
    for ftype in food_types:
        set_ingredients.update(get_edge_labels("http://api.conceptnet.io/query?rel=/r/IsA&limit=200&node=/c/en/" + ftype))

    ingredients = list(set_ingredients)
    
    

def get_ingredient():
    return ingredients[randrange(0, len(ingredients))]



def get_country():
    return countries[randrange(0, len(countries))]



def get_adjective():
    return adjectives[randrange(0, len(adjectives))]



def get_starter_adjective():
    return starter_adjectives[randrange(0, len(starter_adjectives))]



def get_jam_type():
    return jam_types[randrange(0, len(jam_types))]


def get_meal():
    return meals[randrange(0, len(meals))]


# get a random edge returned by [apistring]
def get_word(apistring):
    res = (requests.get(apistring).json())['edges']
    if len(res) == 0:
        return 0
    
    rint = randrange(len(res))
    return res[rint]['start']


# generate a name which is a synonym of [seed]
# we don't care about language here - we are exporting, after all
#    foreign languages will probably make it more appealing, right?
def get_jam_name(seed):
    jword = get_word("http://api.conceptnet.io/query?rel=/r/Synonym&limit=100&node=/c/en/" + seed)
    
    # if we didn't get a result we'll just use the ingredient
    # how unoriginal
    if jword == 0 or jword is None:
        jname = seed
        jname = jname + " " + get_jam_type()

    else:
        jname = sanitise_label(jword['label'])
        
        # we don't want to add jam types to non-latin languages
        # it would look weird
        if jword['language'] not in non_latin_langs:
            jname = jname + " " + get_jam_type()
        
    return jname



# get a hashtag, including jname as an option
def get_hashtag(jname):
    # add some temporary tags based on the current name
    # we strip whitespace from them to make them more hashtaggeriffic
    temptags = ["".join(jname.split()), "".join(get_adjective().split()) + "".join((jname.split()))]
    temptags += hashtags
    return "#" + temptags[randrange(0, len(temptags))]


# make sure a given jstring is less than 140 chars
# if its more we try to return a simple hashtag
# if its still more we return jname
# if jname > 140, we return a clipped version of jname
def clipped_str(jname, jstring):
    
    if len(jstring) <= 140:
        return jstring
    elif len(jname) > 140:
        return jname[:140]
    else:
        hashtag = get_hashtag()
        if (len(jname) + len(hashtag)) <= 140:
            return jname + hashtag
        else:
            return jname


# get a random description
def get_full_tweet(jname):
    rint = randrange(0,5)
    
    # [jamname]: the people of [country] will love this [adj] [jamtype] [hashtag]
    if rint == 0:
        jstring = jname + ": the people of " + get_country() + " will love this " + get_adjective() + " " + get_jam_type() + " " + get_hashtag(jname)
    
    # [country] needs [jamname] [hashtag]
    elif rint == 1:
        jstring = get_country() + " needs " + jname + " " + get_hashtag(jname)
    
    # [adj] [adj] [jamname] [hashtag] [hashtag]
    elif rint == 2:
        jstring = get_starter_adjective() + " " + get_adjective() + " " + jname + " " + get_hashtag(jname) + " " + get_hashtag(jname)
    
    
    # [jamname] : a [adj] [jamtype] made with [ingredient] [hashtag]
    elif rint == 3:
        kingr = get_ingredient()
        jstring = jname + ": a " + get_adjective() + " " + get_jam_type() + " made with " + get_ingredient() + " " + get_hashtag(kingr) + " " + get_hashtag(jname)
    
    # why not spice up your [meal] with [adj] [jam]    
    elif rint == 4:
        jstring = "why not spice up your " + get_meal() + " with " + get_adjective() + " " +  jname + " " + get_hashtag(jname)
    
    
    
    return clipped_str(jname, jstring)








