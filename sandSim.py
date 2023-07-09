import pygame , random
#Keyboard Controls
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#CAPTION of the window
pygame.display.set_caption('Sand Fall')

#FPS
clock = pygame.time.Clock() 
FPS = 60

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#group of the sprites on the board
sand = pygame.sprite.Group()
stopped = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
goals = pygame.sprite.Group()

#Sand Dimensions
SAND_HEIGHT = 10
SAND_WIDTH = 10
search_offset = 7

#Starting Spawn
spawn_width =  SCREEN_WIDTH / 2
spawn_height = SAND_HEIGHT / 2

#BOOL for game loop
game_is_running = True
spawn_sand = False
sandSpawnFreeze = False


#the variables for the Text when the goal is hit
font = pygame.font.SysFont("Arial", 36)
txtsurf = font.render("Hello, World", True, (255 , 0 , 255))
showText = False

#sand square class
class Sand(pygame.sprite.Sprite):
    def __init__(self , x , y) -> None:
        super(Sand , self).__init__()
        #SIZE AND COLOR
        self.surf = pygame.Surface((SAND_WIDTH, SAND_HEIGHT)) # size
        self.surf.fill((255, 255, 255)) #color
        self.rect = self.surf.get_rect( #starting location
            center=( #centered at this X,Y coordinate
                # random.randint(100, 300),
                # SCREEN_WIDTH / 2,
                # SAND_HEIGHT / 2,
                x,y
            )
        )

        #SPEED
        self.dy = 5
        self.dx = 0

        #automatically puts the Player Object into the group of sprites
        pygame.sprite.Sprite.__init__(self, sand)
    def update(self):
        if SCREEN_HEIGHT - self.rect.bottom < self.dy: #makes sure to stay in the screen
            self.rect.move_ip(0 , (SCREEN_HEIGHT - self.rect.bottom))
            self.dy = 0
            self.square_stop()
        elif pygame.sprite.spritecollideany(self, stopped): #and self.test:
            if self.rect.centerx - 13 < 0:
                self.square_stop()
            elif self.rect.centerx + 13 > SCREEN_WIDTH:
                self.square_stop()
            elif screen.get_at((self.rect.centerx - search_offset, self.rect.centery + search_offset)) == (0, 0, 0, 255) and screen.get_at((self.rect.centerx + search_offset, self.rect.centery + search_offset)) == (0, 0, 0, 255):
                if random.randint(0 , 1000) % 2 == 0:
                    self.dx = -SAND_WIDTH
                    self.rect.move_ip(self.dx , self.dy)
                else:
                    self.dx = SAND_WIDTH
                    self.rect.move_ip(self.dx , self.dy)
            elif screen.get_at((self.rect.centerx - search_offset, self.rect.centery + search_offset)) == (0, 0, 0, 255):
                self.dx = -SAND_WIDTH
                self.rect.move_ip(self.dx , self.dy)
            elif screen.get_at((self.rect.centerx + search_offset, self.rect.centery + search_offset)) == (0, 0, 0, 255):
                self.dx = SAND_WIDTH
                self.rect.move_ip(self.dx , self.dy)
            else:
                self.dy = 0
                self.square_stop()
                #Since the collision detection is to the center of a Rect we have to correct for that
                self.rect.move_ip(0 , -(SAND_HEIGHT / 2))
        elif pygame.sprite.spritecollideany(self, obstacles):
            self.square_stop()
            self.rect.move_ip(0 , -(SAND_HEIGHT / 2))
        else:
            self.rect.move_ip(0 , self.dy)
            self.test = True

    def square_stop(self):
        sand.remove(self)
        stopped.add(self)

    def freeze(self):
        self.rect.move_ip(0 , -(SAND_HEIGHT / 2))
        self.dy = 0
        self.dx = 0

