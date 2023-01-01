import logging
import sys

from block_servo_tester import BlockServoTester
from county_deducer import county_deducer
from district_request import district_request

from flask import Flask
from flask import render_template

# insert at 1, 0 is the script path (or '' in REPL)
from servo_block_testing_request import servo_block_testing_request
from servo_cycle_request import servo_cycle_request
from servo_cycler import ServoCycler

logging.basicConfig(level=logging.DEBUG)
sys.path.insert(1, '..')

from duration_testing import duration_check
from counties import BurleighCountyMaster, MortonCountyMaster

burleigh_daisy_master = BurleighCountyMaster()
morton_daisy_master = MortonCountyMaster()
block_servo_tester = BlockServoTester()
servo_cycler = ServoCycler()

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/duration')
def duration_checking():
    durations = duration_check()
    burleigh = None
    morton = None
    for duration in durations:
        if duration['name'] == 'consoles':
            burleigh, morton = county_deducer(duration['daisy'])
    return render_template('duration.html', durations=durations, subtitle="Durations", morton=morton, burleigh=burleigh)


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

@app.route('/servocycle', methods=['POST', 'GET'])
def servo_cycling():
    return servo_cycle_request(servo_cycler)

