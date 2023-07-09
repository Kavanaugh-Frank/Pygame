# Import the pygame module
import pygame , sys , random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


#FPS
clock = pygame.time.Clock() 
FPS = 120

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                # random.randint(100, 300),
                SCREEN_WIDTH / 2,
                0,
            )
        )
        self.dy = 10
        self.moving = True
        # self.dy = random.randint(10 , 25)
        #automatically puts the Player Object into the group of sprites
        pygame.sprite.Sprite.__init__(self, square)
    def update(self):
        if self.moving: #makes sure that if the square is stopped it is stopped
            if SCREEN_HEIGHT - self.rect.bottom < self.dy: #makes sure to stay in the screen
                self.rect.move_ip(0 , (SCREEN_HEIGHT - self.rect.bottom))
                self.stop()
            elif pygame.sprite.spritecollideany(self, stopped): #checks to see if it can go left
                # if both are available make it random
                if screen.get_at((self.rect.centerx - 10, self.rect.centery + 10)) == (0, 0, 0, 255) and screen.get_at((self.rect.centerx + 10, self.rect.centery + 10)) == (0, 0, 0, 255):
                    if random.randint(0 , 100 ) % 2 == 0:
                        self.rect.move_ip(-15, 0)
                    else:
                        self.rect.move_ip(15, 0)
                #go left it that is the only option
                elif screen.get_at((self.rect.centerx - 10, self.rect.centery + 10)) == (0, 0, 0, 255):
                    self.rect.move_ip(-15, 0)
                #go right if that is the only option
                elif screen.get_at((self.rect.centerx + 10, self.rect.centery + 10)) == (0, 0, 0, 255):
                    self.rect.move_ip(15, 0)
                #the square can not move anywhere
                else:
                    self.stop()
            else: #moves the square normalls
                self.rect.move_ip(0, self.dy)
    def stop(self):
        self.moving = False
        self.dy = 0
        square.remove(self)
        stopped.add(self)


#group of the sprites on the board
square = pygame.sprite.Group()
stopped = pygame.sprite.Group()

# Instantiate player. Right now, this is just a rectangle.
# player1 = Player()
# player2 = Player()
# player3 = Player()

# Variable to keep the main loop running
running = True

# Main loop
count = 0
nums = 0
totalNumOfSquares = 200
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    #prints all the squares on the board
    for entity in square:
        screen.blit(entity.surf, entity.rect)
    for entity in stopped:
        screen.blit(entity.surf, entity.rect)

    square.update()

    # square.add(Player())
    # Update the display
    pygame.display.flip()

    if count == FPS * 5 and nums != totalNumOfSquares:
        square.add(Player())
        count = 0
        nums += 1
    count += FPS


    clock.tick(FPS) 