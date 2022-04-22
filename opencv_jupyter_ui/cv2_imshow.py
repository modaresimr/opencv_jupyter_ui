from ipycanvas import Canvas, hold_canvas
from ipywidgets import VBox,HTML
from IPython.display import display
windows={}
def cv2_imshow(name,image,params=None,width=None,height=None):
	if name not in windows:
		windows[name]=Canvas()
		box=VBox([HTML(name),windows[name]])
		box.layout.border='1.5px solid'
# 		box.layout.width = '100px'
		display(box)
        
	canvas=windows[name]
	with hold_canvas(canvas):
		canvas.clear()
		if image is None:
			return
		canvas.put_image_data(image)
		canvas.width=image.shape[1]
		canvas.height=image.shape[0]
		layout={}
        
		if width:layout['width']=f'{width}px' if type(width) ==int else width
		if height:layout['height']=f'{height}px' if type(height) ==int else height
		canvas.layout=layout

def cv2_destroyAllWindows():
	windows.clear()