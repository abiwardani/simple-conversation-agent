from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sentence_transformers import SentenceTransformer, util
import hashlib

# global variables
SALT = b',w\x1dnW\xfdM3T\xe4\x1c\xb3_c(\xeb\xc9\x19\xbat\xe7\x0e\xa3\x19@2u\x0f\x8b;\xe8\xb0'

app = Flask(__name__)
model = SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')

# configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keys.sqlite3'
db = SQLAlchemy(app)


# define key model
class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashed_key = db.Column(db.LargeBinary)

    def __init__(self, api_key, **kwargs):
        super(Key, self).__init__(**kwargs)
        self.hashed_key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            api_key.encode('utf-8'),  # Convert the password to bytes
            SALT,  # Provide the salt
            100000  # It is recommended to use at least 100,000 iterations of SHA-256
        )

    def __repr__(self):
        return '<Hash %r>' % self.hashed_key


def hash_key(api_key):
    return hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        api_key.encode('utf-8'),  # Convert the password to bytes
        SALT,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )


# default app route
@app.route('/')
def index():
    return "Hello, World!"


# compare similarity of two sentences
@app.route('/similarity', methods=['POST'])
def calculate_sentence_similarity():
    # check if hash of API key exists in database
    api_key = request.json['api_key']
    hashed_key = hash_key(api_key)
    if (Key.query.filter_by(hashed_key=hashed_key) is None):
        abort(401, {"error": "Unauthorized access!"})

    s1 = request.json['s1']
    s2 = request.json['s2']
    s1_embedding = model.encode(s1)
    s2_embedding = model.encode(s2)

    sim = util.cos_sim(s1_embedding, s2_embedding)

    return jsonify({'sim': sim[0][0].item()})


if __name__ == '__main__':
    app.run(debug=True)
