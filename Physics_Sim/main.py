import pygame
import sys
import pymunk


def create_ball(space, pos):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    # (mass, inertia, body_type (i.e., Dynamic, Static, or Kinetic)

    body.position = pos
    shape = pymunk.Circle(body, 28)  # (body, radius)
    space.add(body, shape)
    return shape


def draw_balls(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        ball_rect = ball_surface.get_rect(center=(pos_x, pos_y))
        screen.blit(ball_surface, ball_rect)


def obst(space, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # don't need mass or inertia
    body.position = pos
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape


def draw_obst(obsts):
    for obst in obsts:
        pos_x = int(obst.body.position.x)
        pos_y = int(obst.body.position.y)
        pygame.draw.circle(screen, (217, 98, 119), (pos_x, pos_y), 20)
        # (screen, color, center of body (ball), radius)


pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 400)  # (x-grav, y-grav)

ball_surface = pygame.transform.scale(pygame.image.load('apple.png'), (60, 60))

balls = []

obsts = []
obsts.append(obst(space, (250, 250)))
obsts.append(obst(space, (150, 300)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(create_ball(space, event.pos))

    screen.fill((217, 217, 217))
    draw_balls(balls)
    draw_obst(obsts)
    space.step(1 / 50)  # rate at which the physics space is updating
    pygame.display.update()
    clock.tick(120)
