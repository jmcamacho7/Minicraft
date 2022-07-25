import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
from nMap import nMap
from numpy import *
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

musica = []
halland = Audio(
    'assets/Halland.mp3',
    autoplay=False,
    loop=False,
)
wet = Audio(
    'assets/wet.mp3',
    autoplay=False,
    loop=False
)
sweden = Audio(
    'assets/sweden.mp3',
    autoplay=False,
    loop=False
)
musica.append(halland)
musica.append(wet)
musica.append(sweden)


def musicplayer ():
    nombre = random.choice(musica)
    nombre.play()

musicplayer()

class Cielo(Entity):
    def __init__(self):
	    super().__init__(
		    parent = scene,
			model = 'sphere',
			texture = textura_cielo,
            scale = 250,
			double_sided = True)

bloque = 1
prevTime= time.time()

objeto = Entity(model='cube',texture=textura_frame, shader=basic_lighting_shader)


class OTIPO:
    PIEDRA = objeto.texture = textura_piedra
    LANA = objeto.texture = textura_lana
    TIERRA = objeto.texture = textura_tierra
    MADERA = objeto.texture = textura_madera


modoConstruccion = -1

def seleccion():
    if bloque == 1:
        objeto.texture = OTIPO.TIERRA

    if bloque == 2:
        objeto.texture = OTIPO.PIEDRA

    if bloque == 3:
        objeto.texture = OTIPO.MADERA

    if bloque == 4:
        objeto.texture = OTIPO.LANA

def herramientaConstruir():
    if modoConstruccion  == -1:
        objeto.visible = False
        return

    else: objeto.visible = True
    objeto.position = round(player.position +
                         camera.forward * 3)
    objeto.y += 2
    objeto.y = round(objeto.y)
    objeto.x = round(objeto.x)
    objeto.z = round(objeto.z)

def construir():
    seleccion()
    c = duplicate(objeto)
    c.collider = 'cube'
    c.shake(duration=0.2, speed=0.01)



def input(key):
    global tipoBloque, modoConstruccion, generar, puedeGenerar
    if key == "escape":
        quit()

    if key == 'g':
        generar *= 1
        puedeGenerar *= 1

    if key == 'left mouse up':
        construir()
        objeto.texture=textura_frame

    elif key == 'right mouse up':
        x = mouse.hovered_entity
        destroy(x)

    if key == 'f' :
        if modoConstruccion == 1:
            modoConstruccion = -1
        else:
            modoConstruccion = 1,
            objeto.texture = textura_frame


def update():
    global bloque, posicionxA, posicionzA, prevTime, rad, origen, generar, puedeGenerar

    if held_keys['control']: player.speed = 7
    else: player.speed = 4


    if abs(player.z - posicionzA) > 1 or \
        abs(player.x - posicionxA) > 1:

            origen=player.position
            rad=0
            theta=0
            generar = 1 * puedeGenerar
            posicionzA = player.z
            posicionxA = player.x

    generarShell()

    if time.time() - prevTime > velocidadGen:
        for x in range(porCiclo):
            generarTerreno()
        prevTime = time.time()

    if held_keys['1']: bloque = 1
    if held_keys['2']: bloque = 2
    if held_keys['3']: bloque = 3
    if held_keys['4']: bloque = 4

    herramientaConstruir()



semilla = random.choice(range(99,2000000))
noise = PerlinNoise(octaves=1, seed=semilla)

megasets = []
generar = 1
puedeGenerar = 1
velocidadGen = 0
porCiclo = 16
cuboActual = 0
subsetActual = 0
numSubcubo = 16
numSubsets = 420
theta = 0
rad = 0



subDic = {}

terreno = Entity(model=None, collider=None)

chunkSize = 100
subwidth= chunkSize
subsets = []
subCubo = []

sci = 0
subsetActual = 0


for x in range(numSubcubo):
    bud = Entity(model='cube', texture= textura_bedrock)
    bud.rotation_y = random.randint(1,4)*90
    bud.disable()
    subCubo.append(bud)

for x in range(numSubsets):
    bud = Entity(model='cube')
    bud.texture = textura_bedrock
    bud.disable()
    subsets.append(bud)

def perlinGen(_x, _z):
    y = 0
    freq = 64
    amp = 42
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 32
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)
    return floor(y)

def generarTerreno():
    global cuboActual, theta, rad, subsetActual
    global generar

    if generar == -1: return

    # Decide where to place new terrain cube!
    x = floor(origen.x + sin(radians(theta)) * rad)
    z = floor(origen.z + cos(radians(theta)) * rad)
    # Check whether there is terrain here already...
    if subDic.get('x' + str(x) + 'z' + str(z)) != 'i':
        subCubo[cuboActual].enable()
        subCubo[cuboActual].x = x
        subCubo[cuboActual].z = z
        subDic['x' + str(x) + 'z' + str(z)] = 'i'
        subCubo[cuboActual].parent = subsets[subsetActual]
        y = subCubo[cuboActual].y = perlinGen(x, z)
        g = nMap(y, -8, 21, 12, 243)
        g += random.randint(-12,12)
        subCubo[cuboActual].disable()
        cuboActual += 1

        if cuboActual == numSubcubo:
            subsets[subsetActual].combine(auto_destroy=False)
            subsets[subsetActual].enable()
            subsetActual += 1
            cuboActual = 0

            if subsetActual == numSubsets:
                megasets.append(Entity(texture=textura_bedrock))
                for x in subsets:
                    x.parent = megasets[-1]
                megasets[-1].combine(auto_destroy = False)

                for x in subsets:
                    x.parent = scene
                subsetActual=0
                print('Megaset #' +  str(len(megasets))+'!')

    else:
        pass

    if rad > 0:
        theta += 45 / rad
    else:
        rad += 0.5

    if theta >= 360:
        theta = 0
        rad += 0.5


shell = []
shellWidth = 3

for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',
                  collider='box',

                  )
    bud.visible = False
    shell.append(bud)


def generarShell():
    global shellWidth
    for i in range(len(shell)):
        x = shell[i].x =  floor((i/shellWidth) +
                                player.x - 0.5*shellWidth)
        z = shell[i].z = floor((i%shellWidth) +
                               player.z - 0.5*shellWidth)
        shell[i].y = perlinGen(x,z)




scene.fog_color = color.rgb(250,250,250)
scene.fog_density = 0.01

player = FirstPersonController()
player.x = chunkSize/2
player.z= chunkSize/2
player.gravity= 0.5
posicionzA= player.z
posicionxA= player.x
origen = player.position

construir()

cielo = Cielo()
generarShell()




app.run()