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
nationalities = []
opinion_phrases = []


def file_to_set(the_file):
    filename = open(the_file, "r")
    the_set = Set([])
    
    for line in filename:
        the_set.add(line.strip())
        
    filename.close
    
    return the_set


# strip indefinite articles and convert to lowercase
def sanitise_label(label):
    if label[:3] == "an " or label[:3] == "An ":
        label = label[3:]
                
    if label[:2] == "a " or label[:2] == "A ":
        label = label[2:]
    
    return label.lower()


# get sanitised edge labels from a given api string
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
    global nationalities
    global opinion_phrases
    
    # we create sets and then turn into lists to easily remove duplicates
    food_types = list(file_to_set('res/foodtypes.txt'))

    jam_types = list(file_to_set('res/jamtypes.txt'))

    non_latin_langs = list(file_to_set('res/nonlatinlangs.txt'))

    countries = list(file_to_set('res/countries.txt'))

    adjectives = list(file_to_set('res/adjectives.txt'))

    # also use the above list as a basis for our starter adjectives   
    starter_adjectives = list(file_to_set('res/starter_adjectives.txt')) + adjectives
 
    hashtags = list(file_to_set('res/hashtags.txt'))

    meals = list(file_to_set('res/meals.txt'))

    nationalities = list(file_to_set('res/nationalities.txt'))

    opinion_phrases = list(file_to_set('res/unlikely_opinion_phrases.txt'))

    set_ingredients = Set([])
    # pull types of food
    for ftype in food_types:
        set_ingredients.update(get_edge_labels("http://api.conceptnet.io/query?rel=/r/IsA&limit=200&node=/c/en/" + ftype))

    ingredients = list(set_ingredients)
    

def get_rand_element(the_array):
    return the_array[randrange(0, len(the_array))]


def get_ingredient():
    return get_rand_element(ingredients)

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
        jname = jname + " " + get_rand_element(jam_types)

    else:
        jname = sanitise_label(jword['label'])
        
        # we don't want to add jam types to non-latin languages
        # it would look weird
        if jword['language'] not in non_latin_langs:
            jname = jname + " " + get_rand_element(jam_types)
        
    return jname



# get a hashtag, including jname as an option
def get_hashtag(jname):
    # add some temporary tags based on the current name
    # we strip whitespace from them to make them more hashtaggeriffic
    temptags = ["".join(jname.split()), "".join(get_rand_element(adjectives).split()) + "".join((jname.split())), "".join(jname.split()) + "ontoast", "brexitmeans" + "".join(jname.split()), "".join(jname.split()) + "please"]
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
        hashtag = get_hashtag(jname)
        if (len(jname) + len(hashtag) + 1) <= 140:
            return jname + " " + hashtag
        else:
            return jname


# get a random description
def get_full_tweet(jname):
    rint = randrange(5,6)
    
    # [jamname]: the [peoplegroup] of [country] [will have some opinion] [adj] [jamtype] [hashtag]
    if rint == 0:
        jstring = jname + ": the " + get_rand_element(nationalities) + " of " + get_rand_element(countries) + " " + get_rand_element(opinion_phrases) + " " + get_rand_element(adjectives) + " " + get_rand_element(jam_types) + " " + get_hashtag(jname)
    
    # [country] needs [jamname] [hashtag]
    elif rint == 1:
        jstring = get_rand_element(countries) + " needs " + jname + " " + get_hashtag(jname)
    
    # [adj] [adj] [jamname] [hashtag] [hashtag]
    elif rint == 2:
        jstring = get_rand_element(starter_adjectives) + " " + get_rand_element(adjectives) + " " + jname + " " + get_hashtag(jname) + " " + get_hashtag(jname)
    
    # [jamname] : a [adj] [jamtype] made with [ingredient] [hashtag]
    elif rint == 3:
        kingr = get_ingredient()
        jstring = jname + ": a " + get_rand_element(adjectives) + " " + get_jam_type() + " made with " + get_rand_element(ingredients) + " " + get_hashtag(kingr) + " " + get_hashtag(jname)
    
    # why not spice up your [meal] with [adj] [jam]    
    elif rint == 4:
        sint = randrange(0,3)
        if sint == 0:
            jstring = "why not "
        elif sint == 1:
            jstring = "this weekend, "
        else:
            jstring = ""
        jstring = jstring + "spice up your " + get_rand_element(meals) + " with " + get_rand_element(adjectives) + " " +  jname + " " + get_hashtag(jname)
    
    # Hi #[peoplegroup]! Have you thought about importing [adj] [jname] to your native [country]? [hashtag]
    elif rint == 5:
        jstring = "Hi #" + get_rand_element(nationalities) + "! Have you thought about importing " + get_rand_element(adjectives) + " " + jname + " to your native " + get_rand_element(countries) + "? " + get_hashtag(jname)
        

    
    return clipped_str(jname, jstring)
