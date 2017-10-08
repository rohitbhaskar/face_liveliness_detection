# -*- coding: utf-8 -*-
"""
Created on Sat Oct 07 12:52:01 2017

@author: Tanay Shah
"""

from pymongo import *
from bokeh.charts import Bar, output_file, show
import pandas as pd
import random
from datetime import datetime
import bokeh.plotting as bp
from bokeh.plotting import save
from bokeh.models import HoverTool
from bokeh.models import CustomJS , Rect
from bokeh.layouts import row , column
from bokeh.models.widgets import DataTable, TableColumn, Button
from bokeh.models.widgets import MultiSelect
from bokeh.models.widgets import Dropdown
from bokeh.models import  Callback, ColumnDataSource, Rect, Select,CustomJS
from bokeh.plotting import figure, output_file, show,  gridplot
from bokeh.models.widgets.layouts import VBox,HBox
import numpy as np

client = MongoClient('mongodb://user:abcd1234@testcluster-shard-00-00-7f3ht.mongodb.net:27017,testcluster-shard-00-01-7f3ht.mongodb.net:27017,testcluster-shard-00-02-7f3ht.mongodb.net:27017/pureregression?ssl=true&replicaSet=TestCluster-shard-0&authSource=admin')
db = client.pureregression
reccon  = db.transactions
from operator import itemgetter



reciever_acc = ["8353836353" , "3593537324" , "6309123956" ,"3428263300" , "8465589101" ,"8918640615" , "1662370641" , "3936456709" , "3132050691" , "4771819058"]
sender_acc = ["9353856354" , "2553577384" , "9009123556" ,"4728263300" , "5465589321" ,"6918640615" , "9062370641" , "2336456709" , "7832050691" , "6571819058"]
reciever_names= ["Amol" , "Anmol" , "Dhruv", "Ekansh" , "Karan", "Natesh" , "Omkar" , "Prit" , "Rushabh" , "Smitesh"]

sender_corresponding_loc =['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh','Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh','Ambegaon' , 'Gondiya']
sender_names = ["Sumod" , "Kishan", "Ishwar" , "Ramu" , "Gopal" , "Pawar" , "Urvil" , "Yash" , "Pandurang", "Manoj"]
goods= ["Clothes" , "Shoes" , "Grains" , "Pulses" , "Stationery" , "Vegetables" , "Fruits" , "Electronics" , "Utensils" , "Sugar"]
rate= [150 , 250 , 500 , 400 , 50 , 30 , 100 , 2000 , 800 , 80 ]

locations = ['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh']
transaction_methods = ['cash' , 'digital']
complete_sender_goods = {}


# For every user
for i in range(0 , 10):
    count_goods = list(reccon.find({"sender_name": sender_names[i]} , {"reciever_name":1 , "goods":1 , "quantity": 1, "rate": 1, "timestamp": 1 , "_id":0} ))
    count_goods = sorted(count_goods, key=itemgetter('timestamp'))
    
    
    # For every goods
    for k in range(0 , 10):
        summed_goods = {"Clothes":0 , "Shoes":0 , "Grains":0 , "Pulses":0 , "Stationery":0 , "Vegetables":0 , "Fruits":0 , "Electronics":0 , "Utensils":0 , "Sugar":0}
        
        # For every date
        for j in range(0 , len(count_goods)):
            summed_goods[count_goods[j]['goods']] += count_goods[j]['quantity'] * count_goods[j]['rate']
    complete_sender_goods[sender_names[i]] = summed_goods
    

