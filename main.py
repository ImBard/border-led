import time
import socket
import pyautogui
from PIL import Image
import numpy as np
from collections import Counter

# Crie um objeto de soquete
s = socket.socket()

# Defina o endereço IP do seu NodeMCU e a porta que você deseja usar
host = '192.168.0.6'  # Endereço IP do NodeMCU
port = 3000            # Porta para se conectar

# Conecte-se ao NodeMCU
s.connect((host, port))

# Seu código para obter a cor da borda da tela
def capture_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

def dominant_color(image):
    # Redimensionando a imagem para acelerar o processamento
    resized_image = Image.fromarray(image).resize((50, 50), resample=Image.BILINEAR)

    # Redimensionando para uma lista de pixels
    pixels = np.array(resized_image).reshape(-1, 3)

    # Usando o Counter para encontrar a cor mais comum
    most_common_color = Counter(map(tuple, pixels)).most_common(1)[0][0]

    return most_common_color

def get_border_color():
    # Obtendo a largura e altura da tela
    screen_width, screen_height = pyautogui.size()

    # Definindo a faixa de largura de 200px
    strip_width = 200

    # Capturando a faixa da borda esquerda
    left_region = (0, 0, strip_width, screen_height)
    left_strip = capture_screen(left_region)

    # Capturando a faixa da borda direita
    right_region = (screen_width - strip_width, 0, screen_width, screen_height)
    right_strip = capture_screen(right_region)

    # Calculando a cor dominante para a faixa esquerda
    left_dominant_color = dominant_color(left_strip)

    # Calculando a cor dominante para a faixa direita
    right_dominant_color = dominant_color(right_strip)

    return left_dominant_color, right_dominant_color

if __name__ == "__main__":
    while True:
        # Crie um objeto de soquete
        s = socket.socket()

        # Conecte-se ao NodeMCU
        s.connect((host, port))

        left_color, right_color = get_border_color()
        print("Cor dominante da faixa esquerda:", left_color)
        print("Cor dominante da faixa direita:", right_color)

        # Converta as cores para uma string no formato 'R,G,B'
        left_color_str = ','.join(map(str, left_color))
        right_color_str = ','.join(map(str, right_color))

        # Envie as cores para o NodeMCU
        s.send((left_color_str + ';' + right_color_str + '\n').encode())

        # Feche a conexão
        s.close()

        # Aguarde um pouco antes de enviar o próximo conjunto de cores
        # time.sleep(1)
# Feche a conexão
s.close()
