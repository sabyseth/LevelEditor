import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SIDE_MARGIN = 100
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set up font
font = pygame.font.Font(None, 36)

# Draw side margin
pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

# Render text
text = font.render("This text is over the side margin", True, WHITE)

# Get text position
text_rect = text.get_rect()
text_rect.centerx = screen.get_width() - SIDE_MARGIN // 2
text_rect.centery = screen.get_height() // 2

# Draw text on screen
screen.blit(text, text_rect)

# Update the screen
pygame.display.update()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()