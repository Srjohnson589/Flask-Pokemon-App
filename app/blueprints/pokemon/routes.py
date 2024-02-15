from . import pokemon
from flask import render_template, request, redirect, url_for, flash
from .forms import PokemonInput
from flask_login import current_user, login_required, LoginManager
from app.models import db, Pokemon, User, user_pokemon
import requests


# Home route, greeting page
@pokemon.route('/')
def home():
    return render_template('home.html')


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
    return False

@pokemon.route('/pokemon', methods=['GET','POST'])
def pokemon():
    form = PokemonInput()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data
        pokedata = pokemon_info(pokemon)
        if form.submit_btn.data:
            return render_template('pokemon.html', pokedata=pokedata, form=form)
        if form.catch_btn.data:
            if not Pokemon.query.get(pokedata['name']):
                newpoke = Pokemon(pokedata['name'], pokedata['hp'], pokedata['attack'], pokedata['defense'], pokedata['sprite_img'])
                newpoke.save()
            user_pokemon.name = pokedata['name']
            user_pokemon.user_id = current_user.user_id
            flash(f'{newpoke.name} caught!', 'success')
            return redirect(url_for('pokemon.pokemon')) 
    else:
        return render_template('pokemon.html', form=form)
    
