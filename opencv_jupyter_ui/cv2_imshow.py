from ipycanvas import Canvas, hold_canvas
from ipywidgets import VBox,HTML
from IPython.display import display
windows={}
def cv2_imshow(name,image,params=None,width=None,height=None):
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
	windows.clear()