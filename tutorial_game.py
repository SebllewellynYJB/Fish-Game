import random
import pyasge
from gamedata import GameData


def isInside(sprite, mouse_x, mouse_y) -> bool:
    # grab the sprite's bounding box. the box has 4 vertices
    bounds = sprite.getWorldBounds()
    # check to see if the mouse position falls within the x and y bounds
    if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
        return True

    return False


class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
            Initialises the game and sets up the shared data.

            Args:
                settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # Set this data for the Game Menu
        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0
        self.quit_text = None

        # Background data
        self.data.background = pyasge.Sprite()
        self.initBackground()

        # Menu Data
        self.menu_text = None
        self.initMenu()

        # Scoreboard Data
        self.scoreboard = None
        self.initScoreboard()

        # Fish Sprite and List
        self.fish = []
        self.fish.append(pyasge.Sprite())
        self.fish.append(pyasge.Sprite())
        self.fish.append(pyasge.Sprite())
        self.fish.append(pyasge.Sprite())
        self.initFish()

        # Timer details
        self.timer = 0
        self.timer_limit = 60

        # Timer Text
        self.timer_text = pyasge.Text(self.data.fonts["MainFont"])
        self.timer_text.y = 60
        self.timer_text.x = 50
        self.timer_text.colour = pyasge.COLOURS.WHITE

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):
            # loaded, so make sure this gets rendered first
            self.data.background.z_order = -100
            return True
        else:
            return False

    def initFish(self) -> bool:
        for fishy in self.fish:
            fishy.loadTexture("/data/images/kenney_fishpack/fishTile_072.png")
            fishy.z_order = 1
            fishy.scale = 1
            self.spawn(fishy)

    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.x = 1300
        self.scoreboard.y = 75
        self.scoreboard.string = str(self.data.score).zfill(6)

    def initMenu(self) -> bool:
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "The Fish Game"
        self.menu_text.position = [100, 100]
        self.menu_text.colour = pyasge.COLOURS.HOTPINK

        # This option starts the game
        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = ">START"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.HOTPINK

        # This option exits the games
        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "EXIT"
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        # This is the text for the quit at any time
        self.quit_text = pyasge.Text(self.data.fonts["MainFont"])
        self.quit_text.string = "Press Q to exit the game at any time"
        self.quit_text.position = [60, 600]
        self.quit_text.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        # This option is to show how long you have to score points
        self.time_text = pyasge.Text(self.data.fonts["MainFont"])
        self.time_text.string = "You have 60 seconds to score points"
        self.time_text.position = [100, 250]
        self.time_text.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        return True

    def clickHandler(self, event: pyasge.ClickEvent) -> None:

        # look to see if mouse button 1 pressed
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and \
                event.button == pyasge.MOUSE.MOUSE_BTN1:

            # Check if you can click on the fish and all fish load

            for fishy in self.fish:
                if isInside(fishy, event.x, event.y):
                    random_number = random.randint(0, 2)
                    self.data.score += 1
                    self.scoreboard.string = str(self.data.score).zfill(6)
                    if random_number == 0:
                        fishy.loadTexture("/data/images/kenney_fishpack/fishTile_078.png")
                        self.spawn(fishy)
                    elif random_number == 1:
                        fishy.loadTexture("/data/images/kenney_fishpack/fishTile_080.png")
                        self.spawn(fishy)
                    elif random_number == 2:
                        fishy.loadTexture("/data/images/kenney_fishpack/fishTile_077.png")
                        self.spawn(fishy)
                        self.data.score += 1

    def keyHandler(self, event: pyasge.KeyEvent) -> None:
        # only act when the key is pressed and not released
        if event.action == pyasge.KEYS.KEY_PRESSED:

            # use both the right and left keys to select the play/exit options
            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
            if self.menu_option == 0:
                self.play_option.string = ">START"
                self.play_option.colour = pyasge.COLOURS.HOTPINK
                self.exit_option.string = " EXIT"
                self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
            else:
                self.play_option.string = " START"
                self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                self.exit_option.string = " >EXIT"
                self.exit_option.colour = pyasge.COLOURS.HOTPINK

        # if the enter key is pressed, action the menu option
        if event.key == pyasge.KEYS.KEY_ENTER:
            if self.menu_option == 0:
                self.menu = False
            else:
                self.signal_exit()
        # if the key is pressed it exits the game
        if event.key == pyasge.KEYS.KEY_Q:
            self.signal_exit()

        # If key is pressed it takes away 5 points
        if event.key == pyasge.KEYS.KEY_R:
            self.data.score -= 5

    def spawn(self, fishy=None) -> None:
        
        # generate random {x,y} but don't let the fish spawn on edges
        x = random.randint(0, self.data.game_res[0] - self.fish[0].width)
        y = random.randint(0, self.data.game_res[1] - self.fish[0].height)

        fishy.x = x
        fishy.y = y

    def update(self, game_time: pyasge.GameTime) -> None:

        # Time updates here
        self.timer += game_time.frame_time
        self.timer_text.string = str("0".format(self.timer))

        if self.menu:
            # update the menu here
            pass
        else:
            # update the game here
            for fishy in self.fish:
                fishy.x += 6
                if fishy.x > 1600:
                    fishy.x = 0

    def render(self, game_time: pyasge.GameTime) -> None:

        # Render the Time Here
        if self.timer > self.timer_limit:
            self.signal_exit()

        # Render the background here

        self.data.renderer.render(self.data.background)

        if self.menu:

            # render the menu here
            self.data.renderer.render(self.menu_text)
            self.data.renderer.render(self.play_option)
            self.data.renderer.render(self.exit_option)
            self.data.renderer.render(self.quit_text)
            self.data.renderer.render(self.time_text)

        else:

            # render the Fish here
            for fishy in self.fish:
                self.data.renderer.render(fishy)

            # render the rest of the game here
            self.data.renderer.render(self.scoreboard)
            self.data.renderer.render(self.timer_text)

            pass


def main():
    """
    Creates the game and runs it
    For PYASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set a to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
