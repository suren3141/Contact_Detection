# Contact_Detection

This repo is the set of codes for Human-Human and Human-object contact detection. 

You will need to have the images as in the path folders mentioned in the python notebook scripts in order to run the code propoerly. 

To test code use the folder of images 'data/new'. This has the RGB, Grayscale images, handkeypoints, pose keypoints for each frame. 'new' refers to frames 650-975 of video 'seq18' of the [SDHA human interaction dataset](https://cvrc.ece.utexas.edu/SDHA2010/Human_Interaction.html).

Run the notebook "Handshake Detection Full.ipynb" to detect handshakes in the given video stream ie:'data/new'.

To use the openpose model, you will need to install openpose (CMU-openpose) and have the models in the folder of the script. This is required only for the notebook "Handkeypoints.ipynb". 
