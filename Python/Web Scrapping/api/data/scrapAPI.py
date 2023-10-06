from flask import Flask, jsonify

app = Flask(__name__)

data123 = {
    'name' : 'John Doe 123',
    'age': 30,
    'email': 'johndoe@example.com'
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data123)

if __name__ == '__main__':
    app.run()