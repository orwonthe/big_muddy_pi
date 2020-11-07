from big_muddy.daisy_master import DaisyMaster
from flask import render_template
from flask import request
from big_muddy.console import console_clear, console_set


def normalize(district, purpose, cube_dictionary_list):
    for gui_index, cube_dictionary in enumerate(cube_dictionary_list):
        cube_dictionary["district"] = district
        cube_dictionary["purpose"] = purpose
        cube_dictionary["gui_index"] = gui_index
    return sorted(cube_dictionary_list, key= lambda item: item["socket"])

class DistrictMaster(DaisyMaster):
    def __init__(self, big_muddy, district_console):
        self.district_console = district_console
        super().__init__(big_muddy, district_console.daisy_units)
        self.set_for_action()

def request_district(big_muddy, district_master, page):
    district_console = district_master.district_console
    if request.method == 'POST':
        if request.form.get('push_value') == "Clear":
            console_clear(big_muddy)
        elif request.form.get('push_value') == "Set":
            console_set(big_muddy)
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
                index = cube.index
                form_key = f'turnout_{index}'
                form_value = request.form.get(form_key)
                if form_value == "Main":
                    print(index, "Main")
                    cube.set_at_main()
                elif form_value == "Siding":
                    print(index, "Siding")
                    cube.set_at_siding()
            for cube in district_console.block_cubes:
                index = cube.index
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
