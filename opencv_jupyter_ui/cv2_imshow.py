from glob import glob
from ipycanvas import Canvas, hold_canvas
from ipywidgets import VBox,HBox,HTML,Button
from IPython.display import display
import numpy as np
windows={}

old={}

def remove_old_windows_if_needed():
		
		from IPython import get_ipython
		if windows.get('_last_exec',0)==get_ipython().execution_count:
			return
		cv2_destroyAllWindows()
		windows['_last_exec']=get_ipython().execution_count

def cv2_imshow(name,image,width=None,height=None,colorspace='bgr',force_clear=False):
	if not in_notebook():
		try:
			import cv2
			return cv2.imshow(name,image)
		except:
			print('no notebook and cv2 found')
			return

	remove_old_windows_if_needed()
	defineButtons()
	

	if name not in windows:
		box=VBox([HTML(f'<center>{name}</center>'),Canvas()])
		box.layout.border='1.5px solid'
# 		box.layout.width = '100px'
		box.layout.width='fit-content'
		display(box)
		windows[name]=box

	layout={}	
	if width:
		layout['width']=f'{width}px' if type(width) ==int else width

	if height:layout['height']=f'{height}px' if type(height) ==int else height
	if not (width or height):
		layout['width']=f'{image.shape[1]}px'
	try:
	
		h= height if height and type(height) ==int else -1
		w= width if width and type(width) ==int else -1
		if w!=-1 or h!=-1	:
			import cv2
			if w==-1 and h!=-1:
				w=image.shape[1]*h//image.shape[0]
				cv2.resize(image,(h,w))
			elif w!=-1 and h==-1:
				h=image.shape[0]*w//image.shape[1]
				cv2.resize(image,(h,w))
			elif w!=-1 and h!=-1:
				cv2.resize(image,(h,w))
	except:
		showWarning('warning an error occured! maybe cv2 not found-> it may cause performance issue')

	canvas=windows[name].children[1]
	if colorspace=='bgr': image=image[:,:,::-1] # convert to rgb
	with hold_canvas(canvas):
		if image is None:
			canvas.clear()
			return
		if force_clear or old.get(f'{name}-image',np.zeros(1)).shape!=image.shape:
			canvas.clear()
		old[f'{name}-image']=image
		canvas.put_image_data(image)
		
        
		canvas.width=image.shape[1]
		canvas.height=image.shape[0]
		
		canvas.layout=layout
        
def showWarning(msg):
	if windows.get('show_warning',True):
		print(msg)
		windows['show_warning']=False

def cv2_destroyAllWindows():
	if not in_notebook():
		try:
			import cv2
			return cv2.destroyAllWindows()
		except:pass
	windows.clear()
	old.clear()


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


def defineButtons():
	if 'buttons' not in windows:

		wbtn=defineWaitKeyButton();
		sbtn=defineStopButton()

		box=HBox([sbtn,wbtn])
		# box.layout.width='fit-content'
		display(box)
		windows['buttons']={'stop':sbtn,'waitkey':wbtn}
	return windows['buttons']


def defineWaitKeyButton():
	btn=Button(description='OpenCV waitKey')
	btn.layout.visibility = 'hidden'
	def on_click(btn):
	#     btn.description = '👍'
		btn.done=True

	btn.done=False
	btn.on_click(on_click)
		
	return btn
		

def defineStopButton():
		btn=Button(description='Stop',button_style='danger')
		
		def on_click(btn):
			btn.stop=True
			import signal
			
			signal.raise_signal(signal.SIGINT)
		

		btn.on_click(on_click)
		
		return btn
	

def cv2_waitKey(t):
	try:
		if not in_notebook():
			try:
				import cv2
				return cv2.waitKey(t)
			except:
				print('no notebook and cv2 found')
				return
		
		import time
		from jupyter_ui_poll import ui_events

		
		t_in_sec=t/1000.0
		wait_time=max(0.001,min(t_in_sec/10,.1))

		btn=defineButtons()['waitkey']
		btn.done=False
		btn.description=f'CV waitKey {t}'
		if t_in_sec>.5:
			btn.layout.visibility = 'unset'
		
		
		# Wait for user to press the button
		with ui_events() as poll:
			start = time.time()
			while time.time()-start<t_in_sec and not btn.done:
				poll(5)          # React to UI events (upto 10 at a time)
				# print('.', end='')
				time.sleep(wait_time)
				
			btn.layout.visibility = 'hidden'

		return 0xff
	except KeyboardInterrupt:
		class StopExecution(Exception):
			def _render_traceback_(self):
				pass
		print('Exection is stopped')
		defineButtons()['waitkey'].layout.visibility = 'hidden'
		defineButtons()['stop'].layout.visibility = 'hidden'
		raise StopExecution