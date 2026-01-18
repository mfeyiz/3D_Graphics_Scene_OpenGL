from OpenGL.GL import * 
from OpenGL.GLU import * 
from pygame.math import Vector3 
class GraphicsUtils:
    ROOM_SIZE = 8.0  

    @staticmethod 
    def set_material(material_type):
        if material_type == 'polished_metal':
            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))  # mat kırmızı
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))  # difüs oranı arttı
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.9, 0.9, 0.9, 1.0))
            glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

        elif material_type == 'rough_plastic':
            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))  # yeşil 
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.2, 0.2, 0.2, 1.0))  # yansımasz
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
            glMaterialf(GL_FRONT, GL_SHININESS, 5.0)

        elif material_type == 'reflective_glass':
            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.05, 0.05, 0.05, 0.7))  # Mavi 
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.1, 0.1, 0.1, 0.7))  # az yansıma
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.1, 0.1, 0.1, 0.7))  # az yansıma 
            glMaterialf(GL_FRONT, GL_SHININESS, 70.0)  # mat cam olsun

        elif material_type == 'brushed_metal':
            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))  # matlık ve renk
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.3, 0.1, 0.1, 1.0))  # az
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0))  # daha mat
            glMaterialf(GL_FRONT, GL_SHININESS, 5.0)  # mat parlama için

        elif material_type == 'mat_material':
            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))  # Ortam ışığı
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))  # Yayılan ışık
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0)) # Yansıma sıfır
            glMaterialf(GL_FRONT, GL_SHININESS, 0.0)  # Parlaklık sıfır
    @staticmethod
    def draw_room():
            room_size = GraphicsUtils.ROOM_SIZE
            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.02, 0.02, 0.02, 1.0))
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.07, 0.07, 0.07, 1.0))
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
            glMaterialf(GL_FRONT, GL_SHININESS, 1.0)

            glColor3f(0.2, 0.2, 0.2)

            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0)
            glVertex3f(-room_size, 0, -room_size)
            glVertex3f(room_size, 0, -room_size)
            glVertex3f(room_size, 0, room_size)
            glVertex3f(-room_size, 0, room_size)
            glEnd()


            glBegin(GL_QUADS)
            glNormal3f(0, -1, 0)  
            glVertex3f(-room_size, room_size, -room_size)
            glVertex3f(room_size, room_size, -room_size)
            glVertex3f(room_size, room_size, room_size)
            glVertex3f(-room_size, room_size, room_size)
            glEnd()
            
            glColor3f(0.2, 0.2, 0.2)

            glBegin(GL_QUADS)

            glNormal3f(0, 0, 1)
            glVertex3f(-room_size, 0, -room_size)
            glVertex3f(room_size, 0, -room_size)
            glVertex3f(room_size, room_size, -room_size)
            glVertex3f(-room_size, room_size, -room_size)

            glNormal3f(-1, 0, 0)
            glVertex3f(room_size, 0, -room_size)
            glVertex3f(room_size, 0, room_size)
            glVertex3f(room_size, room_size, room_size)
            glVertex3f(room_size, room_size, -room_size)

            glNormal3f(1, 0, 0)
            glVertex3f(-room_size, 0, -room_size)
            glVertex3f(-room_size, 0, room_size)
            glVertex3f(-room_size, room_size, room_size)
            glVertex3f(-room_size, room_size, -room_size)
           
            glNormal3f(0, 0, -1)
            glVertex3f(-room_size, 0, room_size)
            glVertex3f(room_size, 0, room_size)
            glVertex3f(room_size, room_size, room_size)
            glVertex3f(-room_size, room_size, room_size)


            glEnd()


    @staticmethod
    def draw_sphere(size=1):
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, size, 64, 64)

    @staticmethod
    def draw_cube(size=1):
            vertices = [
                ((-size, -size, size), (size, -size, size), (size, size, size), (-size, size, size)),
                ((-size, -size, -size), (-size, size, -size), (size, size, -size), (size, -size, -size)),
                ((-size, size, -size), (-size, size, size), (size, size, size), (size, size, -size)),
                ((-size, -size, -size), (size, -size, -size), (size, -size, size), (-size, -size, size)),
                ((size, -size, -size), (size, size, -size), (size, size, size), (size, -size, size)),
                ((-size, -size, -size), (-size, -size, size), (-size, size, size), (-size, size, -size))
            ]
            normals = [
                (0, 0, 1), (0, 0, -1), (0, 1, 0),
                (0, -1, 0), (1, 0, 0), (-1, 0, 0)
            ]
            glBegin(GL_QUADS)
            for normal, face in zip(normals, vertices):
                glNormal3fv(normal)
                for vertex in face:
                    glVertex3f(*vertex)
            glEnd()

    @staticmethod
    def draw_pyramid(size=1):
        vertices = [
                ((0, size, 0), (-size, -size, size), (size, -size, size)),
                ((0, size, 0), (size, -size, size), (size, -size, -size)),
                ((0, size, 0), (size, -size, -size), (-size, -size, -size)),
                ((0, size, 0), (-size, -size, -size), (-size, -size, size)),
        ]
        normals = [
                Vector3(0, -1, 0),
                Vector3(0, 1, 1).normalize(),
                Vector3(1, 1, 0).normalize(),
                Vector3(0, 1, -1).normalize(),
                Vector3(-1, 1, 0).normalize(),
        ]
        glBegin(GL_TRIANGLES)
        for i in range(1, 5):
                normal = normals[i]
                glNormal3fv(tuple(normal))
                glVertex3f(*vertices[i-1][0])
                glVertex3f(*vertices[i-1][1])
                glVertex3f(*vertices[i-1][2])
        glEnd()

        glBegin(GL_QUADS)
        glNormal3fv(tuple(normals[0]))
        glVertex3f(-size, -size, size)
        glVertex3f(size, -size, size)
        glVertex3f(size, -size, -size)
        glVertex3f(-size, -size, -size)
        glEnd()