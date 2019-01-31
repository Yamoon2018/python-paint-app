# !/usr/bin/env python3
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import copy
import os
import win32api
import atexit
import sqlite3
from sqlite3 import Error
import time, datetime

# Class my frames fo r all frames  start here
class My_frames(object):#(My_drawing_buttons):  # My_actions):

    def __init__(self, **kwds):
        super(My_frames, self).__init__()
        self.canvas_width  = int(kwds['root'].winfo_screenwidth() * 0.75)
        self.window_height = kwds['root'].winfo_screenheight()
        self.canvas_height = int(self.window_height * 0.8)
        self.width_quarter = int(kwds['root'].winfo_screenwidth() * 0.25)
        self.window_width = kwds['root'].winfo_screenwidth()

        # Canvas area frame for drawing start here
        self.drawing_frame = Canvas(kwds['root'], bg='white', borderwidth=1, relief=SUNKEN
                                 , width=self.canvas_width, height=self.canvas_height, scrollregion=(0, 0, 100, 700))
        self.drawing_frame.grid(row=0, column=0, columnspan=3, sticky='W')
        # self.image_frame = Image.new('RGB', (self.canvas_width, self.canvas_height), (255, 255, 255))
        # self.image_render = ImageTk.PhotoImage(self.image_frame)
        # self.image_draw = ImageDraw.Draw(self.image_frame)
        # self.drawing_frame.create_image(self.canvas_width, self.canvas_height, image=self.image_render)
        # Canvas area frame for drawing end here

        # Drawing tools frame start here
        self.drawing_frame_tools = Frame(kwds['root'])
        self.drawing_frame_tools.grid(row=0, column=3, columnspan=2, sticky='E')
        self.tools_frame = LabelFrame(self.drawing_frame_tools, text='Drawing Tools', borderwidth=5,
                                        relief=SUNKEN, width=self.width_quarter, height=self.canvas_height * 0.5)
        self.setting_frame = LabelFrame(self.drawing_frame_tools, text='Setting Tools', borderwidth=5,
                                        relief=SUNKEN, width=self.width_quarter* 0.85, height=self.canvas_height *0.4)
        self.tools_frame.grid(row=0, column=3, columnspan=2, sticky='W')
        self.setting_frame.grid(row=1, column=3, columnspan=2, sticky='W')

        # Drawing toold frame end here

        # Status bar start here
        self.status_frame = LabelFrame(kwds['root'], width=self.window_width)
        self.status_frame.grid(row=1, column=0, columnspan=6, sticky='S')
        self.status_label = Label(self.status_frame, text='', width=int(self.window_width * .126), height=2)
        self.status_label.grid(row=1, column=0, stick='S')
        # Status bar end here


# Class my frames for all frames  end here


