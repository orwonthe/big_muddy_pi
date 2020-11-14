import sys

from district_request import district_request

from flask import Flask
from flask import render_template

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '..')

from duration_testing import duration_check
from counties import BurleighCountyMaster, MortonCountyMaster

burleigh_daisy_master = BurleighCountyMaster()
morton_daisy_master = MortonCountyMaster()

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/duration')
def duration_checking():
    durations = duration_check()
    return render_template('duration.html', durations=durations)


@app.route('/burleigh', methods=['POST', 'GET'])
def burleigh_county():
    return district_request(burleigh_daisy_master, "burleigh")


@app.route('/morton', methods=['POST', 'GET'])
def morton_county():
    return district_request(morton_daisy_master, "morton")


@app.route('/servoblocktesting')
def servo_block_testing():
    return render_template('servo_block_testing.html')
