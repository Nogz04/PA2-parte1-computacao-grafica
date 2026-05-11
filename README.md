# Projeto de Computação Gráfica - Cena 3D com OpenGL e Pygame

Este projeto consiste em uma cena 3D interativa desenvolvida em Python, utilizando OpenGL para renderização e Pygame para gerenciamento de janela e entradas. A cena inclui um chão de grama, paredes de tijolo e um totem de cubos com diferentes texturas, além de um sistema de câmera estilo FPS (First Person Shooter).

## Pré-View

<img width="783" height="587" alt="Captura de tela de 2026-05-10 17-47-40" src="https://github.com/user-attachments/assets/9d4a120e-7f79-4cae-9896-829e5f5f3578" />




## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado em sua máquina.

### 2. Clonar o Repositório
Abra o terminal (ou PowerShell) e execute:
```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd PA2-computacao-grafica-objetos
```

### 3. Criar Ambiente Virtual (Recomendado)
Para evitar conflitos de bibliotecas, crie um ambiente virtual:

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 4. Instalar Dependências
Com o ambiente virtual ativo, instale as bibliotecas necessárias:

**No Linux (Ubuntu/Debian):**
Antes de instalar via pip, instale as bibliotecas gráficas do sistema:
```bash
sudo apt update
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev libglu1-mesa-dev
```

**Em ambos os sistemas (após os pré-requisitos do Linux):**
```bash
pip install -r requirements.txt
```

### 5. Execução do Projeto

**No Linux:**
Devido à compatibilidade com drivers modernos (Wayland/X11), utilize o comando abaixo para garantir que o OpenGL carregue corretamente:
```bash
SDL_VIDEODRIVER=x11 python Aula11_opengl_textura_camera_iluminacao.py
```

**No Windows:**
Basta executar o comando padrão:
```powershell
python Aula11_opengl_textura_camera_iluminacao.py
```

---

## 🎮 Controles
*   **W / S**: Mover para frente / trás.
*   **A / D**: Mover para os lados (Strafe).
*   **Mouse**: Olhar ao redor.
*   **Q / E**: Girar a cena manualmente.
*   **R / F**: Inclinar a cena manualmente.
*   **ESC**: Fechar o programa.

## 🛠️ Tecnologias Utilizadas
*   **Python 3.14+**
*   **Pygame**: Janela e eventos.
*   **PyOpenGL**: Renderização 3D.
*   **Pillow (PIL)**: Processamento de texturas.

---

## 👤 Autor

Desenvolvido por **Matheus Nogueira** — UFN, Computação Gráfica, 05/2026
