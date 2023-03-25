# Magic 8 Ball
# Stuarrt Boekelman - 3/23/2023
# This is a basic Magic 8 Ball game

# imports
import pygame
import pygame.gfxdraw
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Magic 8-Ball")
gameImage = pygame.image.load('game.png')
font = pygame.font.SysFont('CK 8 Ball Regular', 12)


class TriangleTextbox():
    def __init__(self, surface, font, text, triangle_points, scaling_factor, x_shift, y_shift, triangle_color, text_color):
        self.surface = surface
        self.font = font
        self.text = text
        self.triangle_points = triangle_points
        self.scaling_factor = scaling_factor
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.triangle_color = triangle_color
        self.text_color = text_color

        self.shifted_points = [(int(x * self.scaling_factor + self.x_shift), int(y * self.scaling_factor + self.y_shift)) for (x, y) in self.triangle_points]

    def draw(self):
        pygame.draw.polygon(self.surface, self.triangle_color, self.shifted_points)

        text_surface = self.font.render(self.text, True, self.text_color)

        text_x = self.shifted_points[0][0] + (self.shifted_points[1][0] - self.shifted_points[0][0] - text_surface.get_width()) // 2
        text_y = self.shifted_points[0][1] + (self.shifted_points[2][1] - self.shifted_points[0][1] - text_surface.get_height()) // 6

        self.surface.blit(text_surface, (text_x, text_y))


class TextBox():
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('white')
        self.font = font
        self.text = ''
        self.active = False

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color('white'), self.rect)
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('gray') if self.active else pygame.Color('white')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


askQuestionImg = pygame.image.load('question.png').convert_alpha()
quitProgramImg = pygame.image.load('quit.png').convert_alpha()


askQuestionBtn = Button(-100, 310, askQuestionImg, .8)
quitProgramBtn = Button(280, 310, quitProgramImg, .8)


entryFont = pygame.sysfont.SysFont('Arial', 15)
entryBox = TextBox(100, 495, 600, 20, entryFont)
answerFont = pygame.sysfont.SysFont('CK 8 Ball Regular', 25)
answerBox = TextBox(150, 250, 500, 100, answerFont)

def eightBall():
    eightBallAnswers = ["Yes, of course!", "Without a doubt, yes.", \
                        "You can count on it.", "For sure!", "Ask me later.", "I’m not sure", \
                        "I can’t tell you right now.", "I’ll tell you after my nap.", "No way!", \
                        "I don’t think so.", "Without a doubt, no.", "The answer is clearly NO."]
    answer = random.choice(eightBallAnswers)
    return answer


trianglePoints = [(102, 102), (300, 100), (200, 300)]
scalingFactor = 0.65
xShift = 73
yShift = 175
triangleColor = (0, 0, 255)
triTextColor = (0, 0, 0)
shiftedPoints = [(int(x * scalingFactor + xShift), int(y * scalingFactor + yShift)) for (x, y) in trianglePoints]

triBox = TriangleTextbox(screen, font, '', trianglePoints, scalingFactor, xShift, yShift, triangleColor, triTextColor)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if askQuestionBtn.handle_event(event):
                triBox.text = eightBall()
                questionAnswer = eightBall()
                entryBox.text = ''
                entryBox.active = False
                entryBox.color = pygame.Color('white')
                print(questionAnswer)
            elif quitProgramBtn.handle_event(event):
                pygame.quit()
                sys.exit()

        entryBox.handle_event(event)


    screen.blit(gameImage, (0, 0))
    askQuestionBtn.draw(screen)
    triBox.draw()
    quitProgramBtn.draw(screen)
    entryBox.draw(screen)
    pygame.display.update()