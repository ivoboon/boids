import pygame
import random
import math

class Boid():
    def __init__(self, x_min, y_min, x_max, y_max, speed_min, speed_max):
        # Generating position
        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)
        
        # Generating velocity
        magnitude = random.triangular(speed_min, speed_max)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = magnitude * math.cos(angle)
        self.vy = magnitude * math.sin(angle)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x > 1000:
            self.x = 0
        if self.y > 1000:
            self.y = 0
        if self.x < 0:
            self.x = 1000
        if self.y < 0:
            self.y = 1000

    def draw(self, surface, boid_colour, boid_radius):
        pygame.draw.circle(surface, boid_colour, (int(self.x), int(self.y)), boid_radius, 0)

def main():
    fps = 60
    run = True
    boid_colour = (255, 0, 0)
    boid_radius = 5
    background_colour = (0, 0, 0)

    num_boids = 10

    separation_radius = 10
    alignment_radius = 40
    cohesion_radius = 40
    separation_factor = 0.05
    alignment_factor = 0.05
    cohesion_factor = 0.05

    x_min = 0
    y_min = 0
    x_max = 1000
    y_max = 1000
    speed_max = 3
    speed_min = 1

    boids = []

    for _ in range(num_boids):
        boids.append(Boid(x_min, y_min, x_max, y_max, speed_min, speed_max))

    pygame.init()
    screen = pygame.display.set_mode((x_max - x_min, y_max - y_min))
    pygame.display.set_caption("Boids Simulation")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(background_colour)

        for boid in boids:
            boid.update()
            boid.draw(screen, boid_colour, boid_radius)
        
        pygame.display.flip()



if __name__ == "__main__":
    main()