import tkinter as tk 
from tkinter import ttk
import win32gui
from PIL import ImageGrab, Image

from keras.models import load_model
from keras.models import Model

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Recognizer:
	def __init__(self, master):
		# set up for window
		self.window = master
		self.window.title('Digit recognizer')
		self.window.geometry('895x400')

		# load model
		self.model = load_model('mnist.h5')
		# self.model = 1

		# canvas to draw
		self.draw_canvas = tk.Canvas(self.window, width=280, height=280, bg='black', cursor='circle')
		self.old_x = None
		self.old_y = None

		# canvas to show probabilites
		self.proba_canvas = tk.Canvas(self.window, width=600, height=280, bg='white')

		# button
		self.clear_button = tk.Button(self.window, text='Clear', font=('Helvetica', 15), width=8, state='disabled', command=self.clear)
		self.predict_button = tk.Button(self.window, text='Predict', font=('Helvetica', 15), width=8, state='disabled', command=self.draw_prob)
		self.visualize_button = tk.Button(self.window, text='Visualize outputs of each layers',font=('Helvetica', 15), width=25, state='disabled', command=self.visualize)

		# label
		self.predict_label = tk.Label(self.window, text='', font=('Helvetica', 15))


		# grid system
		self.draw_canvas.grid(row=0, column=0, columnspan=2)
		self.proba_canvas.grid(row=0, column=2, columnspan=10, stick='ew')

		self.clear_button.grid(row=1, column=0, pady=5)
		self.predict_button.grid(row=1, column=1, pady=5)
		self.visualize_button.grid(row=2, column=0, columnspan=2, padx=3)

		self.predict_label.grid(row=3, column=2, columnspan=10)

		# bind draw_canvas
		self.draw_canvas.bind('<B1-Motion>', self.draw_digit)
		self.draw_canvas.bind('<ButtonRelease-1>', self.reset_xy)

		# label for digits
		self.create_digit_label()

	def create_digit_label(self):
		d0_label = tk.Label(self.window, text='0', font=('Helvetica', 15))
		d1_label = tk.Label(self.window, text='1', font=('Helvetica', 15))
		d2_label = tk.Label(self.window, text='2', font=('Helvetica', 15))
		d3_label = tk.Label(self.window, text='3', font=('Helvetica', 15))
		d4_label = tk.Label(self.window, text='4', font=('Helvetica', 15))
		d5_label = tk.Label(self.window, text='5', font=('Helvetica', 15))
		d6_label = tk.Label(self.window, text='6', font=('Helvetica', 15))
		d7_label = tk.Label(self.window, text='7', font=('Helvetica', 15))
		d8_label = tk.Label(self.window, text='8', font=('Helvetica', 15))
		d9_label = tk.Label(self.window, text='9', font=('Helvetica', 15))

		diagram_label = tk.Label(self.window, text='Probability histogram', font=('Helvetica', 15))

		d0_label.grid(row=1, column=2)
		d1_label.grid(row=1, column=3)
		d2_label.grid(row=1, column=4)
		d3_label.grid(row=1, column=5)
		d4_label.grid(row=1, column=6)
		d5_label.grid(row=1, column=7)
		d6_label.grid(row=1, column=8)
		d7_label.grid(row=1, column=9)
		d8_label.grid(row=1, column=10)
		d9_label.grid(row=1, column=11)

		diagram_label.grid(row=2, column=2, columnspan=10)

	def draw_digit(self, event):
		if(self.old_x and self.old_y):
			self.draw_canvas.create_line(self.old_x, self.old_y, event.x, event.y, fill='white', width=15, capstyle='round', smooth=True)

		self.old_x = event.x 
		self.old_y = event.y

		if(self.old_x != None and self.old_y != None):
			self.predict_button.configure(state='normal')
			self.clear_button.configure(state='normal')

	def reset_xy(self, event):
		self.old_x = None
		self.old_y = None

	def clear(self):
		self.draw_canvas.delete('all')
		self.proba_canvas.delete('all')

		self.predict_label.configure(text='')

		self.predict_button.configure(state='disabled')
		self.clear_button.configure(state='disabled')
		self.visualize_button.configure(state='disabled')

	def get_image(self):
		HWND = self.draw_canvas.winfo_id()
		rect = win32gui.GetWindowRect(HWND)
		img = ImageGrab.grab(rect)

		img = img.resize((28, 28))
		img = img.convert('L') # convert to grayscale
		img = np.array(img)
		img = img.reshape((1, 28, 28, 1))
		img = img / 255.

		return img 

	def predict(self, img):
		prob = self.model.predict([img])[0]
		digit = np.argmax(prob)

		return prob, digit 


	def draw_prob(self):
		img = self.get_image()
		prob, digit = self.predict(img)

		self.predict_label.configure(text="Predict: " + str(digit))

		# look up prob_canvas_coordinates.png to know how to caculate coordinates

		# for digit 0
		x1, y1 =  45, 280
		x2, y2 = x1 - 30, 280 - (280 * prob[0])
		if(digit == 0):
			self.proba_canvas.create_rectangle(x1, y1, x2, y2, fill='green')
		else:
			self.proba_canvas.create_rectangle(x1, y1, x2, y2, fill='blue')
		if(y2 < 18):
			self.proba_canvas.create_text(x1 - 15, y2 + 10, font=('Helvetica', 10), text='{0:.2f}'.format(prob[0]), fill='white')
		else:
			self.proba_canvas.create_text(x1 - 15, y2 - 10, font=('Helvetica', 10), text='{0:.2f}'.format(prob[0]), fill='black')

		# for onthers digit
		for i in range(1, 10):
			x1, y1 = x1 + 60, 280
			x2, y2 = x1 - 30, 280 - (280 * prob[i])
			if(digit == i):
				self.proba_canvas.create_rectangle(x1, y1, x2, y2, fill='green')
			else:
				self.proba_canvas.create_rectangle(x1, y1, x2, y2, fill='blue')
			if(y2 < 18):
				self.proba_canvas.create_text(x1 - 15, y2 + 10, font=('Helvetica', 10), text='{0:.2f}'.format(prob[i]), fill='white')
			else:
				self.proba_canvas.create_text(x1 - 15, y2 - 10, font=('Helvetica', 10), text='{0:.2f}'.format(prob[i]), fill='black')

		# state of buttons after click predict button

		self.predict_button.configure(state='disabled')
		self.visualize_button.configure(state='normal')

	def visualize(self):
		top_level = tk.Toplevel()
		img = self.get_image()

		Visualize(top_level, self.model, img)


