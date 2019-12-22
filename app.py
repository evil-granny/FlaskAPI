from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class RoomItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<RoomItem %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/rooms/<int:id>', methods=['GET'])
def element(id):
    room_to_show = RoomItem.query.get(id)
    return render_template('element.html', room=room_to_show)


@app.route('/rooms/', methods=['POST', 'GET'])
def list():
    if request.method == 'POST':
        room_number = request.form.get('number')
        room_price = request.form.get('price')
        room_desc = request.form.get('description')
        new_room = RoomItem(
            number=room_number, price=room_price, description=room_desc)

        try:
            db.session.add(new_room)
            db.session.commit()
            return redirect('/rooms/')
        except:
            return 'There was an issue adding your room'

    else:
        rooms = RoomItem.query.order_by(RoomItem.price).all()
        print(rooms)

        return render_template('list.html', rooms=rooms)


@app.route('/delete/<int:id>', methods=['GET','DELETE'])
def delete(id):
    room_to_delete = RoomItem.query.get(id)
    try:
        db.session.delete(room_to_delete)
        db.session.commit()
        return redirect('/rooms/')
    except:
        return 'There was a problem deleting that room'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        room = RoomItem.query.get(id)
        room.number = request.form.get('number')
        room.price = request.form.get('price')
        room.description = request.form.get('description')
        try:
            db.session.commit()
            return redirect('/rooms/')
        except:
            return 'There was an issue updating your room'

    else:
        room = RoomItem.query.get(id)
        return render_template('update.html', room=room)


if __name__ == "__main__":
    app.run(debug=True)
