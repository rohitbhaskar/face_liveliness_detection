# -*- coding: utf-8 -*-
"""
Created on Sat Oct 07 12:08:12 2017

@author: Tanay Shah
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 07 03:36:52 2017

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
from bokeh.models import CustomJS
from bokeh.layouts import row , column
from bokeh.models.widgets import DataTable, TableColumn, Button
from bokeh.models.widgets import MultiSelect
from bokeh.models.widgets import Dropdown

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

'''
#Adding data to DB
for j in range(0 , 100):
    goods_number = random.randint(0 , 9)
    reciever_number = random.randint(0 , 9)
    sending_method = transaction_methods[random.randint(0, 1)]
    recieving_method = transaction_methods[random.randint(0 , 1)]
    if (sending_method == 'cash' and recieving_method == 'cash') :
        recieving_method = 'digital'
    reccon.insert_one({
                        "sender_acc": sender_acc[random.randint(0 , 9)],
                        "reciever_acc": reciever_acc[reciever_number],
                        "sender_name": sender_names[random.randint(0 , 9)],
                        "reciever_name": reciever_names[random.randint(0 , 9)],
                        "goods": goods[goods_number],
                        "quantity" : random.randint(1, 5),
                        "rate":rate[goods_number] + random.randint(0 ,50),
                        "timestamp": str(datetime(2017 , random.randint(1 , 12) , random.randint(1 , 28) , 0, 0 ,0)),
                        "sending_method": sending_method,
                        "recieving_method": recieving_method,
                        "location": locations[reciever_number]
                     })
                     
'''
                 
#getting seller sales
count_sales = list(reccon.find({} , {"sender_name":1 , "goods":1 , "quantity": 1, "rate": 1, "timestamp": 1 , "_id":0} ))
count_sales = sorted(count_sales, key=itemgetter('timestamp'))
sales =[]
dates =[]
seller=[]
ind=[]
for i in range(0 , len(count_sales)):
    dates.append(i)
    ind.append(count_sales[i]['timestamp'][:10])
    sales.append(count_sales[i]['quantity']*count_sales[i]['rate'])
    seller.append(count_sales[i]['sender_name'])
sales_disp = pd.DataFrame()
sales_disp['sales'] = sales
sales_disp['date'] = dates
sales_disp['seller'] = seller
sales_disp['ind'] = ind

#getting cash details
count_cash = list(reccon.find({"sending_method" : "cash"} , {"sender_name":1 , "goods":1 , "quantity": 1, "rate": 1, "timestamp": 1 , "_id":0} ))
count_cash = sorted(count_cash, key=itemgetter('timestamp'))
sales =[]
dates =[]
seller=[]
ind=[]
for i in range(0 , len(count_cash)):
    dates.append(i)
    ind.append(count_cash[i]['timestamp'][:10])
    sales.append(count_cash[i]['quantity']*count_cash[i]['rate'])
    seller.append(count_cash[i]['sender_name'])
cash_disp = pd.DataFrame()
cash_disp['cash'] = sales
cash_disp['date'] = dates
cash_disp['seller'] = seller
cash_disp['ind'] = ind

#getting digital trnx details
#getting seller sales
count_digi = list(reccon.find({"sending_method" : "digital"} , {"sender_name":1 , "goods":1 , "quantity": 1, "rate": 1, "timestamp": 1 , "_id":0} ))
count_digi = sorted(count_digi, key=itemgetter('timestamp'))
sales =[]
dates =[]
seller=[]
ind=[]
for i in range(0 , len(count_digi)):
    dates.append(i)
    ind.append(count_digi[i]['timestamp'][:10])
    sales.append(count_digi[i]['quantity']*count_digi[i]['rate'])
    seller.append(count_digi[i]['sender_name'])
digi_disp = pd.DataFrame()
digi_disp['digi'] = sales
digi_disp['date'] = dates
digi_disp['seller'] = seller
digi_disp['ind'] = ind

seller_source_digi =  bp.ColumnDataSource({
                  "x": digi_disp['digi'],
                  "y": digi_disp['date'],
                  "seller": digi_disp['seller'],
                  "date_range": digi_disp['ind']
                 })

seller_source_cash =  bp.ColumnDataSource({
                  "x": cash_disp['cash'],
                  "y": cash_disp['date'],
                  "seller": cash_disp['seller'],
                  "date_range": cash_disp['ind']
                 })
 
seller_source =  bp.ColumnDataSource({
                  "x": sales_disp['sales'],
                  "y": sales_disp['date'],
                  "seller": sales_disp['seller'],
                  "date_range": sales_disp['ind']
                 })
                  
menu_location = [("Ambegaon", "loc_1"), ("Gondiya", "loc_2"), ("Rampur", "loc_3") , ("Devgadh" , "loc_4")]
dropdown_location = Dropdown(label="Select Locality", button_type="warning", menu=menu_location)

table_seller_source = bp.ColumnDataSource({
                        "seller_tname": reciever_names,
                        "seller_locations": reciever_corresponding_loc 
                    })
columns = [
        TableColumn(field="seller_tname", title="Sellers")]
        
seller_table = DataTable(source=table_seller_source, columns=columns, width=500, height=500 , fit_columns = True)

dropdown_location.callback = CustomJS(args=dict(source=table_seller_source), code="""
    var loc_arr = ['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh']
    var fa = cb_obj.value
    var seller_tname = []
    var seller_loc = []
    var seller_perma = ["Sumod" , "Kishan", "Ishwar" , "Ramu" , "Gopal" , "Pawar" , "Urvil" , "Yash" , "Pandurang", "Manoj"]
    sender_corresponding_loc =['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh','Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh','Ambegaon' , 'Gondiya']
    var len_src = seller_perma.length
    for (i=0 ; i< len_src ; i++){
        if (sender_corresponding_loc[i] == loc_arr[fa[4]-1]){
            seller_tname.push(seller_perma[i])
            seller_loc.push(sender_corresponding_loc[i])
        }          
    }
    
    source['data']['index']= []
    for (j=0 ; j< seller_tname.length ; j++){
        source['data']['index'].push(j)    
    }
    source['data']['seller_tname']=seller_tname  
    source['data']['seller_locations'] =seller_loc
    source.trigger('change');
    console.log(source.data)

    """
)

table_seller_source.callback = CustomJS(args=dict(source=table_seller_source , source1=seller_source , source2=seller_source_cash, source3=seller_source_digi), code="""
       var indices = source.selected["1d"].indices;
       console.log(indices)
       var seller_perma = ["Sumod" , "Kishan", "Ishwar" , "Ramu" , "Gopal" , "Pawar" , "Urvil" , "Yash" , "Pandurang", "Manoj"]
       sending_corresponding_loc =['Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh','Ambegaon' , 'Gondiya' , 'Rampur' , 'Devgadh','Ambegaon' , 'Gondiya']       
       var loop_len = source1.data.x.length
       //console.log(source1.data)
       var x_new = []
       var y_new = []
       var date_new =[]
       var ind_new = []
       for (i=0 ; i<loop_len ; i++){
            //console.log(source1.data.seller[i] + "  " + indices[i])
            if (source1.data.seller[i] == seller_perma[indices[0]]){
                console.log("here")
                x_new.push(source1.data.x[i])
                y_new.push(source1.data.y[i])
                date_new.push(source1.data.date_range[i])
                //ind_new.push(source1.data.ind[i])
            }      
        
       }
        source1['data']['index']= []
        for (j=0 ; j< x_new.length ; j++){
            source1['data']['index'].push(j)    
        }
        source1['data']['x'] = x_new
        source1['data']['y'] = y_new
        source1['data']['date_range'] = date_new
        
        
        // cash disp
        var loop_len = source2.data.x.length
       //console.log(source2.data)
       var x_new_2 = []
       var y_new_2 = []
       var date_new_2 =[]
       var ind_new_2 = []
       for (i=0 ; i<loop_len ; i++){
            //console.log(source1.data.seller[i] + "  " + indices[i])
            if (source2.data.seller[i] == seller_perma[indices[0]]){
                //console.log("here")
                x_new_2.push(source2.data.x[i])
                y_new_2.push(source2.data.y[i])
                date_new_2.push(source2.data.date_range[i])
                //ind_new.push(source2.data.ind[i])
            }      
        
       }
        source2['data']['index']= []
        for (j=0 ; j< x_new.length ; j++){
            source2['data']['index'].push(j)    
        }
        source2['data']['x'] = x_new_2
        source2['data']['y'] = y_new_2
        source2['data']['date_range'] = date_new_2
        //source2['data']['ind'] = ind_new_2
        

        //digi disp
         var loop_len = source3.data.x.length
       //console.log(source3.data)
       var x_new_3 = []
       var y_new_3 = []
       var date_new_3 =[]
       var ind_new_3 = []
       for (i=0 ; i<loop_len ; i++){
            //console.log(source1.data.seller[i] + "  " + indices[i])
            if (source3.data.seller[i] == seller_perma[indices[0]]){
                //console.log("here")
                x_new_3.push(source3.data.x[i])
                y_new_3.push(source3.data.y[i])
                date_new_3.push(source3.data.date_range[i])
                //ind_new.push(source3.data.ind[i])
            }      
        
       }
        source3['data']['index']= []
        for (j=0 ; j< x_new.length ; j++){
            source3['data']['index'].push(j)    
        }
        source3['data']['x'] = x_new_3
        source3['data']['y'] = y_new_3
        source3['data']['date_range'] = date_new_3
        //source3['data']['ind'] = ind_new_3
        source1.trigger('change')
        source2.trigger('change')

        source3.trigger('change')        
        """
)
plot_sales = bp.figure(plot_width=400, plot_height=300,
                     title="Buyer Purchasing patterns Insights",
                     tools="pan,wheel_zoom,box_zoom, box_select,reset,hover,previewsave",min_border=1 , y_axis_label= "Sales" , x_axis_label = "Time")
                     
plot_sales.line(sales_disp['date'],sales_disp['sales'], source=seller_source, line_width=3, line_alpha=0.6)


plot_cash = bp.figure(plot_width=400, plot_height=300,
                     title="Buyer Cash Usage Insights",
                     tools="pan,wheel_zoom,box_zoom, box_select,reset,hover,previewsave",min_border=1 , y_axis_label= "Sales" , x_axis_label = "Time")
                     
plot_cash.line(cash_disp['date'],cash_disp['cash'], source=seller_source_cash, line_width=3, line_alpha=0.6 , line_color="red")

plot_digi = bp.figure(plot_width=400, plot_height=300,
                     title="Buyer Digital Transactions Insights",
                     tools="pan,wheel_zoom,box_zoom, box_select,reset,hover,previewsave",min_border=1 , y_axis_label= "Sales" , x_axis_label = "Time")
                     
plot_digi.line(digi_disp['date'],digi_disp['digi'], source=seller_source_digi, line_width=3, line_alpha=0.6 , line_color="green")

hover_digi = plot_digi.select(dict(type=HoverTool))
hover_digi.tooltips = {"date": "@date_range - seller: @seller"}  

hover_cash = plot_cash.select(dict(type=HoverTool))
hover_cash.tooltips = {"date": "@date_range - seller: @seller"}  

hover_sales = plot_sales.select(dict(type=HoverTool))
hover_sales.tooltips = {"date": "@date_range - seller: @seller"}     

#p = Bar(sales_disp, 'ind', values='sales',
#        title="Total Sales for " , color="yellow" , source= seller_source , legend=False)

save(row(row(column(plot_sales, plot_digi) , plot_cash ) , column(dropdown_location , seller_table)), 'dashboardBuyer.html')


