import ctypes
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
import math


# Importação do módulo pywavefront para carregar e desenhar o modelo OBJ
#from pywavefront.visualization import draw  # agora encontrará GL_V3F corretamente




# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -5  # Câmera posicionada de frente para o cubo
yaw = 0                            # Ângulo de rotação horizontal (inicialmente olhando para Z positivo)
pitch = 0                              # Ângulo de rotação vertical
sensitivity = 0.02                        # Sensibilidade do mouse para rotação
rot_x, rot_y = 0, 0                       # Ângulos de rotação da câmera (x para inclinar, y para girar)


# =================================================================
# EXPLICAÇÃO TÉCNICA: YAW E PITCH
# O Yaw e o Pitch são ângulos de Euler que definem a direção do olhar.
# Para o OpenGL entender, precisamos converter esses ângulos em um 
# "Vetor de Direção" (x, y, z) usando trigonometria:
# - Seno e Cosseno do Pitch determinam a inclinação vertical.
# - Seno e Cosseno do Yaw determinam o giro horizontal.
# =================================================================



# Atualiza a direção de visão da câmera com base em yaw e pitch
def update_camera_direction():
    rad_yaw = math.radians(yaw) # Converte graus do Yaw para radianos (exigência do math.sin/cos)
    rad_pitch = math.radians(pitch) # Converte graus do Pitch para radianos
    
    # Cálculo das componentes do vetor de direção usando trigonometria esférica
    dir_x = math.cos(rad_pitch) * math.sin(rad_yaw) # Componente X da direção
    dir_y = math.sin(rad_pitch)                      # Componente Y da direção (altura do olhar)
    dir_z = math.cos(rad_pitch) * math.cos(rad_yaw) # Componente Z da direção (profundidade)
    return dir_x, dir_y, dir_z # Retorna o vetor unitário de direção

# Função que carrega imagem como textura
def load_texture(filename):
    img = Image.open(filename) # Abre o arquivo de imagem (ex: .jpg, .png)
    img = img.transpose(Image.FLIP_TOP_BOTTOM) # Inverte a imagem (OpenGL lê de baixo para cima)
    img_data = img.convert("RGBA").tobytes() # Converte a imagem em dados binários RGBA
    width, height = img.size # Pega as dimensões da imagem em pixels
    tex_id = glGenTextures(1) # Gera um ID único para esta textura no OpenGL
    glBindTexture(GL_TEXTURE_2D, tex_id) # Ativa essa textura para configuração
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data) # Envia os dados para a GPU
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Faz a textura repetir se as coordenadas forem > 1 no eixo S (X)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # Faz a textura repetir no eixo T (Y)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # Suaviza a textura quando vista de perto
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Suaviza a textura quando vista de longe
    return tex_id # Retorna o ID para usarmos no desenho

# Função que desenha um cubo com textura aplicada, face por face
def draw_textured_cube():
    glBegin(GL_QUADS)  # Inicia desenho de quadriláteros

    #Explicação:
    # glTexCoord2f(0, 0)
    #→ Indica a coordenada da textura (posição do pixel da imagem que será aplicada no vértice).
    #→ Neste caso, 0,0 representa o canto inferior esquerdo da imagem.
    #--------------------------------
    #glVertex3fv(cube_vertices[0])
    #→ Indica a posição do vértice no espaço 3D onde essa parte da textura será aplicada.

    # FACE TRASEIRA (fundo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3])  # superior esquerdo

    # FACE FRONTAL (frente do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # superior esquerdo

    # FACE INFERIOR (base)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[5])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # frontal esquerda

    # FACE SUPERIOR (tampa)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # frontal esquerda

    # FACE DIREITA (lado direito do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[5])  # inferior frontal

    # FACE ESQUERDA (lado esquerdo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[3])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # inferior frontal

    glEnd()  # Finaliza o desenho

