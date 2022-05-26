from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Continent(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)

  def __init__(self, name):
    self.name = name

db.create_all()

@app.route('/api/continents/<int:id>', methods=['GET'])
def get_continent(id):
  continent = Continent.query.get(id)
  del continent.__dict__['_sa_instance_state']
  return jsonify(continent.__dict__)

@app.route('/api/continents', methods=['GET'])
def get_continents():
  continents = []
  for continent in db.session.query(Continent).all():
    del continent.__dict__['_sa_instance_state']
    continents.append(continent.__dict__)
  return jsonify(continents)

@app.route('/api/continents', methods=['POST'])
def create_continent():
  body = request.get_json()
  db.session.add(Continent(body['name'],))
  db.session.commit()
  return "Continent created"

@app.route('/api/continents/<int:id>', methods=['PUT'])
def update_continent(id):
  body = request.get_json()
  db.session.query(Continent).filter_by(id=id).update(
    dict(name=body['name']))
  db.session.commit()
  return "Continent updated"

@app.route('/api/continents/<int:id>', methods=['DELETE'])
def delete_continent(id):
  db.session.query(Continent).filter_by(id=id).delete()
  db.session.commit()
  return "COntinent deleted"
