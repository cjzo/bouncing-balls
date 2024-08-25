import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700
RADIUS = 300  # Radius of the outer circle
SPEED = 0.02  # Speed at which the image moves around the circle
BALL_RADIUS = 15  # Radius of each ball
FONT_SIZE = 32  # Font size for the counter display
GRAVITY = 0.2  # Gravity constant to allow ball to reach the ceiling
INITIAL_VELOCITY = 7  # Initial velocity for ball movement
MAX_BALLS = 1000  # Maximum number of balls to prevent excessive spawning

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You are my sunshine")

# Load and scale the image
image = pygame.image.load("lebron.png")  # Replace 'your_image.png' with your image file path
image = pygame.transform.scale(image, (50, 50))  # Scale the image to 50x50 pixels
image_rect = image.get_rect()  # Get the rect of the image for collision detection

# Load sound effects
bounce_sound = pygame.mixer.Sound("bounce.wav")  # Sound for bouncing off the screen edges
interact_sound = pygame.mixer.Sound("interact.wav")  # Sound for colliding with the image

# Initialize font for displaying counter
font = pygame.font.Font(None, FONT_SIZE)

# Initialize the clock to control the frame rate
clock = pygame.time.Clock()

# Function to calculate the position on the circle
def calculate_position_on_circle(center, radius, angle):
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    return x, y

# Ball class definition
class Ball:
    def __init__(self, position, velocity, radius=BALL_RADIUS):
        self.position = list(position)
        self.velocity = list(velocity)
        self.radius = radius
    
    def update(self):
        # Apply gravity to the vertical velocity
        self.velocity[1] += GRAVITY

        # Update ball position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Check for collision with the outer circle boundary and bounce
        dist_to_center = math.sqrt((self.position[0] - WIDTH / 2) ** 2 + (self.position[1] - HEIGHT / 2) ** 2)
        if dist_to_center + self.radius > RADIUS:
            # Correct position so the ball doesn't phase through the boundary
            overlap = (dist_to_center + self.radius) - RADIUS
            self.position[0] -= overlap * (self.position[0] - WIDTH / 2) / dist_to_center
            self.position[1] -= overlap * (self.position[1] - HEIGHT / 2) / dist_to_center

            # Calculate normal vector at collision point
            normal_vector = [(self.position[0] - WIDTH / 2) / dist_to_center, (self.position[1] - HEIGHT / 2) / dist_to_center]
            dot_product = self.velocity[0] * normal_vector[0] + self.velocity[1] * normal_vector[1]
            
            # Reflect velocity across the normal vector
            self.velocity[0] -= 2 * dot_product * normal_vector[0]
            self.velocity[1] -= 2 * dot_product * normal_vector[1]
            bounce_sound.play()  # Play bounce sound

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.position[0] - self.radius, self.position[1] - self.radius, self.radius * 2, self.radius * 2)

# Initialize variables
angle = 0  # Start angle
center = (WIDTH // 2, HEIGHT // 2)  # Center of the screen
balls = [Ball(center, (INITIAL_VELOCITY, -INITIAL_VELOCITY))]  # Start with one ball at the center with higher upward velocity
collision_counter = 0

# Main loop
running = True
while running:
    # Cap the frame rate at 60 frames per second
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate new position for the moving image
    x, y = calculate_position_on_circle(center, RADIUS, angle)
    image_rect.center = (x, y)  # Update the rect position for collision detection

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the outer circle
    pygame.draw.circle(screen, (255, 255, 255), center, RADIUS, 1)

    # Update and draw all balls
    for ball in balls[:]:  # Use a slice to safely modify the list while iterating
        ball.update()
        ball.draw()
        # Check for collision between each ball and the image
        if ball.get_rect().colliderect(image_rect):
            collision_counter += 1  # Increment counter
            interact_sound.play()  # Play interaction sound
            balls.remove(ball)  # Remove the ball that collided

            # Spawn two new balls at the center with slightly random trajectories if below max limit
            if len(balls) < MAX_BALLS:
                for _ in range(2):
                    # Increase random velocity range for more dynamic motion
                    new_velocity = [random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY), random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)]
                    new_ball = Ball(center, new_velocity)
                    balls.append(new_ball)

    # Draw the image
    screen.blit(image, image_rect.topleft)

    # Display collision counter below the main circle
    counter_text = font.render(f"Collisions: {collision_counter}", True, (255, 255, 255))
    screen.blit(counter_text, (center[0] - counter_text.get_width() // 2, center[1] + RADIUS + 20))

    # Update the display
    pygame.display.flip()

    # Increment the angle for the next frame
    angle += SPEED

    # Reset the angle to keep it within 0 to 2*pi
    if angle > 2 * math.pi:
        angle -= 2 * math.pi

# Quit Pygame
pygame.quit()