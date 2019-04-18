

class example(example1):

    def __init__(self, info_box):
        super(example, self).__init__()
        self.rect = self.image.get_rect()
        self.state = 'selectmenu'
        self.state_dict = self.make_state_dict()
        self.slots = info_box.slots
        self.pos_list = []

    def make_state_dict(self):
        """
        Make state dictionary.
        """
        state_dict = {'selectmenu': self.navigate_select_menu,
                      'itemsubmenu': self.navigate_item_submenu,
                      'magicsubmenu': self.navigate_magic_submenu}

        return state_dict

    def navigate_select_menu(self, pos_index):
        """
        Nav the select menu.
        """
        self.pos_list = self.make_select_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]

    def navigate_item_submenu(self, pos_index):
        """Nav the item submenu"""
        self.pos_list = self.make_item_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]

    def navigate_magic_submenu(self, pos_index):
        """
        Nav the magic submenu.
        """
        self.pos_list = self.make_magic_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]

    def make_magic_menu_pos_list(self):
        """
        Make the list of possible arrow positions for magic submenu.
        """
        pos_list = [(310, 119),
                    (310, 169)]

        return pos_list

    def make_select_menu_pos_list(self):
        """
        Make the list of possible arrow positions.
        """
        pos_list = []

        for i in range(3):
            pos = (35, 443 + (i * 45))
            pos_list.append(pos)

        return pos_list

    def make_item_menu_pos_list(self):
        """
        Make the list of arrow positions in the item submenu.
        """
        pos_list = [(300, 173),
                    (300, 223),
                    (300, 323),
                    (300, 373),
                    (300, 478),
                    (300, 528),
                    (535, 478),
                    (535, 528)]

        return pos_list

    def update(self, pos_index):
        """
        Update arrow position.
        """
        state_function = self.state_dict[self.state]
        state_function(pos_index)

    def draw(self, surface):
        """
        Draw to surface"""
        surface.blit(self.image, self.rect)

    def make_image(self):
        """
        Make the surface for the gold box.
        """
        stat_list = ['GOLD', 'health', 'magic']
        magic_health_list = ['health', 'magic']


    def update(self):
        """
        Update gold.
        """
        self.image, self.rect = self.make_image()

    def draw(self, surface):
        """
        Draw to surface.
        """
        surface.blit(self.image, self.rect)

    def get_attack_power(self):
        """
        Calculate the current attack power based on equipped weapons.
        """
        weapon = self.inventory['equipped weapon']
        return self.inventory[weapon]['power']

    def get_defense_power(self):
        """
        Calculate the current defense power based on equipped weapons.
        """
        defense_power = 0
        for armor in self.inventory['equipped armor']:
            defense_power += self.inventory[armor]['power']

        return defense_power

    def make_state_dict(self):
        """Make the dictionary of state methods"""
        state_dict = {'stats': self.show_player_stats,
                      'items': self.show_items,
                      'magic': self.show_magic,
                      'invisible': self.show_nothing}

        return state_dict

    def assign_slots(self, item_list, starty, weapon_or_armor=False):
        """Assign each item to a slot in the menu"""
        if len(item_list) > 3:
            for i, item in enumerate(item_list[:3]):
                posx = 80
                posy = starty + (i * 50)
                self.slots[(posx, posy)] = item
            for i, item in enumerate(item_list[3:]):
                posx = 315
                posy = (starty + 50) + (i * 5)
                self.slots[(posx, posy)] = item
        else:
            for i, item in enumerate(item_list):
                posx = 80
                posy = starty + (i * 50)
                self.slots[(posx, posy)] = item

    def assign_magic_slots(self, magic_list, starty):
        """
        Assign each magic spell to a slot in the menu.
        """
        for i, spell in enumerate(magic_list):
            posx = 120
            posy = starty + (i * 50)
            self.slots[(posx, posy)] = spell

    def blit_item_lists(self, surface):
        """Blit item list to info box surface"""
        for coord in self.slots:
            item = self.slots[coord]

            if item in self.possible_potions:
                text = "{}: {}".format(self.slots[coord],
                                       self.inventory[item]['quantity'])
            else:
                text = "{}".format(self.slots[coord])
            text_image = self.font.render(text, True, c.NEAR_BLACK)
            text_rect = text_image.get_rect(topleft=coord)
            surface.blit(text_image, text_rect)

    def show_nothing(self):
        """
        Show nothing when the menu is opened from a level.
        """
        self.image = pg.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.image.fill(c.BLACK_BLUE)

    def update(self):
        state_function = self.state_dict[self.state]
        state_function()

    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)


class SelectionBox(pg.sprite.Sprite):
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.image, self.rect = self.make_image()

    def make_image(self):
        choices = ['Items', 'Magic', 'Stats']
        image = setup.GFX['goldbox']
        rect = image.get_rect(left=10, top=425)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for i, choice in enumerate(choices):
            choice_image = self.font.render(choice, True, c.NEAR_BLACK)
            choice_rect = choice_image.get_rect(x=100, y=(15 + (i * 45)))
            surface.blit(choice_image, choice_rect)

        return surface, rect

    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)

    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)
