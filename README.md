# imgSeqLabelTool
imgSeqLabelTool is specifically made to label/annotate image sequences using bounding boxes. There are other tools present that allow labeling images, but when you have thousands of images the task gets exhausting very quickly.

This tool exploits the similar structure in consecutive frames of a continuous sequence of images. Instead of the user labeling all the images manually, imgSeqLabelTool provides a way to get away with labeling a minimum amount of images.

You start by providing bounding boxes for a frame and using dlib's trackers the tool tracks your objects to the next frame. Simple, right?

If you are not satisfied with the tracker's output, you can provide new bounding boxes for the tracker to track from that frame onwards. If you are satisfied with the tracker's bounding boxes, which happens in 4/5 cases, with just a single key press you can save the annotation and move on to the next frame in a flash.

# Setup
Prerequisites:
dlib
opencv
numpy
python

# Getting Started
After you have installed the pre-requisites, let's begin using imgSeqLabelTool.

First, we would want to ensure that you have a folder that holds all the images you wish to label and a directory for storing their corresponding annotation files. This repository has stored the `images/` in the frames folder and the anotated files in the `annotations/` folder (duh!).

Now that we have all the folder setup, just add them to the function call in the imgSeqLabelTool.py file,



Note: Since you'd want to exploit the structure in consecutive frames, make sure your images are named (incrementally) in the order that they are captured to get best results. 



# Future improvements
Currently, imgSeqLabelTool supports labeling a single object class.
It would also be useful for some users to obtain annotation in various formats, especially a comma or space-separated .txt file.