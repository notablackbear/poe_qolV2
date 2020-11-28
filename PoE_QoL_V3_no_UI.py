import os
import tkinter as tk
import tkinter.messagebox as Msg
from ctypes import wintypes, windll, pointer
from math import ceil
from math import floor
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from pynput import mouse, keyboard

import json
import requests

#       code for cmd to convert py to exe
#       data is a folder whith all needed data
#       pyinstaller --onefile --icon "icon.ico" -w --add-data "data\*;." PoE_QoL_V3_no_UI.py
#


class MyApplication():

    # Build the Mainwindow from the UI-file
    def __init__(self):
        Main_Frame = tk.Frame()
        Main_Frame.config(background='#424242', height='800', padx='5', pady='5')
        Main_Frame.config(takefocus=False, width='600')
        Main_Frame.grid(column='0', row='0')
        self.mainwindow = Main_Frame

# TODO: All these repeated lines below should probably be handled by a more general function
        Fragments = tk.Button(Main_Frame)
        self.img_FragmentChimera = self.get_img_path('FragmentChimera.png')
        Fragments.config(activebackground='#424242', background='#424242', image=self.img_FragmentChimera,
                         overrelief='raised')
        Fragments.config(relief='flat', takefocus=False, text='Frags')
        Fragments.grid(column='6', row='1')
        Fragments.configure(command=self.fragments)

        Essence = tk.Button(Main_Frame)
        self.img_Greed7 = self.get_img_path('Greed7.png')
        Essence.config(activebackground='#424242', background='#424242', image=self.img_Greed7, overrelief='raised')
        Essence.config(relief='flat', takefocus=False, text='Essence')
        Essence.grid(column='0', row='1')
        Essence.configure(command=self.essences)

        DivCard = tk.Button(Main_Frame)
        self.img_Deck = self.get_img_path('Deck.png')
        DivCard.config(activebackground='#424242', background='#424242', image=self.img_Deck, overrelief='raised')
        DivCard.config(relief='flat', takefocus=False, text='DivCard')
        DivCard.grid(column='5', row='1')
        DivCard.configure(command=self.div_cards)

        Currency = tk.Button(Main_Frame)
        self.img_CurrencyRerollRare = self.get_img_path('CurrencyRerollRare.png')
        Currency.config(activebackground='#424242', background='#424242', image=self.img_CurrencyRerollRare,
                        overrelief='raised')
        Currency.config(relief='flat', takefocus=False, text='Currency')
        Currency.grid(column='2', row='2')
        Currency.configure(command=self.currency)

        delve = tk.Button(Main_Frame)
        self.img_AbberantFossil = self.get_img_path('AbberantFossil.png')
        delve.config(activebackground='#424242', background='#424242', image=self.img_AbberantFossil,
                     overrelief='raised')
        delve.config(relief='flat', takefocus=False, text='delve')
        delve.grid(column='1', row='1')
        delve.configure(command=self.delve)

        incubator = tk.Button(Main_Frame)
        self.img_IncubationUniques = self.get_img_path('IncubationUniques.png')
        incubator.config(activebackground='#424242', background='#424242', image=self.img_IncubationUniques,
                         overrelief='raised')
        incubator.config(relief='flat', takefocus=False, text='incubator')
        incubator.grid(column='2', row='0')
        incubator.configure(command=self.incubators)

        blight_map = tk.Button(Main_Frame)
        self.img_blight = self.get_img_path('blight.png')
        blight_map.config(activebackground='#424242', background='#424242', image=self.img_blight, overrelief='raised')
        blight_map.config(relief='flat', takefocus=False, text='blight_map')
        blight_map.grid(column='2', row='1')
        blight_map.configure(command=self.blight)

        map = tk.Button(Main_Frame)
        self.img_Gorge3 = self.get_img_path('Gorge3.png')
        map.config(activebackground='#424242', background='#424242', image=self.img_Gorge3, overrelief='raised')
        map.config(relief='flat', takefocus=False, text='map')
        map.grid(column='1', row='2')
        map.configure(command=self.maps)

        veiled = tk.Button(Main_Frame)
        self.img_Veiledmodified = self.get_img_path('Veiled_modified.gif')
        veiled.config(activebackground='#424242', background='#424242', image=self.img_Veiledmodified,
                      overrelief='raised')
        veiled.config(relief='flat', takefocus=False, text='veiled')
        veiled.grid(column='4', row='0')
        veiled.configure(command=self.veiled)

        # Add the veiled-GIF-animation to the Veiled-Button
        length_gif = 91 # number of pictures creating the gif
        updatetime_ms = 70

        img = 'Veiled_modified.gif'
        if getattr(sys, 'frozen', False):
            # running in a bundle
            path = os.path.join(sys._MEIPASS, img)
        else:
            # running live
            path = img
        self.img_Veiled = path

        frames = [PhotoImage(file=self.img_Veiled, format='gif -index %i' % (i)) for i in range(length_gif)]
        def update(ind):
            if ind == length_gif:
                ind = 0
            else:
                ind += 1
            frame = frames[ind - 1]
            veiled.configure(image=frame)
            root.after(updatetime_ms, update, ind)
        root.after(0, update, 0)

        jewels = tk.Button(Main_Frame)
        self.img_Jewels = self.get_img_path('Jewels.png')
        jewels.config(activebackground='#424242', background='#424242', image=self.img_Jewels, overrelief='raised')
        jewels.config(relief='flat', takefocus=False, text='Jewels')
        jewels.grid(column='1', row='0')
        jewels.configure(command=self.jewels)

        unique = tk.Button(Main_Frame)
        self.img_Uniques = self.get_img_path('Uniques.png')
        unique.config(activebackground='#424242', background='#424242', image=self.img_Uniques, overrelief='raised')
        unique.config(relief='flat', takefocus=False, text='unique')
        unique.grid(column='0', row='2')
        unique.configure(command=self.uniques)

        gem = tk.Button(Main_Frame)
        self.img_impale = self.get_img_path('impale.png')
        gem.config(activebackground='#424242', background='#424242', image=self.img_impale, overrelief='raised')
        gem.config(relief='flat', takefocus=False, text='gem')
        gem.grid(column='0', row='0')
        gem.configure(command=self.gems)

        prophecy = tk.Button(Main_Frame)
        self.img_ProphecyOrbRed = self.get_img_path('ProphecyOrbRed.png')
        prophecy.config(activebackground='#424242', background='#424242', image=self.img_ProphecyOrbRed,
                        overrelief='raised')
        prophecy.config(relief='flat', takefocus=False, text='prophecy')
        prophecy.grid(column='3', row='0')
        prophecy.configure(command=self.prophecies)

        six_sockets = tk.Button(Main_Frame)
        self.img_sixsockets = self.get_img_path('six_sockets.png')
        six_sockets.config(activebackground='#424242', background='#424242', bitmap='error', image=self.img_sixsockets)
        six_sockets.config(overrelief='raised', relief='flat', takefocus=False, text='six_sockets')
        six_sockets.grid(column='5', row='0')
        six_sockets.configure(command=self.six_sockets)

        delirium = tk.Button(Main_Frame)
        self.img_delirium = self.get_img_path('delirium.png')
        delirium.config(activebackground='#424242', background='#424242', image=self.img_delirium, overrelief='raised')
        delirium.config(relief='flat', takefocus=False, text='delirium')
        delirium.grid(column='3', row='1')
        delirium.configure(command=self.delirium)

        metamorph = tk.Button(Main_Frame)
        self.img_metamorph = self.get_img_path('metamorph.png')
        metamorph.config(activebackground='#424242', background='#424242', image=self.img_metamorph,
                         overrelief='raised')
        metamorph.config(relief='flat', text='metamorph')
        metamorph.grid(column='4', row='1')
        metamorph.configure(command=self.metamorph)

        remaining = tk.Button(Main_Frame)
        self.img_questionmarkgrey = self.get_img_path('questionmark_grey.png')
        remaining.config(activebackground='#424242', background='#424242', image=self.img_questionmarkgrey,
                         overrelief='raised')
        remaining.config(relief='flat', takefocus=False, text='remaining')
        remaining.grid(column='6', row='0')
        remaining.configure(command=self.remaining)

        settings = tk.Button(Main_Frame)
        settings.config(activebackground='#424242', activeforeground='#ffffff', background='#424242',
                        foreground='#ffffff')
        settings.config(takefocus=False, text='Settings', width='13')
        settings.grid(column='5', columnspan='2', row='4', sticky='e')
        settings.configure(command=self.settings)

        overlay = tk.Button(Main_Frame)
        overlay.config(activebackground='#424242', activeforeground='#ffffff', background='#424242',
                       foreground='#ffffff')
        overlay.config(takefocus=False, text='Overlay', width='13')
        overlay.grid(column='5', columnspan='2', row='3', sticky='se')
        overlay.configure(command=self.overlay)

        remove_highlights_main = tk.Button(Main_Frame)
        remove_highlights_main.config(activebackground='#424242', activeforeground='#ffffff', background='#424242',
                                      foreground='#ffffff')
        remove_highlights_main.config(takefocus=False, text='Remove Highlights', width='15')
        remove_highlights_main.grid(column='3', columnspan='2', row='4', sticky='e')
        remove_highlights_main.configure(command=self.remove_highlights)

        ## TODO: Move save file handling outside of App to a back end function that can be imported if needed
        if not os.path.isfile('savefile.txt'):
            self.savefile = open('savefile.txt', 'w')
            self.savefile.write(' ' + '\n' + ' ' + '\n' + ' ' + '\n' + ' ' + '\n' + ' ' + '\n' + ' ')
            self.savefile.close()

        # load old settings
        self.savefile = open('savefile.txt', 'r')
        ## TODO: Use the standard library config functionality as in original code, which should avoid errors in future
        ##TODO: use a dict instead of list for settings_data so it is more clear what is queried in other parts of code
        self.settings_data = self.savefile.read().splitlines()  # each line -> one entity in list
        self.savefile.close()

        # if old location is available -> set mainwindow location
        if self.settings_data[4].replace(' ', '') != '':
            mainwindow_location_data = self.settings_data[4].split(',')
            root.geometry('388x220+%s+%s' % (mainwindow_location_data[0], mainwindow_location_data[1]))

    def run(self):
        self.mainwindow.mainloop()

