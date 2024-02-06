from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

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
            'name' : data['name'].title(),
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'sprite_img': data['sprites']['front_shiny'],
            'abilities' : [data['abilities'][x]['ability']['name'] for x in range(0, len(data['abilities']))]
        }
        return info_dict
    return None


@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
        pokedata = pokemon_info(pokemon)
        return render_template('pokemon.html', pokedata=pokedata)
    else:
        return render_template('pokemon.html')