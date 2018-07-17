import functools
import random
from flask import Blueprint, jsonify
from flask import g
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask_mail import Message, Mail
from app import models
from app.models import db, User
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


@user_blueprint.route('/user_pic_info')
def user_pic_info():
    return render_template('/news/user_pic_info.html')

@user_blueprint.route('/user_pass_info')
def user_pass_info():
    return render_template('/user/user_pass_info.html')

@user_blueprint.route('/user_pass_release', methods=['POST'])
def user_pass_release():
    pass

@user_blueprint.route('/user_collection')
def user_collection():
    render_template('/user/user_collection.html')
    
@user_blueprint.route('/user_news_list')
def user_news_list():
    render_template('/user/user_news_list.html')

@user_blueprint.route('/user_news_edit')
def user_news_edit():
    render_template('/user/user_news_edit.html')

@user_blueprint.route('/user_news_release')
def user_news_release():
    render_template('/user/user_news_edit.html')









