"""
Main game loop for the Licker-2 application.
Handles initialization, event processing, and rendering.
"""

# Standard library imports
from random import *
from math import *

# Third-party imports
import pygame

# Local imports
from globals import *
from Censors.Picaso import *
from Censors.Bubble import *
from Censors.Fracture import *


def main():
    """Main game function that initializes and runs the game loop."""
    # Initialize pygame
    pygame.init()
    
    # Set up display - fullscreen mode
    SCREEN = pygame.display.set_mode((0, 0))
    SCREEN_SIZE = SCREEN.get_size()
    
    # Create internal rendering surface (fixed resolution)
    INTERNAL_WIDTH = 1920
    INTERNAL_HEIGHT = 1080
    win = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
    
    # Initialize event handler
    AEH = AllEventHandler(SCREEN_SIZE)
    
    # Initialize test censor
    test_censor = Fracture_Censor()
    
    # Main game loop
    run = True
    while run:
        # Update event handler (processes input, mouse, keyboard)
        AEH.update()
        
        # Check for exit condition
        if AEH.exit:
            run = False
            break
        
        # Clear the internal surface
        win.fill((0, 0, 0))
        
        # Update and draw the censor
        test_censor.update(AEH)
        test_censor.draw()
        win.blit(test_censor.surface, (0, 0))
        
        # Scale internal surface to screen size and display
        SCREEN.blit(pygame.transform.scale(win, SCREEN_SIZE), (0, 0))
        pygame.display.update()
    
    # Clean up
    pygame.quit()


if __name__ == "__main__":
    main()