# class menu for creating all menus and items , start here
class My_menus(My_frames):
    def __init__(self, **kwds):
        super(My_menus, self).__init__(**kwds)
        self.shape_Id_list_index=0

        # All menus keys & items
        self.all_menu_dict = {
            'File': [['New', lambda : self.new_file(root = kwds['root'])],
                     ['Open', lambda: self.open_file(root = kwds['root'])],
                     ['Save', lambda: self.save_file(root = kwds['root'])],
                     ['Save as', lambda: self.save_as_file(root = kwds['root'])],
                     ['Print', lambda: self.print_file()],
                     ['Recent Files', ''],
                     ['Exit', lambda: self.program_exit(root=kwds['root'])]],
            'Edit': [['Undo', lambda: self.undo_Drawing()],
                     ['Redo', lambda: self.redo_Drawing()],
                     ['Copy', None],
                     ['Paste', None],
                     ['Cut', None]],
            'Format': [['Font', None]],
            'View': [['Status bar', None],
                     ['Drawing bar', None]],
            'Help': [['About Drawing Pad', None]]
        }

        menubar = Menu(kwds['root'], tearoff=False)
        kwds['root'].config(menu=menubar)
        for menu_title, menu_items in self.all_menu_dict.items():
            menu_list = Menu(menubar, tearoff=False)
            menubar.add_cascade(menu=menu_list, label=menu_title)
            for items in menu_items:
                if(items[0] == 'Recent Files'):
                    menu_list.add_separator()
                    submenu = Menu(menu_list, tearoff=0)
                    menu_list.add_cascade(label='Recent Files', menu=submenu, underline=0)
                    if(self.db_conn is not None):
                        sql_db="select file_name from drawingpad_filename_db"
                        cur = self.db_conn.cursor()
                        result=cur.execute(sql_db)
                        rows=result.fetchall()
                        for row1 in rows:
                                submenu.add_command(label=row1,
                                                    command= lambda row1=row1 :self.open_file(file_name=row1, root=kwds['root']),
                                                    underline=0)
                else:
                    menu_list.add_command(label=items[0], command=items[1])

        self.pop_up_menu = Listbox(self.drawing_frame, selectmode=SINGLE)
        self.pop_up_menu.insert(END, 'Copy')
        self.pop_up_menu.insert(END, 'Cut')
        self.pop_up_menu.insert(END, 'Paste')
        self.pop_up_menu.bind('<<ListboxSelect>>', self.get_selection)

    #Function to do action for List box
    def get_selection(self, event):
        get_item = self.pop_up_menu.get(self.pop_up_menu.curselection()[0])
        if (get_item == 'Cut'):
            self.Cut = 1

        if (get_item == 'Copy' or get_item == 'Cut'):
            self.pop_up_menu.place_forget()

        elif (get_item == 'Paste'):

            x = (self.event_new.x - self.event_prev.x)
            y = (self.event_new.y - self.event_prev.y)
            if (self.Cut == 1):
                self.drawing_frame.move(self.object_ref , x , y)
            else:
                self.Cut = 0
                x1, y1, x2, y2 = self.object_coords

                x1 = min(x1,x2)
                x2 = max(x1,x2)
                y1 = min(y1, y2)
                y2 = max(y1, y2)

                x2 = self.event_new.x + (x2 - x1)
                y2 = self.event_new.y + (y2 - y1)

                x1         = self.event_new.x
                y1         = self.event_new.y
                self.shape = self.object_type
                self.event_prev.x, self.event_prev.y, self.event_new.x, self.event_new.y = x1,y1,x2,y2

                if(self.shape != 'text'):
                        self.Draw_shape(shape_type  = self.shape ,
                                        event_prev_x= self.event_prev.x,
                                        event_prev_y = self.event_prev.y,
                                        event_new_x = self.event_new.x,
                                        event_new_y = self.event_new.y,
                                        widthThickness= self.object_thickness ,
                                        color_box = self.drawing_color  )
                else:
                    shape_text_details = list(self.object_ref)
                    #shape_text_details = ''.join(str(self.object_ref))
                    shape_text_details = self.shape_details_Dictionary[shape_text_details[0]]
                    self.create_shape_text(fill=shape_text_details[5], text=shape_text_details[4],
                                           x1=self.event_new.x,
                                           y1=self.event_new.y,
                                           font=shape_text_details[3])


                    #self.create_shape_text(fill=fill, text=text)

            self.undo_redo_dictionary_update()

            self.event_prev.x = self.event_new.x
            self.event_prev.y = self.event_new.y

            self.pop_up_menu.place_forget()

    #Retreive shape id from undo drawing id list
    def shape_id_split(self, shape_id_split):
        shape_id_split = str(shape_id_split)
        shape_id_split = shape_id_split.split('-')
        shape_id_split = shape_id_split[0]
        return shape_id_split


    # Undo method to detete last object has been drawn on Canvas
    def undo_Drawing(self):
            print('len undo drawing ID=',len(self.undo_drawing_id_list), self.shape_Id_list_index)
            if (self.shape_Id_list_index >= 0 ):
                print('undo_drawing_id_list= ',self.undo_drawing_id_list)
                shape_id_next    = self.undo_drawing_id_list[self.shape_Id_list_index - 2]
                shape_id_current = self.undo_drawing_id_list[self.shape_Id_list_index - 1]
                undo_object_id   = self.shape_details_Dictionary[shape_id_next]
                undo_object_current = self.shape_details_Dictionary[shape_id_current]
                shape_id_next    = self.shape_id_split(shape_id_next)
                shape_id_current = self.shape_id_split(shape_id_current)
                #self.undo_drawing_id_list.pop()
                self.shape_Id_list_index -= 1
                #self.undo_redo_action(undo_object_current=undo_object_current,undo_object_id=undo_object_id , shape_id_current=shape_id_current)
                if   (undo_object_current[0]   == 'fill'):
                    self.drawing_frame.itemconfig(shape_id_current, fill=undo_object_id[4])
                elif (undo_object_current[0] == 'text' or undo_object_id[0] == 'line'):
                    self.drawing_frame.itemconfig(shape_id_current, fill='white')
                else:
                    self.drawing_frame.itemconfig(shape_id_current, fill='white')
                    self.drawing_frame.itemconfig(shape_id_current, outline='white')

                # self.drawing_frame.delete(self.item_ref[-1])
                # self.drawing_frame.configure(self.shape_details_Dictionary)
                # self.undo_Drawing = [self.undo_drawing_id_list.popitem()]


    # Function Redo to reteive last deleted item
    def redo_Drawing(self):
        #if(len(self.redo_drawing_id_list) > 0 and len(self.redo_drawing_id_list) <= len(self.shape_details_Dictionary)):
        print('len redo=',len(self.redo_drawing_id_list), self.shape_Id_list_index)
        if(len(self.redo_drawing_id_list) > (self.shape_Id_list_index )):
            print('shape_Id_list_index=',self.shape_Id_list_index,'' ,self.redo_drawing_id_list )
            redo_shape_id_current    = self.redo_drawing_id_list[self.shape_Id_list_index]
            redo_shape_id            = self.redo_drawing_id_list[self.shape_Id_list_index]
            redo_shape_id_current    = self.shape_id_split(redo_shape_id_current)
            redo_object_id   = self.shape_details_Dictionary[redo_shape_id]
            print('redo dict = ', self.shape_details_Dictionary, redo_shape_id, redo_shape_id_current)
            print('redo object=', redo_object_id )
            self.shape_Id_list_index +=1
            #self.undo_redo_action(undo_object_current=redo_object_id, shape_id_current=redo_shape_id_current)
            #print('',self.shape_details_Dictionary)
            if (redo_object_id[0] == 'fill'):
                self.drawing_frame.itemconfig(redo_shape_id_current, fill= redo_object_id[4])
            elif(redo_object_id[0] == 'text'):
                shape_coords= redo_object_id[1]
                print('shape coords=', shape_coords)
                self.create_shape_text(fill=redo_object_id[4], text= redo_object_id[5],
                                       x1=shape_coords[0],
                                       y1=shape_coords[2],
                                       font=redo_object_id[6])
            elif( redo_object_id[0] == 'line'):
                self.drawing_frame.itemconfig(redo_shape_id_current, fill='white')
            else:
                self.drawing_frame.itemconfig(redo_shape_id_current, fill='white')
                self.drawing_frame.itemconfig(redo_shape_id_current, outline='white')


    def program_exit(self, **kwds):
        if (len(self.shape_details_Dictionary) > 0):
            msg = messagebox.askquestion('Exit?', 'Do you want to save your file (Yes or No)')
            if msg == 'yes':
                if (self.file_name is None):
                        self.save_as_file(root= kwds['root'])
                else:
                    self.save_file(root=kwds['root'])

        self.db_conn.close()
        kwds['root'].destroy()

    def new_file(self, **kwds):
        self.drawing_frame.delete('all')
        self.window_name( image_name='', root=kwds['root'])
        self.shape_details_Dictionary  = {} #Saving all details for shapes drawn on Canvas
        self.undo_drawing_id_list     = [] # Used for Undo drawing IDs
        self.redo_drawing_id_list = []  # Used for Redo drawing IDs
        #self.drawing_frame.configure(state=DISABLED)

    def print_file(self):
        if (self.file_name is not None):
            win32api.ShellExecute(0, "print", self.file_name, None, None, 0)

    def save_file_name(self):
        time_var = time.time()
        date_var = str(datetime.datetime.fromtimestamp(time_var).strftime('%Y-%m-%d %H:%M:%S'))
        file_name = (self.full_file_name, date_var, date_var);
        self.insert_file_name(self.db_conn, file_name)

    def open_file(self, file_name=None, **kwds):
        if(file_name == None):
            self.file_name = filedialog.askopenfilename(
            filetypes=(("PNG", "*.png"), ("Gif", "*.gif"), ("Jpeg", "*.jpg"), ("All Files", "*.*")))
        else:
            self.file_name =''.join(file_name)

        load = Image.open(self.file_name)
        self.full_file_name =self.file_name
        self.file_name = os.path.basename(self.file_name)
        self.window_name(self.file_name, root=kwds['root'])
        image_x = load.size[0]//2
        image_y = load.size[1]//2
        self.image_render = ImageTk.PhotoImage(load)
        self.drawing_frame.create_image(image_x, image_y , image= self.image_render)
        #Save file name in DB to be listed in Recent files
        self.save_file_name()
        self.delete_db()
        load.close()

    def save_file(self, **kwds):
        if self.file_name is not None:
             canvas = self._canvas()  # Get Window Coordinates of Canvas
             self.grabcanvas = ImageGrab.grab(bbox=canvas)
             self.grabcanvas.save(self.file_name)
             self.file_name = os.path.basename(self.file_name)
             self.window_name(image_name=self.file_name , root=kwds['root'])
        else:
            self.save_as_file(root=kwds['root'])

    def save_as_file(self, **kwds):
        self.file_name = filedialog.asksaveasfilename(title='Save as Image',
                                                filetypes=[('JPG', '.jpg'), ('PNG', '.png'), ('all files', '.*')],
                                                defaultextension=".png")

        if self.file_name is not None:
            self.full_file_name = str('\''+self.file_name+'\'')
            canvas = self._canvas()  # Get Window Coordinates of Canvas
            self.grabcanvas = ImageGrab.grab(bbox=canvas)
            self.grabcanvas.save(self.file_name)
            self.file_name = os.path.basename(self.file_name)
            self.window_name(image_name=self.file_name , root=kwds['root'])

