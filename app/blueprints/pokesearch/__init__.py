from flask import Blueprint

pokesearch = Blueprint('pokesearch', __name__, template_folder='poke_templates')

from . import routes