from models import Base, User
from flask import Flask, jsonify, request, url_for, abort, json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.hash import sha256_crypt

from flask import Flask

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/api/users', methods = ['POST'])
def new_user():
    content = request.get_json(silent=True)
    username =  content['username']
    password = content['password']
    # username = request.get_json('username')
    # password = request.get_json('password')
    password = json.dumps(password)
    password_hash = sha256_crypt.encrypt(password)
    # print("Hello %s", username)
    if (not username) or (not password):
        abort(400) # missing arguments
    user = User(username = username, password_hash = password_hash)

    # # if session.query(User).filter_by(username = username).first() is not None:
    # #     abort(400) # existing user
    if user:
        session.add(user)
        session.commit()
        return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5010)