# class menu for creating all menus and items , start here


# class widgets for all widgets start here
class My_widgets(My_menus):
    def __init__(self, **kwds):
        super(My_widgets, self).__init__(**kwds)

        # color dictionary
        self.color_dict = {
            'white': 'white',
            'black': 'black',
            'green': 'green',
            'blue': 'blue',
            'cyan': 'cyan',
            'magenta': 'magenta',
            'red': 'red',
            'yellow': 'yellow',
            'pink': 'pink',
            'gray': 'gray',
            'silver': 'silver',
            'brown': 'brown',
            'light blue': 'light blue'
        }

        self.drawing_area_frame(kwds['root'])
        self.drawing_tools(kwds['root'])

    def drawing_area_frame(self, root):

        for b in [self.drawing_frame]:
            b.bind("<1>", lambda e: self.button_press(e), '+')

        self.drawing_frame.bind_all('<Control-o>', lambda e: self.open_file(root=root), '+')
        self.drawing_frame.bind_all('<Control-s>', lambda e: self.save_file(root = root), '+')
        self.drawing_frame.bind('<3>', lambda e: self.popup_menu(e), '+')
        self.drawing_frame.bind('<ButtonRelease>', lambda e: self.stop_selection(e), '+')
        self.drawing_frame.bind("<B1-Motion>", lambda e: self.draw_shape_parameters(e), '+')
        self.shape = 'status'
        self.drawing_frame.bind('<Motion>', lambda e: self.Status_mouse_axis(e), '+')
        #self.drawing_frame.bind('<Motion>', lambda e:self.shape_text(e),'+')

    #Function to create buttons for colors in drawing tools area
    def button_tools(self, button_root, button_color, button_row, button_column):
        self.button = Button(button_root,
                             activebackground=button_color,
                             takefocus=0,
                             background=button_color,
                             command=lambda: self.color_change(button_color))
        self.button.grid(row=button_row, column=button_column, ipadx=20, ipady=7, pady=1)
        self.label = Label(self.button, width=5, height=1, relief=FLAT, bg='white', fg=button_color)
        self.label.bind('<1>', lambda e: self.color_change(button_color), '+')
        self.button.bind('<Motion>', lambda e: self.Show_tooltip(e, text=button_color), '+')
        self.button.bind('<Leave>', lambda e: self.Hide_tooltip(e), '+')

    def color_change(self, color):
        self.drawing_color   = color

    def Hide_tooltip(self, event):
        self.label.place_forget()

    def Show_tooltip(self, event, text):
        self.label['text'] = text
        event_x = event.x
        event_y = event.y
        self.label.place(x=event_x, y=event_y - 20)

    def drawing_tools(self, root):
        # Drawing panel frame start
        # Tool tip to be shown on mouse movement

        x = 0
        y = 0
        for i, j in self.color_dict.items():
            self.button_tools(button_root=self.tools_frame, button_row=y, button_column=x, button_color=j)
            if (x < 4):
                x += 1
            else:
                x = 0
                y += 1


        self.open_image = Image.open('line.png')
        self.logo1 = ImageTk.PhotoImage(self.open_image)
        self.label_line = Button(self.tools_frame,
                                 image=self.logo1,
                                 command=lambda : self.shape_choose(shape_type= 'line'))
        self.label_line.image = self.logo1
        self.label_line.grid(row=5, column=0)

        self.open_image = Image.open('eraser.png')
        self.logo2 = ImageTk.PhotoImage(self.open_image)
        self.label_eraser = Button(self.tools_frame,
                                   image=self.logo2,
                                   command=lambda : self.shape_choose(shape_type= 'eraser'))
        self.label_eraser.image = self.logo2
        self.label_eraser.grid(row=5, column=1)

        self.open_image = Image.open('fill_color.png')
        self.logo3 = ImageTk.PhotoImage(self.open_image)
        self.label_fill_color = Button(self.tools_frame,
                                       image=self.logo3,
                                       command=lambda : self.shape_choose( shape_type= 'fill'))
        self.label_fill_color.image = self.logo3
        self.label_fill_color.grid(row=5, column=2)

        self.open_image = Image.open('pen.png')
        self.logo4      = ImageTk.PhotoImage(self.open_image)
        self.label_pen  = Button(self.tools_frame,
                                 image=self.logo4,
                                 command=lambda : self.shape_choose(shape_type= 'pen'))
        self.label_pen.image = self.logo4
        self.label_pen.grid(row=5, column=3)

        self.open_image = Image.open('rectangle.png')
        self.logo5      = ImageTk.PhotoImage(self.open_image)
        self.label_rectangle = Button(self.tools_frame,
                                      image=self.logo5,
                                      command=lambda : self.shape_choose(shape_type='rectangle'))
        self.label_rectangle.image = self.logo5
        self.label_rectangle.grid(row=5, column=4)

        self.open_image = Image.open('oval.png')
        self.logo6      = ImageTk.PhotoImage(self.open_image)
        self.label_oval = Button(self.tools_frame,
                                 image=self.logo6,
                                 command=lambda : self.shape_choose(shape_type='oval'))
        self.label_oval.image = self.logo6
        self.label_oval.grid(row=6, column=0)

        self.open_image = Image.open('text.png')
        self.logo7 = ImageTk.PhotoImage(self.open_image)
        self.label_text = Button(self.tools_frame,
                                 image=self.logo7,
                                 command=lambda: self.draw_text())
        self.label_text.image = self.logo7
        self.label_text.grid(row=6, column=1)
        #
        self.open_image = Image.open('select_all.png')
        self.logo8 = ImageTk.PhotoImage(self.open_image)
        self.label_select_all = Button(self.tools_frame,
                                       image=self.logo8,
                                       command=lambda : self.shape_choose(shape_type= 'select_all'))
        self.label_select_all.image = self.logo8
        self.label_select_all.grid(row=6, column=2)

        self.myScale = Scale(
            self.tools_frame, from_=1, to=25,
            orient=HORIZONTAL,
            command=self.setThickness
        )
        self.myScale.set(2)
        self.widthThickness = 2
        shape_label = Label(self.tools_frame, text='Shape Width', bg='red')
        shape_label.grid(row=7, column=0,columnspan=1, sticky=SW)
        self.myScale.grid(
            row=7, column=1,columnspan=3,
            pady=0, padx=0, sticky=W,
        )
