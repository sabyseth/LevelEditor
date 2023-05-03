import pygame
pygame.init()

# Define the screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the background image and get its size
background_img = pygame.image.load('sky_cloud.png')
background_width = background_img.get_width()
background_height = background_img.get_height()

# Set the initial position of the background image
background_x = 0

# Set the speed at which the background scrolls
scroll_speed = 1

# Start the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Scroll the background
    background_x -= scroll_speed

    # Wrap the background image if it goes off the screen
    if background_x <= -background_width:
        background_x = 0

    # Draw the background image twice, side by side
    screen.blit(background_img, (background_x, 0))
    screen.blit(background_img, (background_x + background_width, 0))

    # Update the display
    pygame.display.update()