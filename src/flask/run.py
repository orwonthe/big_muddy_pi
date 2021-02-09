import logging
import sys

from block_servo_tester import BlockServoTester
from district_request import district_request

from flask import Flask
from flask import render_template

# insert at 1, 0 is the script path (or '' in REPL)
from servo_block_testing_request import servo_block_testing_request

logging.basicConfig(level=logging.DEBUG)
sys.path.insert(1, '..')

from duration_testing import duration_check
from counties import BurleighCountyMaster, MortonCountyMaster

burleigh_daisy_master = BurleighCountyMaster()
morton_daisy_master = MortonCountyMaster()
block_servo_tester = BlockServoTester(True)

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/duration')
def duration_checking():
    durations = duration_check()
    return render_template('duration.html', durations=durations, subtitle="Durations")


@app.route('/burleigh', methods=['POST', 'GET'])
@app.route('/Burleigh', methods=['POST', 'GET'])
def burleigh_county():
    return district_request(burleigh_daisy_master, "Burleigh")


@app.route('/morton', methods=['POST', 'GET'])
@app.route('/Morton', methods=['POST', 'GET'])
def morton_county():
    return district_request(morton_daisy_master, "Morton")


@app.route('/servoblocktesting', methods=['POST', 'GET'])
def servo_block_testing():
    return servo_block_testing_request(block_servo_tester)

