from flask import Blueprint, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session
from app.models import User, Article, db, Talk

detail_blueprint = Blueprint('detail_b',__name__)
@detail_blueprint.route('/detail/<int:text_id>')
def detail(text_id):
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    text = Article.query.get(text_id)
    talk_count = text.talk.count()
    return render_template('news/detail.html',text=text,title = '文章详情页',talk_count=talk_count)

@detail_blueprint.route('/collect',methods=['POST'])
def collect():
    flag = int(request.form.get('flag'))
    text_id = request.form.get('text_id')
    if 'user_id' not in session:
        return jsonify(result = 1)
    g.user = User.query.get(session['user_id'])
    collect_text = Article.query.get(text_id)
    if flag==1:
        if collect_text in g.user.collect:
            return jsonify(result = 2)
        g.user.collect.append(collect_text)
    else:
        if collect_text not in g.user.collect:
            return jsonify(result=2)
        g.user.collect.remove(collect_text)
    db.session.commit()
    return jsonify(result=0)

@detail_blueprint.route('/talk',methods=['POST'])
def talk():
    text_id = request.form.get('text_id')
    talk = Talk.query.filter_by(article_id = text_id,parent_id = None).order_by(Talk.time.desc())
    talk_list1 = []
    count = 0
    for i in talk:
        count+=1
        talk_list2 = []
        for j in i.parent:
            talk_list2.append({
                'id':j.id,
                'user_name':j.whotalk.name,
                'content':j.content
            })
        talk_list1.append({
            'id':i.id,
            'user_name':i.whotalk.name,
            'user_pic':i.whotalk.pic_url,
            'time':i.time,
            'content':i.content,
            's_talk':talk_list2
        })
    return jsonify(talk_list=talk_list1,count=count)

# @detail_blueprint.route('/get_talk')
# def get_talk():

