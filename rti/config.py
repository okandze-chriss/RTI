class Config:
    ENV = 'development'
    SECRET_KEY = 'a2cedb8c8801105e4508bd6934cda61d'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/rti'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    OAUTHLIB_INSECURE_TRANSPORT = 1
    MAIL_USERNAME = 'softcodifier@gmail.com'
    MAIL_PASSWORD = 'Softcodifier78'
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    # DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt'
    DROPZONE_ALLOWED_FILE_TYPE = '.xls, .xlsx'
