from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Continent(db.Model):
    __tablename__ = "continents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    countries = db.relationship('Country', backref='countries', lazy=True)

    def __init__(self, name):
        self.name = name


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    continent_id = db.Column(db.Integer, db.ForeignKey('continents.id'), nullable=False, cascade="save-update")
    cities = db.relationship('City', backref='cities', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, continent_id):
        self.name = name
        self.continent_id = continent_id


class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id


db.create_all()


# API heartbeat OK
@app.route('/api')
def index():
    return make_response(jsonify({"API": "OK"}), 200)


# Continents block
# id validated
@app.route('/api/continents/<int:id>', methods=['GET'])
def get_continent(id):
    continent = Continent.query.get_or_404(id)
    del continent.__dict__['_sa_instance_state']
    return jsonify(continent.__dict__)


@app.route('/api/continents', methods=['GET'])
def get_continents():
    continents = []
    for continent in db.session.query(Continent).all():
        del continent.__dict__['_sa_instance_state']
        continents.append(continent.__dict__)
    return jsonify(continents)


# key validated
@app.route('/api/continents', methods=['POST'])
def create_continent():
    body = request.get_json()
    if 'name' in body:
        db.session.add(Continent(body['name'], ))
        db.session.commit()
        return "Continent created"
    else:
        abort(400, "Bad request")


# id and key validated
@app.route('/api/continents/<int:id>', methods=['PUT'])
def update_continent(id):
    body = request.get_json()
    if Continent.query.get_or_404(id):
        if 'name' in body:
            db.session.query(Continent).filter_by(id=id).update(
                dict(name=body['name']))
            db.session.commit()
            return "Continent updated"
        else:
            abort(400, "Bad request")


# id validated
@app.route('/api/continents/<int:id>', methods=['DELETE'])
def delete_continent(id):
    if Continent.query.get_or_404(id):
        db.session.query(Continent).filter_by(id=id).delete()
        db.session.commit()
        return "Continent deleted"


# Cities block
# id validated
@app.route('/api/cities/<int:id>', methods=['GET'])
def get_city(id):
    city = City.query.get_or_404(id)
    del city.__dict__['_sa_instance_state']
    return jsonify(city.__dict__)


@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = []
    for city in db.session.query(City).all():
        del city.__dict__['_sa_instance_state']
        cities.append(city.__dict__)
    return jsonify(cities)


# key validated
@app.route('/api/cities', methods=['POST'])
def create_city():
    body = request.get_json()
    if 'name' in body and 'country_id' in body:
        db.session.add(City(name=body['name'], country_id=body['country_id']))
        db.session.commit()
        return "City created"
    else:
        abort(400, "Bad request")


# id and key validated
@app.route('/api/cities/<int:id>', methods=['PUT'])
def update_city(id):
    body = request.get_json()
    if City.query.get_or_404(id):
        if 'name' in body:
            db.session.query(City).filter_by(id=id).update(
                dict(name=body['name']))
            db.session.commit()
            return "City updated"
        else:
            abort(400, "Bad request")


# id validated
# delete propagation TBD
@app.route('/api/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    if City.query.get_or_404(id):
        db.session.query(City).filter_by(id=id).delete()
        db.session.commit()
        return "City deleted"


# Countries block
# id validated
@app.route('/api/countries/<int:id>', methods=['GET'])
def get_country(id):
    country = Country.query.get_or_404(id)
    del country.__dict__['_sa_instance_state']
    return jsonify(country.__dict__)


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = []
    for country in db.session.query(Country).all():
        del country.__dict__['_sa_instance_state']
        countries.append(country.__dict__)
    return jsonify(countries)


# key validated
@app.route('/api/countries', methods=['POST'])
def create_country():
    body = request.get_json()
    if 'name' in body and 'continent_id' in body:
        db.session.add(Country(name=body['name'], continent_id=body['continent_id']))
        db.session.commit()
        return "Country created"
    else:
        abort(400, "Bad request")


# id and key validated
@app.route('/api/countries/<int:id>', methods=['PUT'])
def update_country(id):
    body = request.get_json()
    if Country.query.get_or_404(id):
        if 'name' in body:
            db.session.query(Country).filter_by(id=id).update(
                dict(name=body['name']))
            db.session.commit()
            return "Country updated"
        else:
            abort(400, "Bad request")


# id validated
# delete propagation TBD
@app.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    if Country.query.get_or_404(id):
        db.session.query(Country).filter_by(id=id).delete()
        db.session.commit()
        return "Country deleted"