## TODO: We probaby don't need to compress all the resources into the .exe, since there are multiple files being installed anyway
    def get_img_path(self, img):
        # we need this function to convert the .py script to an .exe in one file, which includes all images
        # to use the compressed images in the exe we need an special path called sys._MEIPASS, where all intern data is saved
        if getattr(sys, 'frozen', False):
            # running in a bundle
            path = os.path.join(sys._MEIPASS, img)
        else:
            # running live
            path = img
        img = ImageTk.PhotoImage(Image.open(path))
        return img

    def setup_app_with_settings(self):
        self.hightlightbox_size_calculation()
        try:
            item_threshold = int(self.settings_data[1].split(',')[4])
        except:  ##TODO: Handle specific errors here
            Msg.showinfo(title='Warning!', message='Item threshold must be a number! The value is set to 10 (default).')
            item_threshold = 10

        self.item_details = dict(
            Rings=[1, 1, '#33bbee', '4', item_threshold * 2],
            OneHandWeapons=[1, 3, '#bbbbbb', '1', item_threshold * 2],
            BodyArmours=[2, 3, '#ee3377', '1', item_threshold],
            Helmets=[2, 2, '#cc3311', '2', item_threshold],
            Gloves=[2, 2, '#ee7733', '2', item_threshold],
            Boots=[2, 2, '#009988', '2', item_threshold],
            Belts=[2, 1, '#0077bb', '3', item_threshold],
            Amulets=[1, 1, '#33bbee', '4', item_threshold],
        )

        # read chaos items filter
        self.chaos_items_filter_sections = self.read_default_chaos_filter_sections()
        # prepare main filter with the chaos recipe filter code
        self.pre_process_item_filter()
        # update the chaos recipe filter code in the main filter
        self.refresh_me()

    def hightlightbox_size_calculation(self):

        if int(self.settings_data[0].split(',')[1]) == 1:  # checkbutton "windowed mode"
            self.window_mode = 'windowed'
            self.window_props = self.get_poe_window_location(self.window_mode)
            self.tab_origin = self.window_props[2] + 22 / 1440 * self.window_props[1], self.window_props[
                3] + 169 / 1440 * self.window_props[1]
            self.tab_end = self.window_props[2] + 864 / 1440 * self.window_props[1], self.window_props[
                3] + 1013 / 1440 * self.window_props[1]
        else:
            self.window_mode = 'fullscreen_windowed'
            self.window_props = self.get_poe_window_location(self.window_mode)
            self.tab_origin = 22 / 1440 * self.window_props[1], 169 / 1440 * self.window_props[1]
            self.tab_end = 864 / 1440 * self.window_props[1], 1013 / 1440 * self.window_props[1]

        if int(self.settings_data[0].split(',')[0]) == 1:  # checkbutton "quad tab"
            box_density_scalar = 24
        else:
            box_density_scalar = 12

        self.box_width = (self.tab_end[0] - self.tab_origin[0]) / box_density_scalar
        self.box_height = (self.tab_end[1] - self.tab_origin[1]) / box_density_scalar

    def check_chaos_items_filter(self):
        # checks and if not there: create chaos filter text file with default config
        self.filterdir = os.path.dirname(self.settings_data[5])  # directory from the main-filter
        if os.path.isdir(self.filterdir):
            if not os.path.isfile(self.filterdir + '/chaos_items_filter.filter'):
                with open(self.filterdir + '/chaos_items_filter.filter', 'w') as filt:
                    ##TODO: Don't hardcode the default filter. Better to be able to change it without recompiling for example when debugging, or if user wants to change colors
                    # hardcode the default chaos recipe, so no extra file needed
                    filt.writelines(
                        ['# Chaos Recipe BodyArmours\n',
                         'Show\n',
                         'SetBorderColor 0 0 0\n',
                         'SetFontSize 33\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 238 51 119\n',
                         'Class "Body Armours"\n',
                         'ItemLevel <= 74\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe Boots\n',
                         'Show\n',
                         'SetBorderColor 48 255 0\n',
                         'SetFontSize 33\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 0 153 136\n',
                         'ItemLevel <= 74\n',
                         'Class "Boots"\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe Gloves\n',
                         'Show\n',
                         'SetBorderColor 0 59 255\n',
                         'SetFontSize 33\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'Class "Gloves"\n',
                         'ItemLevel <= 74\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 238 119 51\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe Helmets\n',
                         'Show\n',
                         'SetBorderColor 255 245 0\n',
                         'SetFontSize 33\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 204 51 17\n',
                         'Class "Helmets"\n',
                         'ItemLevel <= 74\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe OneHandWeapons\n',
                         'Show\n',
                         'SetBorderColor 255 255 255\n',
                         'SetFontSize 33\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 187 187 187\n',
                         'Class "Daggers" "One Hand Axes" "One Hand Maces" "One Hand Swords" "Rune Daggers" "Sceptres" "Thrusting One Hand Swords" "Wands"\n',
                         'ItemLevel <= 74\n',
                         'Width = 1\n',
                         'Height <= 3\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe Rings\n',
                         'Show\n',
                         'SetBorderColor 255 0 0\n',
                         'SetFontSize 38\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 51 187 238\n',
                         'PlayAlertSound 16 300\n',
                         'MinimapIcon 0 Red Star\n',
                         'PlayEffect Red\n',
                         'Class "Rings"\n',
                         'ItemLevel <= 80\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe Belts\n',
                         'Show\n',
                         'SetBorderColor 255 0 0\n',
                         'SetFontSize 38\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 0 119 187\n',
                         'PlayAlertSound 16 300\n',
                         'MinimapIcon 0 Red Star\n',
                         'PlayEffect Red\n',
                         'Class "Belts"\n',
                         'ItemLevel <= 80\n',
                         'Identified False\n',
                         '\n',
                         '# Chaos Recipe Amulets\n',
                         'Show\n',
                         'SetBorderColor 255 0 0\n',
                         'SetFontSize 38\n',
                         'ItemLevel >= 60\n',
                         'Rarity = Rare\n',
                         'SetTextColor 0 0 0\n',
                         'SetBackgroundColor 51 187 238\n',
                         'PlayAlertSound 16 300\n',
                         'MinimapIcon 0 Red Star\n',
                         'PlayEffect Red\n',
                         'Class "Amulets"\n',
                         'ItemLevel <= 80\n',
                         'Identified False'])
                filt.close()
                Msg.showinfo(title='Information', message='There was no filter for the chaos items in the selected directory. The default filter has been loaded and can now be modified.')

    def read_default_chaos_filter_sections(self):
        ##TODO: See if Better* can handle this functionality instead
        """
        User can use the filter that comes with this program, or customize each slot to their liking.
        Only important things are that each section starts with a '#' and has the correct item slot name in that line
        Correct item slots are give in the self.item_details parameter. This should be the last word in the comment line.
        """
        with open(self.filterdir + '/chaos_items_filter.filter', 'r') as fil:
            chaos_filter = fil.readlines()  # read whole file into memory. each line is stored as a string in a list
            section_starts = []
            for i, line in enumerate(chaos_filter):  # loop through the lines
                _line = line.lstrip()  # remove any leading white space
                # If the line is a comment, record that as the start of an item slot section
                # We need to protect from empty lines which are stored as zero-length lists
                if not _line or not _line[0] == "#":
                    continue
                elif _line and _line[
                    0] == "#":  # I shouldn't need to, but I double check that the line is a comment anyway
                    section_starts.append(i)
            # each section ends where the next begins. The last section goes to the last line in the list, so concatenate that to the other ending indicies
            section_ends = [i for i in section_starts[1:]] + [len(chaos_filter) + 1]
            # create empty dictionary for storing the text of each section
            sections = {}
            # store the text for each section in the dictionary. The key for each section is the last word in the first line, chaos_filter[i].split(" ")[-1].rstrip(). This is maybe a dumb way of doing this and prone to user error.
            # TODO: Find a better way to get the section keys -- Update, trying this below now.
            for i, j in zip(section_starts, section_ends):
                for k in range(i, j - 1):  # loop through all the lines in the section
                    linelistcopy = chaos_filter[k][:].split(
                        " ")  # create a copy to work with and remove white space and make a list
                    linelistcopy = [str(_).rstrip().replace("'", '') for _ in
                                    linelistcopy]  # convert to strings wihtout quotes...?
                    linelistcopy = [_.replace('"', '') for _ in linelistcopy]  # convert to strings wihtout quotes...?
                    if linelistcopy[0].lower() == 'class':
                        if "One" in linelistcopy and "Hand" in linelistcopy:
                            section_class_key = "OneHandWeapons"
                        elif linelistcopy[1].lower() == 'body':
                            section_class_key = "BodyArmours"
                        else:
                            section_class_key = linelistcopy[1]
                sections[section_class_key.rstrip()] = chaos_filter[i:j]
        return sections

    def pre_process_item_filter(self):
        self.filterpath = self.settings_data[5]
        if os.path.isfile(self.filterpath):
            with open(self.filterpath, 'r') as fil:
                self.main_filter = fil.readlines()  # read default file into memory
        else:
            Msg.showinfo('Error!', 'Please check if the selected filter in settings is valid!')

        self.chaos_items_sections_start_line = 0
        self.chaos_items_sections_end_line = len(self.main_filter)
        section_found = 0
        filter_hide_positions = []
        for i, line in enumerate(self.main_filter):
            # I use a random string to find where the chaos recipe section begins and ends
            line.replace(' ', '')
            if line[0:4] == 'Hide':
                filter_hide_positions.append(i)
            elif line[0] != "#":  # If the line isn't a comment, we can just move on
                continue
            elif '234hn50987sd' in line:
                self.chaos_items_sections_start_line = i + 1
                continue
            elif '2345ina8dsf7' in line:
                self.chaos_items_sections_end_line = i
                section_found = 1
                break
        if not section_found:
            # when no section -> create section for the last "Hide" - line
            self.main_filter0 = self.main_filter[0:filter_hide_positions[-1]] + ['\n'] + ['#--------------------------------------------------------------------------\n'] + ['# Chaos Recipe Tool\n'] + ['#--------------------------------------------------------------------------\n'] + ['\n'] + ['# 234hn50987sd Start Chaos Recipe Auto-Update Section \n'] + ['\n']
            self.main_filter1 = ['\n'] + ['# 2345ina8dsf7 End Chaos Recipe Auto-Update Section \n'] + ['\n'] + self.main_filter[filter_hide_positions[-1]:] + ['\n']
        else:
            # take everything before and after the chaos recipe section from the original filter file. It shouldnt be changed ever. We will make changes between these two sections on each update.
            self.main_filter0 = self.main_filter[0:self.chaos_items_sections_start_line] + ['\n']
            self.main_filter1 = ['\n'] + self.main_filter[self.chaos_items_sections_end_line:]

        return

    def update_main_filter(self):
        for slot, details in self.item_details.items():
            # if the slot is on the ignor list or if the number of items is not greater than the threshold, keep it in the filter
            if slot in self.ignore_item_threshold_list or len(self.latest_stash[0][slot]) < details[4]:
                self.chaos_items_filter_sections[slot][1] = "Show\n"  # The show/hide flag is the second entry in the filter section text (see chaos_items_filter in Setup.ini)
            else:  # Otherwise hide that slot
                self.chaos_items_filter_sections[slot][1] = "Hide\n"

        new_filter_lines = [l for slt in self.chaos_items_filter_sections.values() for l in slt]
        new_main_filter = self.main_filter0 + new_filter_lines + self.main_filter1
        with open(self.filterpath, 'w') as fil:
            for line in new_main_filter:
                fil.write(line)
        return True

    def refresh_me(self):
        self.latest_stash = self.stash_finder()
        itemtext_for_overlay = ['Armours: ', 'Helmets: ', 'Weapons: ', 'Gloves: ', 'Boots: ', 'Amulets: ', 'Belts: ', 'Rings: ']
        index = 0
        for key, value in self.latest_stash[0].items():

            new_colour = '#ffffff' # white
            if len(self.latest_stash[0][key]) < self.item_details[key][4]:
                new_colour = '#e6e600' # yellow
            elif len(self.latest_stash[0][key]) >= self.item_details[key][4]:
                new_colour = '#00e600' # green
            if key == 'Rings' or key == 'OneHandWeapons':
                if len(self.latest_stash[0][key]) < 2:
                    new_colour = '#e60000' # red
            elif len(self.latest_stash[0][key]) == 0:
                new_colour = '#e60000'
            # now we want to check if the main-filter must be manually updated
            self.ignore_item_threshold_list = ['BodyArmours', 'Helmets', 'OneHandWeapons', 'Gloves', 'Boots', 'Amulets',
                                               'Rings', 'Belts']
            for i, boolval in enumerate(self.settings_data[0].split(',')[2:10]):
                if boolval != '1':
                    self.ignore_item_threshold_list[i] = ''
            # thats the case when a colour change from green (number of items reached cap) ->  yellow or red / the other way
            exec(f'global actual_colour; actual_colour = self.{key}.cget("foreground")') ## TODO: No more exec uses
            if new_colour == '#00e600' and (actual_colour == '#e6e600' or actual_colour == '#e60000') and key not in self.ignore_item_threshold_list:
                self.flg_filterupdate = 1
                self.show_filter_refresh_icon()
            elif (new_colour == '#e6e600' or new_colour == '#e60000') and actual_colour == '#00e600' and key not in self.ignore_item_threshold_list:
                self.flg_filterupdate = 1
                self.show_filter_refresh_icon()
            exec(f'self.{key}.configure(text="{itemtext_for_overlay[index]}{len(value)}", foreground="{new_colour}")')

            index += 1
        self.update_main_filter()