complete_local_goods = {}
for i in range(0 , 4):
    count_goods = list(reccon.find({"location": locations[i]} , {"reciever_name":1 , "goods":1 , "quantity": 1, "rate": 1, "timestamp": 1 , "_id":0} ))
    count_goods = sorted(count_goods, key=itemgetter('timestamp'))
    summed_goods_arr=[]
    for k in range(0 , 10):
        summed_goods = {"Clothes":0 , "Shoes":0 , "Grains":0 , "Pulses":0 , "Stationery":0 , "Vegetables":0 , "Fruits":0 , "Electronics":0 , "Utensils":0 , "Sugar":0}
        
        for j in range(0 , len(count_goods)):
            summed_goods[count_goods[j]['goods']] += count_goods[j]['quantity'] * count_goods[j]['rate']
        
    complete_local_goods[locations[i]] = summed_goods
    
complete_reciever_goods = {}
for i in range(0 , 10):
    count_goods = list(reccon.find({"reciever_name": reciever_names[i]} , {"reciever_name":1 , "goods":1 , "quantity": 1, "rate": 1, "timestamp": 1 , "_id":0} ))
    count_goods = sorted(count_goods, key=itemgetter('timestamp'))
    summed_goods_arr=[]
    for k in range(0 , 10):
        summed_goods = {"Clothes":0 , "Shoes":0 , "Grains":0 , "Pulses":0 , "Stationery":0 , "Vegetables":0 , "Fruits":0 , "Electronics":0 , "Utensils":0 , "Sugar":0}
        
        for j in range(0 , len(count_goods)):
            summed_goods[count_goods[j]['goods']] += count_goods[j]['quantity'] * count_goods[j]['rate']
        
    complete_reciever_goods[reciever_names[i]] = summed_goods


p1 = figure(title="Goods Distribution by Locality", 
            plot_width=300, plot_height = 300,
            outline_line_color= None)

hardfound_colors = ["#DC143C", "#8B008B", "#0000FF", "#00F5FF", "#32CD32","#e3e300","#7514f6","#f0e68c","#FFFF00", "#FF9912"]

source= bp.ColumnDataSource({
    'x': [1, 2, 3, 4, 5, 6, 7, 8, 9,10 ],
    'y': [1, 12, 3, 14, 5, 6, 17, 8, 9,10 ],
    'complete_local_goods_devgadh': complete_local_goods['Devgadh'].values(),
    'complete_local_goods_ambegaon': complete_local_goods['Ambegaon'].values(),
    'complete_local_goods_gondiya': complete_local_goods['Gondiya'].values(),
    'complete_local_goods_rampur': complete_local_goods['Rampur'].values(),
    'sender_names': sender_names,
    'reciever_names': reciever_names,
    'goods': goods
})

menu_location = [("Ambegaon", "loc_1"), ("Gondiya", "loc_2"), ("Rampur", "loc_3") , ("Devgadh" , "loc_4")]
dropdown_location = Dropdown(label="Select Locality", button_type="warning", menu=menu_location)

dropdown_location.callback = CustomJS(args=dict(source=source), code="""
    var loc_arr = ['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh']
    var fa = cb_obj.value
    source['data']['index']= []
    console.log(fa)
    console.log(source.data)
    if (fa[4] ==1){
        var new_y = source.data.complete_local_goods_ambegaon.slice()
    }
    else if (fa[4] ==2){
        var new_y = source.data.complete_local_goods_gondiya.slice()
    }
    else if (fa[4] == 3){
        var new_y = source.data.complete_local_goods_rampur.slice()
    }
    else{
        var new_y = source.data.complete_local_goods_devgadh.slice()
    }
    for (j=0 ; j< 10 ; j++){
        source['data']['index'].push(j)    
    }
    console.log(source.data)
    source.data.y = new_y
    source.trigger('change')
        
    """
)



