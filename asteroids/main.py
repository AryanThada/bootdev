import pygame
import sys
from constants	import	SCREEN_WIDTH,SCREEN_HEIGHT
from logger	import	log_state , log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot



def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    pygame.init()
    screen= pygame.display.set_mode((SCREEN_WIDTH,	SCREEN_HEIGHT))

    print(f"Screen width: {SCREEN_WIDTH}\n")
    print(f"Screen height: {SCREEN_HEIGHT}\n")

    clock_object = pygame.time.Clock()

    dt = 0.0 # delta time 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots  = pygame.sprite.Group()
    
    Player.containers = (updatable , drawable)
    Asteroid.containers = (asteroids , updatable , drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots , updatable , drawable)

    player_object : Player = Player(SCREEN_WIDTH/2 , SCREEN_HEIGHT/2)
    asteroid_field_object :AsteroidField = AsteroidField()

    
    while(True):
        log_state()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            
            pass

        screen.fill("black")

        updatable.update(dt)
        # player_object.update(dt)

        for objects in asteroids:
            if(player_object.collide_with(objects)):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        for objects in asteroids:
            for bullet in shots:
                if (objects.collide_with(bullet)):
                    log_event("asteroid_shot")
                    bullet.kill()
                    objects.split()

        
        for thing in drawable:
            thing.draw(screen)

        # player_object.draw(screen)

        pygame.display.flip()

        dt = clock_object.tick(60)/1000

        # print(f"delta time: {dt}")


if __name__ == "__main__":
    main()