###

    def show_filter_refresh_icon(self):
        self.img_refresh30 = self.get_img_path('refresh30.png')
        self.refresh_image.config(image=self.img_refresh30)

        self.last_button = None
        self.x_refresh_button_poe = [515, 548]
        self.y_refresh_button_poe = [644, 676]

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

        self.listener2 = keyboard.Listener(on_press=self.on_press)
        self.listener2.start()

    def on_click(self, x, y, button, pressed):
        if self.last_button == 'o' and pressed and button.name == 'left' and (515 <= x <= 548) and (644 <= y <= 676):
            self.refresh_image.config(image=self.img_refresh30_empty)

    def on_press(self, key):
        try:
            self.last_button = key.char
        except AttributeError:
            self.last_button = None

    def hide_filter_refresh_icon(self):
        pass

    def chaos_recipe(self):
        ##TODO: This can be rewritten to be more generalized for all items types and states. V4?
        self.remove_highlights()
        unident = self.check_complete_set()
        if not unident:
            Msg.showinfo(title='POE QoL', message='Not enough Chaos Recipe Items')
        else:
            for x in unident:
                # we will count from the top-left origin
                x_off = self.tab_origin[0]
                y_off = self.tab_origin[1]
                # cord_x, cord_y = self.unident[x].pop(0)  # Leaving this here so you can see the previous method was to pop items from the list. It was problematic. -notaspy 14-9-2020
                for i in range(len(unident[x])):
                    # reimplemented this as a loop over the items that make up the number of complete sets
                    # The execs are legacy. I don't like them, and could probably re-do it, but won't atm
                    # TODO: refactor exec usage
                    cord_x, cord_y = unident[x][i]  # get coordinates of entry
                    cord_x = cord_x * self.box_width + x_off  # convert coordinates to pixels
                    cord_y = cord_y * self.box_height + y_off
                    box_width = self.box_width * self.item_details[x][0]
                    # based on the meta-data about item size in self.item_details, make appropriate size box
                    box_height = self.box_height * self.item_details[x][1]
                    # below is legacy
                    # basically it creates a semi-transparent top level window that disappears when it is clicked. I decided to use different colors by item slot
                    exec(f"self.{x + str(i)} = tk.Toplevel(self.mainwindow)")
                    exec(f'self.{x + str(i)}.attributes("-alpha", 0.65)')
                    exec(f'self.{x + str(i)}.config(background="{self.item_details[x][2]}")')
                    exec(f"self.{x + str(i)}.overrideredirect(1)")
                    exec(f'self.{x + str(i)}.attributes("-topmost", 1)')
                    exec(
                        f'self.{x + str(i)}.geometry("{ceil(box_width)}x{ceil(box_height)}+{ceil(cord_x)}+{ceil(cord_y)}")')
                    exec(f'self.box = self.{x + str(i)}')
                    # was able to get rid of the legacy exec call below. Using the actual object fixes errors in destroying the highlight if highlighting over and over
                    self.box.bind("<Button-1>", lambda command, a=self.box: self.click_item(a))  # bind click command to object
                    # make sure the highlight objects persist so they are all interactive and can be deleted when method is run (see above, before loops)
                    self.highlighted_items.append(self.box)

    def click_item(self, a):
        a.destroy()

    def remove_highlights(self):
        try:  # test that highlight actually exist that need deletion
            for highlight in self.highlighted_items:  # delete them
                highlight.destroy()
        except:
            pass
        self.highlighted_items = []

    def check_complete_set(self):
        # Find the limiting two-slot item
        two_slot_max_sets = min((floor(len(self.latest_stash[0]["Rings"]) / 2),
                                 floor(len(self.latest_stash[0]["OneHandWeapons"]) / 2)))
        # Find limiting one-slot items
        one_slot_max_sets = min([len(self.latest_stash[0][_key]) for _key in self.latest_stash[0].keys() if _key not in ["Rings", "OneHandWeapons"]])
        # Find out if we are limited by two-slot, one-slot, or the user set maximum number of highlighted sets
        try:
            max_highlighted_sets = int(self.settings_data[1].split(',')[5])
        except:
            Msg.showinfo(title='Warning!',
                         message='The number of maximal highlighted itemsets must be an Integer! The value is set to 2 (default).')
            max_highlighted_sets = 2
        max_sets = min(two_slot_max_sets, one_slot_max_sets, max_highlighted_sets)

        if max_sets > 0:
            unident_sets = {_key: [] for _key in self.item_details.keys()}  # create a dictionary of empty lists to fill in and return
            # loop through each slot and find the maximum index in the list of coordinates for each item. We use this to only take the valid items.
            for key in self.item_details.keys():
                if key in ["Rings", "OneHandWeapons"]:  # we need two of these, so the maximum index is twice that of the other items
                    max_index = 2 * max_sets
                else:
                    max_index = max_sets
                # Grab the items and their coordinates up the the maximum. These are dicts with the type of slot as the key, and a list of length-2 coordinates lists
                # I think we don't want to 'pop' the item from the list because the loop will then try to access indexes that are outside the list length
                for i in range(max_index):
                    unident_sets[key].append(self.latest_stash[0][key][i].copy())
            # Now remove these from the local inventory record. This could be more efficient by combining with the above, I am sure
            for key in self.item_details.keys():
                indices_to_delete = []
                for i in range(len(self.latest_stash[0][key])):
                    if self.latest_stash[0][key][i] in unident_sets[key]:
                        indices_to_delete.append(i)
                        continue
                # only keep the items that are not about to be highlighted
                self.latest_stash[0][key] = [_ for j, _ in enumerate(self.latest_stash[0][key]) if
                                             j not in indices_to_delete]
            return unident_sets
        else:
            return False

    def stash_finder(self):
        # search in the desired stash tab for all mandatory items and return there position
        if self.settings_data[0].replace(' ', '') != '':
            pos_last_unid = {'BodyArmours': [], 'Helmets': [], 'OneHandWeapons': [], 'Gloves': [], 'Boots': [],
                             'Amulets': [], 'Belts': [], 'Rings': []}
            currency, essences, div_cards, incubators, maps, veiled, jewels, uniques, gems, prophecies, sixsockets, fragments, delve, blight, delirium, metamorph, remaining = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
            account_name = self.settings_data[1].split(',')[0]
            league = self.settings_data[1].split(',')[1]
            POESESSID = self.settings_data[1].split(',')[2]
        else:
            Msg.showinfo(title='Warning!', message='Please adjust the settings first!')
            return
        try:
            tab_index = int(self.settings_data[1].split(',')[3])
        except:
            Msg.showinfo(title='Warning!', message='Tab number must be an Integer! The value is set to 0 so it search in the first tab (default).')
            tab_index = 0

        stash_tab = f"https://www.pathofexile.com/character-window/get-stash-items?league={league}&tabIndex={str(tab_index)}&accountName={account_name}"
        payload = {
            'league': league,
            'tabIndex': tab_index,
            'accountName': account_name.encode('utf-8'),
        }
        try:
            a = requests.get(stash_tab, cookies=dict(POESESSID=POESESSID), params=payload)
        except requests.HTTPError:
            Msg.showinfo(title='Error!', message='Could not connect to pathofexile.com. Please check your account name, league or your POESESSID in the settings!')
        #self.last_update = datetime.datetime.now()
        try:
            json.loads(a.text)['items']
        except KeyError:
            Msg.showinfo(title='Error!', message='Bad Response from pathofexile.com. Please check the settings!')
        ##TODO: Update this new functionality to make use of Better* functions
        # categories to sort all the items in:
        # 6 sockets                       check
        # currency                      check
        # essences                       check
        # div cards                       check
        # incubators                       check
        # maps                       check
        # veiled                       check
        # jewels                       check
        # uniques                       check
        # gems                       check
        # prophecies                       check
        # delve:                       check
            # resonators
            # fossils
        # blight:                       check
            # oils
            # blighted maps
        # delirium:                       check
            # delirium orbs
            # simulactrum splinters & peace
        # fragments:
            # frags from (uber)atziri, shaper, (uber)elder, key inya und co
            # splinter of breach + peace
            # splinter of timeless + peace
            # scarabs
            # divine vessel
            # offering of the goddess
        # metamorph:                       check
            # catalysts
            # organs


        for x in json.loads(a.text)['items']:
            # sixsockets:
            try: # some items have no sockets
                if len(x['sockets']) == 6:
                    sixsockets.append([x['x'], x['y'], x['w'], x['h']])
                    continue
            except:
                pass
            # essence:
            if '/Essence' in x['icon']:
                essences.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # delve:
            if '/Delve' in x['icon'] and not '/Heist' in x['icon']:
                delve.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # blight: maps not tested
            if '/Blight' in x['icon'] or '/Oil' in x['icon']:
                blight.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # metamorph:
            if '/Metamorph' in x['icon'] or '/Catalyst' in x['icon']:
                metamorph.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # delirium: orbs, medium and small not tested
            if '/Delirium' in x['icon'] or '/NewGemBase' in x['icon']:
                delirium.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # prophecies:
            if x['frameType'] == 8:
                prophecies.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # gems:
            if x['frameType'] == 4:
                gems.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # uniques:
            if x['frameType'] == 3:
                uniques.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # jewels:
            if '/Jewel' in x['icon']:
                jewels.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # veiled:
            try:
                if x['veiled']:
                    veiled.append([x['x'], x['y'], x['w'], x['h']])
                    continue
            except:
                pass
            # maps:
            try:
                if 'Maps can' in x['descrText']:
                    maps.append([x['x'], x['y'], x['w'], x['h']])
                    continue
            except:
                pass
            # incubators:
            if '/Incu' in x['icon']:
                incubators.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # div cards:
            if x['frameType'] == 6:
                div_cards.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # fragments: full emblems not tested
            if '/Scarab' in x['icon'] or '/Maps' in x['icon'] or '/BreachShard' in x['icon']:
                fragments.append([x['x'], x['y'], x['w'], x['h']])
                continue
            # currency:
            if x['frameType'] == 5 and not '/Heist' in x['icon']:
                currency.append([x['x'], x['y'], x['w'], x['h']])
                continue

            # franemtype -> definition here: https://pathofexile.gamepedia.com/Public_stash_tab_API#frameType
            # frametype = 2 -> Rarity = Rare
            if x['frameType'] == 2 and x['identified'] is False:
                if 'BodyArmours' in x['icon']:
                    pos_last_unid['BodyArmours'].append([x['x'], x['y']])
                    continue
                elif 'Helmets' in x['icon']:
                    pos_last_unid['Helmets'].append([x['x'], x['y']])
                    continue
                elif 'OneHandWeapons' in x['icon'] and x['w'] == 1:
                    pos_last_unid['OneHandWeapons'].append([x['x'], x['y']])
                    continue
                elif 'Gloves' in x['icon']:
                    pos_last_unid['Gloves'].append([x['x'], x['y']])
                    continue
                elif 'Boots' in x['icon']:
                    pos_last_unid['Boots'].append([x['x'], x['y']])
                    continue
                elif 'Amulets' in x['icon']:
                    pos_last_unid['Amulets'].append([x['x'], x['y']])
                    continue
                elif 'Belts' in x['icon']:
                    pos_last_unid['Belts'].append([x['x'], x['y']])
                    continue
                elif 'Rings' in x['icon']:
                    pos_last_unid['Rings'].append([x['x'], x['y']])
                    continue
            # remaining:
            remaining.append([x['x'], x['y'], x['w'], x['h']])

        else:
            # sorting the lists from all items so it shows the most right items for the recipe first
            for key in pos_last_unid:
                pos_last_unid[key].sort(reverse=True)
            return (pos_last_unid, currency, essences, div_cards, incubators, maps, veiled, jewels, uniques, gems, prophecies, sixsockets, fragments, delve, blight, delirium, metamorph, remaining)




    def stash_filtering(self, datalist):
        self.remove_highlights()
        # datalist -> [ [x1, y1, w1, h1] , [x2, y2, w2, h2] , ... ]
        for index, itemdata in enumerate(datalist):
            # we will count from the top-left origin
            x_off = self.tab_origin[0]
            y_off = self.tab_origin[1]
            cord_x, cord_y = itemdata[:2]  # get coordinates of entry
            cord_x = cord_x * self.box_width + x_off  # convert coordinates to pixels
            cord_y = cord_y * self.box_height + y_off
            box_width = self.box_width * itemdata[2]
            box_height = self.box_height * itemdata[3]
            # basically it creates a semi-transparent top level window that disappears when it is clicked. I decided to use different colors by item slot
            exec(f"self.highlight{str(index)} = tk.Toplevel(self.mainwindow)")
            exec(f'self.highlight{str(index)}.attributes("-alpha", 0.65)')
            exec(f'self.highlight{str(index)}.config(background="#ee3377")')
            exec(f"self.highlight{str(index)}.overrideredirect(1)")
            exec(f'self.highlight{str(index)}.attributes("-topmost", 1)')
            exec(
                f'self.highlight{str(index)}.geometry("{ceil(box_width)}x{ceil(box_height)}+{ceil(cord_x)}+{ceil(cord_y)}")')
            exec(f'self.box = self.highlight{str(index)}')
            # was able to get rid of the legacy exec call below. Using the actual object fixes errors in destroying the highlight if highlighting over and over
            self.box.bind("<Button-1>", lambda command, a=self.box: self.click_item(a))  # bind click command to object
            # make sure the highlight objects persist so they are all interactive and can be deleted when method is run (see above, before loops)
            self.highlighted_items.append(self.box)




    # Detect PoE-window location
    # Returns width, height, x-, and y-offset
    def get_poe_window_location(self, option):
        hwnd = windll.user32.FindWindowW(0, 'Path of Exile')
        rect = wintypes.RECT()
        windll.user32.GetWindowRect(hwnd, pointer(rect))

        height_offset = 39  # Offset to get correct height
        width_offset = 16  # -||- width
        height = rect.bottom - rect.top - height_offset
        width = rect.right - rect.left - width_offset

        # 7 and 31 are magical offset numbers related to Windows-border size
        if option == 'windowed':
            return (width, height, rect.left + 7, rect.top + 31)
        elif option == 'fullscreen_windowed':
            return (rect.right, rect.bottom)


    # Callbacks for all Filter-Buttons
    def currency(self):
        self.stash_filtering(self.stash_finder()[1])
    def essences(self):
        self.stash_filtering(self.stash_finder()[2])
    def div_cards(self):
        self.stash_filtering(self.stash_finder()[3])
    def incubators(self):
        self.stash_filtering(self.stash_finder()[4])
    def maps(self):
        self.stash_filtering(self.stash_finder()[5])
    def veiled(self):
        self.stash_filtering(self.stash_finder()[6])
    def jewels(self):
        self.stash_filtering(self.stash_finder()[7])
    def uniques(self):
        self.stash_filtering(self.stash_finder()[8])
    def gems(self):
        self.stash_filtering(self.stash_finder()[9])
    def prophecies(self):
        self.stash_filtering(self.stash_finder()[10])
    def six_sockets(self):
        self.stash_filtering(self.stash_finder()[11])
    def fragments(self):
        self.stash_filtering(self.stash_finder()[12])
    def delve(self):
        self.stash_filtering(self.stash_finder()[13])
    def blight(self):
        self.stash_filtering(self.stash_finder()[14])
    def delirium(self):
        self.stash_filtering(self.stash_finder()[15])
    def metamorph(self):
        self.stash_filtering(self.stash_finder()[16])
    def remaining(self):
        self.stash_filtering(self.stash_finder()[17])
    # TODO: if overlay window can be sectioned off like this, can we move it to its own file or class?
    # ---------------- Overlay-Window -------------------------------------------------------------

    # builds the overlay-window from the UI-file
    def overlay(self):
        if self.settings_data[0].replace(' ', '') != '':
            self.overlay_top = tk.Toplevel()
            self.overlay_top.config(background='#424242')
            self.overlay_top.overrideredirect(1)
            self.locked = 0

            # text-fields
            self.OneHandWeapons = tk.Label(self.overlay_top)
            self.OneHandWeapons.config(anchor='w', background='#424242', foreground='#ffffff', justify='left')
            self.OneHandWeapons.config(relief='flat', takefocus=False, text='Weapons:', width='12')
            self.OneHandWeapons.grid(column='2')
            self.BodyArmours = tk.Label(self.overlay_top)
            self.BodyArmours.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.BodyArmours.config(takefocus=False, text='Armours:', width='12')
            self.BodyArmours.grid(column='3', row='0')
            self.Boots = tk.Label(self.overlay_top)
            self.Boots.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.Boots.config(takefocus=False, text='Boots:', width='12')
            self.Boots.grid(column='4', row='0')
            self.Helmets = tk.Label(self.overlay_top)
            self.Helmets.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.Helmets.config(takefocus=False, text='Helmets:', width='9')
            self.Helmets.grid(column='5', row='0')
            self.Gloves = tk.Label(self.overlay_top)
            self.Gloves.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.Gloves.config(takefocus=False, text='Gloves:', width='12')
            self.Gloves.grid(column='2', row='1')
            self.Belts = tk.Label(self.overlay_top)
            self.Belts.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.Belts.config(takefocus=False, text='Belts:', width='12')
            self.Belts.grid(column='3', row='1')
            self.Amulets = tk.Label(self.overlay_top)
            self.Amulets.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.Amulets.config(takefocus=False, text='Amulets:', width='12')
            self.Amulets.grid(column='4', row='1')
            self.Rings = tk.Label(self.overlay_top)
            self.Rings.config(anchor='w', background='#424242', foreground='#ffffff', relief='flat')
            self.Rings.config(takefocus=False, text='Rings:', width='9')
            self.Rings.grid(column='5', row='1')

            # Buttons
            self.Lock_Button = tk.Button(self.overlay_top)
            self.img_opened = self.get_img_path('opened.png')
            self.Lock_Button.config(activebackground='#424242', background='#424242', image=self.img_opened, relief='flat')
            self.Lock_Button.config(takefocus=False, width='24')
            self.Lock_Button.grid(column='1', padx='2', row='0', rowspan='2')
            self.Lock_Button.configure(command=self.lock_overlay)

            button_1 = tk.Button(self.overlay_top)
            button_1.config(activebackground='#424242', activeforeground='#ffffff', background='#424242',
                            foreground='#ffffff')
            button_1.config(takefocus=False, text='Remove Highlights', width='15')
            button_1.grid(column='7', row='0')
            button_1.configure(command=self.remove_highlights)

            button_1_3 = tk.Button(self.overlay_top)
            button_1_3.config(activebackground='#424242', activeforeground='#ffffff', background='#424242',
                              foreground='#ffffff')
            button_1_3.config(takefocus=False, text='Refresh', width='15')
            button_1_3.grid(column='7', row='1')
            button_1_3.configure(command=self.refresh_me)

            button_1_4 = tk.Button(self.overlay_top)
            button_1_4.config(activebackground='#424242', activeforeground='#ffffff', background='#424242',
                              foreground='#ffffff')
            button_1_4.config(takefocus=False, text='Chaos\nRecipe', width='9')
            button_1_4.grid(column='8', ipady='5', row='0', rowspan='2')
            button_1_4.configure(command=self.chaos_recipe)

            close_overlay = tk.Button(self.overlay_top)
            self.img_closebutton = self.get_img_path('close-button.png')
            close_overlay.config(activebackground='#424242', background='#424242', image=self.img_closebutton,
                                 relief='flat')
            close_overlay.config(takefocus=False, width='24')
            close_overlay.grid(column='0', padx='2', row='0', rowspan='2')
            close_overlay.configure(command=self.close_overlay)

            self.refresh_image = tk.Button(self.overlay_top)
            self.img_refresh30_empty = self.get_img_path('refresh30_empty.png')
            self.refresh_image.config(activebackground='#424242', background='#424242', foreground='#ffffff',
                                      image=self.img_refresh30_empty)
            self.refresh_image.config(relief='sunken', borderwidth='0', takefocus=False)
            self.refresh_image.grid(column='6', padx='2', ipadx='5', row='0', rowspan='2')

            # if old location is available -> set window location
            if self.settings_data[3].replace(' ', '') != '':
                toplevel_location_data = self.settings_data[3].split(',')
                self.overlay_top.geometry('+%s+%s' % (toplevel_location_data[0], toplevel_location_data[1]))
                # when old settings are loaded -> auto-fix the overlay on the desired position
                self.locked = 1
                self.picture = self.get_img_path("closed.png")
                self.Lock_Button.configure(image=self.picture)

            # start movement-detection
            def StartMove(event):
                self.overlay_top.x = event.x
                self.overlay_top.y = event.y

            # This handles the stop of the movement
            def StopMove(event):
                self.overlay_top.x = None
                self.overlay_top.y = None

            # This handles the actual movement
            def OnMotion(event):
                deltax = event.x - self.overlay_top.x
                deltay = event.y - self.overlay_top.y
                x = self.overlay_top.winfo_x() + deltax
                y = self.overlay_top.winfo_y() + deltay
                if not self.locked:
                    self.overlay_top.geometry("+%s+%s" % (x, y))

            # Append the functions into the overlay object
            self.overlay_top.StartMove = StartMove
            self.overlay_top.StopMove = StopMove
            self.overlay_top.OnMotion = OnMotion

            # Bind all to left mouse button (TK thinks that Button-1 is the leftmost button no matter the button name)
            self.overlay_top.bind("<ButtonPress-1>", self.overlay_top.StartMove)
            self.overlay_top.bind("<ButtonRelease-1>", self.overlay_top.StopMove)
            self.overlay_top.bind("<B1-Motion>", self.overlay_top.OnMotion)

            self.overlay_top.attributes('-topmost', 1)

            # check if there is a filter for chaos items
            self.check_chaos_items_filter()

            # calculate new variables for functionality based on the settings
            self.setup_app_with_settings()


        else:
            Msg.showinfo(title='Warning!', message='Please adjust the settings first!')
            return

    def on_modified(self, event):  ##TODO: Use a logger here instead :)
        print(f"hey buddy, {event.src_path} has been modified")

    def close_overlay(self):
        # get overlay location and save it to savefile
        overlay_location = [self.overlay_top.winfo_x(), self.overlay_top.winfo_y()]
        overlay_location = [str(i) for i in overlay_location]
        self.settings_data[3] = ','.join(overlay_location)
        with open('savefile.txt', 'w') as f:
            for i in self.settings_data:
                f.write(i + '\n')
            f.close()
        self.overlay_top.destroy()

    def lock_overlay(self):
        # when lock-button pressed -> overlay is locked, when it was free, or free when it was locked
        self.locked = not self.locked
        # change associated picture
        if self.locked:
            self.picture = self.get_img_path("closed.png")
        else:
            self.picture = self.get_img_path("opened.png")
        self.Lock_Button.configure(image=self.picture)
