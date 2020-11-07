import sys

from big_muddy.districts import request_district
from flask import Flask
from flask import render_template

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '..')

from big_muddy.big_muddy_io import BigMuddyIO
from big_muddy.duration_testing import duration_check
from big_muddy.counties import BurleighCountyMaster, MortonCountyMaster

big_muddy = BigMuddyIO.system()
burleigh_daisy_master = BurleighCountyMaster(big_muddy)
morton_daisy_master = MortonCountyMaster(big_muddy)
app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/duration')
def duration_checking():
    durations = duration_check(big_muddy)
    return render_template('duration.html', durations=durations)


@app.route('/burleigh', methods=['POST', 'GET'])
def burleigh_county():
    return request_district(big_muddy, burleigh_daisy_master, "burleigh")


@app.route('/morton', methods=['POST', 'GET'])
def morton_county():
    return request_district(big_muddy, morton_daisy_master, "morton")


@app.route('/servoblocktesting')
def servo_block_testing():
    return render_template('servo_block_testing.html')


