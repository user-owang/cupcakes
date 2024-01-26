"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, flash, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somethinginthashkdgkhs2341'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/api/cupcakes')
def listcupcakes():
    """get a json package with all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def showcupcake(id):
    """get details on a cupcake with cupcake.id of id"""
    cake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def addcupcake():
    data = request.json
    new_cupcake = Cupcake(flavor=data['flavor'], size=data['size'], rating=data['rating'], image=data.get('image', None))
      
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def updatecupcake(id):
    cake = Cupcake.query.get_or_404(id)
    db.session.query(Cupcake).filter_by(id=id).update(request.json)
    db.session.commit()
    return jsonify(cupcake=cake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def deletecupcake(id):
    cake = Cupcake.query.get_or_404(id)
    db.session.delete(cake)
    db.session.commit()
    return jsonify(message='deleted')