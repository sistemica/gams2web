import codecs
import json
import os

from flask import Flask, render_template, g, request, jsonify, abort
from flask.ext.appconfig import AppConfig
from flask.ext.assets import Environment, Bundle


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(APP_ROOT, 'data')
APP_STATIC = os.path.join(APP_ROOT, 'static')

# Configuration
config = AppConfig(app)     #app.config['MODELS_SETTINGS'] = 'static/models.cfg'


# Asset
assets = Environment(app)

css = Bundle('stylesheets/css/normalize.css',
             'stylesheets/css/bootstrap.css',
             'stylesheets/css/font-awesome.css')
assets.register('stylesheets', css)

js = Bundle('scripts/vendor/modernizr.js')
assets.register('header_scripts', js)

js = Bundle()
assets.register('body_scripts', js)


#
# Pages
#

@app.route('/')
def index():
    return render_template("main.html")


#
# REST API
#

# Loads
def data_from_json(filename, root=APP_DATA):
    with codecs.open(os.path.join(root, filename), 'rU', 'utf-8') as models_file:
        return json.load(models_file)


# Gets the all models
@app.route('/api/models', methods=["GET"])
def get_models():
    try:
        lang = 'en' if not request.args.get('lang') else request.args.get('lang')
        return jsonify(models=data_from_json('models-' + lang + '.json'))
    except IOError:
        return abort(404)


# Gets model info (e.g. /models/sudoku)
@app.route('/api/models/<model>', methods=["GET"])
def get_model(model):
    try:
        return jsonify(data_from_json(model + '.json'))
    except IOError:
        return abort(404)


# Gets the all instances
@app.route('/api/instances', methods=["GET"])
def get_instance():
    try:
        return jsonify(instances=data_from_json('instances.json'))
    except IOError:
        return abort(404)


@app.route('/api/models/<model>/instances', methods=["GET"])
def get_model_instances(model):
    try:
        all_instances = data_from_json('instances.json')
        return jsonify(instances=[i for i in all_instances if i["instance"].startswith(model)])
    except IOError:
        return abort(404)


@app.route('/api/models/<model>/instances/<instance_id>', methods=["GET"])
def get_model_instance(model, instance_id):
    try:
        all_instances = data_from_json('instances.json')
        return jsonify(instances=[i for i in all_instances if i["instance"] == model + '-' + instance_id])
    except IOError:
        return abort(404)


@app.route('/api/models/<model>/instance', methods=["POST"])
def run_model_instance(model):
    return jsonify(json.loads(request.data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)