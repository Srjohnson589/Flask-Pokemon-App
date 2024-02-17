from . import pokesearch
from flask import render_template, request, redirect, url_for, flash
from .forms import PokemonInput
from flask_login import current_user, login_required, LoginManager
from app.models import db, Pokemon, User, user_pokemon
import requests


# Home route, greeting page
@pokesearch.route('/')
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

@pokesearch.route('/get_pokemon', methods=['GET','POST'])
def get_pokemon():
    form = PokemonInput()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data
        pokedata = pokemon_info(pokemon)
        if form.submit_btn.data:
            return render_template('get_pokemon.html', pokedata=pokedata, form=form)
        if form.catch_btn.data:
            if not Pokemon.query.get(pokedata['name']):
                newpoke = Pokemon(pokedata['name'], pokedata['hp'], pokedata['attack'], pokedata['defense'], pokedata['sprite_img'])
                newpoke.save()
            if pokedata['name'] in current_user.caught_pokemon or len(current_user.caught_pokemon.all()) >= 6:
                flash(f'Pokemon already caught! Release one to catch another.', 'danger')
                return redirect(url_for('pokesearch.get_pokemon'))
            else:
                caughtpoke = Pokemon.query.get(pokedata['name'])
                current_user.caught_pokemon.append(caughtpoke)
                print(caughtpoke)
                db.session.commit()
                flash(f'{caughtpoke.name} caught!', 'success')
                return redirect(url_for('pokesearch.get_pokemon'))
    else:
        return render_template('get_pokemon.html', form=form)


@pokesearch.route('/release/<poke_name>')
@login_required
def release(poke_name):
    releasepoke = Pokemon.query.filter(Pokemon.name==poke_name).first()
    current_user.caught_pokemon.remove(releasepoke)
    db.session.commit()
    flash(f'{poke_name} has been released!', 'success')
    return redirect(url_for('pokesearch.get_pokemon'))

@pokesearch.route('/battle')
@login_required
def battle():
    users = User.query.filter(User.id != current_user.id)
    return render_template('battle.html', users=users)

@pokesearch.route('/match/<user_id>')
@login_required
def match(user_id):
    opponent = User.query.get(user_id)
    return render_template('match.html', opponent=opponent)