##TODO: Same with Settings-Window; If it is sectioned off here, can it be moved outside of this main class
# ---------------- Settings-Window -------------------------------------------------------------

    def settings(self):
        # close overlay, if its open atm
        try:
            self.close_overlay()
        except:
            pass

        # define settings window as toplevel -> only a second window
        self.settings_top = Toplevel()
        self.settings_top.title("Settings")
        self.settings_top.configure(background='#424242', height='500', width='750', padx='5', pady='5')

        # if old location is available -> set window location
        if self.settings_data[2].replace(' ', '') != '':
            toplevel_location_data = self.settings_data[2].split(',')
            self.settings_top.geometry('750x500+%s+%s' % (toplevel_location_data[0], toplevel_location_data[1]))

        # define variables for checkmarks, tried dict, but dont got it
        for i in range(10):
            exec('self.v' + str(i) + ' = ' + 'IntVar()') # not amazing but works so idc  ##TODO: Re-evaluate this
            # v0 = IntVar() ; v1 = IntVar() ; ....
        # define variables for entry-text
        for i in range(7):
            exec('self.w' + str(i) + ' = ' + 'StringVar()')

        # write data from external savefile (if available) to variables
        if self.settings_data[0].replace(' ', '') != '':
            checkbutton_data = self.settings_data[0].split(',')
            for i in range(10):
                exec('self.v' + str(i) + '.set(' + checkbutton_data[i] + ')')
        if self.settings_data[1].replace(' ', '') != '':
            entry_data = self.settings_data[1].split(',')
            for i in range(7):
                exec('self.w' + str(i) + '.set("' + entry_data[i] + '")')



        # define all checkbuttons
        quad_tab = Checkbutton(self.settings_top)
        quad_tab.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        quad_tab.config(offvalue='0', onvalue='1', overrelief='flat', selectcolor='#555555')
        quad_tab.config(takefocus=False, text='quad tab')
        quad_tab.place(anchor='nw', relx='0.03', rely='0.55', x='0', y='0')
        quad_tab.config(command=self.changed_settings, variable=self.v0)

        windowed_mode = tk.Checkbutton(self.settings_top)
        windowed_mode.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        windowed_mode.config(selectcolor='#555555', takefocus=False, text='windowed mode')
        windowed_mode.place(anchor='nw', relx='0.23', rely='0.55', x='0', y='0')
        windowed_mode.config(command=self.changed_settings, variable=self.v1)

        Body_Armours_check = tk.Checkbutton(self.settings_top)
        Body_Armours_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Body_Armours_check.config(selectcolor='#555555', takefocus=False, text='Body Armours')
        Body_Armours_check.place(anchor='nw', relx='0.03', rely='0.7475', x='0', y='0')
        Body_Armours_check.config(command=self.changed_settings, variable=self.v2)

        Helmets_check = tk.Checkbutton(self.settings_top)
        Helmets_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Helmets_check.config(selectcolor='#555555', takefocus=False, text='Helmets')
        Helmets_check.place(anchor='nw', relx='0.23', rely='0.7475', x='0', y='0')
        Helmets_check.config(command=self.changed_settings, variable=self.v3)

        Weapons_check = tk.Checkbutton(self.settings_top)
        Weapons_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Weapons_check.config(selectcolor='#555555', takefocus=False, text='Weapons')
        Weapons_check.place(anchor='nw', relx='0.43', rely='0.7475', x='0', y='0')
        Weapons_check.config(command=self.changed_settings, variable=self.v4)

        Gloves__check = tk.Checkbutton(self.settings_top)
        Gloves__check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Gloves__check.config(relief='flat', selectcolor='#555555', takefocus=False, text='Gloves')
        Gloves__check.place(anchor='nw', relx='0.65', rely='0.7475', x='0', y='0')
        Gloves__check.config(command=self.changed_settings, variable=self.v5)

        Boots_check = tk.Checkbutton(self.settings_top)
        Boots_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Boots_check.config(selectcolor='#555555', takefocus=False, text='Boots')
        Boots_check.place(anchor='nw', relx='0.03', rely='0.8125', x='0', y='0')
        Boots_check.config(command=self.changed_settings, variable=self.v6)

        Amulet_check = tk.Checkbutton(self.settings_top)
        Amulet_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Amulet_check.config(selectcolor='#555555', takefocus=False, text='Amulets')
        Amulet_check.place(anchor='nw', relx='0.23', rely='0.8125', x='0', y='0')
        Amulet_check.config(command=self.changed_settings, variable=self.v7)

        Rings_check = tk.Checkbutton(self.settings_top)
        Rings_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Rings_check.config(selectcolor='#555555', takefocus=False, text='Rings')
        Rings_check.place(anchor='nw', relx='0.43', rely='0.8125', x='0', y='0')
        Rings_check.config(command=self.changed_settings, variable=self.v8)

        Belts_check = tk.Checkbutton(self.settings_top)
        Belts_check.config(activebackground='#555555', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Belts_check.config(selectcolor='#555555', takefocus=False, text='Belts')
        Belts_check.place(anchor='nw', relx='0.65', rely='0.8125', x='0', y='0')
        Belts_check.config(command=self.changed_settings, variable=self.v9)

        # define all texts
        # first define class for creating help-texts when hovering over specific texts
        class CreateToolTip(object):
            def __init__(self, widget, text='widget info'):
                self.widget = widget
                self.text = text
                self.widget.bind("<Enter>", self.enter)
                self.widget.bind("<Leave>", self.close)

            def enter(self, event):
                x, y, cx, cy = self.widget.bbox("insert")
                x += self.widget.winfo_rootx() + 15
                y += self.widget.winfo_rooty() + 20
                # creates a toplevel window
                self.tw = tk.Toplevel(self.widget)
                # Leaves only the label and removes the app window
                self.tw.wm_overrideredirect(True)
                self.tw.wm_geometry("+%d+%d" % (x, y))
                label = tk.Label(self.tw, text=self.text, justify='left',
                                 background='white', relief='solid', borderwidth=2,
                                 font=("arial", "10", "bold"))
                label.pack(ipadx=1, ipady=1)

            def close(self, event):
                if self.tw:
                    self.tw.destroy()

        text_0 = Text(self.settings_top)
        text_0.config(background='#424242', blockcursor='true', foreground='#ffffff', height='1')
        text_0.config(relief='flat', takefocus=False, width='20')
        _text_ = '''account name:'''
        text_0.insert('0.0', _text_)
        text_0.place(anchor='nw', relx='0.03', rely='0.065', x='0', y='0')

        text_1 = tk.Text(self.settings_top)
        text_1.config(background='#424242', blockcursor='true', cursor='question_arrow', foreground='#ffffff')
        text_1.config(height='1', relief='flat', takefocus=False, width='20')
        _text_ = '''league:'''
        text_1.insert('0.0', _text_)
        text_1.place(anchor='nw', relx='0.03', rely='0.13', x='0', y='0')
        CreateToolTip(text_1,
                      'Name of the league in which you will use the app. \n'
                      'For example: "Heist", "Hardcore Heist", "SSF Heist" or "SSF Heist HC"')

        text_2 = tk.Text(self.settings_top)
        text_2.config(background='#424242', blockcursor='true', cursor='question_arrow', foreground='#ffffff')
        text_2.config(height='1', relief='flat', takefocus=False, width='20')
        _text_ = '''POESESSID:'''
        text_2.insert('0.0', _text_)
        text_2.place(anchor='nw', relx='0.03', rely='0.195', x='0', y='0')
        CreateToolTip(text_2,
                      'Just google how to get your POESESSID.')

        text_3 = tk.Text(self.settings_top)
        text_3.config(background='#424242', blockcursor='true', cursor='question_arrow', foreground='#ffffff')
        text_3.config(height='1', relief='flat', setgrid='false', takefocus=False)
        text_3.config(width='20')
        _text_ = '''main-filter:'''
        text_3.insert('0.0', _text_)
        text_3.place(anchor='nw', relx='0.03', rely='0.46', x='0', y='0')
        CreateToolTip(text_3,
                      'Choose the filter you normally use. If you don`t used this tool before a filter\n'
                      'named "chaos_items_filter.filter" will be created in your filter directory.\n'
                      'There you can individually modify the appearance of the items for the chaos recipe \n'
                      'if you want. After opening the Overlay, this program will copy the chaos_items_filter \n'
                      'in front of the last "Hide" in your main filter (default).\n'
                      'You than can copy and paste the chaos recipe section in your filter wherever you want.')
        text_4 = tk.Text(self.settings_top)
        text_4.config(background='#424242', blockcursor='true', cursor='question_arrow', foreground='#ffffff')
        text_4.config(height='1', relief='flat', takefocus=False, width='20')
        _text_ = '''item threshold:'''
        text_4.insert('0.0', _text_)
        text_4.place(anchor='nw', relx='0.03', rely='0.325', x='0', y='0')
        CreateToolTip(text_4,
                      'Amount of items from each item class which should be collected.')

        text_5 = tk.Text(self.settings_top)
        text_5.config(background='#424242', blockcursor='true', cursor='question_arrow', foreground='#ffffff', height='2')
        text_5.config(relief='flat', takefocus=False, width='20', wrap='word')
        _text_ = '''maximal number of       highlighted sets:'''
        text_5.insert('0.0', _text_)
        text_5.place(anchor='nw', relx='0.03', rely='0.38', x='0', y='0')
        CreateToolTip(text_5,
                      'Recommended is 2, because up to 2 sets will fit in the inventory.')

        text_6 = tk.Text(self.settings_top)
        text_6.config(background='#424242', blockcursor='true', cursor='question_arrow', foreground='#ffffff')
        text_6.config(height='1', relief='flat', takefocus=False, width='20')
        _text_ = '''tab number:'''
        text_6.insert('0.0', _text_)
        text_6.place(anchor='nw', relx='0.03', rely='0.26', x='0', y='0')
        CreateToolTip(text_6,
                      'Index of your loot tab (starts with 0 for the first tab in your stash).\n'
                      'Actually only one tab is supported.')

        text_7 = tk.Text(self.settings_top)
        text_7.config(background='#424242', blockcursor='true', foreground='#ffffff', height='1')
        text_7.config(insertunfocussed='none', relief='flat', takefocus=False, width='30')
        _text_ = '''ignore item threshold for:'''
        text_7.insert('0.0', _text_)
        text_7.place(anchor='nw', relx='0.03', rely='0.676', x='0', y='0')

        # define entry-fields

        account_name = tk.Entry(self.settings_top)
        account_name.config(font='{arial ce} 10 {bold}', validate='key', width='60')
        account_name.place(anchor='nw', relx='0.25', rely='0.065', x='0', y='0')
        account_name.configure(validatecommand=self.changed_settings, textvariable=self.w0)
        league = tk.Entry(self.settings_top)
        league.config(font='{arial ce} 10 {bold}', validate='key', width='60')
        league.place(anchor='nw', relx='0.25', rely='0.13', x='0', y='0')
        league.configure(validatecommand=self.changed_settings, textvariable=self.w1)
        poesessid = tk.Entry(self.settings_top)
        poesessid.config(font='{arial ce} 10 {bold}', validate='key', width='60')
        poesessid.place(anchor='nw', relx='0.25', rely='0.195', x='0', y='0')
        poesessid.configure(validatecommand=self.changed_settings, textvariable=self.w2)
        tab_number = tk.Entry(self.settings_top)
        tab_number.config(font='{arial ce} 10 {bold}', validate='key', width='4')
        tab_number.place(anchor='nw', relx='0.25', rely='0.26', x='0', y='0')
        tab_number.configure(validatecommand=self.changed_settings, textvariable=self.w3)
        item_threshold = tk.Entry(self.settings_top)
        item_threshold.config(font='{arial ce} 10 {bold}', validate='key', width='4')
        item_threshold.place(anchor='nw', relx='0.25', rely='0.325', x='0', y='0')
        item_threshold.configure(validatecommand=self.changed_settings, textvariable=self.w4)
        max_hightlighted_sets = tk.Entry(self.settings_top)
        max_hightlighted_sets.config(font='{arial ce} 10 {bold}', validate='key', width='4')
        max_hightlighted_sets.place(anchor='nw', relx='0.25', rely='0.391', x='0', y='0')
        max_hightlighted_sets.configure(validatecommand=self.changed_settings, textvariable=self.w5)
        filter_directory = tk.Entry(self.settings_top)
        filter_directory.config(font='{arial ce} 10 {bold}', validate='key', width='60')
        filter_directory.place(anchor='nw', relx='0.25', rely='0.46', x='0', y='0')
        filter_directory.configure(validatecommand=self.changed_settings, textvariable=self.w6)

        # define buttons

        browse = tk.Button(self.settings_top)
        browse.config(activebackground='#424242', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        browse.config(takefocus=False, text='Browse', width='12')
        browse.place(anchor='nw', relx='0.835', rely='0.454', x='0', y='0')
        browse.configure(command=self.browse_for_filter_dir)

        Close = tk.Button(self.settings_top)
        Close.config(activebackground='#424242', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        Close.config(takefocus=False, text='Close', width='12')
        Close.place(anchor='nw', relx='0.733', rely='0.945', x='0', y='0')
        Close.configure(command=self.close_settings)

        self.Apply = tk.Button(self.settings_top)
        self.Apply.config(activebackground='#424242', activeforeground='#ffffff', background='#424242', foreground='#ffffff')
        self.Apply.config(state='disabled', takefocus=False, text='Apply', width='12')
        self.Apply.place(anchor='nw', relx='0.87', rely='0.945', x='0', y='0')
        self.Apply.configure(command=self.apply_settings)

        # change icon
        icon = 'icon.ico'
        if getattr(sys, 'frozen', False):
            self.settings_top.wm_iconbitmap(os.path.join(sys._MEIPASS, icon))
        else:
            self.settings_top.wm_iconbitmap(icon)

    # browse for filter-path
    def browse_for_filter_dir(self):
        self.filterpath = filedialog.askopenfilename()      # path from the selected main-filter
        self.w6.set(self.filterpath)
        self.settings_data[5] = self.filterpath
        with open('savefile.txt', 'w') as f:
            for i in self.settings_data:
                f.write(i + '\n')
            f.close()

    def changed_settings(self):
        # this method triggers when something is changed in all of the entry-textfields or checkmarks
        # it will enable the "Apply"-button to apply and save the changes
        # i know using the validation-callback is not smart (focus_get would be nicer) but it works so idc ## TODO:
        try:
            self.Apply['state'] = 'normal'
            return True
        except:
            return True

    def apply_settings(self):
        self.Apply['state'] = 'disabled'
        # after setting the program up, write all the changes in lists so we can use it
        self.text_list = [self.w0.get(), self.w1.get(), self.w2.get(), self.w3.get(), self.w4.get(), self.w5.get(), self.w6.get()] # contains all infos from text-fields
        self.checkmark_list = [self.v0.get(), self.v1.get(), self.v2.get(), self.v3.get(), self.v4.get(), self.v5.get(), self.v6.get(), self.v7.get(), self.v8.get(), self.v9.get()] # contains all infos from checkmarks
        print('new settings for entrys and checkbuttons:')
        print(self.text_list)
        print(self.checkmark_list)
        self.checkmark_list = [str(i) for i in self.checkmark_list]
        self.settings_data[0] = ','.join(self.checkmark_list)
        self.settings_data[1] = ','.join(self.text_list)
        with open('savefile.txt', 'w') as f: # general code to write the actual settings_data to savefile
            for i in self.settings_data:
                f.write(i+'\n')
            f.close()
        # now we have the dirpath from the mainfilter -> check for chaos items filter
        self.check_chaos_items_filter()



    # close settings with close-button
    def close_settings(self):
        settings_location = [self.settings_top.winfo_x(), self.settings_top.winfo_y()]
        settings_location = [str(i) for i in settings_location]
        self.settings_data[2] = ','.join(settings_location)
        with open('savefile.txt', 'w') as f:
            for i in self.settings_data:
                f.write(i + '\n')
            f.close()
        self.settings_top.destroy()




def shut_down():
    # get mainwindow location
    root_location = [root.winfo_x(), root.winfo_y()]
    root_location = [str(i) for i in root_location]
    root_location = ','.join(root_location)
    # get data from savefile
    savefile = open('savefile.txt', 'r')
    settings_data = savefile.read().splitlines()  # each line -> one entity in list
    savefile.close()
    # save data to savefile
    settings_data[4] = root_location
    with open('savefile.txt', 'w') as f:
        for i in settings_data:
            f.write(i + '\n')
        f.close()
    # shut program down
    root.destroy()


# ---------------- actually starting the entire program -------------------------------------------------------------
##TODO: Wrap in if __name__ == '__main__':
root = tk.Tk()
root.title('Path of Exile - Quality of Life Tool')
root.protocol('WM_DELETE_WINDOW', shut_down)
app = MyApplication()
icon = 'icon.ico'
if getattr(sys, 'frozen', False):
    root.wm_iconbitmap(os.path.join(sys._MEIPASS, icon))
else:
    root.wm_iconbitmap(icon)
app.run()