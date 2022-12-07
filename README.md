# virtual_writing_MediaPipe
Application of openCV and MediaPipe for virtual writing in Python.


An application has been developed for writing virtually on the screen.

This is similar to the previous virtual writing system in which only open CV was used.
In this application hands module and drawing module from media pipe has been used for writing.
And for clearing the screen, mask of hand is created and used using openCV.

the tip of the forefinger is being used for writing.The trigger for writing is controlled by the position of the thumb.
A threshold values of the distance between the tips of forefinger and thumb has been set.
Hand landmarks function of hands module is being applied to constantly track all the landmarks of the hands in each consecutive frame, including tips of the thumb and the forefinger.

The XY coordinates of all the landmarks are being calculated and then updated in an array for each frame.
When there is no hand in the frame, the array is being emptied.
The applications which use webcams as input for creating masks heavily depend upon the light sources available around the user as it affects the saturation value of the input image in HSV format. the threshold value set for the mask of the palm is required to be corrected because in the current light conditions it being crossed unintentionally more often.

The distance between the tips of the thumb and forefinger is calculated in each frame by extracting the coordinates values from the set of points.
The circles filled with red colors is also stored in a set and being constantly printed out in each frame.This set is being updated or being emptied based on triggering inputs.

The quality of the application can be improved by setting up the parameters in the code correctly based on the ambient lighting conditions.This may take some time to tune these parameters for best performance.The performance of these type of applications also depends upon the resolution of the camera.In this case, the resolution of the default laptop camera is very low and has negative effect on performance of the application.

One can use a higher resolution camera for better performance. Though the processing power requirement will also increase, laptop or computer should be able to handle that.

# Future scope

This application can be combined with a deep learning application to automatically detect the letters and symbols and correct them in beautiful fonts.
