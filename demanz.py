# -*- coding: utf-8 -*-
# (c) 2021 Allen D. Montgomery

from tkinter import Tk, Text
from tkinter import filedialog as fd
from tkinter.ttk import Frame, Label, Entry, Button
from tkcalendar import Calendar
import pandas as pd

class App(Frame):

    def __init__(self):
        super().__init__()
        
        self.filetypes = (('CSV files', '*.csv'), ('All file types', '*.*'))
        self.sold_products = set()
        self.current_products = set()
        self.initUI()

    def initUI(self):

        self.master.title("Demanz Forecasting Tool (c) 2021    Allen D. Montgomery")
        self.grid()

        frame1 = Frame(self)
        frame1.grid(row = 0, column = 0, pady = 5)
        lbl1 = Label(frame1, text="Days in Period", width=24)
        lbl1.grid(row = 0, column = 0)
        self.period = Entry(frame1)
        self.period.grid(row = 0, column = 1)
        self.period.focus_set()

        frame2 = Frame(self)
        frame2.grid(row = 1, column = 0, pady = 5)
        lbl2 = Label(frame2, text="Forecast Multiplier", width=24)
        lbl2.grid(row = 0, column = 0)
        self.multiplier = Entry(frame2)
        self.multiplier.grid(row = 0, column = 1)
        
        frame3 = Frame(self)
        frame3.grid(row = 2, column = 0, pady = 5)
        lbl3 = Label(frame3, text="Forecast Increment", width=24)
        lbl3.grid(row = 0, column = 0)
        self.increment = Entry(frame3)
        self.increment.grid(row = 0, column = 1)
        
        github_text = Text(self, width = 35, height = 1, bg = 'cyan')
        github_text.insert('current', 'https://github.com/vegebond/Demanz')
        github_text['state'] = 'disabled'
        github_text.grid(row = 0, column = 1, columnspan = 2)

        linkedin_text = Text(self, width = 45, height = 1, bg = "cyan")
        linkedin_text.insert('current', 'https://www.linkedin.com/in/allenmontgomery/')
        linkedin_text['state'] = 'disabled'
        linkedin_text.grid(row = 2, column = 1, columnspan = 2)

        lcl1 = Label(self, text = "Count Date")
        lcl1.grid(row = 3, column = 0)
        self.count = Calendar(master = self)
        self.count.grid(row = 4, column = 0, padx = 10)

        lcl2 = Label(self, text = "Delivery Date")
        lcl2.grid(row = 3, column = 1)
        self.delivery1 = Calendar(master = self)
        self.delivery1.grid(row = 4, column = 1, padx = 10)

        lcl3 = Label(self, text = "Next Delivery")
        lcl3.grid(row = 3, column = 2)
        self.delivery2 = Calendar(master = self)
        self.delivery2.grid(row = 4, column = 2, padx = 10)

        sales_button = Button(self, text = "Read Sales", command = self.select_sold)
        sales_button.grid(row = 5, column = 0, pady = 10)

        current_button = Button(self, text = "Read Current", command = self.select_current)
        current_button.grid(row = 5, column = 1, pady = 10)

        savebutton = Button(self, text = "Save Results", command = self.writefile)
        savebutton.grid(row = 5, column = 2, pady = 10)

        self.sales_text = Text(self, height = 2, width = 30)
        self.sales_text['state'] = 'disabled'
        self.sales_text.grid(row = 6, column = 0, pady = 5)

        self.current_text = Text(self, height = 2, width = 30)
        self.current_text['state'] = 'disabled'
        self.current_text.grid(row = 6, column = 1)

        self.result_text = Text(self, height = 2, width = 30)
        self.result_text['state'] = 'disabled'
        self.result_text.grid(row = 6, column = 2)

        sales_orphan_label = Label(self, text = 'Sales Orphans')
        sales_orphan_label.grid(row = 7, column = 0)
        self.sales_orphan_text = Text(self, height = 8, width = 20, foreground = 'red')
        self.sales_orphan_text['state'] = 'disabled'
        self.sales_orphan_text.grid(row = 8, column = 0)

        current_orphan_label = Label(self, text = 'Current Orphans')
        current_orphan_label.grid(row = 7, column = 1)
        self.current_orphan_text = Text(self, height = 8, width = 20, foreground = 'red')
        self.current_orphan_text['state'] = 'disabled'
        self.current_orphan_text.grid(row = 8, column = 1)

    def orphans(self):
        sold_only = self.sold_products - self.current_products

        self.sales_orphan_text['state'] = 'normal'
        self.sales_orphan_text.delete('current', 'end')

        for x in list(self.sold_products - self.current_products):
            self.sales_orphan_text.insert('current', x + '\n')

        self.sales_orphan_text['state'] = 'disabled'

        self.current_orphan_text['state'] = 'normal'
        self.current_orphan_text.delete('current', 'end')

        for x in list(self.current_products - self.sold_products):
            self.current_orphan_text.insert('current', x + '\n')

        self.current_orphan_text['state'] = 'disabled'


    def select_sold(self):
        self.sold_file = fd.askopenfilename(filetypes = self.filetypes)

        self.sales_text['state'] = 'normal'
        self.sales_text.delete('current', 'end')
        self.sales_text.insert('current', self.sold_file)
        self.sales_text['state'] = 'disabled'

        self.sold_df = pd.read_csv(self.sold_file)
        self.sold_products = set(self.sold_df['product'])
        self.orphans()

    def select_current(self):
        self.current_file = fd.askopenfilename(filetypes = self.filetypes)

        self.current_text['state'] = 'normal'
        self.current_text.delete('current', 'end')
        self.current_text.insert('current', self.current_file)
        self.current_text['state'] = 'disabled'

        self.current_df = pd.read_csv(self.current_file)
        self.current_products = set(self.current_df['product'])
        self.orphans()

    def writefile(self):

        products = list(self.sold_products.intersection(self.current_products))
        products.sort()

        self.period1 = (self.delivery1.selection_get() - self.count.selection_get()).days
        self.period2 = (self.delivery2.selection_get() - self.delivery1.selection_get()).days
        self.days = float(self.period.get())
        
        forecast = pd.DataFrame(columns = ['median', 'adjusted', 'sales1', 'balance', 'sales2', 'purchase'], index = products)

        for x in products:
            forecast.at[x, 'median'] = float(self.sold_df[self.sold_df['product'] == x]['sold'].median())
            forecast.at[x, 'adjusted'] = forecast['median'][x] * float(self.multiplier.get()) + float(self.increment.get())
            forecast.at[x, 'sales1'] = round(forecast['adjusted'][x] * self.period1 / self.days)
            forecast.at[x, 'balance'] = float(self.current_df[self.current_df['product'] == x]['current']) - forecast['sales1'][x]
            forecast.at[x, 'sales2'] = round(forecast['adjusted'][x] * self.period2 / self.days)
            forecast.at[x, 'purchase'] = forecast['sales2'][x] - max(float(forecast['balance'][x]), 0)
        self.result_file = fd.asksaveasfilename(filetypes = self.filetypes)
        if (self.result_file.find('.') == -1 and self.result_file != ''):
            self.result_file += '.csv'

        self.result_text['state'] = 'normal'
        self.result_text.delete('current', 'end')
        self.result_text.insert('current', self.result_file)
        self.result_text['state'] = 'disabled'

        forecast.to_csv(self.result_file, index_label = 'product')

def main():

    root = Tk()
    root.geometry("819x580+50+50")
    app = App()
    root.mainloop()


if __name__ == '__main__':
    main()