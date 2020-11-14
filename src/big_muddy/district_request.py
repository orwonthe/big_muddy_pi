from big_muddy_io import BigMuddyIO

from flask import render_template
from flask import request

def big_muddy_clear_all():
    big_muddy_io = BigMuddyIO.system()
    print("clearing console")
    big_muddy_io.set_all(0)

def big_muddy_set_all():
    big_muddy_io = BigMuddyIO.system()
    print("setting console")
    big_muddy_io.set_all(1)


def district_request(district_master, page):
    big_muddy_io = BigMuddyIO.system()
    district_console = district_master.district_console
    if request.method == 'POST':
        if request.form.get('push_value') == "Clear":
            big_muddy_clear_all(big_muddy_io)
        elif request.form.get('push_value') == "Set":
            big_muddy_set_all(big_muddy_io)
        elif request.form.get('push_value') == "Grab":
            district_master.pull_data()
            district_master.show_status()
        elif request.form.get('push_value') == "Reflect":
            district_master.pull_data()
            district_console.reflect()
            district_master.transfer_data()
            district_master.show_status()
        else:
            for cube in district_console.turnout_cubes:
                index = cube.gui_index
                form_key = f'turnout_{index}'
                form_value = request.form.get(form_key)
                if form_value == "Main":
                    print(index, "Main")
                    cube.set_at_main()
                elif form_value == "Siding":
                    print(index, "Siding")
                    cube.set_at_siding()
            for cube in district_console.block_cubes:
                index = cube.gui_index
                form_key = f'block_{index}'
                form_value = request.form.get(form_key)
                if form_value == "Off":
                    cube.set_contrary_off()
                    cube.set_normal_off()
                elif form_value == "-Red":
                    cube.set_contrary_red()
                elif form_value == "-Green":
                    cube.set_contrary_green()
                elif form_value == "-Yellow":
                    cube.set_contrary_yellow()
                elif form_value == "+Red":
                    cube.set_normal_red()
                elif form_value == "+Green":
                    cube.set_normal_green()
                elif form_value == "+Yellow":
                    cube.set_normal_yellow()
            district_master.transfer_data()

    return render_template('district.html', district=district_console, page=page)