# class widgets for all widgets end here


# Class my actions for all functions and related actions
class My_actions(My_widgets):
    def __init__(self, **kwds):
        super(My_actions, self).__init__(**kwds)
        self.shape_details_Dictionary = {}  #Save IDs and other details for all obejcts drawn on Canvas
        self.undo_drawing_id_list = []   #Used for Undo drawing IDs
        self.redo_drawing_id_list = []  # Used for Redo drawing IDs
        self.image_render = None
        self.text_entry   = None
        self.text_button  = None
        self.shape_status = None
        self.fontMenu_value = 1
        self.rootFrame  = kwds['root']
        self.shape_type ='line'
        self.drawing_color = 'blue'  # Global variable for the color for all drawing tools

    def setThickness(self, event):
        self.widthThickness = self.myScale.get()


    def _canvas(self):
        x=self.drawing_frame.winfo_rootx()+self.drawing_frame.winfo_x()
        y=self.drawing_frame.winfo_rooty()+self.drawing_frame.winfo_y()
        x1=x+self.drawing_frame.winfo_width()
        y1=y+self.drawing_frame.winfo_height()

        box=(x,y,x1,y1)
        return box

    #         self.drawing_frame.create_text(370, 490, text = image_file)
    #         self.text_entry.insert(END, image_file)

    def program_destroy(self):
        print('Done')


    #Adding details about Undo & Redo in Dictionary
    def undo_redo_dictionary_update(self, **kwds):
        self.shape_details_Dictionary.update({kwds['shape_id'] :  [kwds['shape_type'],
                                                                   kwds['shape_coords'],
                                                                   kwds['shape_thickness'],
                                                                   kwds['shape_outline'],
                                                                   kwds['shape_color'],
                                                                   kwds['shape_text'],
                                                                   kwds['shape_font']
                                                                   ]})
        self.undo_drawing_id_list.append(kwds['shape_id'])
        self.redo_drawing_id_list.append(kwds['shape_id'])
        self.shape_Id_list_index +=1# len(self.shape_details_Dictionary)

    def shape_fill(self):
        num='0'
        if (self.drawing_frame.find_withtag(CURRENT)):
            object_id = list(self.drawing_frame.find_withtag(CURRENT))
            self.drawing_frame.itemconfig(object_id, fill=self.drawing_color  )
            object_id = str(str(object_id[0] )+'-'+ str(self.shape_Id_list_index))
            if(object_id > num):
                    self.undo_redo_dictionary_update(shape_id=object_id,
                                                     shape_type= 'fill',
                                                     shape_coords=None,
                                                     shape_thickness=None,
                                                     shape_outline=None,
                                                     shape_color=self.drawing_color,
                                                     shape_text=None,
                                                     shape_font=None)
            #self.shape_details_Dictionary.update({object_ref_fill : [self.shape, shape_old_fill, self.drawing_color  ] })
            # self.undo_drawing_id_list.append(object_id)
            # self.redo_drawing_id_list.append(object_id)
            # self.shape_Id_list_index = len(self.shape_details_Dictionary)

    def button_press(self, event):
        self.event_prev   = event
        self.shape_status = True
        self.shape_Id = 0
        self.delete_selection_rectangle()
        self.pop_up_menu.place_forget()
        self.shape_fill()


    #Get object id, coordinates, type, thickness and color
    def shape_click_parameters(self):
        if (self.drawing_frame.find_withtag(CURRENT)):
            #Saving object id
            self.object_ref          = self.drawing_frame.find_withtag(CURRENT)
            #Get object coordinates for object under mouse arrow
            self.object_coords       = self.drawing_frame.bbox(self.object_ref)
            # Get object type for object under mouse arrow
            self.object_type         = self.drawing_frame.type(self.object_ref)
            #Save object width (thickness)
            self.object_thickness    = self.drawing_frame.itemcget(self.object_ref, 'width')
            #Save object color
            self.drawing_color  = self.drawing_frame.itemcget(self.object_ref, 'fill')


    def popup_menu(self, event):
        self.event_new = event
        self.pop_up_menu.place(x=self.event_new.x, y=self.event_new.y)

    def Status_mouse_axis(self, event):
        self.event_new = event
        self.status_label['text'] = ('Mouse Axis : ', self.event_new.x, ':', self.event_new.y)
        self.status_label.place(x=155, y=1)

    def delete_shape(self, shape_Id):
        self.drawing_frame.delete(shape_Id)

    def delete_selection_rectangle(self):
        self.drawing_frame.delete('sel_rect')

    def stop_selection(self, event):
        self.start_selection = None
        self.shape_status = False

    def select_all(self, event_new_x, event_new_y):
        #self.event_new = event
        if (self.start_selection == None):
            self.start_selection = [event_new_x, event_new_y]

        sel_x = event_new_x
        sel_y = event_new_y

        self.delete_selection_rectangle()

        dashes = [2, 3]

        self.drawing_frame.create_rectangle(self.start_selection, sel_x, sel_y, dash=dashes, tags='sel_rect')

    def hide_Text_field(self):
        #self.setting_frame.grid_forget()
        self.text_button.lower(self.setting_frame)# .grid_forget()
        self.text_label.lower(self.setting_frame)
        self.text_entry.lower(self.setting_frame)
        self.x_entry.lower(self.setting_frame)
        self.y_entry.lower(self.setting_frame)
        self.x_Label.lower(self.setting_frame)
        self.y_Label.lower(self.setting_frame)
        self.font_OptionMenu.lower(self.setting_frame)
        self.font_OptionMenu_Label.lower(self.setting_frame)

    def show_Text_field(self):
        #self.setting_frame.grid_forget()
        self.text_button.lift(self.rootFrame)# .grid_forget()
        self.text_label.lift(self.rootFrame)
        self.text_entry.lift(self.rootFrame)
        self.x_entry.lift(self.rootFrame)
        self.y_entry.lift(self.rootFrame)
        self.x_Label.lift(self.rootFrame)
        self.y_Label.lift(self.rootFrame)
        self.font_OptionMenu.lift(self.rootFrame)
        self.font_OptionMenu_Label.lift(self.rootFrame)

    def get_Option_Menu_Value(self,value):
         self.fontMenu_value = format("Times %d" % value)

    #Create button, text field and labels to create TEXT
    def draw_text(self):

            self.text_label = Label(self.rootFrame, text='Text Field', bg='red')
            self.x_Label = Label(self.rootFrame, text='X :')
            self.y_Label = Label(self.rootFrame, text='Y :')
            self.font_OptionMenu_Label = Label(self.rootFrame, text='Font size:')

            self.text_entry = Entry(self.rootFrame)
            self.x_entry = Entry(self.rootFrame)
            self.y_entry = Entry(self.rootFrame)
            self.font_entry = StringVar(self.rootFrame)
            self.text_button = Button(self.rootFrame, text='Ok')

            font_option=[]
            for font_size in range(1,200,1):
                font_option.append(font_size)

            self.font_entry.set(font_option[0])  # default value

            self.font_OptionMenu = OptionMenu(self.rootFrame, self.font_entry, *font_option,
                                       command= lambda e:self.get_Option_Menu_Value(e))

            self.text_label.grid(row=0, column=0, columnspan=1, sticky=W, in_= self.setting_frame)
            self.text_entry.grid(row=0, column=1, columnspan=3, sticky=W, in_= self.setting_frame)
            self.text_button.grid(row=0, column=3, columnspan=1, sticky=W, in_= self.setting_frame)
            self.x_Label.grid(row=1, column=0, columnspan=2, sticky=W, in_= self.setting_frame)
            self.x_entry.grid(row=1, column=1, columnspan=2, sticky=W, in_= self.setting_frame)
            self.y_Label.grid(row=2, column=0, columnspan=2, sticky=W, in_= self.setting_frame)
            self.y_entry.grid(row=2, column=1, columnspan=2, sticky=W, in_= self.setting_frame)
            self.font_OptionMenu_Label.grid(row=3, column=0, columnspan=2, sticky=W, in_= self.setting_frame)
            self.font_OptionMenu.grid(row=3, column=1, columnspan=2, sticky=W, in_= self.setting_frame)

            self.text_button.bind('<1>', lambda e:self.create_shape_text(x1=self.x_entry.get(),
                                                                         y1=self.y_entry.get(),
                                                                         fill=self.drawing_color  ,
                                                                        text=self.text_entry.get(),
                                                                         font= self.fontMenu_value), '+')
            self.text_entry.bind('<Return>', lambda e:self.create_shape_text(fill=self.drawing_color  ,
                                                                        text=self.text_entry.get()), '+')
            self.x_entry.bind('<Return>', lambda e:self.create_shape_text(fill=self.drawing_color  ,
                                                                        text=self.text_entry.get()), '+')
            self.y_entry.bind('<Return>', lambda e:self.create_shape_text(fill=self.drawing_color  ,
                                                                        text=self.text_entry.get()), '+')

        #return text_entry.get()
    #Create text on canvas
    def create_shape_text(self, **kwds):

            x1 = kwds['x1']
            y1 = kwds['y1']

            self.shape_Id = self.drawing_frame.create_text(x1,y1,
                                                           text = kwds['text'],
                                                           font=kwds['font'],
                                                           fill=kwds['fill'])
            #self.shape='text'
            shape_coords = self.drawing_frame.bbox (self.shape_Id) #self.x_entry.get(), self.y_entry.get())

            #Call undo redo function to save data in shape dictionary
            self.undo_redo_dictionary_update(shape_id        = self.shape_Id,
                                             shape_type      = 'text',
                                             shape_coords    = shape_coords,
                                             shape_thickness = None,
                                             shape_outline   = None,
                                             shape_color     = kwds['fill'],
                                             shape_text      = kwds['text'],
                                             shape_font      = kwds['font'])

            self.hide_Text_field()

    def shape_choose(self, shape_type):
        self.shape_type = shape_type


    # Preparing all required parameters to call Draw shape function
    def draw_shape_parameters(self,event):
        if (self.shape_type is not 'select_all' and self.shape_type is not 'fill' and self.shape_type is not 'text'):
            self.drawing_frame.create_line(self.event_prev.x, self.event_prev.y, self.event_prev.x + 1,
                                           self.event_prev.y + 1,
                                           width=self.widthThickness, fill=self.drawing_color)

        self.shape_click_parameters()
        self.event_new = event
        # self.event_prev_x = self.event_prev.x
        # self.event_prev_y = self.event_prev.y
        self.Draw_shape(shape_type     = self.shape_type ,
                        event_new_x    = self.event_new.x,
                        event_prev_x   = self.event_prev.x,
                        event_new_y    = self.event_new.y,
                        event_prev_y   = self.event_prev.y,
                        widthThickness = self.widthThickness,
                        color_box      = self.drawing_color  )

    #TO draw all shapes and text and also to change color
    def Draw_shape(self, **kwds ):

        if (self.shape_status == True and kwds['shape_type'] != 'text'):

            # If new shape has been drawn on Canvas remove all shadows and delete IDs from shape_details_Dictionary
            self.delete_shape(self.shape_Id)
            if (len(self.shape_details_Dictionary) > 0 and int(self.shape_Id) > 0):
                self.shape_details_Dictionary.pop(self.shape_Id)
                self.undo_drawing_id_list.remove(self.shape_Id)
                self.redo_drawing_id_list.remove(self.shape_Id)

        #Draw rectangle on Canvas
        if (kwds['shape_type'] == 'rectangle'):
            self.shape_Id = self.drawing_frame.create_rectangle(kwds['event_prev_x'], kwds['event_prev_y'], kwds['event_new_x'] + 1,
                                                             kwds['event_new_y'] + 1, width= kwds['widthThickness'],
                                                             fill= kwds['color_box'],
                                                             outline= kwds['color_box'])
        #Eraser to delete objects drawn on Canvas
        elif (kwds['shape_type'] == 'eraser'):
            self.drawing_frame.create_rectangle(kwds['event_prev_x'], kwds['event_prev_y'], kwds['event_new_x'] + 1,
                                             kwds['event_new_y'] + 1,
                                             width= kwds['widthThickness'],
                                             fill='white',
                                             outline='white')
        # Draw line on Canvas
        elif (kwds['shape_type'] == 'line'):
            self.shape_Id = self.drawing_frame.create_line(kwds['event_prev_x'], kwds['event_prev_y'], kwds['event_new_x'] + 1,
                                                        kwds['event_new_y'] + 1,
                                                        width= kwds['widthThickness'],
                                                        fill= kwds['color_box'])
        # Draw oval on Canvas
        elif (kwds['shape_type'] == 'oval'):
            self.shape_Id = self.drawing_frame.create_oval(kwds['event_prev_x'],
                                                           kwds['event_prev_y'],
                                                           kwds['event_new_x'] + 1,
                                                           kwds['event_new_y'] + 1,
                                                           width   = kwds['widthThickness'],
                                                           fill    =  kwds['color_box'],
                                                           outline = kwds['color_box'])

        # Draw pixels on Canvas
        elif (kwds['shape_type'] == 'pen'):
            self.shape_Id = self.drawing_frame.create_line(kwds['event_prev_x'],
                                                           kwds['event_prev_y'],
                                                           kwds['event_new_x'] + 1,
                                                           kwds['event_new_y'] + 1,
                                                           width=kwds['widthThickness'],
                                                           fill=kwds['color_box'])
            self.event_prev.x = kwds['event_new_x']
            self.event_prev.y = kwds['event_new_y']

        elif (kwds['shape_type'] == 'select_all'):
            self.select_all(kwds['event_new_x'], kwds['event_new_y'])

        #Get latest coordinates for drawn shape
        shape_coords = ( kwds['event_prev_x'], kwds['event_prev_y'], kwds['event_new_x'] + 1, kwds['event_new_y'] + 1)
        #Save shape Id and details in shape_details_Dictionary
        self.shape_Id = str(self.shape_Id)
        #Call undo redo function to save data in Shape dictionary
        num = '0'
        if(self.shape_Id > num):
                self.undo_redo_dictionary_update(shape_id      = self.shape_Id,
                                                 shape_type    = kwds['shape_type'],
                                                 shape_coords  = shape_coords,
                                                 shape_thickness = kwds['widthThickness'],
                                                 shape_outline = kwds['color_box'],
                                                 shape_color   = kwds['color_box'],
                                                 shape_text    = None,
                                                 shape_font    = None)

