
#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk
import copy
# from pynput.mouse import Controller, Listener



#Class button for all buttons in drawing tools area start here
class My_button_dict(object):#(My_menus):
    def __init__(self, **kwds):
##        print('button dict==',self.color_box)
        super(My_button_dict, self).__init__()

        
    def button_tools(self, button_root, button_color, button_row, button_column ):
        self.button = Button( button_root, activebackground= button_color, takefocus=0 , background= button_color ,
                              command = lambda :self.Color_Change( button_color))
        self.button.grid(row = button_row , column= button_column , ipadx=20, ipady=7, pady=1)
        self.label = Label(self.button, width=5, height=1 , relief=FLAT, bg= 'white' , fg= button_color)
        self.label.bind('<1>',  lambda e:self.Color_Change(button_color),'+')
        self.button.bind('<Motion>', lambda e:self.Show_tooltip(e, text= button_color), '+')
        self.button.bind('<Leave>', lambda e:self.Hide_tooltip(e), '+')
        
    def Hide_tooltip(self, event):
        self.label.place_forget()
        
    def Show_tooltip(self, event, text):
        self.label['text'] = text
        event_x = event.x
        event_y = event.y
        self.label.place(x= event_x, y=event_y-20)
        
    def Color_Change(self, color):
        global color_box
        color_box = color
        
    
#Class button for all buttons in drawing tools area end here
        
#Class my frames fo r all frames  start here
class My_frames(My_button_dict):#My_actions):
    
    def __init__(self, **kwds):
        super(My_frames, self).__init__(**kwds)
       
        #Canvas area frame for drawing start here
        self.text_frame = Canvas(kwds['root'],  bg='white',borderwidth=5, relief=SUNKEN 
                                 ,width= self.canvas_width, height=self.canvas_height, scrollregion=(0,0,100,700))
        self.text_frame.grid(row=0, column=0, columnspan=3, sticky='W') 
        
        #Canvas area frame for drawing end here
        
        #Drawing tools frame start here
        self.drawing_frame = LabelFrame(kwds['root'] , text='Drawing Tools' , borderwidth=5 ,
                                        relief=SUNKEN , width=self.width_quarter , height=self.canvas_height)
        self.drawing_frame.grid(row=0, column = 3, columnspan=2, sticky= 'E')
        
        #Drawing toold frame end here
        
        
        #Status bar start here
        self.status_frame = LabelFrame(kwds['root'], width=self.window_width )
        self.status_frame.grid(row = 1, column = 0, columnspan= 6, sticky= 'S')
        self.status_label = Label(self.status_frame , text= '', width= int(self.window_width* .126) , height= 2 )            
        self.status_label.grid(row=1, column=0, stick='S' )
        
        #Status bar end here
        
#Class my frames for all frames  end here


#class menu for creating all menus and items , start here
class My_menus(My_frames):
    def __init__(self, **kwds):
        super(My_menus, self).__init__(**kwds)
        #All menus keys & items 
        self.all_menu_dict = {
            #'New File':[['Open'   , lambda :self.open_file()]],
            'File' :[['Open'   , lambda :self.open_file()],
                    ['Save'    , None],
                    ['Save as' , None],
                    ['Print'  , None],
                    ['Close'  , None],
                    ['Exit'  , lambda :self.program_exit(root=kwds['root'])]],
            'Edit' : [['Undo', lambda :self.delete_item()],
                      ['Redo', None],
                      ['Copy', None],
                      ['Paste', None],
                      ['Cut', None]],
            'Format' : [['Font', None]],
            'View' : [['Status bar', None],
                      ['Drawing bar', None]],
            'Help' : [['About Drawing Pad',None ]]
            }
        
        menubar = Menu(kwds['root'] )
        kwds['root'].config(menu = menubar)
        for menu_title , menu_items in self.all_menu_dict.items():
                menu_list = Menu(menubar)
                menubar.add_cascade(menu = menu_list, label=menu_title)
                for items in menu_items:
                        menu_list.add_command(label= items[0], command=items[1])
        
        self.pop_up_menu = Listbox(self.text_frame, selectmode=SINGLE)
        self.pop_up_menu.insert(END, 'Copy')
        self.pop_up_menu.insert(END, 'Cut')
        self.pop_up_menu.insert(END, 'Paste')
        self.pop_up_menu.bind('<<ListboxSelect>>', self.get_selection)
        
