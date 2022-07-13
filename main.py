import ursina.shader
from ursina import *

from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader

app = Ursina()

textura_tierra = load_texture('assets/tierra.jpg')
textura_cielo = load_texture('assets/cielo.jpg')

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = textura_tierra,
            color = color.rgb(255,255,255),
            highlight_color = color.lime,
            shader = basic_lighting_shader,
        )

    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position= self.position + mouse.normal)
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


player = FirstPersonController()

cielo = Cielo()

app.run()