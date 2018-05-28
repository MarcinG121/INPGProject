from flask import render_template, Flask, request
import osm_parser

app = Flask(__name__)
g = osm_parser.parse_osm("data\msagh.osm")

@app.route('/route/', methods=['GET'])
def find_route():
    args = request.args.to_dict()
    try:
        if args["n1"] and args["n2"]:
            coordinates = osm_parser.get_route(g, args["n1"], args["n2"])
        else:
            coordinates = osm_parser.get_route(g)
    except KeyError:
        coordinates = osm_parser.get_route(g)
    return render_template("index.html", coordinates=coordinates)

# TODO: request obslugujacy requesty po klikaniu na mape
@app.route('/route/route', methods=['GET'])
def find_route_by_coordinates():
    args = request.args.to_dict()
    pass
