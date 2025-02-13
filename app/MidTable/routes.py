from flask import render_template, request
from app.MidTable import bp
from app.MidTable.MidTable import MidTable
from app.cantor.BaseService import BaseService  # ← Import BaseService
from datetime import datetime

@bp.route('/')
def index():
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    base_service = BaseService()
    mid_table = MidTable(base_service, date)
    table_data = mid_table.get_table()

    if isinstance(table_data, str):
        return render_template('MidTable/index.html', error=table_data)

    return render_template('MidTable/index.html', table_data=table_data)
