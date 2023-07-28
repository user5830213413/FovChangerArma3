import dearpygui.dearpygui as dpg
import getpass
import math
import time

dpg.create_context()
dpg.create_viewport(title='Fov changer Arma 3', decorated=True, resizable=False)
dpg.configure_viewport(0, x_pos=500, y_pos=200, width=500, height=500)


def test():
    dpg.show_item(loading)
    time.sleep(0.5)
    try:
        width_user = dpg.get_value(input_width_screen)
        height_user = dpg.get_value(input_height_screen)
        fov_user = dpg.get_value(input_fov)

        if width_user == '' or height_user == '' or fov_user == '':
            dpg.set_value(text_popup, 'You are trying to apply an empty value')
            dpg.configure_item(popup, show=True, label='Error')

        elif width_user == 0 or height_user == 0 or fov_user == 0:
            dpg.set_value(text_popup, 'error')
            dpg.configure_item(popup, show=True, label='Error')
        else:
            width_user = float(width_user)
            height_user = float(height_user)
            fov_user = float(fov_user)

            vfov = math.degrees(2 * math.atan(math.tan(math.radians(fov_user) / 2) * (height_user / width_user)))

            fovTop = round(vfov * 0.0175, 2)
            fovLeft = round(fovTop / height_user * width_user, 2)

            with open(path_file_arma_3, 'r') as user_profile_arma:
                info_arma3 = user_profile_arma.readlines()

                for i, lines_profile in enumerate(info_arma3):
                    if 'fovTop' in lines_profile:
                        fovTop_old = info_arma3[i]
                        info_arma3[i] = f'fovTop = {fovTop};\n'
                    elif 'fovLeft' in lines_profile:
                        fovLeft_old = info_arma3[i]
                        info_arma3[i] = f'fovLeft = {fovLeft};\n'

                
                with open(path_file_arma_3, 'w') as user_profile_arma:
                    user_profile_arma.writelines(info_arma3)
                    dpg.set_value(text_popup, f'Successfully fov changed\n\nNew Fov value [fovTop: {fovTop}; | fovLeft: {fovLeft};]\nOld Fov value [{fovTop_old.strip()} | {fovLeft_old.strip()}]')
                    dpg.configure_item(popup, show=True, label='Success')
        
    except NameError:
        dpg.set_value(text_popup, 'Specify the path to your arma 3 profile')
        
        dpg.configure_item(popup, show=True, label='Error')


    dpg.hide_item(loading)


def callback(sender, app_data):
    global path_file_arma_3
    path_file_arma_3 = app_data['file_path_name']

    dpg.set_value(nuss, path_file_arma_3)
     

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, file_count=3, tag="file_dialog_tag", width=400,height=350, default_path=f'C:/Users/{getpass.getuser()}/Documents/Arma 3 - Other Profiles'):
    dpg.add_file_extension(".Arma3Profile", color=(255, 255, 0, 255))


with dpg.window(tag="main_window") as main_window:
    with dpg.tab_bar():            
        with dpg.tab(label="Home"):
            dpg.add_text("Welcome friend, this is changer fov for arma 3", pos=(100, 30))

        
            nuss = dpg.add_input_text(enabled=False, width=200, pos=(150, 80), hint='arma 3 user file path')
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text("Here should be the path to your character\nin arma 3, to do this click the\nFile Selector button")
            dpg.add_button(label="File Selector", callback=lambda: dpg.show_item("file_dialog_tag"), width=100, pos=(200, 55))
            input_width_screen = dpg.add_input_text(hint='width', width=200, pos=(150, 105))
            input_height_screen = dpg.add_input_text(hint='height', width=200, pos=(150, 130))
            input_fov = dpg.add_input_text(hint='Fov °', width=200, pos=(150, 155))
            button = dpg.add_button(label='Apply', show=True, callback=test, pos=(200, 185), width=100)

        with dpg.tab(label="Info & Contacts"):
            with dpg.tree_node(label="Help"):

                dpg.add_separator()
                dpg.add_text("About fov changer:")
                dpg.add_text("I'm a dunce.", bullet=True, indent=20)

            with dpg.tree_node(label="Discord"):
                dpg.add_separator()
                dpg.add_text("hattabich", bullet=True)

    popup = dpg.generate_uuid()
    with dpg.window(tag=popup, modal=True, show=False, width=350, height=150):
        text_popup = dpg.add_text('')
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item(popup, show=False))
    

    loading = dpg.add_loading_indicator(circle_count=9, show=False, pos=(230, 220))


dpg.set_primary_window(window=main_window, value=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()