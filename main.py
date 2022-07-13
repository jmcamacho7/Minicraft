import ursina.shader
from ursina import *

from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin import *
import random


app = Ursina()

textura_tierra = load_texture('assets/tierra.jpg')
textura_piedra = load_texture('assets/piedra.jpg')
textura_madera = load_texture('assets/madera.png')
textura_lana = load_texture('assets/lana.png')
textura_cielo = load_texture('assets/cielo.jpg')

bloque = 1
semilla = random.randrange(1,1000000000)
semillafinal = str(semilla)

def update():
    global bloque
    if held_keys['1']: bloque = 1
    if held_keys['2']: bloque = 2
    if held_keys['3']: bloque = 3
    if held_keys['4']: bloque = 4


class Voxel(Button):
    def __init__(self, position=(0,0,0), texture = textura_tierra):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = texture,
            color = color.rgb(255,255,255),
            highlight_color = color.gray,
            shader = basic_lighting_shader,
        )

    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                if bloque == 1: voxel = Voxel(position= self.position + mouse.normal, texture= textura_tierra)
                if bloque == 2: voxel = Voxel(position= self.position + mouse.normal, texture= textura_piedra)
                if bloque == 3: voxel = Voxel(position= self.position + mouse.normal, texture= textura_madera)
                if bloque == 4: voxel = Voxel(position= self.position + mouse.normal, texture= textura_lana)

            if key == "right mouse down":
                destroy(self)


class Cielo(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = textura_cielo,
            scale = 250,
			double_sided = True)

chunkSize = 40

for z in range(chunkSize):
    for x in range(chunkSize):
        voxel = Voxel(position=(x, 0, z))

def input(key):
  if key == "escape":
    quit()


player = FirstPersonController()

cielo = Cielo()

app.run()