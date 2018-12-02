import pickle

# layer 0: Background Objects
# layer 1: Foreground Objects
objects = [[], [], []]


def add_object(o, layer):
    objects[layer].append(o)


def add_objects(l, layer):
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def remove_object_in_layer(layer):
    while len(objects[layer]) > 0:
        data_deleted = objects[layer].pop()
        del data_deleted
        #global objects=[[], [], []]


def clear():
    for l in objects:
        l.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o


def save():
    with open('game.sav', 'wb') as f:
        pickle.dump(objects, f)


def load():
    global objects
    with open('game.sav', 'rb') as f:
        objects = pickle.load(f)
