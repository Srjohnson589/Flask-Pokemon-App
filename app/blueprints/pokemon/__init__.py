from flask import Blueprint

pokemon = Blueprint('pokemon', __name__, template_folder='poke_templates')

from . import routes