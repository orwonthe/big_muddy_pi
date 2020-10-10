from flask import Flask
from flask import render_template
from flask import request
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '..')

from big_muddy.big_muddy_io import BigMuddyIO
from big_muddy.duration_testing import duration_check
from big_muddy.console import console_clear, console_set
from big_muddy.counties import create_burleigh_console, create_morton_console
from big_muddy.daisy_master import DaisyMaster

big_muddy = BigMuddyIO.system()
burleigh_county_console = create_burleigh_console()
morton_county_console = create_morton_console()
burleigh_daisy_master = DaisyMaster(big_muddy, burleigh_county_console.daisy_units)
morton_daisy_master = DaisyMaster(big_muddy, morton_county_console.daisy_units)
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/duration')
def duration_checking():
    durations = duration_check(big_muddy)
    return render_template('duration.html', durations=durations)

@app.route('/burleigh', methods = ['POST', 'GET'])
def burleigh_county():
    return request_county(burleigh_county_console, burleigh_daisy_master, "burleigh")

@app.route('/morton', methods = ['POST', 'GET'])
def morton_county():
    return request_county(morton_county_console, morton_daisy_master, "morton")


def request_county(county_console, daisy_master, page):
    if request.method == 'POST':
        if request.form.get('push_value') == "Clear":
            console_clear(big_muddy)
        elif request.form.get('push_value') == "Set":
            console_set(big_muddy)
        elif request.form.get('push_value') == "Grab":
            daisy_master.pull_data()
            daisy_master.show_status()
        elif request.form.get('push_value') == "Reflect":
            daisy_master.pull_data()
            county_console.reflect()
            daisy_master.transfer_data()
            daisy_master.show_status()
        else:
            for cube in county_console.turnout_cubes:
                index = cube.index
                form_key = f'turnout_{index}'
                form_value = request.form.get(form_key)
                if form_value == "Main":
                    print(index, "Main")
                    cube.set_at_main()
                elif form_value == "Siding":
                    print(index, "Siding")
                    cube.set_at_siding()
            for cube in county_console.block_cubes:
                index = cube.index
                form_key = f'block_{index}'
                form_value = request.form.get(form_key)
                if form_value == "Off":
                    cube.set_contrary_off()
                    cube.set_normal_off()
                elif form_value == "-Red":
                    cube.set_contrary_red()
                    # cube.set_normal_off()
                elif form_value == "-Green":
                    cube.set_contrary_green()
                    # cube.set_normal_off()
                elif form_value == "-Yellow":
                    cube.set_contrary_yellow()
                    # cube.set_normal_off()
                elif form_value == "+Red":
                    cube.set_normal_red()
                    # cube.set_contrary_off()
                elif form_value == "+Green":
                    cube.set_normal_green()
                    # cube.set_contrary_off()
                elif form_value == "+Yellow":
                    cube.set_normal_yellow()
                    # cube.set_contrary_off()
            daisy_master.transfer_data()

    return render_template('county.html', county=county_console, page=page)
