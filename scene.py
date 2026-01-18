import math
import sys
import time
import numpy as np
import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from graphics_utils import GraphicsUtils

class AdvancedGraphicsScene:
    CAMERA_FOV = 45
    CAMERA_NEAR = 0.1
    CAMERA_FAR = 100.0
    MOVE_SPEED = 2.0
    ROTATE_SPEED = 1.0
    MOUSE_SENSITIVITY = 0.15
    DEFAULT_LIGHT_POS = (5.0, 7.0, 5.0, 1.0)
    AMBIENT_GLOBAL_LIGHT = (0.1, 0.1, 0.1, 1.0)
    LIGHT_AMBIENT = (0.1, 0.1, 0.1, 1.0)
    LIGHT_DIFFUSE = (1.0, 1.0, 1.0, 1.0)
    LIGHT_SPECULAR = (0.4, 0.4, 0.4, 1.0)
    ROOM_SIZE = 8.0
    LIGHT_ROTATE_SPEED = 180.0
    POINT_LIGHT_POS1 = (-4.0, 4.0, -4.0, 1.0)
    POINT_LIGHT_POS2 = (4.0, 3.0, -4.0, 1.0)

    def __init__(self, width=1024, height=768):
        try:
            pygame.init()
        except pygame.error as e:
            print(f"Error initializing Pygame: {e}")
            sys.exit(1)

        self.width = width
        self.height = height
        pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.OPENGLBLIT)
        pygame.display.set_caption("3D Graphics Scene")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.mouse_sensitivity = AdvancedGraphicsScene.MOUSE_SENSITIVITY

        glClearColor(0.3, 0.3, 0.3, 1.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        self.light_intensity = 1.0
        self.light_angle = 0.0
        self.light_rotate_speed = AdvancedGraphicsScene.LIGHT_ROTATE_SPEED
        self.fixed_light_pos = np.array(AdvancedGraphicsScene.DEFAULT_LIGHT_POS, dtype=float)
        self.directional_light_intensity = 0.3
        self.dir_light_direction = (0, -1, 0)  
        self.setup_lights()

        self.camera_pos = Vector3(0, 2, 12)
        self.camera_target = Vector3(0, 1, 0)
        self.camera_rotation_x = 0
        self.camera_rotation_y = 0
        self.move_speed = AdvancedGraphicsScene.MOVE_SPEED
        self.rotate_speed = AdvancedGraphicsScene.ROTATE_SPEED

        self.objects = []
        self.add_object('sphere', (-2, 1, -1), (0.8, 0.2, 0.2, 1.0), 0.7, 'polished_metal')
        self.add_object('cube', (2, 1, -2), (0.2, 0.8, 0.2, 1.0), 0.6, 'rough_plastic')
        self.add_object('pyramid', (-1, 0.5, -3), (0.2, 0.2, 0.8, 1.0), 0.5, 'reflective_glass')
        self.add_object('sphere', (1, 0.5, -1), (0.7, 0.5, 0.2, 1.0), 0.4, 'mat_material')

        self.last_frame_time = time.time()
        self.camera_has_moved = True
        self.object_has_moved = True
       
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(AdvancedGraphicsScene.CAMERA_FOV, (width / height), AdvancedGraphicsScene.CAMERA_NEAR,
                       AdvancedGraphicsScene.CAMERA_FAR)
        glMatrixMode(GL_MODELVIEW)

    def setup_lights(self):
        glEnable(GL_LIGHTING)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, AdvancedGraphicsScene.AMBIENT_GLOBAL_LIGHT)

        light_pos = self.calculate_rotated_light_pos()

        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (AdvancedGraphicsScene.LIGHT_AMBIENT[0] * self.light_intensity,
                                          AdvancedGraphicsScene.LIGHT_AMBIENT[1] * self.light_intensity,
                                          AdvancedGraphicsScene.LIGHT_AMBIENT[2] * self.light_intensity,
                                          AdvancedGraphicsScene.LIGHT_AMBIENT[3]))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (AdvancedGraphicsScene.LIGHT_DIFFUSE[0] * self.light_intensity,
                                          AdvancedGraphicsScene.LIGHT_DIFFUSE[1] * self.light_intensity,
                                          AdvancedGraphicsScene.LIGHT_DIFFUSE[2] * self.light_intensity,
                                          AdvancedGraphicsScene.LIGHT_DIFFUSE[3]))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (AdvancedGraphicsScene.LIGHT_SPECULAR[0] * self.light_intensity,
                                           AdvancedGraphicsScene.LIGHT_SPECULAR[1] * self.light_intensity,
                                           AdvancedGraphicsScene.LIGHT_SPECULAR[2] * self.light_intensity,
                                           AdvancedGraphicsScene.LIGHT_SPECULAR[3]))
        glEnable(GL_LIGHT0)

        dir_ambient = np.array(AdvancedGraphicsScene.LIGHT_AMBIENT, dtype=float) * self.directional_light_intensity
        dir_diffuse = np.array(AdvancedGraphicsScene.LIGHT_DIFFUSE, dtype=float) * self.directional_light_intensity
        dir_specular = np.array(AdvancedGraphicsScene.LIGHT_SPECULAR, dtype=float) * self.directional_light_intensity

        glLightfv(GL_LIGHT1, GL_AMBIENT, dir_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, dir_diffuse)
        glLightfv(GL_LIGHT1, GL_SPECULAR, dir_specular)
        glLightfv(GL_LIGHT1, GL_POSITION, self.dir_light_direction)
        glEnable(GL_LIGHT1)

        point_light_ambient = (
        0.05 * self.light_intensity, 0.05 * self.light_intensity, 0.05 * self.light_intensity, 1.0)  
        point_light_diffuse = (
        0.3 * self.light_intensity, 0.3 * self.light_intensity, 0.3 * self.light_intensity, 1.0) 
        point_light_specular = (
        0.08 * self.light_intensity, 0.08 * self.light_intensity, 0.08 * self.light_intensity, 1.0) 

        glLightfv(GL_LIGHT2, GL_POSITION, AdvancedGraphicsScene.POINT_LIGHT_POS1)
        glLightfv(GL_LIGHT2, GL_AMBIENT, point_light_ambient)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, point_light_diffuse)
        glLightfv(GL_LIGHT2, GL_SPECULAR, point_light_specular)

        glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.1)
        glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.01)

        glEnable(GL_LIGHT2)

        point_light_ambient_2 = (0.05 * self.light_intensity, 0.05 * self.light_intensity, 0.05 * self.light_intensity,
                                 1.0)  
        point_light_diffuse_2 = (
        0.2 * self.light_intensity, 0.2 * self.light_intensity, 0.2 * self.light_intensity, 1.0)
        point_light_specular_2 = (
        0.09 * self.light_intensity, 0.09 * self.light_intensity, 0.09 * self.light_intensity, 1.0)  # spec az.

        glLightfv(GL_LIGHT3, GL_POSITION, AdvancedGraphicsScene.POINT_LIGHT_POS2)
        glLightfv(GL_LIGHT3, GL_AMBIENT, point_light_ambient_2)
        glLightfv(GL_LIGHT3, GL_DIFFUSE, point_light_diffuse_2)
        glLightfv(GL_LIGHT3, GL_SPECULAR, point_light_specular_2)

        glLightf(GL_LIGHT3, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT3, GL_LINEAR_ATTENUATION, 0.1)
        glLightf(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, 0.01)
        glEnable(GL_LIGHT3)


    def calculate_rotated_light_pos(self):
        radius = 5
        x = radius * math.cos(math.radians(self.light_angle))
        z = radius * math.sin(math.radians(self.light_angle))
        return (x, self.fixed_light_pos[1], z, 1.0)


    def handle_camera_movement(self):
            keys = pygame.key.get_pressed()
            mouse_movement = pygame.mouse.get_rel()

            current_frame_time = time.time()
            delta_time = current_frame_time - self.last_frame_time
            self.last_frame_time = current_frame_time

            if keys[pygame.K_KP4]:
                self.light_angle += self.light_rotate_speed * delta_time
            if keys[pygame.K_KP6]:
                self.light_angle -= self.light_rotate_speed * delta_time

            if mouse_movement[0] != 0 or mouse_movement[1] != 0:
                self.camera_rotation_x += mouse_movement[0] * self.mouse_sensitivity
                self.camera_rotation_y -= mouse_movement[1] * self.mouse_sensitivity
                self.camera_rotation_y = max(min(self.camera_rotation_y, 90), -90)
                self.camera_has_moved = True

            forward = Vector3(
                math.sin(math.radians(self.camera_rotation_x)),
                0,
                -math.cos(math.radians(self.camera_rotation_x))
            )

            right = Vector3(
                math.cos(math.radians(self.camera_rotation_x)),
                0,
                math.sin(math.radians(self.camera_rotation_x))
            )

            move_vector = Vector3(0, 0, 0)
            if keys[pygame.K_w]:
                move_vector += forward * self.move_speed
            if keys[pygame.K_s]:
                move_vector -= forward * self.move_speed
            if keys[pygame.K_a]:
                move_vector -= right * self.move_speed
            if keys[pygame.K_d]:
                move_vector += right * self.move_speed

            if move_vector.length() > 0:
                self.camera_pos += move_vector * delta_time
                self.camera_has_moved = True
            look_dir = Vector3(
                math.sin(math.radians(self.camera_rotation_x)) * math.cos(math.radians(self.camera_rotation_y)),
                math.sin(math.radians(self.camera_rotation_y)),
                -math.cos(math.radians(self.camera_rotation_x)) * math.cos(math.radians(self.camera_rotation_y))
            )
            self.camera_target = self.camera_pos + look_dir

    def add_object(self, obj_type, position, color, size, material):
        self.objects.append({
            'type': obj_type,
            'position': position,
            'color': color,
            'size': size,
            'material': material
        })
        self.object_has_moved = True

    def render(self):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluLookAt(
                self.camera_pos.x, self.camera_pos.y, self.camera_pos.z,
                self.camera_target.x, self.camera_target.y, self.camera_target.z,
                0, 1, 0
            )
            self.setup_lights()
            GraphicsUtils.draw_room()
            for obj in self.objects:
                glPushMatrix()
                glTranslatef(*obj['position'])
                GraphicsUtils.set_material(obj['material'])
                glColor4fv(obj['color'])

                if obj['type'] == 'sphere':
                    GraphicsUtils.draw_sphere(obj['size'])
                elif obj['type'] == 'cube':
                    GraphicsUtils.draw_cube(obj['size'])
                elif obj['type'] == 'pyramid':
                    GraphicsUtils.draw_pyramid(obj['size'])
                glPopMatrix()

            pygame.display.flip()
            self.handle_camera_movement()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEWHEEL:
                    self.light_intensity += event.y * 0.05
                    self.light_intensity = max(0.0, min(self.light_intensity, 2.0))
                    self.setup_lights()
            self.render()
            clock.tick(60)
        pygame.quit()