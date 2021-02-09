from big_muddy_io import BigMuddyIO

from flask import render_template
from flask import request

def servo_block_testing_request(block_servo_tester):
    if request.method == 'POST':
        if request.form.get('action') == "XYZ Off":
            block_servo_tester.set_off()
        elif request.form.get('action') == "Flash":
            block_servo_tester.set_flash()
        elif request.form.get('action') == "X_normal":
            block_servo_tester.set_x_normal()
        elif request.form.get('action') == "X_contrary":
            block_servo_tester.set_x_contrary()
        elif request.form.get('action') == "Y_normal":
            block_servo_tester.set_y_normal()
        elif request.form.get('action') == "Y_contrary":
            block_servo_tester.set_y_contrary()
        elif request.form.get('action') == "Z_normal":
            block_servo_tester.set_z_normal()
        elif request.form.get('action') == "Z_contrary":
            block_servo_tester.set_z_contrary()
        elif request.form.get('action') == "Shorted":
            block_servo_tester.set_is_shorted(True)
        elif request.form.get('action') == "Not_shorted":
            block_servo_tester.set_is_shorted(False)
        block_servo_tester.transfer_data()
    return render_template('servo_block_testing.html', tester=block_servo_tester, subtitle="Block Servo")