#class menu for creating all menus and items , start here


        
#class widgets for all widgets start here        
class My_widgets(My_menus):
    def __init__(self, **kwds):
        super(My_widgets, self).__init__(**kwds)
        
        #color dictionary
        self.color_dict = {
            'white': 'white',
            'black': 'black',
            'green': 'green',
            'blue' : 'blue',
            'cyan' : 'cyan',
            'magenta' : 'magenta',
            'red' : 'red',
            'yellow' : 'yellow',
            'pink' : 'pink',
            'gray' : 'gray',
            'silver' : 'silver',
            'brown' : 'brown',
            'light blue' : 'light blue'
        }
        
        self.drawing_area_frame(kwds['root'])
        self.drawing_tools(kwds['root'])
            
    def drawing_area_frame(self, root):      

        for b in [self.text_frame]:
            b.bind("<1>", lambda e: self.button_press(e ), '+')
        
        self.text_frame.bind('<3>', lambda e: self.popup_menu(e) , '+')
        self.text_frame.bind('<ButtonRelease>', lambda e: self.stop_selection(e) , '+')
        self.text_frame.bind("<B1-Motion>",   lambda e:self.Draw_shape(e) , '+') 
        self.shape='status'
        self.text_frame.bind('<Motion>', lambda e:self.Status_mouse_axis(e) , '+')


                        
    def drawing_tools(self, root):
                #Drawing panel frame start
                #Tool tip to be shown on mouse movement
                
                x=0
                y=0
                for i,j in self.color_dict.items():
                            self.B = My_button_dict()
                            self.B.button_tools(button_root= self.drawing_frame, button_row=y, button_column=x, button_color= j)
                            if (x < 4 ):
                                x += 1
                            else:
                                x = 0
                                y += 1
                
                self.open_image = Image.open('line.png')
                self.logo1 = ImageTk.PhotoImage(self.open_image)
                self.label_line = Button  (self.drawing_frame, image=self.logo1, command = lambda :self.shape_click('line'))
                self.label_line.image=self.logo1
                self.label_line.grid(row=5, column=0)
               
                self.open_image = Image.open('eraser.png')                
                self.logo2 = ImageTk.PhotoImage(self.open_image)
                self.label_eraser = Button  (self.drawing_frame, image=self.logo2, command = lambda :self.shape_click('eraser'))
                self.label_eraser.image=self.logo2
                self.label_eraser.grid(row=5, column=1)
                
                self.open_image = Image.open('fill_color.png')                
                self.logo3 = ImageTk.PhotoImage(self.open_image)
                self.label_fill_color = Button  (self.drawing_frame, image=self.logo3, command = lambda :self.shape_click('fill'))
                self.label_fill_color.image=self.logo3
                self.label_fill_color.grid(row=5, column=2)
            
                        
                self.open_image = Image.open('pen-new.png')
                self.logo4 = ImageTk.PhotoImage(self.open_image)
                self.label_pen = Button  (self.drawing_frame, image=self.logo4, command = lambda :self.shape_click('pen'))
                self.label_pen.image=self.logo4
                self.label_pen.grid(row=5, column=3)
                
                self.open_image = Image.open('rectangle-new.png')
                self.logo5 = ImageTk.PhotoImage(self.open_image)    
                self.label_rectangle = Button  (self.drawing_frame, image=self.logo5, command = lambda :self.shape_click('rectangle'))
                self.label_rectangle.image=self.logo5
                self.label_rectangle.grid(row=5, column=4)
                
                self.open_image = Image.open('oval.png')                
                self.logo6 = ImageTk.PhotoImage(self.open_image)
                self.label_oval = Button  (self.drawing_frame, image=self.logo6, command = lambda :self.shape_click('oval'))
                self.label_oval.image=self.logo6
                self.label_oval.grid(row=6, column=0)
        
                self.open_image = Image.open('text.png')                
                self.logo7 = ImageTk.PhotoImage(self.open_image)
                self.label_text = Button  (self.drawing_frame, image=self.logo7, command = lambda :self.shape_click('text'))
                self.label_text.image=self.logo7
                self.label_text.grid(row=6, column=1)

                self.open_image = Image.open('select_all.png')                
                self.logo8 = ImageTk.PhotoImage(self.open_image)
                self.label_select_all = Button  (self.drawing_frame, image=self.logo8, command = lambda :self.shape_click('select_all'))
                self.label_select_all.image=self.logo8
                self.label_select_all.grid(row=6, column=2)
        
