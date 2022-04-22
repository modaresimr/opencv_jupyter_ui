# opencv_jupyter_ui
As you know it is not possible to use `cv2.imshow` in the remote jupyter notebook or colab.
This is the replacement of `cv2.imshow` for jupyter. you need only to replace `cv2.imshow` to `cv2_imshow`. It will works in jupyter.

Please don't forget to call `cv2_releaseAllWindows()` in the begining of your jupyter cells otherwise it will not be displayed for the next time

# Installation

```
pip install opencv_jupyter_ui
```

# Usage
## import
```
from opencv_jupyter_ui import cv2_imshow, cv2_releaseAllWindows
```
## reseting windows:
Don't forget to add the following line to the first line of your cells
```
cv2_releaseAllWindows()
```
## Showing Frame
It is exactly like `cv2.imshow` you just need to change `.` to `_`.
```
cv2_imshow('test',frame)
```
### more options for showing frame
you can specify target width or height:
```
cv2_imshow('test',frame,width=100) # scale down/up your image to fit this width
cv2_imshow('test',frame,height=150) # scale down/up your image to fit this height
cv2_imshow('test',frame,width=100,height=150) # skretch your image to this size
```
Please note that you can also put CSS string instead e.g., `width='100%'`

# Example
```
from opencv_jupyter_ui import cv2_imshow, cv2_releaseAllWindows

cv2_releaseAllWindows() # Important otherwise it will work only for the first time

def getTestCV2Frame(i):
	import numpy as np
	x = np.linspace(-1, 1, 200)
	y = np.linspace(-1, 1, 200)
	x_grid, y_grid = np.meshgrid(x, y)
	blue_channel = np.array(np.sin(x_grid**2 + y_grid**2) * 255, dtype=np.int32)
	red_channel = (np.zeros_like(blue_channel) + 200*i)%222
	green_channel = np.zeros_like(blue_channel) + 50
	return np.stack((red_channel, blue_channel, green_channel), axis=2)

import time
for i in range(200):
	frame= getTestCV2Frame(i)
	cv2_imshow('test',frame)
	time.sleep(.1)
```
Output:
![test](text.gif)

