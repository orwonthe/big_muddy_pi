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
    district_console = district_master.district_console
    block_cubes = district_master.block_cubes
    turnout_cubes = district_master.turnout_cubes
    if request.method == 'POST':
        if request.form.get('push_value') == "Clear":
            big_muddy_clear_all()
        elif request.form.get('push_value') == "Set":
            big_muddy_set_all()
        elif request.form.get('push_value') == "Grab":
            district_master.pull_data()
            district_master.show_status()
        elif request.form.get('push_value') == "Reflect":
            district_master.pull_data()
            district_console.reflect()
            district_master.transfer_data()
            district_master.show_status()
        else:
            for cube in turnout_cubes:
                index = cube.gui_index
                form_key = f'turnout_{index}'
                form_value = request.form.get(form_key)
                if form_value == "Main":
                    print(f'Main {cube.moniker}')
                    cube.set_at_main()
                elif form_value == "Siding":
                    print(f'Siding {cube.moniker}')
                    cube.set_at_siding()
            for cube in block_cubes:
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

    return render_template('district.html', console=district_console, block_cubes=block_cubes,
                           turnout_cubes=turnout_cubes, page=page)
