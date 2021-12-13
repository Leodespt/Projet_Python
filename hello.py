from flask import Flask
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

from flask import request

os.chdir("P:\\ESILV\\Année 4\\S1\\Python for Data Analysis\\Projet")
df = pd.read_csv("ObesityDataSet_raw_and_data_sinthetic.csv")


def Age_on_GoodFormat(age):
    return age>=0 and age<=100    

def Height_on_GoodFormat(height):
    return height>=0.20 and height<=2.50    

def Weight_on_GoodFormat(weight):
    return weight>=1 and weight<=250    

def family_history_with_overweight_on_GoodFormat(family_history_with_overweight):
    return str(family_history_with_overweight) in ["Insufficient_Weight","Normal_Weight","Obesity_Type_I","Obesity_Type_II","Obesity_Type_III","Overweight_Level_I","Overweight_Level_II"]    

def FAVC_on_GoodFormat(favc):
    return favc in [0,1]    

def FCVC_on_GoodFormat(fcvc):
    return fcvc>=1 and fcvc<=3

def CALC_on_GoodFormat(calc):
    return calc>=1 and calc<=4


# Age	Height	Weight	family_history_with_overweight	FAVC	FCVC	CALC

# numpy.float64
#numpy.float64
# numpy.float64

#numpy.int8

# numpy.int8
# FCVC
# CALC

app = Flask(__name__)


@app.route("/")
def hello_world():
    

    
    Age = request.args.get('Age',default=-1,type= float )
    Height = request.args.get('Height',default=-1,type= float )
    Weight = request.args.get('Weight',default=-1,type= float )
    Family_history_with_overweight = request.args.get('family_history_with_overweight',default="empty",type= str )
    FAVC = request.args.get('FAVC',default=-1,type= int )
    FCVC = request.args.get('FCVC',default=-1,type= int )
    CALC = request.args.get('CALC',default=-1,type= int )


    return '''Age={}  on good Format: {}
    Height={}  on good Format: {}
    Weight={}  on good Format {}
    family_history_with_overweight={}  on good Format: {}
    FAVC={}  on good Format: {}
    FCVC={}  on good Format: {}
    CALC={}  on good Format: {}
    '''.format(Age,Age_on_GoodFormat(Age),
    Height,Height_on_GoodFormat(Height),
    Weight,Weight_on_GoodFormat(Weight),
    Family_history_with_overweight,family_history_with_overweight_on_GoodFormat(Family_history_with_overweight),
    FAVC,FAVC_on_GoodFormat(FAVC),
    FCVC,FCVC_on_GoodFormat(FCVC),
    CALC,CALC_on_GoodFormat(CALC))




    # return "<p><b>Hello</b>, World!</p>"
    


app.run(debug=True)


