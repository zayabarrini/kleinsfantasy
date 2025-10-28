# Tipos de animações

- Blender, Maya, Houdini, Cinema4D: modeling, texturing, shading, animation, VFX - use scripting
- Create an game using Ursina or Godot
- Do it using Unity
- Do it as a 2D animation using OpenToonz

# Projeto: Criar uma Garrafa de Klein do vídeo do Dunker

- Seções: Cortar a garrafa, duplicar, move suas partes, colorir, deformar, rotacionar, ondular. Software 3D: Blender ou outro
- Aplicar texturas diferentes na garrafa, separar alça, buraco, centro, produzir leve protuberância vermelha como na garrafa do Dunker
- Aplicar sombra/cobertura sobre a garrafa, textura com escritos chineses, estofado: recobrimento com a fantasia
- Animação: aumentar/dimunuir proporções da garrafa: alça, buraco, centro, junção entre alça e buraco - Nome-do-Pai
- Animação: movimento de onda pela garrafa
- Animação: interação entre duas garrafas, interação entre três garrafas, interação entre várias garrafas - Colisão, mesclar
- Animação com o estofado da garrafa, diferentes fantasias, crise de gozo, furos na fantasia
- IA: gerar diferentes modelos de garrafas e animações baseadas em prompt - garrafas artísticas

Details: CGI.md, KleinsbottleFantasy.md

# everytime
source ~/blender_venv/bin/activate

# Create a venv using Blender's Python
/usr/bin/python3.12 -m venv ~/blender_venv
source ~/blender_venv/bin/activate

# Install packages
pip install numpy pillow

Method 1: Direct Execution
blender --python /path/to/your_script.py

Method 2: Background Mode (No GUI)
blender --background --python /path/to/your_script.py

Method 3: Interactive Python Console
blender --python-console

# Handle External Dependencies
If your script uses packages (e.g., numpy), ensure Blender can see them:

import sys
sys.path.append("/home/you/blender_venv/lib/python3.12/site-packages")  # For venv


# Cleaning up
No problem! Let's clean up and set up the Blender Python environment correctly in /home/zaya/Documents/Gitrepos/kleinsfantasy.

Step 1: Clean Up the Wrong Installation
First, let's remove the incorrectly installed dependencies:

bash
Copy
# Navigate to the wrong project
cd /home/zaya/Documents/Gitrepos/Linktrees/Business/Dev/Py/Blender

# Remove any virtual environment if you created one
rm -rf venv .venv blender_venv

# Remove Pipenv files if used
rm -rf Pipfile Pipfile.lock

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
Step 2: Set Up Correct Project Directory
bash
Copy
# Navigate to the correct project
cd /home/zaya/Documents/Gitrepos/kleinsfantasy

# Remove any existing environment files (if they exist)
rm -rf venv .venv blender_venv Pipfile Pipfile.lock

# To-do

Cortar a Garrafa com um plano

Adicionar imagens ao plano: Escritos Chinese, Grafo do desejo, Equações topológicas

Adicionar uma Faixa de Moebius

Ambiente

