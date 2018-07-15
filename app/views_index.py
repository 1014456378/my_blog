from flask import Blueprint
from flask import render_template
from app import models
from app.models import db
index_blueprint = Blueprint('index_b',__name__)

@index_blueprint.route('/')
def index():
    # articlee = models.Article(title='python之flask学习', content='我使用flask制作个人博客，这是第一篇文章')
    # db.session.add(articlee)
    # db.session.commit()
    article = models.Article.query.all()
    return render_template('news/index.html',article = article)