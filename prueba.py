for i in range(int((chunkSize*chunkSize)/subwidth)):
    bud = Entity(model=None)
    bud.parent = terreno
    subsets.append(bud)

def generarSubset():
    global sci, subsetActual, noise, freq, amp, chunkSize
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

    if z > chunkSize * 0.5:
        g = 0
        b = 0
        r = nMap(y, 0, amp, 110, 255)

    subCubo[i].color = color.rgb(r, g, b)
    subCubo[i].visible = False

    subsets[subsetActual].combine(auto_destroy=False)
    sci += subwidth
    subsetActual += 1