#class widgets for all widgets end here



#Class my actions for all functions and related actions
class My_actions(My_widgets):
    def __init__(self, **kwds):         
        super(My_actions, self).__init__(**kwds)
        self.item_ref = list()
        global color_box

    def shape_click(self, shape_type):
        self.shape = shape_type
        
    def delete_item(self):
        if (len(self.item_ref) > 0):
            self.text_frame.delete(self.item_ref[-1])
            self.item_ref.pop()
    
    def open_file(self ):
        file_name = filedialog.askopenfilename(filetypes=(("PNG","*.png"),("Gif","*.gif"),("Jpeg","*.jpg"),("All files","*.*")))
#         image_file = open(file_name).read()
        load = Image.open(file_name)
        if(load):
            image_render = ImageTk.PhotoImage(load)
            x,y = load.size
            img_label = Label(self.text_frame, image=image_render, width=x, height=y)
            img_label.image = image_render
            img_label.place(x= 500, y= 200)
        else: pass
        
#         self.text_frame.create_text(370, 490, text = image_file)
#         self.text_entry.insert(END, image_file)
                    
    def program_exit(self , **kwds):
            kwds['root'].destroy()  
    
    def get_selection(self,event):            
        get_item = self.pop_up_menu.get(self.pop_up_menu.curselection()[0])
        if(get_item == 'Cut'):
            self.Cut=1
        
        if (get_item == 'Copy' or get_item == 'Cut'):
            self.pop_up_menu.place_forget()
            
        elif (get_item == 'Paste' ):
            x= (self.event_new.x - self.event_prev.x) 
            y= (self.event_new.y - self.event_prev.y)
            if (self.Cut == 1):
                self.text_frame.move(self.object_ref, x, y)
            else:
                self.Cut=0
                x1, y1, x2, y2=self.object_coords
                x2 =  self.event_new.x + (x2 - x1)
                y2 =  self.event_new.y + (y2 - y1)
                
                self.text_frame.coords(self.object_new, self.event_new.x, self.event_new.y , x2 , y2)               

            self.event_prev.x = self.event_new.x
            self.event_prev.y = self.event_new.y
                
            self.pop_up_menu.place_forget()
    
    def shape_release(self, event):
        self.shape_id=0
        self.shape_status=False
        
    def shape_fill(self):
        
        if (self.text_frame.find_withtag(CURRENT)):
                self.object_ref = self.text_frame.find_withtag(CURRENT)
                self.text_frame.itemconfig(self.object_ref, fill= color_box)
        
    def button_press(self, event):
        self.event_prev = event
        self.shape_id=0
        self.shape_status=True
        self.del_selection()
        self.pop_up_menu.place_forget()

        if(self.shape is not 'select_all' and self.shape is not 'fill'):
            self.text_frame.create_line(event.x, event.y, event.x+1, event.y+1, width=3, fill= color_box)
        elif(self.shape == 'fill'):
            self.shape_fill()

        if (self.text_frame.find_withtag(CURRENT)):
                self.object_ref = self.text_frame.find_withtag(CURRENT)
