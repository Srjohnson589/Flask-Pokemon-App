from flask import request, render_template
import requests
from app import app
from .forms import PokemonInput, SignUpInput, LoginInput

# Home route, greeting page with or without a name
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/<user>')
def greeting(user):
     return render_template('home.html', user=user)

# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginInput()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        submit_btn = form.submit_btn.data
        return render_template('login.html', form=form, username=username, password=password, submit_btn=submit_btn)
    else:
        return render_template('login.html', form=form)

# Signup route
@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpInput()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        submit_btn = form.submit_btn.data
        return render_template('signup.html', form=form, username=username, email=email, password=password, submit_btn=submit_btn)
    else:
        return render_template('signup.html', form=form)

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