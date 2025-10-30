import cv2
from vmbpy import *
import vmbpy
import functions
from functions import *
import numpy as np
import os
import time



delay_camera_screen  = 500E-3   # delay to sinchronize screen projection and camera acquisition
shifted_frames = []             # List for storing the acquired frames
fringe_shift_counter = 0        # fringe shift counter to guarantee the phase shifting-technique
freq = 3                        # initial freq for projected fringes
displacement, resize_h, resize_w, = monitor_info()
patterns_to_project = fringe_generator(freq, screen_width=resize_w, screen_height=resize_h)    
base_path = os.path.dirname(__file__) # Directorio para save_images las imágenes
path_folder = os.path.join(base_path, f"Results/surface")
create_folder(path_folder)

#  try for testing the camera conection
try:
    init_camera()
    cam = functions.cam                      # variable for contolling camera features
    vmb = functions.vmb                     # vimba system
except:
    print("camera is not connected.")
    close_camera()
    exit()

# the user have to posicionate the camera to observe the fringe projection 
display_pattern_second_screen(patterns_to_project[0], resize_w, resize_h, displacement)
positionate_camera()

print("Frames acquisition has started...")
# Loop for acquiring shifted-images
while True:
    cv2.imshow('pattern',((patterns_to_project[fringe_shift_counter])))
    cv2.waitKey(1)
    time.sleep(delay_camera_screen)

    # to save image under uniform illumination
    if fringe_shift_counter == 5:
        cam.set_pixel_format(PixelFormat.Rgb8) 
        frame = cam.get_frame()
        frame = frame.as_numpy_ndarray()
        frame = np.squeeze(frame)
        cv2.imwrite(path_folder+f"/Phase_{fringe_shift_counter}color.png", frame)

    # acquiring and saving the shifted-phase
    cam.set_pixel_format(PixelFormat.Mono8) 
    frame = cam.get_frame()
    frame = frame.as_numpy_ndarray()
    frame = np.squeeze(frame)
    cv2.imwrite(path_folder + f"/Phase_{fringe_shift_counter}.png", frame)

    # storing the frame for post-processing
    shifted_frames.append(frame)
    fringe_shift_counter +=1

    # finish at the sixth capture
    if fringe_shift_counter == 6 :
        cv2.destroyAllWindows()
        close_camera()
        break

# post-proccesing
# obatain significant ...phase, phasor, compensed_phase, modulated intensity map... from the acquired frames
complex_matrix = phasor(shifted_frames)
amplitude_from_complex = amplitude_from_phasor(complex_matrix)
phase = phase_calculation_from_array(shifted_frames)

save_images = input("save_images (yes) (no):") 
# save_images
if save_images.lower() == "si" or save_images.lower() == "s" or save_images.lower() == "yes" or save_images.lower() == "y" or save_images == "Si" or save_images == "SI" or save_images.lower() == "YES":
        
        if os.path.exists(path_folder):
            cv2.imwrite(path_folder+"/modulated_intensity_map.png", np.uint8(255*amplitude_from_complex/np.max(amplitude_from_complex)))
            cv2.imwrite(path_folder+"/wrapped_phase.png", phase)
            # realización de la compensacion
            compensation = input("Realize the phase compensation: (yes) (no)")
            if compensation.lower() == "yes":
                compensed_phase = phase_compensation(phase)
                cv2.imwrite(path_folder+"/compensed_phase.png", np.uint8(255*compensed_phase/np.max(compensed_phase)))
        print("Images succesfully saved")