from flask import request, render_template
import requests
from app import app
from .forms import PokemonInput

# Home route, greeting page with or without a name
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/<user>')
def greeting(user):
     return render_template('home.html', user=user)

# Pokemon API function and route to get and return info
def pokemon_info(name_or_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{name_or_id}'
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
    return 404

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    form = PokemonInput()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data
        pokedata = pokemon_info(pokemon)
        return render_template('pokemon.html', pokedata=pokedata, form=form)
    else:
        return render_template('pokemon.html', form=form)