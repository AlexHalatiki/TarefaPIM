import cv2
import numpy as np
from skimage import io, color

def equalizaMatriz(matriz):
    histograma, intervalos = np.histogram(matriz, bins=8, range=(0, 255))
    histograma = histograma / matriz.size

    roundgk = []

    for i in range(0,8):
        if i != 0:
            histograma[i] += histograma[i-1]
        roundgk.append(round(histograma[i] * 7))

    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            indice_intervalo = np.digitize(matriz[i][j], intervalos)

            if(indice_intervalo > 8):
                indice_intervalo = 8

            novo_intervalo = roundgk[indice_intervalo - 1] + 1

            minimo_intervalo = intervalos[indice_intervalo - 1]
            maximo_intervalo = intervalos[indice_intervalo]

            minimo_novo_intervalo = intervalos[novo_intervalo - 1]
            maximo_novo_intervalo = intervalos[novo_intervalo]

            matriz[i][j] = minimo_novo_intervalo + ((matriz[i][j] - minimo_intervalo) / (maximo_intervalo - minimo_intervalo)) * (maximo_novo_intervalo - minimo_novo_intervalo)

def equalizaImagemRGB(caminho, nome, formato):
    img = cv2.imread(caminho)

    blue = img[:, :, 0]
    green = img[:, :, 1]
    red = img[:, :, 2]

    equalizaMatriz(blue)
    equalizaMatriz(green)
    equalizaMatriz(red)

    imagem_equalizada = cv2.merge([blue, green, red])

    cv2.imwrite(f'./ex3/rgb_equalizadas/{nome}_equalizada.{formato}', imagem_equalizada)

def equalizaImagemYIQ(caminho, nome, formato):
    img = io.imread(caminho)

    img_yiq = color.rgb2yiq(img)

    img_yiq = img_yiq - img_yiq.min()
    img_yiq = img_yiq * 255 / img_yiq.max()
    img_yiq = np.uint8(img_yiq)

    y = img_yiq[:, :, 0]

    equalizaMatriz(y)

    img_yiq[:, :, 0] = y

    img_rgb = color.yiq2rgb(img_yiq)
   
    img_rgb = img_rgb - img_rgb.min()
    img_rgb = img_rgb * 255 / img_rgb.max()
    img_rgb = np.uint8(img_rgb)

    io.imsave(f'./ex3/yiq_equalizadas/{nome}_equalizada.{formato}', img_rgb)


equalizaImagemRGB('./imagens/outono_LC.png', 'outono_equalizada', 'png')
equalizaImagemRGB('./imagens/predios.jpeg', 'predios_equalizada', 'jpeg')
equalizaImagemYIQ('./imagens/outono_LC.png', 'outono_equalizada', 'png')
equalizaImagemYIQ('./imagens/predios.jpeg', 'predios_equalizada', 'jpeg')