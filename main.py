import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
from nMap import nMap
import time

app = Ursina()

textura_tierra = load_texture('assets/tierra.jpg')
textura_piedra = load_texture('assets/piedra.jpg')
textura_madera = load_texture('assets/madera.png')
textura_lana = load_texture('assets/lana.png')
textura_cielo = load_texture('assets/cielo.jpg')
textura_bedrock = load_texture('assets/bedrock.png')
textura_zombie = load_texture('assets/mobs/zombie/zombie.png')
textura_frame = load_texture('assets/wireframe.png')

musica = Audio(
    'assets/Halland.mp3',
    autoplay=True,
    loop=True,
)

bloque = 1
prevTime= time.time()

bte = Entity(model='cube',texture=textura_frame)



def herramientaConstruir():

    bte.position = round(player.position +
                         camera.forward * 3)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)

def construir():
    c = duplicate(bte)
    c.collider = 'cube'

    if bloque == 1:
        c.texture = textura_piedra

    if bloque == 2:
        c.texture = textura_madera

    if bloque == 3:
        c.texture = textura_tierra

    if bloque == 4:
        c.texture = textura_lana

    c.shake(duration=0.5, speed=0.01)

def input(key):

    if key == 'control':
        player.speed = 7

    if key == "escape":
        quit()

    if key == 'left mouse up':
        construir()

    elif key == 'right mouse up':
        x = mouse.hovered_entity
        destroy(x)


def update():
    global bloque, posicionxA, posicionzA, prevTime
    if held_keys['1']: bloque = 1
    if held_keys['2']: bloque = 2
    if held_keys['3']: bloque = 3
    if held_keys['4']: bloque = 4
    if abs(player.z - posicionzA) > 1 or \
            abs(player.x - posicionxA) > 1:
        generarShell()
    if time.time() - prevTime > 0.05:
        generarSubset()
        prevTime = time.time()

    if player.y < -amp + 1:
        player.y = 2 + floor((noise([player.x / freq,
                                     player.z / freq])) * amp)
        player.land()

    herramientaConstruir()

class Cielo(Entity):
    def __init__(self):
	    super().__init__(
		    parent = scene,
			model = 'sphere',
			texture = textura_cielo,
            scale = 250,
			double_sided = True)


semilla = random.randrange(1000, 2000000)

noise = PerlinNoise(octaves=1, seed=semilla)
amp = random.randrange(20,70)
freq = random.randrange(70, 100)


terreno = Entity(model=None, collider=None)
chunkSize = 100
subwidth= chunkSize
subsets = []
subCubo = []

sci = 0
subsetActual = 0


for i in range(subwidth):
    bud = Entity(model='cube')
    subCubo.append(bud)

for i in range(int((chunkSize*chunkSize)/subwidth)):
    bud = Entity(model=None)
    bud.parent = terreno
    subsets.append(bud)

def generarSubset():
    global sci, subsetActual, noise, freq, amp
    if subsetActual >= len(subsets):
        terminarTerreno()
        return
    for i in range(subwidth):
        x = subCubo[i].x = floor((i + sci)/chunkSize)
        z = subCubo[i].z = floor((i + sci)%chunkSize)
        y = subCubo[i].y = floor((noise([x/freq,z/freq]))*amp)

        subCubo[i].parent = subsets[subsetActual]
        subCubo[i].visible = False

    y += random.randrange(-4,4)
    r = 0
    g = 0
    b = 0
    if y > amp * 0.3:
        b = 255
    if y == 4:
        r = g = b = 255
    else:
        g = nMap(y, 0, amp * 0.5, 0, 255)
    subCubo[i].color = color.rgb(r, g, b)
    subCubo[i].visible = False

    subsets[subsetActual].combine(auto_destroy=False)
    sci += subwidth
    subsetActual += 1


terrenoAcabado = False

def terminarTerreno():
    global terrenoAcabado
    if terrenoAcabado == True: return
    terreno.combine()
    terrenoAcabado = True
    terreno.texture = textura_bedrock






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
shellWidth = 3

for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',
                  collider='box',
                  )
    bud.visible = False
    shell.append(bud)


def generarShell():
    global shellWidth, amp, freq
    for i in range(len(shell)):
        x = shell[i].x =  floor((i/shellWidth) +
                                player.x - 0.5*shellWidth)
        z = shell[i].z = floor((i%shellWidth) +
                               player.z - 0.5*shellWidth)
        y = shell[i].y = floor((noise([x/freq,z/freq]))*amp)




scene.fog_color = color.rgb(250,250,250)
scene.fog_density = 0.01

player = FirstPersonController()
player.x = chunkSize/2
player.z= chunkSize/2
player.gravity= 0.5
posicionzA= player.z
posicionxA= player.x

construir()

cielo = Cielo()
generarShell()




app.run()