import pygame
from pygame import Vector2, mixer, Color
import math

# Constants
WIDTH, HEIGHT = 700, 700
INITIAL_RADIUS = 30
GRAVITY = 0.32
INITIAL_VELOCITY = -7
BACKGROUND_COLOR = (0, 0, 0)
BOUNDARY_COLOR = (255, 255, 255)
BALL_COLOR = (0, 0, 0)

# Initialize Pygame and Mixer
pygame.init()
mixer.init()


# Load multiple sound effects
try:
    bounce_sound = mixer.Sound("bounce.wav")  # Sound effect for bouncing
    interact_sound = mixer.Sound("interact.wav")  # Sound effect for interaction
    print("Sound effects loaded successfully.")
except pygame.error as e:
    print(f"Failed to load sound effects: {e}")

# Load background music (optional)
try:
    mixer.music.load("background_music.mp3")  # Background music
    print("Background music loaded successfully.")
except pygame.error as e:
    print(f"Failed to load background music: {e}")

# Set up display
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")

class Ball:
    def __init__(self, x, y, radius, color):
        self.position = Vector2(x, y)
        self.radius = radius
        self.color = color
        self.velocity = Vector2(INITIAL_VELOCITY, INITIAL_VELOCITY)
        self.gravity = Vector2(0, GRAVITY)
        self.prevPos = Vector2(self.position.x, self.position.y)
    
    def update(self):
        self.prevPos = self.position.copy()

        # Change in positioning
        self.position += self.velocity
        self.velocity += self.gravity

        if self.check_collision():
            # On bounce effects (play sound, increase radius, change color)
            bounce_sound.play()  # Play bounce sound
            self.radius += 1

            # Set position to last non-colliding position
            self.position = self.prevPos

            # Get speed
            speed = self.velocity.length()

            # Calculate angles for the velocity and collision response
            dir_to_center = self.position - Vector2(WIDTH / 2, HEIGHT / 2)
            angle_to_collision_point = math.atan2(-dir_to_center.y, dir_to_center.x)
            old_velocity_angle = math.atan2(-self.velocity.y, self.velocity.x)
            new_velocity_angle = 2 * angle_to_collision_point - old_velocity_angle

            # Update velocity direction based on the new angle after collision
            self.velocity = Vector2(-speed * math.cos(new_velocity_angle), speed * math.sin(new_velocity_angle))

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.radius)

    def check_collision(self):
        dist_sq = (self.position.x - WIDTH / 2) ** 2 + (self.position.y - HEIGHT / 2) ** 2
        boundary_radius_sq = (WIDTH / 2 - self.radius) ** 2
        return dist_sq > boundary_radius_sq

# Create ball instance
ball = Ball(WIDTH / 2, HEIGHT / 2, INITIAL_RADIUS, BALL_COLOR)

# Initialize color for dynamic effect
color = Color(211, 12, 211)
h, s, l = color.hsla[0], color.hsla[1], color.hsla[2]
color_direction = 1

# Start playing background music
try:
    mixer.music.play(-1)  # Play background music in a loop
    if mixer.music.get_busy():
        print("Background music is playing.")
    else:
        print("Background music failed to play.")
except pygame.error as e:
    print(f"Error playing background music: {e}")

# Main loop
running = True
while running:
    clock.tick(60)
    
    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Update and draw the ball
    ball.update()
    pygame.draw.circle(screen, BOUNDARY_COLOR, (WIDTH / 2, HEIGHT / 2), WIDTH / 2, 5)
    
    # Dynamic color change
    color.hsla = (h, s, l, 1)
    h += 1 * color_direction
    if h >= 360:
        color_direction = -1
    elif h <= 0:
        color_direction = 1

    pygame.draw.circle(screen,
                       (color.r, color.g, color.b),
                       (ball.position.x, ball.position.y),
                       ball.radius + 2)

    ball.draw()

    pygame.display.flip()

pygame.quit()