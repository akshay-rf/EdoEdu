
import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from .request import businessArticles, entArticles, get_news_source, healthArticles, publishedArticles, randomArticles, scienceArticles, sportArticles, techArticles, topHeadlines
from . import translator

views_bp = flask.Blueprint('views', __name__, url_prefix='/home')

@views_bp.route('/', endpoint='home')
def home():
    articles = publishedArticles()

    return  render_template('home.html', articles = articles)

@views_bp.route('/headlines', endpoint='headlines')
def headlines():
    headlines = topHeadlines()

    return  render_template('headlines.html', headlines = headlines)

@views_bp.route('/articles', endpoint='articles')
def articles():
    random = randomArticles()

    return  render_template('articles.html', random = random)

@views_bp.route('/sources', endpoint='sources')
def sources():
    newsSource = get_news_source()

    return  render_template('sources.html', newsSource = newsSource)

@views_bp.route('/category/business', endpoint='business')
def business():
    sources = businessArticles()

    return  render_template('business.html', sources = sources)

@views_bp.route('/category/tech', endpoint='tech')
def tech():
    sources = techArticles()

    return  render_template('tech.html', sources = sources)

@views_bp.route('/category/entertainment', endpoint='entertainment')
def entertainment():
    sources = entArticles()

    return  render_template('entertainment.html', sources = sources)

@views_bp.route('/category/science', endpoint='science')
def science():
    sources = scienceArticles()

    return  render_template('science.html', sources = sources)

@views_bp.route('/category/sports', endpoint='sports')
def sports():
    sources = sportArticles()

    return  render_template('sport.html', sources = sources)

@views_bp.route('/category/health', endpoint='health')
def health():
    sources = healthArticles()

    return  render_template('health.html', sources = sources)

@views_bp.route("/dashboard", endpoint='edomeet')
def dashboard():
    return render_template("dashboard.html")


@views_bp.route("/meeting", endpoint='meeting')
def meeting():
    return render_template("meeting.html")


@views_bp.route("/join", endpoint='join', methods=["GET", "POST"])
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/meeting?roomID={room_id}")

    return render_template("join.html")

@views_bp.route('/translator', endpoint='translator', methods=['GET', 'POST'])
def translate_summary():
    if request.method == 'POST':

        summary = request.form['summary']
        print(summary)
        
        tgt_lang = request.form['language']
        print("Selected language:", tgt_lang)
        
        # Translate the summary
        text_translated = translator(summary,
                                     src_lang="eng_Latn",
                                     tgt_lang=tgt_lang)
        
        # Process the translated text as required
        translated_text = text_translated[0]['translation_text']
        return render_template('translated_summary.html', translated_text=translated_text)
    
    return flask.render_template('form.html')