source1= bp.ColumnDataSource({
    'x': [1, 2, 3, 4, 5, 6, 7, 8, 9,10 ],
    'y': [1, 12, 3, 14, 5, 6, 17, 8, 9,10 ],
    'complete_sender_goods_1': complete_sender_goods['Gopal'].values(),
    'complete_sender_goods_2': complete_sender_goods['Ishwar'].values(),
    'complete_sender_goods_3': complete_sender_goods['Kishan'].values(),
    'complete_sender_goods_4': complete_sender_goods['Manoj'].values(),
    'complete_sender_goods_5': complete_sender_goods['Pandurang'].values(),
    'complete_sender_goods_6': complete_sender_goods['Pawar'].values(),
    'complete_sender_goods_7': complete_sender_goods['Ramu'].values(),
    'complete_sender_goods_8': complete_sender_goods['Sumod'].values(),
     'complete_sender_goods_9': complete_sender_goods['Urvil'].values(),
    'complete_seller_goods_10': complete_sender_goods['Yash'].values(),
    'sender_names': sender_names,
    'reciever_names': reciever_names,
    'goods': goods
})

menu_seller = [("Gopal" ,"rcv_0") , ("Ishwar" , "rcv_1") , ("Kishan" , "rcv_2"), ("Manoj" , "rcv_3") , ("Pandurang", "rcv_4"), ("Pawar" , "rcv_5") , ("Ramu" , "rcv_6") , ("Sumod" ,"rcv_7") , ("Urvil" , "rcv_8") , ("Yash" , "rcv_9")]
dropdown_seller = Dropdown(label="Select Buyers", button_type="warning", menu=menu_seller)

dropdown_seller.callback = CustomJS(args=dict(source=source1), code="""
    var loc_arr = ['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh']
    var fa = cb_obj.value
    source['data']['index']= []
    console.log(fa)
    console.log(source.data)
    if (fa[4] ==0){
        var new_y = source.data.complete_sender_goods_1.slice()
    }
    else if (fa[4] ==1){
        var new_y = source.data.complete_sender_goods_2.slice()
    }
    else if (fa[4] == 2){
        var new_y = source.data.complete_sender_goods_3.slice()
    }
     else if (fa[4] == 3){
        var new_y = source.data.complete_sender_goods_4.slice()
    }
     else if (fa[4] == 4){
        var new_y = source.data.complete_sender_goods_5.slice()
    }
     else if (fa[4] == 5){
        var new_y = source.data.complete_sender_goods_6.slice()
    }
     else if (fa[4] == 6){
        var new_y = source.data.complete_sender_goods_7.slice()
    } 
    else if (fa[4] == 7){
        var new_y = source.data.complete_sender_goods_8.slice()
    }
    else if (fa[4] == 8){
        var new_y = source.data.complete_sender_goods_9.slice()
    }
    else{
        var new_y = source.data.complete_sender_goods_10.slice()
    }
    for (j=0 ; j< 10 ; j++){
        source['data']['index'].push(j)    
    }
    console.log(source.data)
    source.data.y = new_y
    source.trigger('change')
        
    """
)

source2= bp.ColumnDataSource({
    'x': [1, 2, 3, 4, 5, 6, 7, 8, 9,10 ],
    'y': [1, 12, 3, 14, 5, 6, 17, 8, 9,10 ],
    'complete_reciever_goods_1': complete_reciever_goods['Amol'].values(),
    'complete_reciever_goods_2': complete_reciever_goods['Anmol'].values(),
    'complete_reciever_goods_3': complete_reciever_goods['Dhruv'].values(),
    'complete_reciever_goods_4': complete_reciever_goods['Ekansh'].values(),
    'complete_reciever_goods_5': complete_reciever_goods['Karan'].values(),
    'complete_reciever_goods_6': complete_reciever_goods['Natesh'].values(),
    'complete_reciever_goods_7': complete_reciever_goods['Omkar'].values(),
    'complete_reciever_goods_8': complete_reciever_goods['Prit'].values(),
     'complete_reciever_goods_9': complete_reciever_goods['Rushabh'].values(),
    'complete_reciever_goods_10': complete_reciever_goods['Smitesh'].values(),
    'sender_names': sender_names,
    'reciever_names': reciever_names,
    'goods': goods
})

