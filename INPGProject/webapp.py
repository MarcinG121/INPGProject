from flask import render_template, Flask, request
import osm_parser

app = Flask(__name__)


@app.route('/route/', methods=['GET'])
def find_route():
    nodes, g = osm_parser.parse_osm("data\msagh.osm")
    args = request.args.to_dict()
    coordinates = osm_parser.get_route(g, nodes, args["n1"], args["n2"])
    return render_template("index.html", coordinates=coordinates)
