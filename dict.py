import json
path = 'json_reglas/'

def json_a_dict(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)


def a_dict(dict_n, dict_e, key):
    for layer, i in dict_n.items():
        #print(f"layer: {layer}")
        #print(f"key: {key}")
        #print(f"i: {i}")
        dict_e[layer][key]=i
    return dict_e

arch = {}
#arch['layerMapping'] = json_a_dict(path+'layerMapping.json')
arch['maskNumbers'] = json_a_dict(path+'maskNumbers.json')
arch['layerMaterials'] = json_a_dict(path+'layerMaterials.json')

reglas = json_a_dict(path+'layerMapping.json')

for k, val in arch.items():
    #print(f"key: {k}")
    reglas = a_dict(val, reglas, str(k))

with open('reglas.json', 'w') as json_file:
    json.dump(reglas, json_file, indent=4)