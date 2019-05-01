from flask import Flask, request
import json
import requests


app = Flask('bootcamp-app')

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    body = request.values['Body'].lower()
    
    types = [0,'normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy']
    superEffective = []
    notVeryEffective = []
    notEffective = []
    
    if body in types:
        type = requests.get('https://pokeapi.co/api/v2/type/'+str(types.index(body)))
        typeData = json.loads(type.content)
        typeRelations = typeData['damage_relations']
        sprite = False
        
        def typestring(key,listName):
            if typeRelations[key]:
                for i in typeRelations[key]:
                    thisType = str(i['name']).capitalize()
                    if thisType not in listName:
                        listName.append(thisType)
    
        typestring('no_damage_from', notEffective)
        typestring('half_damage_from', notVeryEffective)
        typestring('double_damage_to', notVeryEffective)
        typestring('double_damage_from', superEffective)
        # typestring('half_damage_to', superEffective)
        typestring('no_damage_to', superEffective)
    else:  
        typeName = []
    
        if body == 'jordan':
            body = 'squirtle'
            sprite = 'https://i.imgur.com/mN1efdX.png'
        else: sprite = False
        
        pokemon = requests.get('https://pokeapi.co/api/v2/pokemon/'+body)
        pokemonData = json.loads(pokemon.content)
        if not sprite:
            sprite = pokemonData['sprites']['front_default']
        
        def typestring(key,listName):
            for x in typeName:
                if typeRelations[key]:
                    for i in typeRelations[key]:
                        thisType = str(i['name']).capitalize()
                        if (thisType not in listName) and (thisType not in notEffective):
                            if thisType in notVeryEffective:
                                notVeryEffective.remove(thisType)
                            elif thisType in superEffective:
                                superEffective.remove(thisType)
                            else:
                                listName.append(thisType)
                                
        for i in pokemonData['types']:
            typeName.append(str(i['type']['name']).capitalize())
            typeUrl = i['type']['url']
            type = requests.get(typeUrl)
            typeData = json.loads(type.content)
            typeRelations = typeData['damage_relations']
            
            typestring('no_damage_from', notEffective)
            typestring('half_damage_from', notVeryEffective)
            typestring('double_damage_to', notVeryEffective)
            typestring('double_damage_from', superEffective)
            # typestring('half_damage_to', superEffective)
            typestring('no_damage_to', superEffective)
        
    if superEffective:
        superEffective = '\nUSE: ' + ', '.join(superEffective)
    else: superEffective = ''
    if notVeryEffective:
        notVeryEffective = '\nAVOID: ' + ', '.join(notVeryEffective)
    else: notVeryEffective = ''
    if notEffective:
        notEffective = '\nDON\'T USE: ' + ', '.join(notEffective)
    else: notEffective = ''
    
    if sprite:
        return '<?xml version="1.0" encoding="UTF-8" ?><Response><Message>' + ''\
        '<Media>' + str(sprite) + '</Media>' + ''\
        '<Body>Type: ' + ', '.join(typeName) + ''\
        '\n' + superEffective + notVeryEffective + notEffective + '</Body></Message></Response>'
    else:
        return '<?xml version="1.0" encoding="UTF-8" ?><Response><Message>' + ''\
        '' + superEffective + notVeryEffective + notEffective + '</Message></Response>'

app.run(debug=True, host='0.0.0.0', port=8080)
