from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api

db=SQLAlchemy()
app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///library.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["JWT_SECRET_KEY"] = "change-me"

jwt=JWTManager(app)
migrate=Migrate(app,db)

db.init_app(app)
bcrypt=Bcrypt(app)
api=Api(app)