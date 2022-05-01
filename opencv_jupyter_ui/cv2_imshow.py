from glob import glob
from ipycanvas import Canvas, hold_canvas
from ipywidgets import VBox,HTML
from IPython.display import display
windows={}

def remove_old_windows_if_needed():
		
		from IPython import get_ipython
		if windows.get('_last_exec',0)==get_ipython().execution_count:
			return
		cv2_destroyAllWindows()
		windows['_last_exec']=get_ipython().execution_count

def cv2_imshow(name,image,width=None,height=None,colorspace='bgr'):
	if not in_notebook():
		try:
			import cv2
			return cv2.imshow(name,image)
		except:
			print('no notebook and cv2 found')
			return

	remove_old_windows_if_needed()
	if name not in windows:
		box=VBox([HTML(f'<center>{name}</center>'),Canvas()])
		box.layout.border='1.5px solid'
# 		box.layout.width = '100px'
		box.layout.width='fit-content'
		display(box)
		windows[name]=box
	
	canvas=windows[name].children[1]
	with hold_canvas(canvas):
		canvas.clear()
		if image is None:
			return
		if colorspace=='bgr':
			image=image[:,:,::-1] # convert to rgb
		canvas.put_image_data(image)
		layout={}
        
		canvas.width=image.shape[1]
		canvas.height=image.shape[0]
        
		if width:
			layout['width']=f'{width}px' if type(width) ==int else width
        
		if height:layout['height']=f'{height}px' if type(height) ==int else height
		if not (width or height):
			layout['width']=f'{image.shape[1]}px'
		canvas.layout=layout
        
		

def cv2_destroyAllWindows():
	if not in_notebook():
		try:
			import cv2
			return cv2.destroyAllWindows()
		except:pass
	windows.clear()


def in_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True