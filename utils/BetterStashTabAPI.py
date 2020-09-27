import requests
import json
import re

# URL Format to access a specific stash tab information
STASH_TAB_URL = "https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}"


class stash_tab_item(dict):
    """
    Created by: 0xdavidel
    This class is simply a wrapper for the raw json dictionary of an item
    Mainly for allowing a easier representation and the flexability of adding features in the future

    General item json format
    {"verified":false,
    "w":1,
    "h":3,
    "icon":"URL",
    "league":"Heist",
    "id":"11642c...",
    "sockets":
        [
            {"group":0,"attr":"I","sColour":"B"},
            ...],
    "name":"",
    "typeLine":"Boot Blade",
    "identified":false,
    "ilvl":66,
    "properties":[
        {"name":"Rune Dagger","values":[],"displayMode":0},
        {"name":"Physical Damage","values":[
            ["15-59",0]],"displayMode":0,"type":9},
        {"name":"Critical Strike Chance","values":[
            ["6.30%",0]],"displayMode":0,"type":12},
        {"name":"Attacks per Second","values":[
            ["1.40",0]],"displayMode":0,"type":13},
        {"name":"Weapon Range","values":[["10",0]],"displayMode":0,"type":14}],
    "requirements":[
        {"name":"Dex","values":[["63",0]],"displayMode":1},
        {"name":"Int","values":[["90",0]],"displayMode":1}],
    "implicitMods":["30% increased Global Critical Strike Chance"],
    "frameType":2,
    "x":0,
    "y":12,
    "inventoryId":"Stash2",
    "socketedItems":[]}
    """

    @staticmethod
    def parse_icon_url_into_tags(url):
        """
        Created by: 0xdavidel
        This function is used to extract "tags" of an item, I was not able to see a easy way to extract what item was what so I had to resort to wierd tricks

        This time its by parsing the path the icon of the item is stored in:

        General format of the icon URL
        "https://web.poecdn.com/image/Art/2DItems/Weapons/OneHandWeapons/OneHandSwords/OneHandSword2.png?v=a94ce74a6007ca561bb3a4bfa3abe15b&w=1&h=3&scale=1"
        Or it could be a lot shorter in case of Rings, Belts, Currency and Other items with less types and tags:
        "https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyUpgradeToMagic.png?v=333b8b5e28b73c62972fc66e7634c5c8&w=1&h=1&scale=1"

        Both cases the "tags" of the item are stored as directories in the URL path and thats what I am extracting
        """
        tmp = url.replace(
            r"https://web.poecdn.com/image/Art/2DItems/", "")
        tmp = tmp.split("/")
        tmp = tmp[:-1]
        # Lower for ease of use
        return [i.lower() for i in tmp]

    def __init__(self, json):
        self.json = json
        self.tags = stash_tab_item.parse_icon_url_into_tags(self.json["icon"])
        self.is_unique = json["frameType"] == 3
        self.is_identified = self.json["identified"]

    def __getitem__(self, key):
        return self.json[key]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{} : {} | {} | ilvl {} | ({},{})".format(self.json["typeLine"], self.json["name"], "identified" if self.is_identified else "NOT identified", self.json["ilvl"], self.json["x"], self.json["y"])


class stash_tab:
    """
    Created by: 0xdavidel
    This class hold all the basic information of a stash tab.
    Information like :
        * is it a quad tab
        * list of items it holds
        * the amount of items in the stash tab
    And it adds an aditional layer of being able to filter and search with ease by the using retrieve_all_by_tag function
    """

    def __init__(self, tab_data, index=None):
        self.tab_items = []
        self.isQuadTab = False
        self.index = None
        self.tab_data = tab_data
        self.isQuadTab = self.tab_data["quadLayout"] if "quadLayout" in self.tab_data else False
        self.index = index

        for item_data in self.tab_data["items"]:
            self.tab_items.append(stash_tab_item(item_data))

    def remove_item(self, target):
        """
        Created by: 0xdavidel

        Delete a single item from the tab_items list
        This has to be done in this manner because stash_tab_item is not a hashable object
        Meaning you cannot use .remove or 'in' operations to find and delete it
        """
        for i, item in enumerate(self.tab_items):
            if item.json == target.json:
                self.tab_items.pop(i)
                return

    def retrieve_all_by_tag(self, tag, unique_only=False, identified_only=False):
        """
        Created by: 0xdavidel

        Return all items that contain a single tag
        """
        myList = []
        tag = tag.lower()
        for item in self.tab_items:
            if unique_only:
                if item.is_unique:
                    continue
            if identified_only:
                if not item.is_identified:
                    continue
            # The +"s" is because all the tags look like "rings", and its for ease of use if you forget to add "s" in the filter
            if tag in item.tags or tag+"s" in item.tags:
                myList.append(item)
        return myList

    def count(self):
        return len(self.tab_items)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        items = []
        for item in self.tab_items:
            items.append(str(item))

        return "TAB INDEX: {} | isQuad: {} | items : {}".format(self.index, self.isQuadTab, json.dumps(items))


def get_stash_tab_content(accountName, league, tabIndex, POESESSID=None, DEBUG=False):
    """
    Created by: 0xdavidel

    Retrieve a stash_tab object representing a single stash tab
    """
    # Create the request URL
    formatted_stash_tab_url = STASH_TAB_URL.format(
        league, tabIndex, accountName)
    # COOKIEEESSSS YUMMY
    cookies_dict = {"POESESSID": POESESSID}
    # Do the request
    try:
        stash_tab_content_request = requests.get(
            formatted_stash_tab_url, cookies=cookies_dict)
    except:
        # Yes I am aware that capturing ALL exceptions is not the best practice
        raise Exception("Unable to connect to pathofexile.com")

    try:
        # Jsonify the whole ting
        text_json = stash_tab_content_request.text
        tab_content_json = json.loads(text_json)
    except:
        raise Exception(
            "Unable to parse result (is path of exile down for maintenance?)")

    # Error handeling
    if "error" in tab_content_json:
        msg = tab_content_json["error"]["message"]
        code = tab_content_json["error"]["code"]
        # Handle POESESSID error
        if msg == "Forbidden":
            raise Exception(
                "Error retrieving stash tab content\nPlease check that your entered the correct POESESSID")

        # Handle Account name error
        if msg == 'Resource not found':
            raise Exception(
                "Error retrieving stash tab content\nPlease check that your entered the correct Account name")

        # Handle League name error
        if msg == 'Invalid query' and code == 2:
            raise Exception(
                "Error retrieving stash tab content\nPlease check that your entered the correct League name")

        # Handle Tab index error
        if msg == 'Invalid query' and code == 1:
            raise Exception(
                "Error retrieving stash tab content\nPlease check that your entered the correct tab index")
        # Well damm, didnt see this error yet
        raise Exception(
            "Error retrieving stash tab content\nNever saw this exception:\n{}".format(tab_content_json))
    
    # New stash tab object
    my_stash_tab = stash_tab(tab_content_json, tabIndex)

    return my_stash_tab