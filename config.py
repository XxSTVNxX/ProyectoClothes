import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta_super_segura_1234')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/clothes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
