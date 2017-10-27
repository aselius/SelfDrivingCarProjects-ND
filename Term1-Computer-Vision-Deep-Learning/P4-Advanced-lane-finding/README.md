## Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

The Project
---

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

Key files in the Project Directory
---
* camera_cal : Images used to calibrate the camera used in the recording
* Advanced Lane Detection.ipynb : Jupyter Notebook with the lane detection python code embedded
* output.mp4 : Results of the lane detection processing done for the challenge_video.mp4
* distortion.p : Holds the distortion coefficients obtained during the camera calibration stage

Further detail on the lane detection notebook
---
(refer to jupyter notebook for examples, thought process in comments and somewhat self documenting code)
### Camera Calibration
Camera calibration is performed in order to undistort the images taken with the camera. I utilized the OpenCV2 functions findchessboardcorners, calibrate camera and undistort using the calibration 9x6 checkerboard images taken with the camera. I then output the coefficients to a pickle file for future use, and also kept it in memory to use.

### Color Transforms
I utilized the following thresholding techniques, followed by masking to obtain the regions of interest
* Sobel gradient thresholding (x orientation)
* Gradient magnitude thresholding
* Gradient direction thresholding
* HLS color thresholding (S)

The parameters used are the following:
* ksize = 7
* sobel thresshold 50-255 (x)
* magnitude threshold 50-255
* direction threshold 0.7-1.3
* hls threshold 170-255 (s)

Applying the thresholding techniques and masking techniques, I was able to get a good degree of isolation of the two lanes plus some noise. (See notebook for a side by side comparison for 6 examples)

### Perspective Transform
So after designating the areas of interest, I applied a perspective transform on the parts of the road the lane markings are on to get a bird's eye view of the lane. This was done using the getPerspectiveTransform from OpenCV 2. (Refer to notebook for a side by side comparison)

### Finding the lanes
So for the sake of working under a giant time constraint, I refactored a lot of code I used from the Udacity exercises I;ve done during the coursework on Computer Vision, and used Line objects to store information, but I would have liked to use a functional approach to better calculate the average polynomial values and to retain the polynomial values calculated for rapid repeatability.

Aside from this, I used the windows approach to tackle this. The image was divided up laterally into different windows with a certain window length (100 pixels in this case) and after obtaining the starting point by taking an argmax of the histogram of the binary values (pixels), each window gathered all the nonzero values within that window and appended to an all points array. After collecting all y values for the image with n windows, a polyfit was done on the non-zero points that were collected. (Predicted lanes were overlayed in one sample image in the notebook)

To prevent this window scanning to happen at everyframe, a margin was drawn around the predicted lane line, and if the first point in the next frame lay within a margin, the prior windows were kept and the indices in that was collected.

### Problems, Improvements and Retrospective
I ran into a couple of problems (which I had to put in my latest commit message five times due to a git error..) while rapidly prototyping this project. A couple being,
#### Problems and future Improvements
* I started very ambitious, but quickly ran into a time constraint and this ended up in code becoming very monolithic towards the end
* (SOLVED) Radius curvature is indeed calculated, but for the first frame I could not solve the NaN issue I was getting. So I had to delete the text overlay that was showing the radius value in the video itself
* Oh objects.. I have a mathematical background (not traditional CS) and thought this was very applicable to do some fp on.. but time constraints as mentioned above.
* Manual region of interest declaration. Self explanatory but if the road width, shapes change vastly, the model is not valid anymore.
* Fine tuning on thresholding parameters.. If you stare very carefully at the interpolation being done on the right lane in the video you will notice the right corner tends to fluctuate a little bit. This is due to the lack of further fine tuning I should have done.

### Retrospective and future features
* Application of deep learning. This would be a very interesting side project I would love to do on spare time
* Improving features
    * YOLO on top of this to detect near vehicles
    * Distance from other cars
    * Distance from each ends of the road
    * (SOLVED) Distance away from center
* Sanity checks