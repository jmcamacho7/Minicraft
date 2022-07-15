import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
from numpy import abs
import time

app = Ursina()

textura_tierra = load_texture('assets/tierra.jpg')
textura_piedra = load_texture('assets/piedra.jpg')
textura_madera = load_texture('assets/madera.png')
textura_lana = load_texture('assets/lana.png')
textura_cielo = load_texture('assets/cielo.jpg')
textura_bedrock = load_texture('assets/bedrock.png')
textura_zombie = load_texture('assets/mobs/zombie/zombie.png')

bloque = 1
prevTime= time.time()

def update():
    global bloque, posicionxA, posicionzA, prevTime
    if held_keys['1']: bloque = 1
    if held_keys['2']: bloque = 2
    if held_keys['3']: bloque = 3
    if held_keys['4']: bloque = 4
    if      abs(player.z - posicionzA) > 1 or \
            abs(player.x - posicionxA) > 1:
        generarShell()
    if time.time() - prevTime > 0.4:
        generarSubset()

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

semilla = 280000

noise = PerlinNoise(octaves=1, seed=semilla)
amp = 64
freq = 100


terreno = Entity(model=None, collider=None)
terrenowidth= 100
subwidth= terrenowidth
subsets = []
subCubo = []

sci = 0
subsetActual = 0


for i in range(subwidth):
    bud = Entity(model='cube')
    subCubo.append(bud)

for i in range(int((terrenowidth*terrenowidth)/subwidth)):
    bud = Entity(model=None)
    bud.parent = terreno
    subsets.append(bud)

def generarSubset():
    global sci, subsetActual, noise, freq, amp
    if subsetActual >= len(subsets):
        terminarTerreno()
        return
    for i in range(subwidth):
        x = subCubo[i].x = floor((i + sci)/subwidth)
        z = subCubo[i].z = floor((i + sci)%subwidth)
        y = subCubo[i].y = floor((noise([x/freq,z/freq]))*amp)

        subCubo[i].parent = subsets[subsetActual]
        subCubo[i].visible = False


    subsets[subsetActual].combine(auto_destroy=False)
    subsets[subsetActual].texture = textura_tierra
    sci += subwidth
    subsetActual += 1

terrenoAcabado = False

def terminarTerreno():
    global terrenoAcabado
    if terrenoAcabado == True: return
    application.pause()
    terreno.combine()
    player.y = 32
    terreno.texture= textura_tierra
    application.resume


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
    bud = Entity(model='cube',
                  collider='box',
                  shader=basic_lighting_shader,
                  )
    bud.visible = False

    shell.append(bud)


def generarShell():
    global shellWidth, amp, freq
    for i in range(len(shell)):
        x = shell[i].x =  floor((i/shellWidth) + player.x - 0.5*shellWidth)
        z = shell[i].z = floor((i%shellWidth) + player.z - 0.5*shellWidth)
        y = shell[i].y = floor((noise([x/freq,z/freq]))*amp)


window.show_ursina_splash=True

def input(key):

    if key == 'control':
        player.speed = 7

    if key == "escape":
        quit()

    if key == "g":
        generarSubset()

scene.fog_color = color.rgb(250,250,250)
scene.fog_density = 0.01

player = FirstPersonController()
player.x = chunkSize/2
player.z= chunkSize/2
player.gravity= 0.5
posicionzA= player.z
posicionxA= player.x

cielo = Cielo()
generarShell()




app.run()