# Função para desenhar um plano (chão ou parede) (Desafios 2 e 3)
def draw_textured_plane(size=10, tiles=5):
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0) # Normal virada para cima
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(tiles, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(tiles, tiles); glVertex3f(size, 0, size)
    glTexCoord2f(0, tiles); glVertex3f(-size, 0, size)
    glEnd()



# Lista de coordenadas 3D dos vértices do cubo
# Cada vértice é representado por uma tupla (x, y, z)
# Observação: o cubo tem 8 vértices no total
cube_vertices = [
    (-1, -1, -1),  # 0 - canto inferior esquerdo traseiro
    ( 1, -1, -1),  # 1 - canto inferior direito traseiro
    ( 1,  1, -1),  # 2 - canto superior direito traseiro
    (-1,  1, -1),  # 3 - canto superior esquerdo traseiro

    (-1, -1,  1),  # 4 - canto inferior esquerdo frontal
    ( 1, -1,  1),  # 5 - canto inferior direito frontal
    ( 1,  1,  1),  # 6 - canto superior direito frontal
    (-1,  1,  1)   # 7 - canto superior esquerdo frontal
]

# Índices que definem as 6 faces do cubo com 4 vértices cada
cube_faces = [
    (0, 1, 2, 3),  # Traseira
    (4, 5, 6, 7),  # Frontal
    (0, 1, 5, 4),  # Inferior
    (2, 3, 7, 6),  # Superior
    (1, 2, 6, 5),  # Lateral direita
    (0, 3, 7, 4)   # Lateral esquerda
]

# Coordenadas 2D da textura (mapeamento)
'''cube_texcoords = [
    (0, 0), # canto inferior esquerdo,
    (1, 0), # inferior direito,
    (1, 1), # superior direito,
    (0, 1)  # superior esquerdo
]'''




# Configura o OpenGL (textura, profundidade, iluminação)
def init_opengl(display):
    glEnable(GL_DEPTH_TEST) # Habilita o Z-Buffer (objetos na frente escondem os de trás)
    glEnable(GL_TEXTURE_2D) # Habilita o uso de imagens 2D sobre polígonos
    
    # Luz Ambiente personalizada (Desafio 4)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.4, 1.0)) # Tom azulado (luz fria/noturna)
    
    glEnable(GL_LIGHTING) # Liga o sistema de cálculos de iluminação
    glEnable(GL_LIGHT0) # Liga a primeira fonte de luz (Luz 0)
    
    # Posição e Propriedades da Luz (Desafio 5)
    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 10.0, 5.0, 1.0)) # Posição alta e lateral
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0)) # Luz branca direta
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0)) # Brilho reflexivo
    
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 80)
    glMatrixMode(GL_PROJECTION) # Muda para a matriz de projeção (lente da câmera)
    glLoadIdentity() # Limpa a matriz de projeção

    #gluPerspective(fov, aspect, near, far) define uma matriz de projeção em perspectiva, onde:
    #fov: Campo de visão vertical (em graus). Ex: 45 → visão razoavelmente aberta.
    #aspect: Proporção da tela (largura / altura).
    #near: Distância mínima visível (objetos mais próximos são cortados).
    #far: Distância máxima visível (objetos mais distantes são cortados).
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) #
    glMatrixMode(GL_MODELVIEW)

