from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/<user>')
def greeting(user):
     return render_template('home.html', user=user)

def pokemon_info(name_or_id):
    inpt = str(name_or_id)
    url = f'https://pokeapi.co/api/v2/pokemon/{inpt}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        info_dict = {
            'name' : data['name'],
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'sprite_img': data['sprites']['front_shiny'],
            'abilities' : []
        }
        abilities = data['abilities']
        for index in range(0, len(abilities)):
            if index == len(abilities)-1:
                info_dict['abilities'] += abilities[index]['ability']['name']
            else:
                info_dict['abilities'] += abilities[index]['ability']['name'] + ", "
        return info_dict
    return None


@app.route('/pokemon', method=['GET','POST'])
def pokemon():
    if request.method == 'POST':
        pass
    else:
        return render_template('pokemon.html')