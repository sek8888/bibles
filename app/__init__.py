from datetime import datetime
from time import sleep
from flask import (
    Flask,
    request,
    redirect,
    flash,
    render_template
)

from app.lib.db import DB
import config

app = Flask(__name__)
app.secret_key = config.sys['secret_key']
app.config['DEBUG'] = True


# Open the DB connection and log the event
db = DB(config.db['db_file'])

from app.lib.utils import json_response
from app.main import Controller

# TODO; remove
sleep_time = 1
sleep_time = 0


@app.route("/", methods=['GET'])
def _index():
    sleep(sleep_time)
    return render_template("page.html")


@app.route("/data/<int:parent_id>/<table_name>/list", methods=['GET'])
def get_table(table_name, parent_id):
    # get all table
    sleep(sleep_time)
    return json_response(Controller().list_table(table_name, parent_id))


@app.route("/data/<table_name>/form", methods=['GET'])
def get_fields(table_name):
    # get table fields
    sleep(sleep_time)
    return json_response(Controller().get_fields(table_name))


@app.route("/data/<table_name>/<int:id>", methods=['GET'])
def get_record(table_name, id):
    # get record by id
    sleep(sleep_time)
    return json_response(Controller().get_record(table_name, id))


@app.route("/data/<table_name>/create", methods=['POST'])
def create_record(table_name):
    # create record
    sleep(sleep_time)
    return json_response(Controller().create_record(table_name, request.form))


@app.route("/data/<table_name>/<int:id>/edit", methods=['POST'])
def edit_record(table_name, id):
    # edit record
    sleep(sleep_time)
    return json_response(
        Controller().edit_record(table_name, id, request.form)
    )


@app.route("/data/<table_name>/<int:id>/delete", methods=['POST'])
def delete_record(table_name, id):
    # delete record by id
    sleep(sleep_time)
    return json_response(Controller().delete_record(table_name, id))


@app.before_request
def before_request():
    log_line = '"{}" "{}" "{}" "{}" "{}{}{}"{}'.format(
        datetime.now(),
        request.environ['HTTP_USER_AGENT'],
        request.environ['SERVER_PROTOCOL'],
        request.environ['REQUEST_METHOD'],
        request.environ['REMOTE_ADDR'],
        request.environ['PATH_INFO'],
        "?{}".format(request.environ['QUERY_STRING'])
        if request.environ['QUERY_STRING'] else '',
        '\n'
    )
    with open("var/log/reguest.log", "a") as fd:
        fd.write(log_line)
