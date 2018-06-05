from flask import render_template, Flask, request
import osm_parser

app = Flask(__name__)
g = osm_parser.parse_osm("data\msagh.osm")

@app.route('/routenodes', methods=['GET'])
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


@app.route('/routecoords', methods=['GET'])
def find_route_by_coordinates():
    args = request.args.to_dict()
    try:
        node1_id = osm_parser.find_closest(args["lat_1"], args["len_1"])
        node2_id = osm_parser.find_closest(args["lat_2"], args["len_2"])
        # coordinates = osm_parser.get_route(g, node1_id, node2_id)
    except KeyError:
        print("cos poszlo nie tak")
        coordinates = osm_parser.get_route(g)
    return render_template("index.html", coordinates=coordinates)