# class my actions end here

class Drawingpad(My_actions):
    global mouse_axis  # list to save all mouse events (x,y) while moving the mouse

    def insert_file_name(self, conn, date_var):
        """
        Insert data to file_name table
        """
        sql = ''' INSERT INTO drawingpad_filename_db(file_name,begin_date,update_date)
                  VALUES(?,?,?) '''

        cur = conn.cursor()
        cur.execute(sql, date_var)
        conn.commit()


    def create_fileName_table(self, conn, create_table_sql):
        """
        create a table file_name for drawingpad
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def delete_db(self):
        sql_select = "select file_name from drawingpad_filename_db"
        sql_delete = "DELETE FROM drawingpad_filename_db"
        cur = self.db_conn.cursor()
        result = cur.execute(sql_select)
        rows = len(result.fetchall())
        if (rows > 10):
            cur = self.db_conn.cursor()
            result = cur.execute(sql_delete)
            self.db_conn.commit()

    def create_connection(self,db_file):
        """ create a database connection to a SQLite database """
        try:
            self.db_conn = sqlite3.connect(db_file)
            return self.db_conn
        except Error as e:
            print(e)
        return None

    def __init__(self, **kwds):
        self.window_name(root=kwds['root'])
        self.window_size_x = 0
        self.window_size_y = 0
        self.start_selection = None
        self.white_color = (255, 255, 255)
        self.file_name = None


        self.status_frame_width = int(kwds['root'].winfo_screenwidth() * 0.108)



        self.database_name = "C:\\Users\\pc\\Documents\\Yamin\\Python\\Games\\Drawingpad\\db\\drawingpad_db.db"
        self.db_conn=None
        self.full_file_name=None

        self.Cut=0

        sql_create_drawingpad_file_name_table = """ CREATE TABLE IF NOT EXISTS drawingpad_filename_db (
                                                id integer PRIMARY KEY,
                                                file_name text NOT NULL,
                                                begin_date text,
                                                update_date text
                                            ); """

        # create a database connection
        self.db_conn = self.create_connection(self.database_name)
        if self.db_conn is not None:
            # create table to save file name for drawing pad
            self.create_fileName_table(self.db_conn, sql_create_drawingpad_file_name_table)
            # self.delete_db()


        kwds['root'].geometry("%dx%d+%d+%d" % (kwds['root'].winfo_screenwidth(),
                                               kwds['root'].winfo_screenheight(),
                                               self.window_size_x,
                                               self.window_size_y))
        super(Drawingpad, self).__init__(**kwds)
        # atexit.register(lambda: self.program_exit(root=kwds['root']))


    def window_name(self, image_name='',**kwds):

        if image_name is not '':
            window_name = "Yamin\'s Drawing Pad, Image Name: " + image_name

        else:
            window_name = "Yamin\'s Drawing Pad"
        kwds['root'].title(window_name)

        # My_actions(root=root)

# class Drawingpad end here


class main_program:
    def __ini__(self):
        pass

    def main(self):
        root = Tk()

        Drawingpad(root=root)

        root.mainloop()


main = main_program()
if __name__ == '__main__': main.main()
