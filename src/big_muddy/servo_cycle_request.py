from big_muddy_io import BigMuddyIO

from flask import render_template
from flask import request

def servo_cycle_request(servo_cycler):
    if request.method == 'POST':
        if request.form.get('action') == "Once":
            servo_cycler.cycle(1)
        elif request.form.get('action') == "Twice":
            servo_cycler.cycle(2)
        elif request.form.get('action') == "Ten":
            servo_cycler.cycle(10)
        elif request.form.get('action') == "Hundred":
            servo_cycler.cycle(100)
        elif request.form.get('action') == "Endless":
            servo_cycler.cycle(-1)
    return render_template('servo_cycle.html', tester=servo_cycler, subtitle="Servo Cycle")