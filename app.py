# Server Side

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)

#database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dabase.db'

api = Api(app)


class CityModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'City(name={name}, temp={temp}, weather={weather}, people={people})'

db.create_all()

#Add Request Parser
city_add_args = reqparse.RequestParser()
city_add_args.add_argument('name', type=str, required=True, help='pls fill ur province name')
city_add_args.add_argument('temp', type=str, required=True, help='pls fill ur province temperature')
city_add_args.add_argument('weather', type=str, required=True, help='pls fill ur province weather')
city_add_args.add_argument('people', type=str, required=True, help='pls fill ur number of people of the province ')

#Update Request Parser
city_update_args = reqparse.RequestParser()
city_update_args.add_argument('name', type=str, help='pls specify ur province name')
city_update_args.add_argument('temp', type=str, help='pls specify ur province temperature')
city_update_args.add_argument('weather', type=str, help='pls specify ur province weather')
city_update_args.add_argument('people', type=str, help='pls specify ur number of people of the province ')


resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'temp': fields.String,
    'weather': fields.String,
    'people': fields.String
}

# my_city = {
#     1 : { 'province_name':'Bangkok', 'weather': 'hot', 'people': 5000},
#     2 : { 'province_name':'Chonburi', 'weather': 'rainny', 'people': 4000},
#     3 : { 'province_name':'Rayong', 'weather': 'cloudy', 'people': 3000}
# }

# #validate request
# def not_found_name_city(city_id):
#     if name not in my_city:
#         abort(404, message="no province u've called")

#design
class WeatherCity(Resource):
    
    @marshal_with(resource_field)
    def get(self, city_id):
        # not_found_city_id_city(city_id)
        # return my_city[name]
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404, message='city not found')
        return result

    @marshal_with(resource_field)
    def post(self, city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409, message='used id')
        args = city_add_args.parse_args()
        city = CityModel(id=city_id, name=args['name'], temp=args['temp'], weather=args['weather'], people=args['people'])
        db.session.add(city)
        db.session.commit()
        return city, 201

    @marshal_with(resource_field)
    def patch(self, city_id):
        args=city_update_args.parse_args()
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404, message='city to update not found')
        if args['name']:
            result.name = args['name'] # change name
        if args['temp']:
            result.temp = args['temp'] # change temp
        if args['weather']:
            result.weather = args['weather'] # change weather
        if args['people']:
            result.people = args['people'] # change people

        db.session.commit()
        return result
#call
api.add_resource(WeatherCity, "/weather/<string:city_id>")




if __name__ == "__main__":
    app.run(debug=True)