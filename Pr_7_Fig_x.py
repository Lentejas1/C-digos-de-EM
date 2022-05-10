import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np


# IMPORTANTE: hay que importar en la consola el paquete SciencePlots para usar el estilo de gráficos adecuado.
plt.style.use('science')


def run(bx=None, by=None, bz=None):
    coil = magpy.Collection()  # Crea la colección de espiras (bobina)

    current = 1     # Intensidad eléctrica en A
    loops = 300     # Número de espiras
    diametre = 33   # Diámetro de las espiras en mm
    distance = 0.1  # Distancia entre espiras en mm

    for i in range(loops): # Posiciona cada una de las espiras
        espira = magpy.current.Circular(current=current, diameter=diametre, position=(0, 0, i * distance))
        coil.add(espira)

    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(121, projection='3d')
    coil.display(markers=[(0, 0, 0)], axis=ax1)

    ax2 = fig.add_subplot(122, )
    ts = np.linspace(-distance * loops * 1.5, distance * loops * 2, 50)
    grid = np.array([[(x, 0, z) for x in ts] for z in ts])
    B = magpy.getB(coil, grid)

    amp = np.linalg.norm(B, axis=2)
    strm = ax2.streamplot(grid[:, :, 0], grid[:, :, 2], B[:, :, 0], B[:, :, 2], density=2, color=np.log(amp),
                          linewidth=1, cmap='autumn')
    cb = fig.colorbar(strm.lines)
    cb.set_label(r"$\vec{B}$ [mT]")

    ax2.set_xlabel("$x$ [mm]")
    ax2.set_ylabel("$z$ [mm]")

    plt.show()

    if bx is not None:
        if by is not None:
            if bz is not None:
                print(f"B = {magpy.getB(sources=coil, observers=(bx, by, bz))} mT")


run(0, 0, 0)  # Insertar tres variables (coordenadas) en caso de querer calcular el campo B en cierto punto
