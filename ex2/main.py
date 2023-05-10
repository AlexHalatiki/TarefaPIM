import numpy as np
from skimage import io, color

def equalizaImagem(caminho, nome, formato):
    imagem = io.imread(caminho)

    histograma, intervalos = np.histogram(imagem, bins=8, range=(0, 255))
    histograma = histograma / imagem.size

    roundgk = []

    for i in range(0,8):
        if i != 0:
            histograma[i] += histograma[i-1]
        roundgk.append(round(histograma[i] * 7))

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            indice_intervalo = np.digitize(imagem[i][j], intervalos)

            if(indice_intervalo > 8):
                indice_intervalo = 8

            novo_intervalo = roundgk[indice_intervalo - 1] + 1

            minimo_intervalo = intervalos[indice_intervalo - 1]
            maximo_intervalo = intervalos[indice_intervalo]

            minimo_novo_intervalo = intervalos[novo_intervalo - 1]
            maximo_novo_intervalo = intervalos[novo_intervalo]

            imagem[i][j] = minimo_novo_intervalo + ((imagem[i][j] - minimo_intervalo) / (maximo_intervalo - minimo_intervalo)) * (maximo_novo_intervalo - minimo_novo_intervalo)

    io.imsave(f'./ex2/imagens_equalizadas/{nome}_equalizada.{formato}', imagem)

    print(f'{nome}:')
    print(histograma)
    print(roundgk)
    print(imagem)
    print()

#equalizaImagem('./imagens/xadrez_lowCont.png', 'xadrezLowCont', 'png')
equalizaImagem('./imagens/marilyn.jpg', 'marilyn', 'jpg')
equalizaImagem('./imagens/figuraEscura.jpg', 'figuraEscura', 'jpg')
equalizaImagem('./imagens/figuraClara.jpg', 'figuraClara', 'jpg')