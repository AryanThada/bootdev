import pygame
import random
from constants import *
from logger import log_event

from circleshape import CircleShape

class Asteroid(CircleShape):

    def __init__(self  , x: float, y: float , radius: float)->None:

        super().__init__(x , y, radius)

    def draw(self, screen: pygame.Surface ) -> None:

        pygame.draw.circle(screen , "white" , self.position , self.radius , LINE_WIDTH)

    def update(self, dt: float) -> None:

        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if(self.radius <= ASTEROID_MIN_RADIUS):
            return

        else :
            log_event("asteroid_split")

            random_theta = random.uniform(20 , 50)
            velocity_1 = self.velocity.rotate(random_theta)
            velocity_2 = self.velocity.rotate(random_theta * (-1))

            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_object_1 : Asteroid = Asteroid(self.position[0] , self.position[1] ,new_radius)
            asteroid_object_2 : Asteroid = Asteroid(self.position[0] , self.position[1] ,new_radius)

            asteroid_object_1.velocity = velocity_1 * 1.2
            asteroid_object_2.velocity = velocity_2 * 1.2
            




