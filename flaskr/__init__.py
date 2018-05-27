import os

from flask import Flask
# from flask_bootstrap import Bootstrap

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # when not testing, load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # the index page
    # @app.route('/')
    # def index():
    #     # print('Welcome to the index page! :D')
    #     return 'Welcome to the index page! :D'

    # a simple hello page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the db functions
    from . import db
    db.init_app(app)

    # register the login blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # register the blog blueprint, setting it as the default index
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # Bootstrap(app)

    return app
