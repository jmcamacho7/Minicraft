import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
from numpy import abs

app = Ursina()

textura_tierra = load_texture('assets/tierra.jpg')
textura_piedra = load_texture('assets/piedra.jpg')
textura_madera = load_texture('assets/madera.png')
textura_lana = load_texture('assets/lana.png')
textura_cielo = load_texture('assets/cielo.jpg')
textura_bedrock = load_texture('assets/bedrock.png')
textura_zombie = load_texture('assets/mobs/zombie/zombie.png')

bloque = 1


def update():
    global bloque, posicionxA, posicionzA
    if held_keys['1']: bloque = 1
    if held_keys['2']: bloque = 2
    if held_keys['3']: bloque = 3
    if held_keys['4']: bloque = 4
    if held_keys['control']:
        player.speed = 7
    if      abs(player.z - posicionzA) > 1 or \
            abs(player.x - posicionxA) > 1:
        generarShell()

class Bedrock(Entity):
    def __init__(self, position=(0,0,0), texture = textura_bedrock):
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


chunkSize = 25

semilla = random.randrange(1,1000000000)

noise = PerlinNoise(octaves=1, seed=semilla)
amp = random.randrange(3,10)
freq = random.randrange(3,30)


terreno = Entity(model=None, collider=None)
terrenowidth= 10
subwidth= terrenowidth
subsets = []
subCubo = []

for i in range(subwidth):
    bud = Entity(model='cube')

#for a in range(chunkSize*chunkSize):
    # bud = Entity(model='cube')
    # bud.x = floor(a/chunkSize)
    # bud.z = floor(a%chunkSize)
    # bud.y = floor((noise([bud.x/freq,bud.z/freq]))*amp)
    # bud.parent = terreno

# terreno.combine()
# terreno.collider = 'mesh'
# terreno.texture= textura_tierra

shell = []
shellWidth = 20

for i in range(shellWidth*shellWidth):
    blok = Entity(model='cube',
                  collider='box',
                  texture=textura_tierra,
                  shader=basic_lighting_shader,
                  highlight_color = color.gray,
                  )

    shell.append(blok)


def generarShell():
    global shellWidth, amp, freq
    for i in range(len(shell)):
        x = shell[i].x =  floor((i/shellWidth) + player.x - 0.5*shellWidth)
        z = shell[i].z = floor((i%shellWidth) + player.z - 0.5*shellWidth)
        y = shell[i].y = floor((noise([x/freq,z/freq]))*amp)


window.show_ursina_splash=True

def input(key):
  if key == "escape":
    quit()

scene.fog_color = color.rgb(0,200,211)
scene.fog_density = 0.02

player = FirstPersonController()
player.x = chunkSize/2
player.z= chunkSize/2
player.gravity= 0.5
posicionzA= player.z
posicionxA= player.x

cielo = Cielo()
generarShell()



app.run()