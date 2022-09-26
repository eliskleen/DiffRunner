import pygame

from textEditor import TextEditor


class Form:
    def __init__(self, runDiff):
        self.runDiff = runDiff

    def rDiff(self):
        self.runDiff()
        self.textEditor.open_file("result.txt")
    def load(self):
        print("Hello World")

        # initializing the constructor
        pygame.init()

        # screen resolution
        res = (300, 150)

        # opens up a window
        screen = pygame.display.set_mode(res)

        # white color
        color = (255, 255, 255)

        # light shade of the button
        color_light = (170, 170, 170)

        # dark shade of the button
        color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        width = screen.get_width()

        # stores the height of the
        # screen into a variable
        height = screen.get_height()
        clock = pygame.time.Clock()
        self.textEditor = TextEditor()
        screen.fill((60,25,60))
        pygame.display.set_caption('LimeRegiStatus')

        button1 = Button(
            screen,
            "Run diff from files",
            (30, 10),
            font=30,
            # bg="black",
            bg = (60,25,60),
            feedback=self.rDiff)
        button2 = Button(
            screen,
            "Edit known diffs",
            (30, 60),
            font=30,
            bg = (60,25,60),
            # bg="black",
            feedback=self.openDiffs)
        button3 = Button(
            screen,
            "Edit LimeStatus",
            (30, 110),
            font=30,
            bg = (60,25,60),
            # bg="black",
            feedback=self.openStatus)

        """ The infinite loop where things happen """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                button1.click(event)
                button2.click(event)
                button3.click(event)
            button1.show()
            button2.show()
            button3.show()
            clock.tick(30)
            pygame.display.update()

    def openDiffs(self):
        self.textEditor.open_file("knownDiffs.txt")
    def openStatus(self):
        self.textEditor.open_file("statusInLime.txt")
    def testPoint(self):
        print("Im a fun pointer")


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, screen, text,  pos, font, bg="black", feedback=""):
        self.screen = screen
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.feedback = feedback
   #    b if feedback == "":
    #         self.feedack = "text"
    #     else:
    #         self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        # self.text = self.font.render(text, 1, pygame.Color("White"))
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    # self.change_text(self.feedback, bg="red")
                    self.feedback()
