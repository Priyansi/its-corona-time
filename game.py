import pygame
pygame.init()

# setting the width and height of the window
screenWidth = 750
screenHeight = 500
win = pygame.display.set_mode((750, 500))

# naming the game
pygame.display.set_caption("It's Corona Time")

# loading character left and right images, bullet and background images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load(
    'R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load(
    'L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
bulletImage = pygame.image.load('bullet.png')

hitSound = pygame.mixer.Sound('hit.wav')
gameoverSound = pygame.mixer.Sound('gameover.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0

# optimizing code


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.prev = 'right'
        self.hitbox = (self.x+15, self.y, 40, 60)

    def draw(self, win):
        if self.walkCount + 1 >= 27:  # 9 images and each image for 3 frames
            self.walkCount = 0

        if self.left:
            # drawing images by changing walkCount
            win.blit(walkLeft[(self.walkCount)//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[(self.walkCount)//3], (self.x, self.y))
            self.walkCount += 1
        else:
            if self.prev == 'right':
                # drawing standing still images
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x+15, self.y, 40, 60)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 30
        self.y = 405
        self.walkCount = 0
        text = font[2].render('-10', 1, (255, 0, 0))
        win.blit(text, (screenWidth//2-(text.get_width()//2), screenHeight//3))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.facing = facing
        self.vel = 8*facing

    def draw(self, win):
        win.blit(bulletImage, (self.x, self.y))


class enemy(object):
    walkRight = pygame.image.load('virusR.png')
    walkLeft = pygame.image.load('virusL.png')

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = 3
        self.hitbox = (self.x+2, self.y, 60, 60)
        self.health = 20
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.vel > 0:
                win.blit(self.walkRight, (self.x, self.y))
            else:
                win.blit(self.walkLeft, (self.x, self.y))

            pygame.draw.rect(
                win, (255, 0, 0), (self.hitbox[0]+5, self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(
                win, (0, 255, 0), (self.hitbox[0]+5, self.hitbox[1]-20, 50-((50/20)*(20-self.health)), 10))
            self.hitbox = (self.x+2, self.y, 60, 60)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel*-1

        else:
            if self.x-self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel*-1

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font[0].render('Score : '+str(score), 1, (0, 0, 0))
    text1 = font[1].render(
        'Shoot 20 Soaps To Kill The Coronavirus', 1, (0, 0, 0))
    win.blit(text, (600, 10))
    win.blit(text1, (10, 10))
    girl.draw(win)
    virus.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# main loop
girl = player(30, 405, 64, 64)
virus = enemy(100, 405, 64, 63, 600)
bullets = []
font = []
shootLoop = 0
font = [pygame.font.SysFont('comicsans', 35, True), pygame.font.SysFont(
    'comicsans', 35), pygame.font.SysFont('comicsans', 150), pygame.font.SysFont('comicsans', 150)]
run = True
level = 1
while run:
    clock.tick(27)

    if girl.hitbox[1] < virus.hitbox[1]+virus.hitbox[3] and girl.hitbox[1]+girl.hitbox[3] > virus.hitbox[1]:
        if girl.hitbox[0]+girl.hitbox[2] > virus.hitbox[0] and girl.hitbox[0] - girl.hitbox[2] < virus.hitbox[0] + virus.hitbox[2]:
            score -= 10

            if score < 0:
                pygame.mixer.music.set_volume(0)
                gameoverSound.play()
                text = font[3].render('You\'re Dead XD', 1, (255, 0, 0))
                win.blit(
                    text, (screenWidth//2-(text.get_width()//2), screenHeight//3))
                pygame.display.update()
                i = 0
                while i < 300:
                    pygame.time.delay(10)
                    i += 1
                break
            girl.hit()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y-bullet.width//2 < virus.hitbox[1]+virus.hitbox[3] and bullet.y+bullet.height/2 > virus.hitbox[1]:
            if bullet.x+bullet.width//2 > virus.hitbox[0] and bullet.x - bullet.width//2 < virus.hitbox[0] + virus.hitbox[2]:
                hitSound.play()
                virus.hit()
                if virus. visible:
                    score += 1
                else:
                    score += 1

                    if level < 5:
                        level += 1
                    else:
                        text = font[3].render('You Won :D', 1, (255, 0, 0))
                        win.blit(
                            text, (screenWidth//2-(text.get_width()//2), screenHeight//3))
                        pygame.display.update()
                        i = 0
                        while i < 300:
                            pygame.time.delay(10)
                            i += 1
                        break

                    virus = enemy(100, 405-level*20, 64, 63, 600)
                bullets.pop(bullets.index(bullet))
        if bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if girl.prev == 'right':
            facing = 1
        else:
            facing = -1

        if len(bullets) < 5:
            drawWidth = girl.width//2 if facing == 1 else 0
            bullets.append(projectile(
                round(girl.x+drawWidth), round(girl.y + girl.height//2), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and girl.x > girl.vel:
        girl.x -= girl.vel
        girl.left = True
        girl.right = False
        girl.prev = 'left'

    elif keys[pygame.K_RIGHT] and girl.x < screenWidth - girl.width-girl.vel:
        girl.x += girl.vel
        girl.right = True
        girl.left = False
        girl.prev = 'right'

    else:
        girl.right = False
        girl.left = False
        girl.walkcount = 0

    if not girl.isJump:
        if keys[pygame.K_UP]:
            girl.isJump = True
            girl.left = False
            girl.right = False
            girl.walkCount = 0

    else:
        if girl.jumpCount >= -10:
            neg = 1
            if girl.jumpCount < 0:
                neg = -1
            girl.y -= ((girl.jumpCount**2)//2)*neg
            girl.jumpCount -= 1

        else:
            girl.isJump = False
            girl.jumpCount = 10

    redrawGameWindow()

pygame.quit()
