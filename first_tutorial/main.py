import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>= 300:
            self.jump_sound.play()
            self.gravity = -30

    def apply_gravity(self):
        self.gravity += 2
        self.rect.y +=self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
        else:
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animate(self):
        self.index += 0.1
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.animate()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite, obs_group, False):
        obs_group.empty()
        return False
    else: 
        return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Hopper')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
ground_surf = pygame.image.load('graphics/ground.png').convert()
sky_surf = pygame.image.load('graphics/Sky.png').convert()
game_active = False
start_time = 0
score = 0
music = pygame.mixer.Sound('audio/music.wav')
music.set_volume(0.3)
music.play(loops = -1)

# Groups
obs_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player.add(Player())

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Hopper',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obs_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:   
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        obs_group.draw(screen)
        obs_group.update()
        
        game_active = collisions()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)

        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)