# Função principal do programa
def main():
    global camera_x, camera_y, camera_z, yaw, pitch, rot_x, rot_y # Declara uso das variáveis globais
    pygame.init() # Inicializa o motor do Pygame
    display = (800, 600) # Define resolução da janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # Cria janela com suporte a Buffer Duplo e OpenGL
    
    # DIAGNÓSTICO: Verificando se o OpenGL carregou corretamente
    print("--- DIAGNÓSTICO OPENGL ---")
    try:
        print(f"Vendor: {glGetString(GL_VENDOR).decode()}")
        print(f"Renderer: {glGetString(GL_RENDERER).decode()}")
        print(f"Version: {glGetString(GL_VERSION).decode()}")
    except Exception as e:
        print(f"Erro ao obter informações do OpenGL: {e}")
    print("--------------------------")

    pygame.event.set_grab(True) # Prende o mouse dentro da janela do jogo
    pygame.mouse.set_visible(False) # Esconde o cursor do mouse (estilo FPS)

    init_opengl(display) # Chama as configurações do OpenGL definidas acima

    # Carregamento das Texturas (Desafios 1, 2, 3 e 6)
    tex_cubo   = load_texture("texturas/textura-cubo1/Onyx015_4K-PNG_Color.png")
    tex_cubo2  = load_texture("texturas/textura-cubo2/Marble006_4K-PNG_Color.png")
    tex_cubo3  = load_texture("texturas/textura-cubo3/Tiles074_4K-PNG_Color.png")
    tex_grama  = load_texture("texturas/textura-chao-grama/Grass005_4K-PNG_Color.png")
    tex_tijolo = load_texture("texturas/textura-parede-tijolo/Bricks104_4K-PNG_Color.png")


    #configuração do relógio para limitar FPS
    clock = pygame.time.Clock() # Cria relógio para controlar os frames por segundo (FPS)
    running = True # Variável de controle do laço principal

    # Carregar objeto
    #objeto = Wavefront('modelo.obj', collect_faces=True)
    #objeto = Wavefront('OBJS/MercedezB/Mercedez.obj', collect_faces=True)


    while running:
        clock.tick(120) # Trava a execução em 60 frames por segundo

        for event in pygame.event.get(): # Verifica se o usuário interagiu (fechar, teclado, etc)
            if event.type == QUIT: # Se clicar no X da janela
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE: # Se apertar ESC
                running = False

        # ROTAÇÃO COM O MOUSE
        dx, dy = pygame.mouse.get_rel() # Pega o quanto o mouse moveu desde o último frame
        yaw -= dx * sensitivity     # Move o olhar para os lados (Yaw)
        pitch -= dy * sensitivity   # Move o olhar para cima/baixo (Pitch)

        # Atualiza o Vetor de Direção com base nos novos ângulos do mouse
        dir_x, dir_y, dir_z = update_camera_direction()

        keys = pygame.key.get_pressed() # Pega o estado atual de todas as teclas do teclado

        # MOVIMENTO COM TECLAS (Baseado na direção do olhar)
        if keys[K_w]: # Andar para frente
            camera_x += dir_x * 0.2
            camera_y += dir_y * 0.2
            camera_z += dir_z * 0.2
        if keys[K_s]: # Andar para trás
            camera_x -= dir_x * 0.2
            camera_y -= dir_y * 0.2
            camera_z -= dir_z * 0.2
        if keys[K_a]: # Passo lateral esquerda (Strafe)
            camera_x += dir_z * 0.2
            camera_z -= dir_x * 0.2
        if keys[K_d]: # Passo lateral direita (Strafe)
            camera_x -= dir_z * 0.2
            camera_z += dir_x * 0.2
        if keys[K_PAGEUP]: # Voar para cima
            camera_y += 0.2
        if keys[K_PAGEDOWN]: # Voar para baixo
            camera_y -= 0.2

        # Rotação manual da cena via teclado
        if keys[K_q]: rot_y -= 1 # Gira cena no eixo Y
        if keys[K_e]: rot_y += 1 # Gira cena no eixo Y
        if keys[K_r]: rot_x -= 1 # Inclina cena no eixo X
        if keys[K_f]: rot_x += 1 # Inclina cena no eixo X

        # =================================================================
        # EXPLICAÇÃO TÉCNICA: gluLookAt
        # Esta é a função que "posiciona a câmera" no mundo.
        # Parâmetros: 
        # 1. Posição (camera_x, y, z): Onde seu "olho" está.
        # 2. Alvo (camera+direcao): Para qual ponto você está olhando.
        # 3. Up (0, 1, 0): Indica que o topo da sua cabeça aponta para o eixo Y.
        # =================================================================
        
        glLoadIdentity() # Limpa a matriz antes de aplicar a visão da câmera
        gluLookAt(camera_x, camera_y, camera_z,
                  camera_x + dir_x, camera_y + dir_y, camera_z + dir_z,
                  0, 1, 0)

        # Aplica rotações extras vindas do teclado (Q, E, R, F)
        glRotatef(rot_x, 1, 0, 0) # Rotação vertical da cena
        glRotatef(rot_y, 0, 1, 0) # Rotação horizontal da cena

        # Limpa a tela e o buffer de profundidade para desenhar o novo frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 1. DESENHO DO CHÃO (Desafio 2)
        glBindTexture(GL_TEXTURE_2D, tex_grama)
        glPushMatrix()
        glTranslatef(0, -1.0, 0) # Posiciona o chão levemente abaixo da origem
        draw_textured_plane(size=20, tiles=10) # Desenha um plano grande
        glPopMatrix()

        # 2. DESENHO DAS PAREDES (Desafio 3 e 7)
        glBindTexture(GL_TEXTURE_2D, tex_tijolo)
        # Parede de Fundo
        glPushMatrix()
        glTranslatef(0, 4, -10)
        glRotatef(90, 1, 0, 0) # Rotaciona para ficar vertical
        draw_textured_plane(size=10, tiles=4)
        glPopMatrix()
        # Parede Lateral
        glPushMatrix()
        glTranslatef(-10, 4, 0)
        glRotatef(90, 0, 0, 1) # Rotaciona para o lado
        draw_textured_plane(size=10, tiles=4)
        glPopMatrix()

        # 3. DESENHO DO TOTEM DE CUBOS (Desafio 6)
        totem_textures = [tex_cubo, tex_cubo2, tex_cubo3]
        for i in range(3):
            glBindTexture(GL_TEXTURE_2D, totem_textures[i]) # Cada cubo com sua textura
            glPushMatrix()
            glTranslatef(0, i * 2, 0) # Empilha um em cima do outro (y=0, 2, 4)
            draw_textured_cube()
            glPopMatrix()

        # 4. DESENHO DO SEGUNDO CUBO (Desafio 1)
        glBindTexture(GL_TEXTURE_2D, tex_tijolo) # Usando textura de tijolo para diferenciar
        glPushMatrix()
        glTranslatef(4, 0, -2) # Posicionado ao lado do totem
        glRotatef(45, 0, 1, 0) # Uma leve rotação para estilo
        draw_textured_cube()
        glPopMatrix()
        

        # PRINTS DE DEPURAÇÃO REMOVIDOS PARA MELHORAR PERFORMANCE
        '''
        print("\n")
        print("yaw:", yaw, "pitch:", pitch, "camera:", (camera_x, camera_y, camera_z)  )
        print("\n")
        print("dir:", (dir_x, dir_y, dir_z))
        print("\n")
        '''
        
        pygame.display.flip() # Troca os buffers (exibe o que foi desenhado na tela)

    pygame.quit() # Encerra o Pygame ao sair do laço

# Ponto de entrada do script
if __name__ == "__main__":
    main()