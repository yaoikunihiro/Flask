from crypt import methods
import logging
import os
from urllib import response
from fileinput import filename
from unicodedata import name
from email_validator import validate_email, EmailNotValidError
from flask import (Flask, render_template, url_for, current_app, g,request, redirect, flash,
 make_response, session)
from dotenv import load_dotenv
load_dotenv()
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
# gfreiogjarei
# url_for("static", filename="style.css")

app = Flask(__name__)
#SECRET_KEYを追加
app.config["SECRET_KEY"] = "45ei40h30t6BAajriJ"
#ログレベル設定
app.logger.setLevel(logging.DEBUG)
#リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
#DebugToolbarExtensionにアプリをセット
toolbar = DebugToolbarExtension(app)

 #Mailクラスのコンフィグの追加 
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = (os.environ.get("MAIL_USE_TLS") == 'True')
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
app.config["MAIL_USE_SSL"] = (os.environ.get("MAIL_USE_SSL") == 'True')

# app.config["MAIL_SERVER"] = 'smtp.gmail.com'
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_TLS"] = False
# app.config["MAIL_USERNAME"] = 'raw.iujk.7820@gmail.com'
# app.config["MAIL_PASSWORD"] = 'Doragonyappo1'
# app.config["MAIL_DEFAULT_SENDER"] = 'raw.iujk.7820@gmail.com'
# app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


"""HTMLファイルは__pycache__にある"""
# @app.route("/")
# def index():
#      return "Hello, Flask!"

# @app.route("/hello/<kuni>",
#    methods=["GET", "POST"],
#    endpoint="hello-endpoint")
# def hello(kuni):
#      return f"Hello,{kuni}!"

# @app.route("/name/<kuni>")
# def show_name(kuni):
#     return render_template("index.html", kuni=kuni)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        #メールを送る

        #入力チェック
        is_valid = True


        send_email(
          email,
          "お問合せありがとうございました。",
          "contact_mail",
          username=username,
          description=description,
        )

        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力して下さい")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

       #メールを送信

        #問い合わせ完了エンドポイントへリダイレクトする
        
        flash("問い合わせありがとうございました。")
        
        return redirect(url_for("contact_complete"))

        
        

    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
     """メールを送信する関数"""
     msg = Message(subject, recipients=[to])
     msg.body = render_template(template + ".txt", **kwargs)
     msg.html = render_template(template + ".html", **kwargs)
     mail.send(msg)









@app.get("/hello")
@app.get("/hello")
def hello():
     return "Hello, World!"


with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))
    """下記テストサイト用URL"""
    # print(url_for("index"))
    # print(url_for("hello-endpoint", kuni="world"))
    # print(url_for("show_name", kuni="kuni",page="1"))


ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection="connection"
print(g.connection)

# source venv/bin/activate