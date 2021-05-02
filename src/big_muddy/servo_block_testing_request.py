from big_muddy_io import BigMuddyIO

from flask import render_template
from flask import request


def servo_block_testing_request(block_servo_tester):
    if request.method == 'POST':
        action_pieces = request.form.get('action' ).split(": ")
        socket_letter = action_pieces[0]
        command = action_pieces[1]
        if command == "XYZ Off":
            block_servo_tester.set_off(socket_letter)
        elif command == "Flash":
            block_servo_tester.set_flash(socket_letter)
        elif command == "X_normal":
            block_servo_tester.set_x_normal(socket_letter)
        elif command == "X_contrary":
            block_servo_tester.set_x_contrary(socket_letter)
        elif command == "Y_normal":
            block_servo_tester.set_y_normal(socket_letter)
        elif command == "Y_contrary":
            block_servo_tester.set_y_contrary(socket_letter)
        elif command == "Z_normal":
            block_servo_tester.set_z_normal(socket_letter)
        elif command == "Z_contrary":
            block_servo_tester.set_z_contrary(socket_letter)
        elif command == "Shorted":
            block_servo_tester.set_is_shorted(True)
        elif command == "Not_shorted":
            block_servo_tester.set_is_shorted(False)
        block_servo_tester.kick_start()  # trigger logic analyzer frame
        block_servo_tester.push_data()  # push out the commands
        block_servo_tester.pull_data()  # pull back the resulting status

    daisy_nulls = block_servo_tester.daisy_nulls
    daisy_shorts = block_servo_tester.daisy_shorts
    status_report = block_servo_tester.status_report
    return render_template('servo_block_testing.html',
                           daisy_shorts=daisy_shorts,
                           daisy_nulls=daisy_nulls,
                           status_report=status_report,
                           subtitle=("Block Servo")
                           )
