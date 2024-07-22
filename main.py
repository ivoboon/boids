import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import random
import math

class Boid():
	def __init__(self,
				 x_min, y_min, x_max, y_max,
				 speed_min, speed_max,
				 separation_radius, alignment_radius, cohesion_radius,
				 separation_factor, alignment_factor, cohesion_factor,
				 boid_colour, boid_radius):
		# Generating position
		self.x = random.uniform(x_min, x_max)
		self.y = random.uniform(y_min, y_max)
		
		# Generating velocity
		magnitude = random.triangular(speed_min, speed_max)
		angle = random.uniform(0, 2 * math.pi)
		self.vx = magnitude * math.cos(angle)
		self.vy = magnitude * math.sin(angle)
		self.dvx = self.vx
		self.dvy = self.vy

		# Setting radii and factors
		self.separation_radius = separation_radius
		self.alignment_radius = alignment_radius
		self.cohesion_radius = cohesion_radius
		self.separation_factor = separation_factor
		self.alignment_factor = alignment_factor
		self.cohesion_factor = cohesion_factor

		# Setting speed limits
		self.speed_min = speed_min
		self.speed_max = speed_max

		# Setting visualisation parameters
		self.colour = boid_colour
		self.radius = boid_radius

	def update_position(self):
		speed = math.sqrt(self.dvx ** 2 + self.dvy ** 2)
		if speed < self.speed_min:
			self.dvx = self.speed_min * self.dvx / speed
			self.dvy = self.speed_min * self.dvy / speed
		if speed > self.speed_max:
			self.dvx = self.speed_max * self.dvx / speed
			self.dvy = self.speed_max * self.dvy / speed
		self.vx = self.dvx
		self.vy = self.dvy
		self.x += self.vx
		self.y += self.vy
		if self.x > 1200:
			self.x = 0
		elif self.x < 0:
			self.x = 1200
		if self.y > 1200:
			self.y = 0
		elif self.y < 0:
			self.y = 1200

	def draw(self, surface):
		pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), self.radius, 0)

def update_velocity(boids):
	for outer_boid in boids:
		close_dx = 0
		close_dy = 0
		xvel_avg = 0
		yvel_avg = 0
		alignment_neighbours = 0
		xpos_avg = 0
		ypos_avg = 0
		cohesion_neighbours = 0
		for inner_boid in boids:
			if inner_boid != outer_boid:
				dist = math.sqrt((outer_boid.x - inner_boid.x) ** 2 + (outer_boid.y - inner_boid.y) ** 2)
				if dist <= outer_boid.separation_radius:
					close_dx += outer_boid.x - inner_boid.x
					close_dy += outer_boid.y - inner_boid.y
				if dist <= outer_boid.alignment_radius:
					xvel_avg += inner_boid.vx
					yvel_avg += inner_boid.vy
					alignment_neighbours += 1
				if dist <= outer_boid.cohesion_radius:
					xpos_avg += inner_boid.x
					ypos_avg += inner_boid.y
					cohesion_neighbours += 1
		if close_dx != 0 or close_dy != 0:
			outer_boid.dvx += close_dx * outer_boid.separation_factor
			outer_boid.dvx += close_dy * outer_boid.separation_factor
		if alignment_neighbours > 0:
			xvel_avg = xvel_avg / alignment_neighbours
			yvel_avg = yvel_avg / alignment_neighbours
			outer_boid.dvx += (xvel_avg - outer_boid.vx) * outer_boid.alignment_factor
			outer_boid.dvy += (yvel_avg - outer_boid.vy) * outer_boid.alignment_factor
		if cohesion_neighbours > 0:
			xpos_avg = xpos_avg / cohesion_neighbours
			ypos_avg = ypos_avg / cohesion_neighbours
			outer_boid.dvx += (xpos_avg - outer_boid.x) * outer_boid.cohesion_factor
			outer_boid.dvy += (ypos_avg - outer_boid.y) * outer_boid.cohesion_factor

def main():
	fps = 60
	run = True
	boid_colour = (255, 0, 0)
	boid_radius = 5
	background_colour = (0, 0, 0)

	num_boids = 200

	separation_radius = 10
	alignment_radius = 75
	cohesion_radius = 100
	separation_factor = 0.05
	alignment_factor = 0.05
	cohesion_factor = 0.0005

	x_min = 0
	y_min = 0
	x_max = 1200
	y_max = 1200
	speed_max = 6
	speed_min = 3

	boids = []

	for _ in range(num_boids):
		boids.append(Boid(x_min, y_min, x_max, y_max,
						  speed_min, speed_max,
						  separation_radius, alignment_radius, cohesion_radius,
						  separation_factor, alignment_factor, cohesion_factor,
						  boid_colour, boid_radius))

	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((x_max - x_min, y_max - y_min))
	pygame.display.set_caption("Boids Simulation")

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		screen.fill(background_colour)

		update_velocity(boids)

		for boid in boids:
			boid.update_position()
			boid.draw(screen)
		
		pygame.display.flip()

		clock.tick(fps)

if __name__ == "__main__":
	main()