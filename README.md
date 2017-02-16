# imgSeqLabelTool
imgSeqLabelTool is specifically made to label/annotate image sequences using bounding boxes. There are other tools present that allow labeling images, but when you have thousands of images the task gets exhausting very quickly.

This tool exploits the similar structure in consecutive frames of a continuous sequence of images. Instead of the user labeling all the images manually, imgSeqLabelTool provides a way to get away with labeling a minimum amount of images.

You start by providing bounding boxes for a frame and using dlib's trackers the tool tracks your objects to the next frame. Simple, right?

If you are not satisfied with the tracker's output, you can provide new bounding boxes for the tracker to track from that frame onwards. If you are satisfied with the tracker's bounding boxes, which happens in 4/5 cases, with just a single key press you can save the annotation and move on to the next frame in a flash.
# Contents
1. [Setup](#setup)
2. [Getting Started](#getting-started)
3. [Future Improvements](#future-improvements)

# Setup
Prerequisites:

[python](https://www.python.org/)
[OpenCV](http://opencv.org/)
[numpy](http://www.numpy.org/)
[dlib](https://pypi.python.org/pypi/dlib)


# Getting Started
After you have installed the pre-requisites, let's begin using imgSeqLabelTool.

First, we would want to ensure that you have a folder that holds all the images you wish to label and a directory for storing their corresponding annotation files. This repository has stored the images in the [`frames/`](https://github.com/ankitdhall/imgSeqLabelTool/tree/master/frames) folder and the anotated files in the [`annotations/`](https://github.com/ankitdhall/imgSeqLabelTool/tree/master/annotations) folder (duh!).

> Since you'd want to exploit the structure in consecutive frames, make sure
> your images are named (incrementally) in the order that they are captured to 
> get best results. 

Now that we have all the folder setup, just add them to the function call in the [`imgSeqLabelTool.py`](https://github.com/ankitdhall/imgSeqLabelTool/blob/master/imgLabelTool.py),
```python
if __name__ == '__main__':
    # pass the ("path/to/img/directory", "path/to/annotation/directory", "image_extension", "image_index_to_begin_from")
    a = annotate("frames/", "annotations/", "png", 0)
    a.viewer()
```

Once you have added your paths to [`imgSeqLabelTool.py`](https://github.com/ankitdhall/imgSeqLabelTool/blob/master/imgLabelTool.py) you are ready to begin.
```shell
python imgSeqLabelTool.py
```

### Usage
There are a couple features that come with `imgSeqLabelTool`. Hopefully, there will be more additions in the future. Make sure the image window is active while executing these commands.

* To begin, `press n` on the first image
* Draw bounding boxes by clicking and dragging. You should see your labels overlayed on the image.
* Once you are done with labeling the boxes, `press m` to tell the tool that you've *marked* the boxes and that it can now begin tracking them and proceed to the next frame.
* The next frame will show you the proposed boxes by the tracker, if you like them, `press m` and move to the next frame. Otherwise, you can `press n` if you are *not happy* and reset the boxes, providing new ones yourself.
* If you are unhappy with a box that you drew, `press e` to *erase* the latest box drawn by you.
* Each time you `press m` the annotations for the file are saved automatically (refer to [`to_xml.py`](https://github.com/ankitdhall/imgSeqLabelTool/blob/master/to_xml.py)).
* To *quit*, `press q`

In summary,

Key press | function         
--------- | -------------------------------
`press n` | reset boxes, when *not happy* by boxes provided by the tracker (at the beginning of each image)
`press m` | tell `imgSeqLabelTool` that you have *marked* the boxes, save annotation and move to next image
`press e` | *erase* the latest box that you made
`press q` | *quit* `imgSeqLabelTool`

# Future improvements
Currently, imgSeqLabelTool supports writing annotation files only for a single object class. It would also be useful for some users to obtain annotation in various formats, especially a comma or space-separated .txt file.

- [ ] support multi-class label writing to annotation file
- [ ] support `.txt` format
