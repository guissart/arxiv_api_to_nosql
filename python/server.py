import os
from flask import Flask, jsonify, request

import json
from request_function import paper_abstract, get_paper, sorted_colaborators


HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def flask_app():
    app = Flask(__name__)


    @app.route('/', methods=['GET'])
    def server_is_up():
        # print("success")
        return 'server is up'

    @app.route('/get_paper', methods=['POST'])
    def get_paper_route():
        input_dict = request.json

        papers = get_paper(input_dict["author_name"], input_dict["tag"])
        return papers

    @app.route('/sorted_colaborators', methods=['POST'])
    def sorted_colaborators_route():
        input_dict = request.json

        colaborators = sorted_colaborators(input_dict["author_names"])
        return jsonify(colaborators)

    return app

if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0')


