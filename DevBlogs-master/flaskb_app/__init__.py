import os

import flask

from transformers import pipeline

print("loaded")
translator = pipeline(task="translation",
                        model="facebook/nllb-200-distilled-600M",
                        torch_dtype='float32')


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
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError as exc:
        pass

    # a simple page that says hello
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
