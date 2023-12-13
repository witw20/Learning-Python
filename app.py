from flask import Flask, jsonify, abort
from flask_restful import Api, Resource, reqparse, inputs
import sys
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import datetime


app = Flask(__name__)
api = Api(app)
event_parser = reqparse.RequestParser()
date_parser = reqparse.RequestParser()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
db = SQLAlchemy(app)


event_parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)

event_parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)

date_parser.add_argument(
    'start_time',
    type=inputs.date,
    help="The event start date with the correct format is required! The correct format is YYYY-MM-DD!"
)

date_parser.add_argument(
    'end_time',
    type=inputs.date,
    help="The event end date with the correct format is required! The correct format is YYYY-MM-DD!"
)


class Event(db.Model):
    __tablename__ = 'event_table'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


# create the table in the database
db.create_all()


class EventSchema(Schema):
    id = fields.Integer()
    event = fields.String()
    date = fields.Date()


class EventResource(Resource):
    def get(self):
        args = date_parser.parse_args()
        if args.get('start_time') is not None and args.get('end_time') is not None:
            event_list = Event.query.filter(
                Event.date.between(args['start_time'], args['end_time'])
            ).all()
        else:
            event_list = Event.query.all()
        schema = EventSchema(many=True)
        return schema.dump(event_list)

    def post(self):
        args = event_parser.parse_args()
        new_event = Event(event=args['event'], date=args['date'])
        # saves data into the table
        db.session.add(new_event)
        # commits changes
        db.session.commit()
        event_response = jsonify(
            {"message": "The event has been added!",
             "event": args['event'],
             "date": str(args['date'].date())}
        )
        return event_response


class EventToday(Resource):
    def get(self):
        event_list = Event.query.filter(Event.date == datetime.date.today()).all()
        schema = EventSchema(many=True)
        return schema.dump(event_list)


class EventByID(Resource):
    def get(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        schema = EventSchema()
        if event is None:
            abort(404, "The event doesn't exist!")
        return schema.dump(event)

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        delete_response = jsonify(
            {"message": "The event has been deleted!"}
        )
        return delete_response


api.add_resource(EventResource, '/event')
api.add_resource(EventToday, '/event/today')
api.add_resource(EventByID, '/event/<int:event_id>')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
