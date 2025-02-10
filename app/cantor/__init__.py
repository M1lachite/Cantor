from flask import Blueprint

bp = Blueprint('cantor', __name__, template_folder='templates')

from app.cantor import routes