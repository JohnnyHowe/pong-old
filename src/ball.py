import math
from window import Window


class Ball:
    def __init__(self, initial_position):
        self.position = initial_position 
        self.radius = 0.02
        self.speed = 0.005
        self.direction = 90  # angle from up (clockwise)
        self.max_paddle_angle = 20
        self.max_angle_from_horizontal = 45

    def update(self):
        self.move()
        self.bounce_off_walls()
        self.cap_angle()

    def cap_angle(self):
        if 0 <= self.direction <= 90 - self.max_angle_from_horizontal:
            # top right
            self.direction = 90 - self.max_angle_from_horizontal
        elif 90 + self.max_angle_from_horizontal <= self.direction <= 180:
            # bottom right
            self.direction = 90 + self.max_angle_from_horizontal
        elif 180 <= self.direction <= 270 - self.max_angle_from_horizontal:
            # bottom left
            self.direction = 270 - self.max_angle_from_horizontal
        elif 270 + self.max_angle_from_horizontal <= self.direction <= 360:
            # top left
            self.direction = 270 + self.max_angle_from_horizontal

    def show(self):
        Window.draw_circle(self.position, self.radius, (255, 255, 255))

    def move(self):
        self.position[0] += math.sin(math.radians(self.direction)) * self.speed
        self.position[1] -= math.cos(math.radians(self.direction)) * self.speed

    def bounce_off_walls(self):
        """ Handle the bouncing off the window borders """
        if (self.position[1] + self.radius > 1):
            self.position[1] = 1 - self.radius
            self.bounce(0)
        elif (self.position[1] - self.radius < 0):
            self.position[1] = self.radius
            self.bounce(180)

    def bounce_off_player(self, rect):
        if self.is_touching(rect):
            self.player_collision(rect)

    def is_in_bounds(self):
        return 0 < self.position[0] < 1

    def player_collision(self, rect):
        """ Get the collision normal angle. """
        # Collision res
        near_x = max(rect[0] - rect[2] / 2, min(self.position[0], rect[0] + rect[2] / 2))
        near_y = max(rect[1] - rect[3] / 2, min(self.position[1], rect[1] + rect[3] / 2))
        dist_vec = (self.position[0] - near_x, self.position[1] - near_y)
        dist = math.sqrt(dist_vec[0] ** 2 + dist_vec[1] ** 2)
        depth = self.radius - dist
        dist_vec_normalised = normalise(dist_vec)
        pen_vec = [dist_vec_normalised[0] * depth, dist_vec_normalised[1] * depth]
        self.position[0] += pen_vec[0]
        self.position[1] += pen_vec[1]

        # Bounce
        angle_offset = (2 * (rect[1] - self.position[1]) / rect[3]) * self.max_paddle_angle * math.copysign(1, self.position[0] - rect[0])
        dot = dist_vec_normalised[1]
        angle = math.degrees(math.acos(dot)) + 180
        self.bounce(angle - angle_offset)

    def is_touching(self, rect):
        """ Is the ball touching rect? """
        return (self.position[0] + self.radius >= rect[0] - rect[2] / 2 and
                self.position[0] - self.radius <= rect[0] + rect[2] / 2 and
                self.position[1] + self.radius >= rect[1] - rect[3] / 2 and
                self.position[1] - self.radius <= rect[1] + rect[3] / 2)

    def bounce(self, normal_angle):
        da = mod(normal_angle, 180) - mod(self.direction, 180)
        self.direction = mod((self.direction - 180) + 2 * da, 360)

def normalise(vec):
    d = math.sqrt(vec[0] ** 2+ vec[1] ** 2)
    if (d == 0):
        return vec
    else:
        return [vec[0] / d, vec[1] / d]

# mod = (a, n) -> a - floor(a/n) * n
def mod(a, n):
    return a - math.floor(a / n) * n
