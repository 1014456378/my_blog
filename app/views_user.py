import functools
import random
from datetime import datetime

from flask import Blueprint, jsonify
from flask import g
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask_mail import Message, Mail
from app import models
from app.models import db, User, Article
from app.utils import qiniu_upload
from app.utils.captcha.captcha import captcha
mail = Mail()
user_blueprint = Blueprint('user_b',__name__,url_prefix='/user')

@user_blueprint.route('/image_code')
def image_code():
    #生成图片验证码
    name,text,image = captcha.generate_captcha()
    response = make_response(image)
    #文件标准，告诉前端是啥类型的
    response.mimetype = 'image/png'
    # 验证码的文本
    print(text)
    session['image_code'] = text
    return response

@user_blueprint.route('/email_code')
def email_code():
    image_code = request.args.get('image_code')
    user_mail = request.args.get('mail')
    if image_code != session['image_code']:
        return jsonify(result = 1)   #图片验证码不正确
    #其中subject为邮件标题。 sender为发送方，如果你设置了 “MAIL_DEFAULT_SENDER”，
    # 就不必再次填写发件人，默认情况下将会使用配置项的发件人。
    # recipients为接收方，可以设置一个或者多个收件人，也可以后续再添加。
    msg = Message(subject="李豪的博客注册验证",recipients=[user_mail])
    mail_code = str(random.randint(1000,9999))
    print(mail_code)
    msg.body = "验证码为%s" % mail_code
    # mail.send(msg)
    session['mail_code'] = mail_code
    return jsonify(result = 0)

@user_blueprint.route('/register',methods=['POST'])
def register():
    user_mail = request.form.get('user_mail')
    mail_code = request.form.get('mail_code')
    pwd = request.form.get('pwd')
    print(user_mail,mail_code,pwd)
    if not all([user_mail,mail_code,pwd]):
        return jsonify(result=1)#参数有空
    if mail_code!=str(session['mail_code']):
        return jsonify(result=2)#邮箱验证码不正确
    user = User.query.filter_by(email = user_mail).count()
    print(user)
    if user:
        return jsonify(result=3)#用户已存在
    user = User()
    user.email = user_mail
    user.password = pwd
    db.session.add(user)
    db.session.commit()
    return jsonify(result=0)

@user_blueprint.route('/login',methods=['POST'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not all([email,pwd]):
        return jsonify(result = 3)
    user = User.query.filter_by(email = email).first()
    if  not user:
        return jsonify(result = 1)
    check_result = user.check_pwd(pwd)
    pic = user.pic
    name = user.name
    if check_result:
        session['user_id']=user.id
        return jsonify(result = 0,pic = pic,name=name)#登陆成功
    else:
        return jsonify(result = 2)#登录失败

def yanzheng(fun):
    @functools.wraps(fun)
    def fun1(*args,**kwargs):
        if 'user_id' in session:
            g.user = User.query.get(session['user_id'])
        else:
            return redirect('/')
        return fun(*args,**kwargs)
    return fun1


@user_blueprint.route('/')
@yanzheng
def user():
    return render_template('/news/user.html',title='用户中心')

@user_blueprint.route('/user_base_info',methods=['GET','POST'])
@yanzheng
def user_base_info():
    if request.method=='GET':
        return render_template('/news/user_base_info.html')
    name = request.form.get('name')
    if not name:
        return jsonify(result=1)
    g.user.name = name
    db.session.commit()
    return jsonify(result=0)


@user_blueprint.route('/user_pic_info',methods=['GET','POST'])
@yanzheng
def user_pic_info():
    user=g.user
    if request.method=='GET':
        return render_template('/news/user_pic_info.html')
    pic = request.files.get('pic')
    print(pic)
    if not pic:
        return jsonify(result=1)
    pic_name = qiniu_upload.upload(pic)
    user.pic=pic_name
    db.session.commit()
    return jsonify(result=0,pic=user.pic_url)

@user_blueprint.route('/user_pass_info',methods=['GET','POST'])
@yanzheng
def user_pass_info():
    if request.method=='GET':
        return render_template('/news/user_pass_info.html')
    old_pass = request.form.get('old_pass')
    new_pass1 = request.form.get('new_pass2')
    new_pass2 = request.form.get('new_pass2')
    if not all([old_pass,new_pass1,new_pass2]):
        return jsonify(result=1)
    user = g.user
    pass_yanzheng = user.check_pwd(old_pass)
    if not pass_yanzheng:
        return jsonify(result=2)
    if new_pass1 != new_pass2:
        return jsonify(result=3)
    user.password = new_pass1
    db.session.commit()
    return jsonify(result=0)

@user_blueprint.route('/user_collection')
@yanzheng
def user_collection():
    user = g.user
    page = int(request.args.get('page','1'))
    pagination = user.collect.paginate(page,6,False)
    total_page = pagination.pages
    user_collection_list = pagination.items
    return render_template('/news/user_collection.html',page=page,total_page=total_page,col_list = user_collection_list)
    
@user_blueprint.route('/user_news_list')
def user_news_list():
    page = int(request.args.get('page',1))
    art = Article.query.order_by(Article.time.desc())
    pagination = art.paginate(page,5,False)
    total_page = pagination.pages
    art_list = pagination.items

    return render_template('/news/user_news_list.html',total_page=total_page,art_list=art_list,page=page)

@user_blueprint.route('/user_news_edit',methods=['GET','POST'])
def user_news_edit():
    if not g.user.isMaster:
        return redirect('/')
    if request.method=='GET':
        return render_template('/news/user_news_edit.html')
    title = request.form.get('title')
    content = request.form.get('content')
    art = Article()
    art.title = title
    art.content = content
    db.session.add(art)
    db.session.commit()
    return redirect('/user/user_news_list')
@user_blueprint.route('/user_news_release',methods=['GET','POST'])
def user_news_release():
    if not g.user.isMaster:
        return redirect('/')
    if request.method=='GET':
        title = request.args.get('title')
        art = Article.query.filter_by(title = title).first()
        return render_template('/news/user_news_release.html',art = art)
    title = request.form.get('title')
    content = request.form.get('content')
    id = request.form.get('id')
    art = Article.query.get(id)
    art.title = title
    art.content = content
    art.time = datetime.now()
    db.session.commit()
    return redirect('/user/user_news_list')








