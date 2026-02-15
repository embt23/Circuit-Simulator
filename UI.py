import pygame

#colors

BLACK = (0, 0, 0)
GREEN = (0, 192, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


class button:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
    
    def draw(self, screen, width, height, outline=False):
        rect = (width * self.x1, height * self.y1, width * (self.x2 - self.x1), height * (self.y2 - self.y1))
        pygame.draw.rect(screen, self.color, rect, 0)
        if outline:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    def isClicked(self, mouseX, mouseY, width, height):
        if (mouseX >= width * self.x1 and mouseX <= width * self.x2 and
            mouseY >= height * self.y1 and mouseY <= height * self.y2):
            return True
        return False

class changingButton(button):
    def __init__(self, x1, y1, x2, y2, color, changeColor):
        super().__init__(x1, y1, x2, y2, color)
        self.changeColor = changeColor
        self.isChanged = False

    def draw(self, screen, width, height, outline=False):
        if self.isChanged:
            rect = (width * self.x1, height * self.y1, width * (self.x2 - self.x1), height * (self.y2 - self.y1))
            pygame.draw.rect(screen, self.changeColor, rect, 0)
            if outline:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        else:
            super().draw(screen, width, height)

    def isClicked(self, mouseX, mouseY, width, height):
        if (mouseX >= width * self.x1 and mouseX <= width * self.x2 and
            mouseY >= height * self.y1 and mouseY <= height * self.y2):
            self.isChanged = not self.isChanged
            return True
        return False



# Define buttons
wireButton = button(3/16, 7/8, 5/16, 1, BLACK)
voltage_sourceButton = button(5/16, 7/8, 7/16, 1, GREEN)
resistorButton = button(7/16, 7/8, 9/16, 1, RED)
capacitorButton = button(9/16, 7/8, 11/16, 1, YELLOW)
inductorButton = button(11/16, 7/8, 13/16, 1, BLUE)
startStopButton = changingButton(7/8, 0, 1, 1/8, BLACK, GREEN)


#User Interface
def ShowToolBar(screen, width, height, globalState):
    wireButton.draw(screen, width, height, globalState == "wire")
    voltage_sourceButton.draw(screen, width, height, globalState == "voltage_source")
    resistorButton.draw(screen, width, height, globalState == "resistor")
    capacitorButton.draw(screen, width, height, globalState == "capacitor")
    inductorButton.draw(screen, width, height, globalState == "inductor")
    startStopButton.draw(screen, width, height)
