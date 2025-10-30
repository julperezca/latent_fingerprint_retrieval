# latent_fingerprint_retrieval
This repository contains the reprogramable-code for retrieving latent fingerprint using deflectometry-modulated intensity map

## Dependency instalations if any alliedvision camera vmbpy is used
python -m pip install 'C:/Users/usuario/Desktop/GitHub/id_defectos_porcelana/vmbpy-1.1.0-py3-none-win_amd64.whl[numpy,opencv]'

## How it works
1. Selection of the fringe pattern frequency
2. Posicionate the camera and focus the surface under test and display the structured pattern and make sure that the reflection of the fringes are on the camera field of view.
3. The program ask in terminal if you want to save in folder Results/surface  the result of the phase-shift, phase, and amplitude = modulated intensity map 
   3.1. The program ask in terminal if you want to realize the phase compensation
