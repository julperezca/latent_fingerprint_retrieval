from functions import compensacion, desenvolvimiento
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__)) # path del .py

# contorno para posicionamiento inicial  
image_dir = os.path.join(script_dir,f"Resultados/MesaRestaurante/Mesa_toma2/Phase_masked.png")  
image_dir_save =   os.path.join(script_dir,f"Resultados/MesaRestaurante/Mesa_toma2/FaseCompensada_desenvuelta_masked.tiff")        
phase_image = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)

plt.imshow(phase_image, cmap='gray')
plt.show()

    
compensed_phase = compensacion(phase_image)
unwrapped_phase = desenvolvimiento(phase_image)
compensed_phase = np.uint8(255*compensed_phase/np.max(compensed_phase))

plt.imshow(unwrapped_phase, cmap='gray')
plt.show()

cv2.imwrite(image_dir_save, compensed_phase)
# escalado de [-pi a pi)
