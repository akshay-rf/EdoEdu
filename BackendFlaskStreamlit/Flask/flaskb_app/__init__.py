import os

import flask

print("loaded")



def create_app(test_config=None):
    # create and configure the app

    app = flask.Flask(__name__, instance_relative_config=True)

    from . import db
    db.init_app(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskb_app.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as exc:
        pass

    @app.route('/hello')
    def greet():
        return 'Hello, world!'

    from . import auth
    from . import blog
    from . import views

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(blog.blog_bp)
    app.register_blueprint(views.views_bp)

    app.add_url_rule('/', endpoint='index')

    return app