#                 self.object_ref.__dict__ = self.object_ref.__dict__.copy()
                self.object_new = copy.deepcopy(self.text_frame.find_withtag(CURRENT))
                self.object_coords  = self.text_frame.bbox(self.text_frame.find_withtag(CURRENT))
                
                self.object_type = self.text_frame.type(self.text_frame.find_withtag(CURRENT))
                
     
    def popup_menu(self, event):
        self.event_new = event
        self.pop_up_menu.place(x=event.x, y=event.y)
        
    
    def Status_mouse_axis(self, event):
        self.status_label['text']= ( 'Mouse Axis : ', event.x,':',event.y)
        self.status_label.place(x=155, y=1)
        
                            
    def del_shape(self):
        self.text_frame.delete(self.shape_id)
        
    def del_selection(self):
        self.text_frame.delete('sel_rect')
    
    def stop_selection(self, event):
        self.start_selection= None
        
    def select_all(self, event):
        if(self.start_selection == None):
            self.start_selection = [event.x, event.y]

        sel_x = event.x
        sel_y = event.y

        self.del_selection()

        dashes=[2,3]

        self.text_frame.create_rectangle(self.start_selection, sel_x, sel_y, dash= dashes, tags='sel_rect')
        print(self.start_selection, sel_x, sel_y)
    
    def Draw_shape(self, event):
            item=None
            
            
            if(self.shape_status == True):
                self.del_shape()
            
            if(self.shape == 'rectangle'):
                self.shape_id = self.text_frame.create_rectangle(self.event_prev.x, self.event_prev.y, event.x+1, event.y+1, width=3, fill= color_box,
                                                 outline= color_box)
            elif(self.shape == 'eraser'):
                self.text_frame.create_rectangle(self.event_prev.x, self.event_prev.y, event.x+2, event.y+2, width=3, fill='white', 
                                                 outline='white')
            elif(self.shape == 'line'):
                self.shape_id = self.text_frame.create_line(self.event_prev.x, self.event_prev.y, event.x+1, event.y+1, width=3, fill= color_box )
            elif(self.shape == 'oval'):
                self.shape_id = self.text_frame.create_oval(self.event_prev.x, self.event_prev.y, event.x+1, event.y+1, width=3, fill= color_box ,
                                            outline= color_box)
                
            elif(self.shape == 'pen'):
                self.shape_id = self.text_frame.create_line(event.x, event.y, event.x+1, event.y+1, width=3, fill= color_box)
            elif(self.shape == 'select_all'):
                self.select_all(event)
            elif(self.shape == 'fill'):
                self.shape_fill()
            self.item_ref.append(self.shape_id)
#class my actions end here

class Drawingpad(My_actions):
    
    global mouse_axis  # list to save all mouse events (x,y) while moving the mouse
    global color_box
    color_box='red'  #Global variable for the color for all drawing tools
    
    def __init__(self, **kwds):
        self.window_name ="Yamin\'s Drawing Pad"     
        kwds['root'].title(self.window_name)
        self.window_size_x=0
        self.window_size_y=0
        self.start_selection = None
        
        help(Canvas)
        
        self.window_height = kwds['root'].winfo_screenheight()
        self.canvas_height = int(self.window_height * 0.8)
        self.status_frame_width = int(kwds['root'].winfo_screenwidth() * 0.108)
        self.window_width= kwds['root'].winfo_screenwidth()
        self.width_quarter= int(kwds['root'].winfo_screenwidth() * 0.25)
        self.canvas_width = int(kwds['root'].winfo_screenwidth() *0.75)
        
        kwds['root'].geometry("%dx%d+%d+%d" %(kwds['root'].winfo_screenwidth(), 
                                      kwds['root'].winfo_screenheight(), 
                                      self.window_size_x, 
                                      self.window_size_y))
        super(Drawingpad, self).__init__(**kwds)
        #My_actions(root=root)
        
#class Drawingpad end here    


class main_program:
    def __ini__(self):
        pass
            
    def main(self):
            root = Tk()

            Drawingpad(root=root )

            root.mainloop()


        
            
main = main_program()
if __name__ == '__main__' : main.main() 
