class GameConstants:
    # Window dimensions
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 600
    
    # Kitten movement boundaries
    KITTEN_MIN_X = 0
    KITTEN_MAX_X = 320  # WINDOW_WIDTH - (width + 50)
    KITTEN_MIN_Y = 86
    KITTEN_MAX_Y = 255  # 335 - height
    
    # Fish movement boundaries
    FISH_MIN_X = 0
    FISH_MAX_X = 330
    FISH_MIN_Y = 335
    FISH_MAX_Y = 550
    
    # Fish parameters
    FISH_WIDTH = 50
    FISH_HEIGHT = 50
    FISH_TAIL_WIDTH = 20
    
    # Movement speeds
    KITTEN_MOVE_SPEED = 10
    FISH_SPEED_X = (-3, 3)  # (min, max) for random
    FISH_SPEED_Y = (-2, 2)
    
    # Fishing line
    LINE_LENGTH = 280
    
    # Available colors
    COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'black', 'gray']
    
    # Bar parameters
    BAR_WIDTH = 150
    BAR_HEIGHT = 20
    BAR_INCREASE = 15
    BAR_DECREASE = 5
    CLICK_TIMEOUT = 3