menu_reciever = [("Amol" ,"rcv_0") , ("Anmol" , "rcv_1") , ("Dhruv" , "rcv_2"), ("Ekansh" , "rcv_3") , ("Karan", "rcv_4"), ("Natesh" , "rcv_5") , ("Omkar" , "rcv_6") , ("Prit" ,"rcv_7") , ("Rushabh" , "rcv_8") , ("Smitesh" , "rcv_9")]
dropdown_reciever = Dropdown(label="Select Sellers", button_type="warning", menu=menu_reciever)

dropdown_seller.callback = CustomJS(args=dict(source=source2), code="""
    var loc_arr = ['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh']
    var fa = cb_obj.value
    source['data']['index']= []
    console.log(fa)
    console.log(source.data)
    if (fa[4] ==0){
        var new_y = source.data.complete_reciever_goods_1.slice()
    }
    else if (fa[4] ==1){
        var new_y = source.data.complete_reciever_goods_2.slice()
    }
    else if (fa[4] == 2){
        var new_y = source.data.complete_reciever_goods_3.slice()
    }
     else if (fa[4] == 3){
        var new_y = source.data.complete_reciever_goods_4.slice()
    }
     else if (fa[4] == 4){
        var new_y = source.data.complete_reciever_goods_5.slice()
    }
     else if (fa[4] == 5){
        var new_y = source.data.complete_reciever_goods_6.slice()
    }
     else if (fa[4] == 6){
        var new_y = source.data.complete_reciever_goods_7.slice()
    } 
    else if (fa[4] == 7){
        var new_y = source.data.complete_reciever_goods_8.slice()
    }
    else if (fa[4] == 8){
        var new_y = source.data.complete_reciever_goods_9.slice()
    }
    else{
        var new_y = source.data.complete_sender_goods_10.slice()
    }
    for (j=0 ; j< 10 ; j++){
        source['data']['index'].push(j)    
    }
    console.log(source.data)
    source.data.y = new_y
    source.trigger('change')
        
    """
)
            
p = figure(plot_width=400, plot_height=400 ,  title="Locality Goods wise sale Insights", y_range = (0 , 15000) , x_axis_label = "goods" , y_axis_label = 'Sales')
p.rect(x=[1, 2, 3 , 4, 5, 6 ,7 ,8 ,9, 10], y=0.5*np.array(complete_local_goods['Ambegaon'].values()), width=1, height=complete_local_goods['Ambegaon'].values(), color="#CAB2D6")

p1 = figure(plot_width=400, plot_height=400 ,  title="Seller Goods wise sale Insights", y_range = (0 , 15000), x_axis_label = "goods" , y_axis_label = 'Sales')
p1.rect(x=[1, 2, 3 , 4, 5, 6 ,7 ,8 ,9, 10], y=0.5*np.array(complete_sender_goods['Gopal'].values()), width=1, height=complete_sender_goods['Gopal'].values(), color="#00FF00")

p2 = figure(plot_width=400, plot_height=400 ,  title="Buyer Goods wise sale Insights", y_range = (0 , 15000), x_axis_label = "goods" , y_axis_label = 'Sales')
p2.rect(x=[1, 2, 3 , 4, 5, 6 ,7 ,8 ,9, 10], y=0.5*np.array(complete_reciever_goods['Amol'].values()), width=1, height=complete_reciever_goods['Amol'].values(), color="#FF0000")


hover_p = p.select(dict(type=HoverTool))
hover_p.tooltips = {"Goods": "@goods"}  

hover_p1 = p1.select(dict(type=HoverTool))
hover_p1.tooltips = {"Goods": "@goods"}  

hover_p2 = p2.select(dict(type=HoverTool))
hover_p2.tooltips = {"Goods": "@goods"}     
save(row(column(dropdown_location , p) , column(dropdown_seller , p1) , column(dropdown_reciever , p2)), 'dashboardGoods.html')
