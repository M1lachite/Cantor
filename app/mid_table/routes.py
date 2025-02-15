from flask import render_template, request
from app.mid_table import bp
from app.mid_table.MidTable import MidTable
from app.main.BaseService import BaseService

@bp.route('/')
def index():
    base_service = BaseService()
    date_str = base_service.get_valid_date(request.args.get('date') or base_service.date)

    mid_table = MidTable(base_service, date_str)
    table_data = mid_table.get_table()

    if isinstance(table_data, str):
        return render_template('MidTable/index.html', error=table_data, date=date_str)

    return render_template('MidTable/index.html', table_data=table_data, date=date_str)
