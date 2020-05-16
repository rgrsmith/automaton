#!/usr/bin/env  python3

from tkinter import *

class GUI:
    def __init__(self,params):
        self.params = dict(params)
        self.params['reset'] = True
        self.slider_vals = [0.99999, 0.9999, 0.999, 0.99, 0.9, 0.5, 0.1, 0.01, 0.001, 0.0001, 0.00001, 'center']
        self.master = Tk()
        self.top_frame = Frame(self.master)
        self.top_frame.pack()
        self.bottom_frame = Frame(self.master)
        self.bottom_frame.pack(side=BOTTOM)
        self.right_frame = Frame(self.master)
        self.right_frame.pack(side=RIGHT)
        self.init_slider()
        self.init_button()
        self.init_rule_box()
        # self.update_gui()

    def print_all_params(self):
        for key,val in self.params.items():
            print("%s : %s" % (key, val))

    def init_slider(self):
        self.w1 = Scale(self.top_frame, orient=HORIZONTAL, bd=2, showvalue=0, label='init density', from_=0, to=len(self.slider_vals)-1, command=self.set_slider)
        self.text = Label(self.top_frame, font=('Arial',18), padx=50, pady=30)
        self.text.pack(side=TOP)
        self.w1.set(0)
        self.w1.pack()

    def init_rule_box(self):
        self.rule_box = Label(self.right_frame, text="Rule", padx=50, pady=30).grid(row=0)
        self.rule_box_entry = Entry(self.right_frame)
        #self.rule_box_entry.insert(END, '30')
        #self.rule_box_entry.pack()
        self.rule_box_entry.grid(row=0, column=1)

    def set_slider(self,val):
        if int(val) == len(self.slider_vals)-1:
            self.params['random_seed'] = None
            self.text.configure(text='%s   ' % self.slider_vals[int(val)])
        else:
            self.params['random_seed'] = self.slider_vals[int(val)]
            self.text.configure(text='%.5f' % self.slider_vals[int(val)])

    def init_button(self):
        self.button = Button(self.bottom_frame, text='Update', command=self.button_update).pack(side=BOTTOM)

    def update_gui(self):
        self.master.update_idletasks()
        self.master.update()

    def button_update(self):
        print(self.params)
        self.params['reset'] = True
        self.params['rule'] = int(self.rule_box_entry.get())

    def get_params(self):
        return self.params

    def set_params(self, params):
        self.params = dict(params)

    def add_param(self, key, val):
        self.params[key] = val
