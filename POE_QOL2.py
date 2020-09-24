import tkinter as tk
import tkinter.messagebox as Msg
from tkinter import filedialog
import pygubu, pyautogui
from math import floor
import requests, json, configparser
from pygubu.builder import ttkstdwidgets
import os, time
from pathlib import Path
from math import ceil
# import win32con, win32gui
from tkinter import font
import datetime
import pyperclip

def debug_app(debug_bool):
        import sys
        sys.stdout = open('poeqol2_logfile.txt', 'w')
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        return pp

def click_item(a, b, c):
    """
    Used for when the user clicks on the highlight. Destroys the highlight and passes through the click action.
    Wish I knew how to make it 'click-through able'
    """
    a.destroy()
    # exec(f"app.{a}.destroy()")  #legacy -notaspy 14-9-2020
    x, y = pyautogui.position()
    pyautogui.click(x=x, y=y)  


class MyApplication(pygubu.TkApplication):

    def __init__(self, master=None):
        """
        This seems fine. -notaspy 14-9-2020
        """
        self.config = configparser.ConfigParser()
        self.config.read('setup.ini')

        DEBUG = (self.config['Config']['debug'].lower() == 'true' or 'y' in self.config['Config']['debug'].lower() or self.config['Config']['debug'].lower() != 0)
        if DEBUG:
            self.DEBUG = True
            self.pp = debug_app(debug_bool=DEBUG)
            self.pp.pprint("Setting up App")
            self.pp.pprint("Initializing App")
        else:
            self.DEBUG = False
        super().__init__(master=master)

    def _create_ui(self):
        if self.DEBUG:
            self.pp.pprint("Creating UI")
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path('.')
        builder.add_from_file('Gui_Button_V2.ui')
        self.mainwindow = builder.get_object('Frame_1', self.master)
        self.font = font.Font(self.master, family="Times", size=20, weight="bold")
        builder.connect_callbacks(self)

        # TODO: Create a method that reloads the Setup.ini file before executing certain methods so it can be updated on the fly
        # TODO: Validate the Setup.ini file contents and formatting and instruct user how to fix it if necessary
        # TODO: Validate the chaos_items_filter.filter file contents and formatting and instruct user how to fix it if necessary
        # TODO: Restore the original main filter file one exit. I really am bad at handling exit callbacks
        # TODO: The overlay widget doesn't seem to sync with the local stash record (self.latest_stash)
        # self.check_filter()  # This is legacy, to set the self.active_status parameter. I don't think that is needed anymore
        self.setup_app()

    def setup_app(self):

        """
        We run this on initialization. This is a separate method so that we can reload the settings while app is running. It *might* cause some undesired effects. TBD
        """
        if self.DEBUG:
            self.pp.pprint("Setting Up App")
        #Note to self,  from trying a bunch of different resolutions and 3 monitors i found that,
        # stash/inv tabs had a fixed width to height ratio of 886/1440 (~0.6153)that must be obeyed.
        self.screen_res = [int(dim) for dim in self.config['Config']['screen_res'].split('x')]
        if len(self.screen_res) != 2:
            raise ValueError("Screen Resolution was not given correctly. Use no spaces and only a single 'x'.")
        # self.tab_width_frac = 888/1440 * self.screen_res[1] / self.screen_res[0] # Not actually used in the end.
        # from same experiments, stash starts 22 pixels away from edge, or 22/1440 fraction of screen width, and top is 215/1440 fraction.
        self.tab_origin = 22/1440 * self.screen_res[1], 215/1440 * self.screen_res[1]
        # apply similar rules to ending coordinates  -notaspy 14-9-2020
        self.tab_end = 864/1440 * self.screen_res[1], 1057/1440 * self.screen_res[1]
        # scale the size of a stash tab box depending on if it is quad or not.
        # TODO: currently set by user, but can actually get this from the site request
        if self.config['Config']['quad_tab'].lower() == 'true':
            box_density_scalar = 24
        else:
            box_density_scalar = 12
        # store the dimensions of an individual stash tab box (could be rectangular for some resolutions, so we store width and height)
        self.box_width = (self.tab_end[0] - self.tab_origin[0]) / (box_density_scalar)
        self.box_height = (self.tab_end[1] - self.tab_origin[1]) / (box_density_scalar)
        # Store some meta-data about each item slot
        # Probably better to use another data-structure other than a list of dicts
        # scheme is [normalized width,
        # normalized height,
        # highlight color (can use any tk names color for now),
        # order user should add item to inventory to avoid inventory tetris fail situations,
        # threshold of how many items before dynamic filter editor starts to hide this item slot
        #]
        # TODO: We can get the sizes of the items directly from the site, rather than hard coding them as below
        self.item_details = dict(
            Rings=[1, 1, '#33bbee', '4', int(self.config['Config']['threshold'])*2],
            OneHandWeapons=[1, 3, '#bbbbbb', '1', int(self.config['Config']['threshold'])*2],
            BodyArmours=[2, 3, '#ee3377', '1', int(self.config['Config']['threshold'])],
            Helmets=[2, 2, '#cc3311', '2', int(self.config['Config']['threshold'])],
            Gloves=[2, 2, '#ee7733', '2', int(self.config['Config']['threshold'])],
            Boots=[2, 2, '#009988', '2', int(self.config['Config']['threshold'])],
            Belts=[2, 1, '#0077bb', '3', int(self.config['Config']['threshold'])],
            Amulets=[1, 1, '#33bbee', '4', int(self.config['Config']['threshold'])],
            )
        # below is legacy code for when the screen resolution was hard-coded -notaspy 14-9-2020
        ## if self.config['Config']['screen_res'] == '1920x1080':
        ##     for win in getWindowSizes():
        ##         print(win)
        ##         if 'Path of Exile' in win[2]:
        ##             win32gui.SetWindowPos(win[0], win32con.HWND_NOTOPMOST, 0, 0, 1920, 1081, 0)
        
        # Here is where things start to get convoluted with me trying to re-do the algorithm. I'd like to streamline this.
        # I'll try to comment as best I can here and elsewhere

        # This is legacy, but works okay, so left it. stash_finder returns a dict of item slots and thier coordinates in the stash for unid'd and id'd items.
        # id'd items are basically ignored in this code, so not sure why they are tracked. Could be useful in future iterations.
        # self.unident and self.ident represent the remote inventory last time it was checked. These values should not be changed other than when the remote has changed.
        #TODO: Use data about identified items
        self.unident, self.ident = self.stash_finder()
        # Since the app has asynchronous knowledge of the items in tab, we want to have some local record. We'll call that latest_stash and allow it to be changed.
        # ~~~IMPORTANT~~~~: The remote snapshot and the local record are two separate dict parameters and a length-2 list of dicts. I need to change this for consistency
        # TODO: refactor remote snapshot and local record to be either both lists or both separate dicts for unidentified and identified items
        self.latest_stash = list((self.unident.copy(), self.ident.copy()))

        # initialize data for app's filter algorithm
        self.chaos_items_filter_sections = self.read_default_chaos_filter_sections()  # the custom formatting for items that match the chaos recipe
        self.pre_process_item_filter()
        # initial dynamic filter update
        self.update_filter()
        # check if the local and remote inventories are synchronized. Uses the refresh rate (in seconds) set in the Setup.ini file.
        # I don't know the actual refresh rate of the website; seems random.
        # Probably fine to assume that the local record is most accurate for 60s since it should take about that long to vendor everything.
        self.check_inventory_sync()  # Can't remember why I do this here, but it doesn't hurt anything (lol only one day later and I can't remember yikes)
        # Because of all the wonky `exec` calls, I am keeping track of the highlight overlay objects created by the self.chaos_recipe() method
        self.highlighted_items = []
        if self.DEBUG:   
            self.pp.pprint("Done setting up App")

    def run(self):
        """Run the main loop. Self explanatory."""
        self.mainwindow.mainloop()

    def remove_highlights(self, update_local_record=True):
        """
        In case the user wants to manually remove the highlights on screen. By default it resets to local record to be synced with the remote snapshot.
        We assume the user did not click on items if they removed all the highlights.
        This is prone to errors if a user clicks on some, but not all of the highlights and then clicks this button.
        TODO: handle half-removed highlights in combination with this method.
        """
        if self.highlighted_items:  # test that highlight actually exist that need deletion
            for highlight in self.highlighted_items:  # delete them
                highlight.destroy()
            if update_local_record:  # update the snapshot and local record if requested
                self.unident, self.ident = self.stash_finder()
                self.latest_stash = list((self.unident.copy(), self.ident.copy()))
            return True
        else:
            return False

    def chaos_recipe(self):
        """
        The meat of the program. Based on the number of complete sets, create top-level geometries that highlight areas of the screens for each item in the set.
        TODO: Make it so that the item is removed from local inventor ONLY if the user clicks on the highlight box. I am sure someone will click it without actually removing the item and it will not be recognize and user will complain.
        # TODO: HIGH Priority: figure out why sometimes the same initial areas are highlighted. I may have fixed this by checking the inventory sync (and for left over highlights) first thing
        """
        # if any previous highlights still exist, destroy them. 
        # If we don't do this, the way it is written below, if user doesn't manually click each highlight, they become non-interactive.
        # So, just killing everything is the fast and dirty way I decided wipe the screen clear if needed.
        if self.check_inventory_sync():
            self.remove_highlights(update_local_record=False)
        else:
            self.remove_highlights(update_local_record=True)

        # get a dictionary of the LOCAL complete sets items. 
        # this will be sync'd with the online stash if this is the first time this method has been called since last remote refresh
        # If user has clicked on a highlighted item, it gets removed locally, but the remote won't know that for a little.    
        # Dict keys are the slot name and values are the normalized positions.
        # the positions are lists of length-2 lists:eg [[x0, y0], [x1, y1]]

        unident = self.check_complete_set()

        # unident will be an empty dict if there's no complete sets left, and will inform user
        # TODO: This should work better
        if not unident:
            Msg.showinfo(title='POE QoL', message='Not enough Chaos Recipe Items')
        # if we have sets, go into the highlighting logic
        else:

            # loop through each item slot (key)
            for x in unident:
                if self.DEBUG:
                    self.pp.pprint(('Item Slot:', x))
                    self.pp.pprint(('Item coordinates', unident[x]))
                # we will count from the top-left origin
                x_off = self.tab_origin[0]
                y_off = self.tab_origin[1]
                # cord_x, cord_y = self.unident[x].pop(0)  # Leaving this here so you can see the previous method was to pop items from the list. It was problematic. -notaspy 14-9-2020
                for i in range(len(unident[x])):
                    # reimplemented this as a loop over the items that make up the number of complete sets
                    # The execs are legacy. I don't like them, and could probably re-do it, but won't atm
                    #TODO: refactor exec usage
                    cord_x, cord_y = unident[x][i]  # get coordinates of entry
                    cord_x = cord_x * self.box_width + x_off  # convert coordinates to pixels
                    cord_y = cord_y * self.box_height + y_off
                    if self.DEBUG:
                        self.pp.pprint(('Screen Coordinates:',(cord_x, cord_y)))
                    box_width = self.box_width * self.item_details[x][0]  # based on the meta-data about item size in self.item_details, make appropriate size box
                    box_height = self.box_height * self.item_details[x][1]
                    if self.DEBUG:       
                        self.pp.pprint(('Box dimensions (pixels):',(box_width, box_height)))
                    # below is legacy
                    # basically it creates a semi-transparent top level window that disappears when it is clicked. I decided to use different colors by item slot
                    exec(f"self.{x + str(i)} = tk.Toplevel(self.mainwindow)")
                    exec(f'self.{x + str(i)}.attributes("-alpha", 0.65)')
                    exec(f'self.{x + str(i)}.config(background="{self.item_details[x][2]}")')
                    exec(f"self.{x + str(i)}.overrideredirect(1)")
                    exec(f'self.{x + str(i)}.attributes("-topmost", 1)')
                    exec(f'self.{x + str(i)}.geometry("{ceil(box_width)}x{ceil(box_height)}+{ceil(cord_x)}+{ceil(cord_y)}")')
                    exec(f'self.box = self.{x + str(i)}')
                    # was able to get rid of the legacy exec call below. Using the actual object fixes errors in destroying the highlight if highlighting over and over
                    # exec(f'self.{x + str(i)}.bind("<Button-1>",lambda command, a=x,b=cord_x,c=cord_y: click_item(a,b,c))')  #legacy -notaspy 14-9-2020
                    self.box.bind("<Button-1>",lambda command, a=self.box,b=cord_x,c=cord_y: click_item(a,b,c))  #bind click command to object
                    # make sure the highlight objects persist so they are all interactive and can be deleted when method is run (see above, before loops)
                    self.highlighted_items.append(self.box)

    def check_inventory_sync(self):
        """
        This is kinda useful. Checks if the local and remote stashes are the same OR if the user-give refresh interval has elapsed.
        Sets and returns a bool. I made this. -notaspy 14-9-2020
        """
        t_check = datetime.datetime.now()  # get current time
        t_previous_check = self.last_update  # we need to have this here since it is reset by the next call to self.stash_finder()
        # compare local and remote stash inventories. short circuits if the refresh time has not elapsed
        remote_inventory_unident, remote_inventory_ident = self.stash_finder()
        if (t_check - t_previous_check) < datetime.timedelta(seconds=float(self.config['Config']['refresh_time'])) and remote_inventory_unident == self.unident:
            self.synced = True
        else:
            self.synced = False
        if self.DEBUG:
            self.pp.pprint(f"Synced?: {self.synced}")
        return self.synced

    def check_complete_set(self):
        """
        This is kind-of a Frakenstein code between legacy and my own.
        I did my best to re-implement the logic to handle the local/remote problem. -notaspy 14-9-2020
        """
        # If the local inventory and the last snapshot are not sync'd, update the remote snap shot and also make it the latest local stash inventory
        if not self.check_inventory_sync():
            self.unident, self.ident = self.stash_finder()
            self.latest_stash = (self.unident, self.ident)
            if self.DEBUG:
                self.pp.pprint(self.unident)
        # legacy test for existance of the attributes. kinda tried to refactor it. Functional but not pretty. 
        # Notice the different syntax for the remote snapshot and the local record (ie local is a list of dicts)
        try:
            self.unident
            self.latest_stash[0]
        except AttributeError:
            self.unident, self.ident = self.stash_finder()
            self.latest_stash[0] = (self.unident, self.ident)
        else:
            # Some more meat. Check for peices of a complete chaos set.
            # first, if we don't have enough rings or one-handed weapons, just return false
            if len(self.latest_stash[0]["Rings"]) < 2 or len(self.latest_stash[0]['OneHandWeapons']) < 2:
                return False
            # If we do, continue to determine how many sets we can make
            else:
                # Find the limiting two-slot item
                two_slot_max_sets = min((floor(len(self.latest_stash[0]["Rings"]) / 2), floor(len(self.latest_stash[0]["OneHandWeapons"]) / 2)))
                # Find limiting one-slot items
                one_slot_max_sets = min([len(self.latest_stash[0][_key]) for _key in self.latest_stash[0].keys() if _key not in ["Rings", "OneHandWeapons"]])
                # Find out if we are limited by two-slot, one-slot, or the user set maximum number of highlighted sets
                max_sets = min((two_slot_max_sets, one_slot_max_sets, int(self.config['Config']['highlight_max_num_sets'])))
                # if we have 1 or more sets, create a dictionary of the items that make up the sets
                # this only works for unidentified sets
                # TODO: do same for identified items?
                if max_sets:
                    unident_sets = {_key:[] for _key in self.item_details.keys()}  # create a dictionary of empty lists to fill in and return
                    # loop through each slot and find the maximum index in the list of coordinates for each item. We use this to only take the valid items.
                    for key in self.item_details.keys():
                        if self.DEBUG:
                            self.pp.pprint(f"Item Slot name for item in {max_sets} complete sets: {key}")
                        if key in ["Rings", "OneHandWeapons"]:  # we need two of these, so the maximum index is twice that of the other items
                            max_index = 2 * max_sets
                        else:
                            max_index = max_sets
                        # Grab the items and their coordinates up the the maximum. These are dicts with the type of slot as the key, and a list of length-2 coordinates lists
                        # I think we don't want to 'pop' the item from the list because the loop will then try to access indexes that are outside the list length
                        for i in range(max_index):
                            unident_sets[key].append(self.latest_stash[0][key][i].copy())
                            if self.DEBUG:
                                self.pp.pprint(f"Item of slot {key}, item number {i} passed to highlighting method self.chaos_recipe(): {unident_sets[key][-1]}")
                    # Now remove these from the local inventory record. This could be more efficient by combining with the above, I am sure
                    # TODO: This logic needs testing and scrutiny. I am not 100% sure it is doing what I think it is.
                    for key in self.item_details.keys():
                        indices_to_delete = []
                        if self.DEBUG:
                            self.pp.pprint((f"self.latest_stash entry of {key}:", self.latest_stash[0][key]))
                        for i in range(len(self.latest_stash[0][key])):
                            if self.latest_stash[0][key][i] in unident_sets[key]:
                                indices_to_delete.append(i)
                                continue
                        # only keep the items that are not about to be highlighted
                        self.latest_stash[0][key] = [_ for j, _ in enumerate(self.latest_stash[0][key]) if j not in indices_to_delete]
                    return unident_sets
                else:
                    # If we didn't have enough items for a complete set, return False
                    return False

    def show_chaos(self):
        """
        This is all legacy. It creates and shows the overlay that has a running counter of items in each stash
        I did not make changes other than to comment out the error being raised if the monitor was not 1920x1080
        I honestly don't know what the buttons are even for, they never show up?
        It uses this bizzare and obscure pygubu library.
        It also relies on some html file that comes with this code (or ccs? idk some web language)
        """
        self.builder2 = pygubu.Builder()
        self.builder2.add_from_file('Gui_Button_V2.ui')
        self.top3 = tk.Toplevel(self.mainwindow)
        # self.top3 = tk.Toplevel(self.mainwindow)
        self.frame3 = self.builder2.get_object('Frame_2', self.top3)
        self.builder2.connect_callbacks(self)
        self.top3.overrideredirect(1)
        print(self.top3.__dict__)
        # I went ahead and put this at bottom center
        overlay_location = f'+{self.screen_res[0] // 2 - 130}+{floor(self.screen_res[1] * (1 - 80/1080))}'
        self.top3.geometry(overlay_location)
        self.top3._offsetx = 260
        self.top3._offsety = 80

        def clickwin(event):
            self.top3._offsetx = event.x
            self.top3._offsety = event.y
        def move_overlay(event):
            x = round(self.top3.winfo_pointerx() - self.top3._offsetx)
            y = round(self.top3.winfo_pointery() - self.top3._offsety)
            print(x, y)
            self.top3.geometry('+{x}+{y}'.format(x=x,y=y))
        self.top3.clickwin = clickwin
        self.top3.move_overlay = move_overlay
        self.top3.bind('<Button-1>',self.top3.clickwin)
        self.top3.bind('<B1-Motion>',self.top3.move_overlay)
        if self.DEBUG:
            self.pp.pprint(f'Overlay Location:{overlay_location}')
        # if self.config['Config']['screen_res'] == '1920x1018':
        #     self.top3.geometry('+1180+900')
        # elif self.config['Config']['screen_res'] == '1920x1080':
        #     self.top3.geometry('+1180+940')
        # else:
        #     Msg.showinfo(title='POE QoL', message='Wrong Resolution msg: macr0s on Discord')
        self.top3.attributes('-topmost', 1)
        self.refresh_me()

    def close_overlay(self):
        # more legacy for overlay
        self.top3.destroy()


    # def move_overlay(self, event):
    #     x = self.top3.winfo_pointerx() - self.top3._offsetx
    #     y = self.top3.winfo_pointery() - self.top3._offsety
    #     print(x, y)
    #     self.top3.geometry('+{x}+{y}'.format(x=x,y=y))


    def refresh_me(self):
        # Refreshes the running count of unidentified and identified items in the stash tab.
        # Fails silently if inventories are considered synced
        # more legacy.  Tried harder to make this work better with the syncing scheme
        self.check_inventory_sync()
        if not self.synced:
            self.unident, self.ident = self.stash_finder()
            self.latest_stash = list((self.unident.copy(), self.ident.copy()))
        if self.DEBUG:
            self.pp.pprint("Refreshing filter within refresh me.")
            # unident, ident = self.stash_finder()
        for key, value in self.unident.items():
            alternative = len(self.ident.get(key, 0))
            exec(f'self.builder2.get_object("{key}").configure(text="{key[:4]}: {len(value)}/{alternative}")')
        if self.DEBUG:
            self.pp.pprint("Printing Out Latest Stash:")
            self.pp.pprint(self.latest_stash)
            self.pp.pprint("Printing Out Latest Snapshot:")
            self.pp.pprint(self.unident)
        self.update_filter()


    def check_filter(self):
        """
        Legacy dynamic filter code. This doesn't work as far as I can tell. I am in the process of re-implementing this.
        Right now all I can tell it is good for is setting the self.active_status parameter. Other methods looks for this.
        This is called in the init method.
        """
        rewrite = 0
        with open(self.config['Config']['filter'], 'r') as f:
            lines = f.readlines()
            if '# Chaos Recipe Ring' not in lines[0]:
                rewrite = 1
        if rewrite == 1:
            with open(self.config['Config']['filter'], 'w') as f:
                filterfile = open(self.config['Config']['filter'])
                f.write(filterfile.read())
                filterfile.close()
                for line in lines:
                    f.writelines(line)

        self.active_status = {'Rings':[1, lines[1]],
                              'Belts':[15, lines[15]],
                              'Amulets':[28, lines[28]],
                              'Boots':[41, lines[41]],
                              'Gloves':[55, lines[55]],
                              'Helmets':[69, lines[69]],
                              'BodyArmours':[83, lines[83]],
                              'OneHandWeapons':[97, lines[97]]
                            }

    def stash_finder(self):
        """
        Legacy code. This works well enough.
        Grabs the json object of the stash tab. Takes only the items, and grabs their stash position if they are unidentified.
        TODO: Right now, the items are disordered. They should be ordered to register from top-left to bottom right for efficiency
        """
        pos_last_unid = {'BodyArmours':[],  'Helmets':[],  'OneHandWeapons':[],  'Gloves':[],  'Boots':[],  'Amulets':[],  'Belts':[],  'Rings':[]}
        pos_last_id = {'BodyArmours':[],  'Helmets':[],  'OneHandWeapons':[],  'Gloves':[],  'Boots':[],  'Amulets':[],  'Belts':[],  'Rings':[]}

        stash_tab = f"https://www.pathofexile.com/character-window/get-stash-items?league={self.config['Config']['league']}&tabIndex={self.config['Config']['tab']}&accountName={self.config['Config']['account']}"
        payload = {
        'league': self.config['Config']['league'],
        'tabIndex': self.config['Config']['tab'],
        'accountName': self.config['Config']['account'].encode('utf-8'),
        }
        if self.DEBUG:
            self.pp.pprint("Pulling from pathofexile.com")
            self.pp.pprint("trying payload: {}".format(payload))
            self.pp.pprint(f"trying: {stash_tab}")
        try:
            a = requests.get(stash_tab, cookies=dict(POESESSID=(self.config['Config']['POESESSID'])), params=payload)
        except requests.HTTPError as exception:
            Msg.showinfo(title='POE QoL', message='Could not connect to pathofexile.com.')

        if self.DEBUG:
            try:
                self.pp.pprint("json retrieved:")
                self.pp.pprint(json.loads(a.text)['items'])
            except:  # I have no clue what error types might return here, but I want to output something to log file
                self.pp.pprint("JSON could not be output to logfile.")
        self.last_update = datetime.datetime.now()  #added by notaspy 14-9-2020
        # I am not sure the logic here. It is able to find the item coordinates, but it looks like it does it twice. Didn't mess with it
        try:
            json.loads(a.text)['items']
        except KeyError:
            Msg.showinfo(title='POE QoL', message='Bad Response from pathofexile.com. Please check your Setup file that the accoud and POESESSID are correct and current as a first step (and restart app if they needed to be changed).')
            #TODO: log this error in a log file
        for x in json.loads(a.text)['items']:
            if x['name'] == '' and x['frameType'] != 3:
                if 'BodyArmours' in x['icon']:
                    pos_last_unid['BodyArmours'].append([x['x'], x['y']])
                elif 'Helmets' in x['icon']:
                    pos_last_unid['Helmets'].append([x['x'], x['y']])
                elif 'OneHandWeapons' in x['icon']:
                    pos_last_unid['OneHandWeapons'].append([x['x'], x['y']])
                elif 'Gloves' in x['icon']:
                    pos_last_unid['Gloves'].append([x['x'], x['y']])
                elif 'Boots' in x['icon']:
                    pos_last_unid['Boots'].append([x['x'], x['y']])
                elif 'Amulets' in x['icon']:
                    pos_last_unid['Amulets'].append([x['x'], x['y']])
                elif 'Belts' in x['icon']:
                    pos_last_unid['Belts'].append([x['x'], x['y']])
                elif 'Rings' in x['icon']:
                    pos_last_unid['Rings'].append([x['x'], x['y']])
            else:
                #TODO: This is what handles unknown/new items i think. It is 99% probably responsible for the download short circuit on alternate artwork
                if x['frameType'] == 3:  # I dont know what this is fore
                    pass
                else:
                    if 'BodyArmours' in x['icon']:
                        pos_last_id['BodyArmours'].append([x['x'], x['y']])
                    else:
                        if 'Helmets' in x['icon']:
                            pos_last_id['Helmets'].append([x['x'], x['y']])
                        else:
                            if 'OneHandWeapons' in x['icon']:
                                pos_last_id['OneHandWeapons'].append([x['x'], x['y']])
                            else:
                                if 'Gloves' in x['icon']:
                                    pos_last_id['Gloves'].append([x['x'], x['y']])
                                else:
                                    if 'Boots' in x['icon']:
                                        pos_last_id['Boots'].append([x['x'], x['y']])
                                    else:
                                        if 'Amulets' in x['icon']:
                                            pos_last_id['Amulets'].append([x['x'], x['y']])
                                        else:
                                            if 'Belts' in x['icon']:
                                                pos_last_id['Belts'].append([x['x'], x['y']])
                                            else:
                                                if 'Rings' in x['icon']:
                                                    pos_last_id['Rings'].append([x['x'], x['y']])
        else:
            return (pos_last_unid, pos_last_id)

    # below is some half-implemented code for dynamically updating a main filter file. Idea is to be able to use your normal filter along with this helper. 
    # I could use some help/optimization here. -notaspy 14-9-2020
    def read_default_chaos_filter_sections(self):
        """
        User can use the filter that comes with this program, or customize each slot to their liking.
        Only important things are that each section starts with a '#' and has the correct item slot name in that line
        Correct item slots are give in the self.item_details parameter. This should be the last word in the comment line.
        """
        with open(self.config['Config']['chaos_items_filter'], 'r') as fil:
            chaos_filter = fil.readlines()  # read whole file into memory. each line is stored as a string in a list
            section_lines_start_end = []  # need a place to store where sections start and end
            section_starts = []
            for i, line in enumerate(chaos_filter):  # loop through the lines
                _line = line.lstrip()  # remove any leading white space
                # If the line is a comment, record that as the start of an item slot section
                # We need to protect from empty lines which are stored as zero-length lists
                if self.DEBUG:
                    self.pp.pprint(("Default Filter Line as read:", _line))
                    self.pp.pprint(("Result of bool test for empty line:", not _line))
                    if _line:
                        self.pp.pprint(("Result of bool test for comment:", not _line[0] == "#"))
                if not _line or not _line[0] == "#":
                    continue  
                elif  _line and _line[0] == "#":  # I shouldn't need to, but I double check that the line is a comment anyway
                    section_starts.append(i)
            # each section ends where the next begins. The last section goes to the last line in the list, so concatenate that to the other ending indicies
            section_ends = [i for i in section_starts[1:]] + [len(chaos_filter)+1]
            # create empty dictionary for storing the text of each section
            sections = {}
            # store the text for each section in the dictionary. The key for each section is the last word in the first line, chaos_filter[i].split(" ")[-1].rstrip(). This is maybe a dumb way of doing this and prone to user error.
            # TODO: Find a better way to get the section keys -- Update, trying this below now.
            for i, j in zip(section_starts, section_ends):
                # sections[chaos_filter[i].split(" ")[-1].rstrip()] = chaos_filter[i:j]  # for each key, separate line into list of words, ensure whitespace is stripped. Text is from starting to ending indices
                for k in range(i, j-1):  #loop through all the lines in the section
                    print(k)
                    linelistcopy = chaos_filter[k][:].split(" ") # create a copy to work with and remove white space and make a list
                    linelistcopy = [str(_).rstrip().replace("'", '') for _ in linelistcopy] # convert to strings wihtout quotes...?
                    linelistcopy = [_.replace('"', '') for _ in linelistcopy] # convert to strings wihtout quotes...?
                    self.pp.pprint(linelistcopy)
                    if linelistcopy[0].lower() == 'class':
                        if "One" in linelistcopy and  "Hand" in linelistcopy:
                            section_class_key = "OneHandWeapons"
                        elif linelistcopy[1].lower() == 'body':
                            section_class_key = "BodyArmours"
                        else:
                            section_class_key = linelistcopy[1]
                sections[section_class_key.rstrip()] = chaos_filter[i:j]

            if self.DEBUG:
                self.pp.pprint(sections)
        return sections

    def pre_process_item_filter(self):
        """
        This accomplishes a few tasks that only need to be performed once on start up.
        1) Determine if the included filter is in the users My Games\\Path of Exile\\ directory. If it exists we open it, and if not, we open the included default.
        2) Open that file and find the starting and ending lines of the chaos recipe items and remember those for updating. These are bound by the random strings '234hn50987sd' and '2345ina8dsf7' respectively.
        3) Store the parts of the item filter that don't change into memory. The current filter is small (~350kB), so we don't need to worry about memory. This saves from needing to ever read it again.
        4) Insert the chaos_items_filter.filter contents into the filter text and write the file to the user's USERPROFILE\\Documents\\My Games\\Path of Exile\\ directory
        We want to be reading and searching this file once.
        """
        #TODO: Maybe someone has a custom location for their item filters, so this search path probably shouldn't be hard coded like this
        # self.main_filter_path = os.path.join(os.environ['USERPROFILE'], "Documents", "My Games", "Path of Exile", self.config['Config']['filter'])
        user_path = Path.home()  # Get the user home directory to look for the POE filters directory
        if os.path.isabs(self.config['Config']['filter']):  # if the path given is absolute, lets try it as is, else let stry to figure some more information about the location
            self.main_filter_path = self.config['Config']['filter']
            path_pre = os.path.split(self.main_filter_path)
        else:  # if not lets try the default PoE path
            # path_suf = os.path.relpath(os.path.join("My Games", "Path of Exile", self.config['Config']['filter']), start=user_path)  # handle if the user put in a full path or other extra information
            path_pre = os.path.join(user_path, "Documents", "My Games", "Path of Exile")  # handle if the user put in a full path or other extra information
            path_to_filter = os.path.join(path_pre, self.config['Config']['filter'])
            self.main_filter_path = path_to_filter
        if self.DEBUG:
            self.pp.pprint(f"Path Prefix: {path_pre}\n")
            self.pp.pprint(f"Searching for filter:\n {self.main_filter_path}\n")
        filter_exists = os.path.isfile(self.main_filter_path)
        def_filter_path = os.path.abspath(self.main_filter_path)
        if filter_exists:
            with open(def_filter_path, 'r') as fil:
                self.main_filter = fil.readlines()  # read default file into memory
            if self.DEBUG:
                self.pp.pprint(f"Found filter:")
                # self.pp.pprint(self.main_filter)
        else:
            # If it didn't exist, we will write it at the end of this method.
            # Use the included default for now.
            Msg.showinfo('POE QoL', f'POE QoL could not automatically find a filter at {self.main_filter_path}.\n\nPlease select the folder where your pathofexile fitlers are located to create a new filter named "POEQOL_Base.filter" based on the filter of the same name in this directory.')
            self.main_filter_path = os.path.normpath(os.path.join(filedialog.askdirectory(), 'POEQOL_Base.filter'))
            with open('POEQOL_Base.filter', 'r') as fil:
                if self.DEBUG:
                    self.pp.pprint(f"Could not find the filter as indicated in config file at: {def_filter_path}")
                    self.pp.pprint("User has selected {} to write the default filter:".format(self.main_filter_path))
                self.main_filter = fil.readlines()  # read default filter file into memory

        # There was way too much trouble with reading files from a setup file and with users not following directions, so I am going to try walking them through an initial setup.



        # we are now just going to update the setup file with what the user says to avoid errors in the future
        config_file_updates = {'filter':{'path': self.main_filter_path, 'lino': None, 'field':'filter='}}
        with open('Setup.ini', 'r', encoding='utf-8') as configfile_in:
            contents0 = configfile_in.readlines()
            for lino, l in enumerate(contents0):
                if l[0:7] == 'filter=':
                    config_file_updates['filter']['lino'] = lino 
                else:
                    continue
        with open('Setup.ini', 'w', encoding='utf-8') as configfile_out:
            contents0[config_file_updates['filter']['lino']] = config_file_updates['filter']['field'] + config_file_updates['filter']['path'] + "\n" # encode it at utf-8 for international players
            for l in contents0:
                configfile_out.write(l)


        self.chaos_items_sections_start_line = 0  # start a line counter to find the section in the filter where we should insert the dynamic text from the chaos_items_filter file (see read_default_chaos_filter_sections())
        self.chaos_items_sections_end_line = len(self.main_filter)
        for i, line in enumerate(self.main_filter):
            # I use a random string to find where the chaos recipe section begins and ends
            # break after the end of the section has been found
            if line[0] != "#": # If the line isn't a comment, we can just move on
                continue
            elif '234hn50987sd' in line:
                self.chaos_items_sections_start_line = i + 1
                if self.DEBUG:
                    self.pp.pprint(f"Start of chaos recipe section found at line {self.chaos_items_sections_start_line}")
                continue
            elif '2345ina8dsf7' in line:
                self.chaos_items_sections_end_line = i
                if self.DEBUG:
                    self.pp.pprint(f"End of chaos recipe section found at line {self.chaos_items_sections_end_line}")
                break
                #TODO: This else clause should be implemented, but doesn't work right now
                # else:
                #     # If we cannot find the section. alert the user... with some vague, unhelpful instructions and return False. Didn't raise an error here, idk if I should
                #     Msg.showinfo(title='POE QoL', message='Cannot find the chaos recipe section in your main filter.\n' + 
                #                                           'It should start with "# 234hn50987sd End Chaos Recipe Auto-Update Section" and end in "# 2345ina8dsf7 End Chaos Recipe Auto-Update Section".\n'+
                #                                           'Msg @notaspy#6561 for help. 14-09-2020 \n')
                #     return False
                if self.DEBUG:
                    self.pp.pprint("The entire filter file was looped through. This should not happen.")
        # take everything before and after the chaos recipe section from the original filter file. It shouldnt be changed ever. We will make changes between these two sections on each update.
        self.main_filter0 = self.main_filter[0:self.chaos_items_sections_start_line] + ['\n']
        self.main_filter1 = ['\n'] + self.main_filter[self.chaos_items_sections_end_line:] + ['\n']
        if not filter_exists:
            with open(self.main_filter_path, 'w') as fil:
                for line in self.main_filter:
                    fil.write(line)
        return self.main_filter

    def update_filter(self):
        """
        Attempt to update the main filter with showing/hiding recipe item slots that have reached the threshold.
        It is inefficient, since it loops through a very large filter blade file, and re-writes text that should not change. 
        I re-insert all the text from the chaos_items_filter just to be safe, but wouldn't need to if this is implemented in a better way.
        This will not hide any items set to be ignored in the Setup.ini file.
        """
        if self.DEBUG:
            self.pp.pprint("Trying to update Filter.")
        assert(self.main_filter)  # assert that a main filter was loaded
        assert(self.main_filter0)  # assert that a main filter prefix exists
        assert(self.main_filter1)  # assert that a main filter suffix exists
        if self.DEBUG:
            self.pp.pprint("Found necessary filter files.")        
        # go through the item slots and their meta-data (which has the threshold for items set by user)
        for slot, details in self.item_details.items():
            try:
                # if the slot is on the ignor list or if the number of items is not greater than the threshold, keep it in the filter
                if slot in self.config['Config']['ignore_threshold'] or len(self.latest_stash[0][slot]) < details[4]: 
                    self.chaos_items_filter_sections[slot][1] = "Show\n" # The show/hide flag is the second entry in the filter section text (see chaos_items_filter in Setup.ini)
                    if self.DEBUG:
                        self.pp.pprint(f"Found {len(self.latest_stash[0][slot])} items and ignore_threshold is set to {self.config['Config']['ignore_threshold']}. The filter will now show items of {slot} slot.")
                else:  # Otherwise hide that slot
                    self.chaos_items_filter_sections[slot][1] = "Hide\n"
                    if self.DEBUG:
                        self.pp.pprint(f"Found {len(self.latest_stash[0][slot])} items and ignore_threshold is set to {self.config['Config']['ignore_threshold']}. The filter will now show items of {slot} slot.")
            except (AttributeError, ValueError):  # Try to catch some errors. Not sure if this will work, don't have time to test the string formatting and message box
                # TODO: Test this error message
                Msg.showinfo(title='POE QoL', message=f'Check default filter formatting. There should be a valid entry for each item slot. The last word in each line should be one of the following: {[str(_[0]) for _ in self.item_details]}')
        # flatten the list of lists for the lines that should be added to the filter file
        new_filter_lines = [l for slt in self.chaos_items_filter_sections.values() for l in slt]
        if self.DEBUG:
            self.pp.pprint(f"Text to be inserted into the user's main filter file between lines {self.chaos_items_sections_start_line} and {self.chaos_items_sections_end_line}")
            self.pp.pprint(new_filter_lines)
        new_main_filter = self.main_filter0 + new_filter_lines + self.main_filter1
        if self.DEBUG:
            self.pp.pprint((len(self.main_filter0), len(self.main_filter1), len(new_filter_lines)))
        # TODO:enable the writing after testing
        with open(self.main_filter_path, 'w') as fil:
            for line in new_main_filter:
                fil.write(line)
        return True

    #Below are just methods that will search the stash tab for common things. didn't mess with these -notaspy 14-9-2020
    def search(self, text):
        pyperclip.copy(text)
        x, y = pyautogui.position()
        pyautogui.click(x= floor(self.tab_end[0] * 19/24), y=floor(self.tab_end[1] * 1183/1057))
        pyautogui.moveTo(x=x, y=y)
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.hotkey('ctrl', 'v')


    def currency(self):
        self.search('"currency"')

    def essence(self):
        self.search('"essence of"')

    def divcard(self):
        self.search('"divination"')

    def fragment(self):
        self.search('"can be used in a personal Map device"')

    def splinter(self):
        self.search('"splinter"')

    def delve(self):
        self.search('"fossil"')

    def incubator(self):
        self.search('"incubator"')

    def map(self):
        self.search('"map""tier"')

    def blight_map(self):
        self.search('"blighted" "tier"')

    def veiled(self):
        self.search('"veiled"')

    def rare(self):
        self.search('"rare"')

    def unique(self):
        self.search('"unique"')

    def prophecy(self):
        self.search('"prophecy"')

    def gem(self):
        self.search('"gem"')

    def unid(self):
        self.search('"unid"')

if __name__ == '__main__':
    # legacy. Run the applet.
    root = tk.Tk()
    root.title('Path of Exile - Quality of Life (POE-QOL)')
    app = MyApplication(root)
    app.run()

