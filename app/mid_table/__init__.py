from flask import Blueprint

bp = Blueprint('MidTable', __name__, template_folder='templates')

from app.mid_table import routes