class Visualize:
	def __init__(self, master, model, img):
		self.top_level = master
		self.top_level.title('Visualize outputs of each layers')
		self.top_level.geometry('1170x550')
		self.model = model
		self.img = img.reshape(28, 28, 1)

		self.window = self.create_frame_scrollbar(self.top_level) 
		self.frame_for_conv2d_0 = self.create_frame_scrollbar(root=self.window, row=1, column=1, width=180, height=450)
		self.frame_for_conv2d_1 = self.create_frame_scrollbar(root=self.window, row=1, column=2, width=180, height=450)
		self.frame_for_max_pooling2d_0 = self.create_frame_scrollbar(root=self.window, row=1, column=3, width=180, height=450)
		self.frame_for_dense_0 = self.create_frame_scrollbar(root=self.window, row=1, column=4, width=120, height=450)
		self.frame_for_dense_1 = self.create_frame_scrollbar(root=self.window, row=1, column=5, width=120, height=450)

		self.create_labels()

		self.visualize_layer_output()

	def create_frame_scrollbar(self, root, row=None, column=None, width=None, height=None, padx=None, pady=None, background=None):
		main_frame = tk.Frame(root)

		canvas = tk.Canvas(main_frame, width=width, height=height, bg=background)

		vscrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
		vscrollbar.pack(side='right', fill='y')
		canvas.pack(side='left', fill='both', expand=1)
		canvas.configure(yscrollcommand=vscrollbar.set)

		if(row != None and column != None):
			main_frame.grid(row=row, column=column, padx=padx, pady=pady)
		else:
			main_frame.pack(fill='both', expand=1)
			hscrollbar = ttk.Scrollbar(main_frame, orient='horizontal', command=canvas.xview)
			hscrollbar.pack(side='bottom', fill='x')
			canvas.pack(side='top', fill='both', expand=1)
			canvas.configure(xscrollcommand=hscrollbar.set)


		canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

		frame = tk.Frame(canvas)

		canvas.create_window((0,0), window=frame, anchor='nw')

		return frame

	def create_labels(self):
		label_0 = tk.Label(self.window, text='Input: 28x28', font=('Helvetica', 10))
		label_1 = tk.Label(self.window, text='Conv2d_0: 24x24    ', font=('Helvetica', 10))
		label_2 = tk.Label(self.window, text='Conv2d_1: 12x12    ', font=('Helvetica', 10))
		label_3 = tk.Label(self.window, text='Max_pooling2d_0: 12x12   ', font=('Helvetica', 10))
		label_4 = tk.Label(self.window, text='Dense_0: 1x1     ', font=('Helvetica', 10))
		label_5 = tk.Label(self.window, text='Dense_1: 1x1     ', font=('Helvetica', 10))
 
		label_0.grid(row=0, column=0, pady=15)
		label_1.grid(row=0, column=1, pady=15)
		label_2.grid(row=0, column=2, pady=15)
		label_3.grid(row=0, column=3, pady=15)
		label_4.grid(row=0, column=4, pady=15)
		label_5.grid(row=0, column=5, pady=15)

	def get_layer_ouput(self):
		img = self.img.reshape(1, 28, 28, 1)
		conv2d_0 = Model(inputs=self.model.input, outputs=self.model.get_layer(index=0).output)
		conv2d_1 = Model(inputs=self.model.input, outputs=self.model.get_layer(index=1).output)
		max_pooling2d_0 = Model(inputs=self.model.input, outputs=self.model.get_layer(index=2).output)
		dense_0 = Model(inputs=self.model.input, outputs=self.model.get_layer(index=5).output)
		dense_1 = Model(inputs=self.model.input, outputs=self.model.get_layer(index=7).output)
	
		conv2d_0_output = conv2d_0.predict(img)[0]
		conv2d_1_output = conv2d_1.predict(img)[0]
		max_pooling2d_0_output = max_pooling2d_0.predict(img)[0]
		dense_0_output = dense_0.predict(img)[0].reshape(1, 1, -1)
		dense_1_output = dense_1.predict(img)[0].reshape(1, 1, -1)

		return (conv2d_0_output, conv2d_1_output, max_pooling2d_0_output, dense_0_output, dense_1_output)

	def imshow_img(self, root, figsize, dpi=None, layer_output=None, name=None, row=None, column=None, padx=None, pady=None, background=None):
		if(layer_output is None):
			fig = Figure(figsize=figsize, dpi=dpi, tight_layout={'pad':0})

			ax = fig.add_subplot(111)
			ax.imshow(self.img, cmap='gray', vmin=0, vmax=1) 

			ax.axes.get_xaxis().set_visible(False)
			ax.axes.get_yaxis().set_visible(False)

			canvas = FigureCanvasTkAgg(fig,  master=root)
			canvas.get_tk_widget().grid(row=row, column=column, padx=padx, pady=pady)
		else:
			m, n, c = layer_output.shape 
			print(m, n, c)
			fig, ax = plt.subplots(nrows=c, ncols=1, figsize=figsize, dpi=dpi)
			for i in range(c):
			    ax[i].imshow(layer_output[:,:,i].reshape(m, n, 1), cmap='gray', vmin=0, vmax=1)
			    ax[i].axes.get_xaxis().set_visible(False)
			    ax[i].axes.get_yaxis().set_visible(False)
			    ax[i].set_title(str(i), fontsize=10)
			    print(name + '[{}]: done'.format(i))
			fig.set_facecolor(background)
			fig.tight_layout()

			canvas = FigureCanvasTkAgg(fig, master=root)  
			canvas.get_tk_widget().pack()

	def visualize_layer_output(self):
		self.imshow_img(root=self.window, figsize=(2, 2), dpi=100, row=1, column=0, padx=15, pady=15)

		conv2d_0_output, conv2d_1_output, max_pooling2d_0_output, dense_0_output, dense_1_output = self.get_layer_ouput()

		self.imshow_img(root=self.frame_for_conv2d_0, figsize=(1.85, 60), layer_output=conv2d_0_output, name='conv2d_0', background='red')
		self.imshow_img(root=self.frame_for_conv2d_1, figsize=(1.85, 120), layer_output=conv2d_1_output, name='conv2d_1', background='green')
		self.imshow_img(root=self.frame_for_max_pooling2d_0, figsize=(1.85, 120), layer_output=max_pooling2d_0_output, name='max_pooling2d_0', background='blue')
		self.imshow_img(root=self.frame_for_dense_0, figsize=(1.3, 250), layer_output=dense_0_output, name='dense_0', background='yellow')
		self.imshow_img(root=self.frame_for_dense_1, figsize=(1.3, 10), layer_output=dense_1_output, name='dense_1', background='purple')


root = tk.Tk()
Recognizer(master=root)
root.mainloop()



