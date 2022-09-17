from time import sleep
from flask import Flask
from flask_restx import Api, Resource, fields
from celery import Celery
from celery.result import AsyncResult


# create flask instance
app = Flask(__name__)

#create celery instance
celery = Celery(__name__, broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')

# create flask_restx instance
api = Api(app, version='0.0.1',
         title='2022鐵人賽', doc='/api/doc')


add_ns = api.namespace("add_namespace", description='2022鐵人賽_Namespace')

add_payload = add_ns.model('數字加總', {
    'number one': fields.Integer(default=1),
    'number two': fields.Integer(default=2)
})

add_output = add_ns.model('數字加總結果', {
    'number total': fields.Integer(default=3),
    'task_id': fields.String,
})


@add_ns.route('/add')
class Add(Resource):
    @add_ns.expect(add_payload)
    @add_ns.marshal_with(add_output)
    def post(self):
        data = add_ns.payload
        result = add.delay(data)
        res = result.state
        return result

@celery.task(bind=True)
def add(self, data):
    x = data["number one"]
    y = data["number two"]
    result = {'number total': x+y,
            'task_id': self.request.id}
    sleep(20)
    return result


check_payload = add_ns.model('輸入task_id', {
    'task_id': fields.String
})

check_output = add_ns.model('檢查task_status', {
    'status': fields.String
})

@add_ns.route('/check')
class Check(Resource):
    @add_ns.expect(check_payload)
    @add_ns.marshal_with(check_output)
    def post(self):
        task_id = api.payload["task_id"]
        status = celery.AsyncResult("%s" % task_id)
        return status

api.add_namespace(add_ns)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # 備註練習
