import math as m
import numpy as np
import pygame
import sys

pygame.init()

screen_length = 400
screen_width = 400
screen = pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption('donut')
clock = pygame.time.Clock()
text_font=pygame.font.SysFont("monospace", 15)

donut_R = 2
donut_r = 1
cam_z = -5
donut_dir_x=0
donut_dir_z=0
light_source_pos=np.array([0,-1,-6])
sin_cache = {}
cos_cache = {}


def rotation(pos, dir_x,dir_y, dir_z):
    x_rotation_mat = np.array([[1, 0, 0],
                               [0, cos_cache[dir_x], sin_cache[dir_x]],
                               [0, -sin_cache[dir_x], cos_cache[dir_x]]])
    y_rotation_mat = np.array([[cos_cache[dir_y], 0, sin_cache[dir_y]],
                               [0, 1, 0],
                               [-sin_cache[dir_y], 0, cos_cache[dir_y]]])
    z_rotation_mat = np.array([[cos_cache[dir_z], sin_cache[dir_z], 0],
                               [-sin_cache[dir_z], cos_cache[dir_z], 0],
                               [0, 0, 1]])
    ryp = np.matmul(pos, y_rotation_mat)
    rxp = np.matmul(ryp, x_rotation_mat)
    rzp = np.matmul(rxp, z_rotation_mat)
    return rzp

def calc_normal_line(circle_dir, dir_x, dir_y, dir_z):
  pos=np.array([cos_cache[circle_dir],sin_cache[circle_dir],0])
  return rotation(pos , dir_x, dir_y, dir_z)

def calc_light_level(normal_line):
  l=m.floor(np.matmul(normal_line,light_source_pos))
  return l*40

def projection(pos3d):
    x, y, z = pos3d
    return x * 240 / (z + cam_z), y * 240 / (z + cam_z)


def render_a_donut():
    for circle_dir in range(0, 360, 12): #theta
        x = donut_R + donut_r * cos_cache[circle_dir]
        y = donut_r * sin_cache[circle_dir]
        z = 0
        pos = np.array([x, y, z])
        for sy_dir in range(0, 360, 12):
            normal_line=calc_normal_line(circle_dir, donut_dir_x, sy_dir, donut_dir_z)
            light_level=calc_light_level(normal_line)
            if light_level>0:
              npos = rotation(pos, donut_dir_x,sy_dir, donut_dir_z)
              x2d, y2d = projection(npos)
              pygame.draw.circle(screen, (light_level, light_level, light_level), (int(x2d+screen_length//2), int(y2d+screen_width//2)), 1)
              # screen.set_at((int(x2d+screen_length//2), int(y2d+screen_width//2)), (light_level, light_level, light_level))

def show__text(text,pos):
    text_image=text_font.render(text, 1, (255,255,255))
    screen.blit(text_image, pos)
    
# Pre-calculate sin and cos values
for angle in range(0, 360):
    rad = m.radians(angle)
    sin_cache[angle] = m.sin(rad)
    cos_cache[angle] = m.cos(rad)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    donut_dir_x+=2
    donut_dir_z+=2
    donut_dir_x%=360
    donut_dir_z%=360

    render_a_donut()
    show__text(str(round(clock.get_fps(),2)), (0,0))
    
    pygame.display.flip()
    clock.tick(30)