class Cursor(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Cursor , self).__init__()
        #SIZE AND COLOR
        self.surf = pygame.Surface((SAND_WIDTH, SAND_HEIGHT)) # size
        self.surf.fill((255, 0, 0)) #color
        self.rect = self.surf.get_rect( #starting location
            center=( spawn_width, spawn_height )
        )

class Wood(pygame.sprite.Sprite):
    def __init__(self , height , width , x , y):
        super(Wood , self).__init__()
        #SIZE AND COLOR
        #the var width must be odds only because of the pyramid aspect
        self.surf = pygame.Surface((SAND_WIDTH * width , SAND_HEIGHT * height)) # size
        self.surf.fill((0, 255, 0)) #color
        self.rect = self.surf.get_rect( #starting location
            center=( x , y)
        )

        #automatically puts the Player Object into the group of sprites
        pygame.sprite.Sprite.__init__(self, obstacles)

class Goal(pygame.sprite.Sprite):
    def __init__(self , height , width , x , y):
        super(Goal , self).__init__()
        #SIZE AND COLOR
        #the var width must be odds only because of the pyramid aspect
        self.surf = pygame.Surface((SAND_WIDTH * width , SAND_HEIGHT * height)) # size
        self.surf.fill((0, 0, 255)) #color
        self.rect = self.surf.get_rect( #starting location
            center=( x , y )
        )

        #automatically puts the Player Object into the group of sprites
        pygame.sprite.Sprite.__init__(self, goals)
    def update(self):
        if pygame.sprite.spritecollideany(self, sand):
            for item in sand:
                item.freeze()

            global showText , sandSpawnFreeze
            showText = True
            sandSpawnFreeze = True
            




#spawns a new cube at this increment
count = 0

#the unmovable obstacles
    #height , width , x , y
Goal(1 , 1 , SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)

Wood(1 , 11 , SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2)
Wood(4 , 1 , (SCREEN_WIDTH / 2) - 50 ,(SCREEN_HEIGHT / 2) - 20)
Wood(4 , 1 , (SCREEN_WIDTH / 2) + 50 ,(SCREEN_HEIGHT / 2) - 20)
Wood(1 , 40 , (SCREEN_WIDTH / 2) ,(SCREEN_HEIGHT / 2) + 100)



#the game loop
while game_is_running:
    #Keyboard Checks
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                    game_is_running = False
            #moves the spawn of the sand 
            elif event.key == K_RIGHT:
                spawn_width += SAND_WIDTH
            elif event.key == K_LEFT:
                spawn_width -= SAND_WIDTH
            #stops or starts the spawning or sand
            elif event.key == K_UP and not sandSpawnFreeze:
                if spawn_sand:
                    spawn_sand = False
                else:
                    spawn_sand = True
            #clears the sand
            elif event.key == K_DOWN:
                sand.empty()
                stopped.empty()

                #Reesets all the bools
                showText = False
                spawn_sand = False
                sandSpawnFreeze = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            game_is_running = False


    # Fill the screen with black
    screen.fill((0, 0, 0))

    
    #Spawning the Sand/Cursor
    if spawn_sand:
        if count == FPS:
            Sand(spawn_width , spawn_height)
            count = 0
        else:
            count += FPS / 2
    else:
        cursor = Cursor()
        screen.blit(cursor.surf, cursor.rect)


    #prints all the sand on the board
    for entity in sand:
        screen.blit(entity.surf, entity.rect)

    for entity in stopped:
        screen.blit(entity.surf, entity.rect)

    for entity in obstacles:
        screen.blit(entity.surf, entity.rect) 
    
    for entity in goals:
        screen.blit(entity.surf, entity.rect) 

    #Updates the positions of the sand
    sand.update()
    #Checks for collision between Sand and the Goal
    goals.update()

    

    #If the goal is hit, then show the text saying so
    if showText:
        screen.blit(txtsurf , (SCREEN_WIDTH / 2 - (txtsurf.get_rect().width / 2) , 150 ))

    # Update the display
    pygame.display.flip()

    clock.tick(FPS) 
