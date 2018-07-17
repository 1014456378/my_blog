from flask import Blueprint
from flask import render_template

detail_blueprint = Blueprint('detail_b',__name__,'detail')

@detail_blueprint.route('/detail/<int:text_id>')
def detail(text_id):
    return render_template('news/detail.html')