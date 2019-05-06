import pygame

from astar import AStar

class Sprite:
    """
    tool for drawing character
    """

    @staticmethod
    def draw(dest, source, x, y, cell_x, cell_y, cell_w=32, cell_h=32):
        """
        :param dest: surface type，objective surface that needed to be painted
        :param source: surface type，from surface
        :param x: drawing picture coordinate in dest
        :param y: drawing picture coordinate in dest
        :param cell_x: unit coordinate inside character picture
        :param cell_y: unit coordinate inside character picture
        :param cell_w: width of single character
        :param cell_h: height of sigle character
        :return:
        """
        dest.blit(source, (x, y), (cell_x * cell_w, cell_y * cell_h, cell_w, cell_h))


class Array2D:
    """
            1.two variables are needed to create the method，width and height of 2D array
            2.variable w and h are width and height of 2D array
            3.use 'object[x][y]’to get the values
            4.default setting in array are 0
    """

    def __init__(self, w, h, default=0):
        self.w = w
        self.h = h
        self.data = []
        self.data = [[default for y in range(h)] for x in range(w)]

    def show_array2d(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.data[x][y], end=' ')
            print("")

    def __getitem__(self, item):
        return self.data[item]


class GameMap(Array2D):
    """
    Game map
    """

    def __init__(self, bottom, top, x, y):
        # divided map into w*h units，32*32 pixel each unit
        w = int(bottom.get_width() / 32) + 1
        h = int(top.get_height() / 32) + 1
        super().__init__(w, h)
        self.bottom = bottom
        self.top = top
        self.x = x
        self.y = y

    def draw_bottom(self, screen_surf):
        screen_surf.blit(self.bottom, (self.x, self.y))

    def draw_top(self, screen_surf):
        screen_surf.blit(self.top, (self.x, self.y))

    def draw_grid(self, screen_surf):
        """
        draw grid
        """
        for x in range(self.w):
            for y in range(self.h):
                if self[x][y] == 0:  # non obstruct，draw empty square
                    pygame.draw.rect(screen_surf, (255, 255, 255), (self.x + x * 32, self.y + y * 32, 32, 32), 1)
                else:  # obstruct，draw black solid square
                    pygame.draw.rect(screen_surf, (0, 0, 0), (self.x + x * 32 + 1, self.y + y * 32 + 1, 30, 30), 0)

    def roll(self, role_x, role_y, WIN_WIDTH=640, WIN_HEIGHT=480):
        """
        map rolling
        :param role_x: character's coordinate relative to map
        :param role_y:
        """
        # print(role_x, role_y)
        if role_x < WIN_WIDTH / 2:
            self.x = 0
        elif role_x > self.bottom.get_width() - WIN_WIDTH / 2:
            self.x = -(self.bottom.get_width() - WIN_WIDTH)
        else:
            self.x = -(role_x - WIN_WIDTH / 2)

        if role_y < WIN_HEIGHT / 2:
            self.y = 0
        elif role_y > self.bottom.get_height() - WIN_HEIGHT / 2:
            self.y = -(self.bottom.get_height() - WIN_HEIGHT)
        else:
            self.y = -(role_y - WIN_HEIGHT / 2)

    def load_walk_file(self, path):
        """
        load walkable area file
        """
        with open(path, 'r') as file:
            for x in range(self.w):
                for y in range(self.h):
                    v = int(file.readline())
                    self[x][y] = v
        # self.show_array2d()


class CharWalk:
    """
    character walking class, char is the short of character
    """
    DIR_DOWN = 0
    DIR_LEFT = 1
    DIR_RIGHT = 2
    DIR_UP = 3

    def __init__(self, hero_surf, char_id, dir, mx, my):
        """
        :param hero_surf: character surface
        :param char_id: character id
        :param dir: character  direction
        :param mx: unit coordinate where character is
        :param my: unit coordinate where character is
        """
        self.hero_surf = hero_surf
        self.char_id = char_id
        self.dir = dir
        self.mx = mx
        self.my = my

        self.is_walking = False  # if character is moving
        self.frame = 1  # whare character frame is
        self.x = mx * 32  # character position
        self.y = my * 32
        # where character is going to
        self.next_mx = 0
        self.next_my = 0
        # step length
        self.step = 2  # pixel length for each move
        #finding path
        self.path = []
        #current path
        self.path_index = 0

    def draw(self, screen_surf, map_x, map_y):
        cell_x = self.char_id % 12 + int(self.frame)
        cell_y = self.char_id // 12 + self.dir
        Sprite.draw(screen_surf, self.hero_surf, map_x + self.x, map_y + self.y, cell_x, cell_y)

    def goto(self, x, y):
        """
        :param x: goto point
        :param y: goto point
        """
        self.next_mx = x
        self.next_my = y

        # set character facing direction
        if self.next_mx > self.mx:
            self.dir = CharWalk.DIR_RIGHT
        elif self.next_mx < self.mx:
            self.dir = CharWalk.DIR_LEFT

        if self.next_my > self.my:
            self.dir = CharWalk.DIR_DOWN
        elif self.next_my < self.my:
            self.dir = CharWalk.DIR_UP

        self.is_walking = True

    def move(self):
        if not self.is_walking:
            return
        dest_x = self.next_mx * 32
        dest_y = self.next_my * 32

        # get close to destination
        if self.x < dest_x:
            self.x += self.step
            if self.x >= dest_x:
                self.x = dest_x
        elif self.x > dest_x:
            self.x -= self.step
            if self.x <= dest_x:
                self.x = dest_x

        if self.y < dest_y:
            self.y += self.step
            if self.y >= dest_y:
                self.y = dest_y
        elif self.y > dest_y:
            self.y -= self.step
            if self.y <= dest_y:
                self.y = dest_y

        # update current frame
        self.frame = (self.frame + 0.1) % 3

        # character current position
        self.mx = int(self.x / 32)
        self.my = int(self.y / 32)

        # arrive destination
        if self.x == dest_x and self.y == dest_y:
            self.frame = 1
            self.is_walking = False

    def logic(self):
            self.move()

            # if moving then ignore
            if self.is_walking:
                return

            # if ended
            if self.path_index == len(self.path):
                self.path = []
                self.path_index = 0
            else:  # if not the destination then moveon
                self.goto(self.path[self.path_index].x, self.path[self.path_index].y)
                self.path_index += 1

    def find_path(self, map2d, end_point):
            """
            :param map2d: map
            :param end_point: find path end point
            """
            start_point = (self.mx, self.my)
            path = AStar(map2d, start_point, end_point).start()
            if path is None:
                return

            self.path = path
            self.path_index = 0