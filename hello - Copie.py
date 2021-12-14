from flask import Flask
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns


from sklearn.preprocessing import OrdinalEncoder
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier

from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.ensemble import VotingClassifier
from flask import request






def Age_on_GoodFormat(age):
    return age>=0 and age<=100    

def Height_on_GoodFormat(height):
    return height>=0.20 and height<=2.50    

def Weight_on_GoodFormat(weight):
    return weight>=1 and weight<=250    


def family_history_with_overweight_on_GoodFormat(family_history_with_overweight):
    return family_history_with_overweight in [0,1]
def FAVC_on_GoodFormat(favc):
    return favc in [0,1]    

def FCVC_on_GoodFormat(fcvc):
    return fcvc>=1 and fcvc<=3

def CALC_on_GoodFormat(calc):
    return calc>=1 and calc<=4

def All_Variable_on_Good_Format(age,height,weight,family_history_with_overweight,favc,fcvc,calc):
    return all(list([Age_on_GoodFormat(age),Height_on_GoodFormat(height),Weight_on_GoodFormat(weight),family_history_with_overweight_on_GoodFormat(family_history_with_overweight),FAVC_on_GoodFormat(favc),FCVC_on_GoodFormat(fcvc),CALC_on_GoodFormat(calc)]))

def prediction(Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC):
    if All_Variable_on_Good_Format(Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC)==False:
        return "ERROR TYPE: Not valid features"
    

#LOAD BDD
    url = 'https://github.com/Leodespt/Projet_Python/blob/main/ObesityDataSet_raw_and_data_sinthetic.csv?raw=true'
    df = pd.read_csv(url)
#CREATE DATAFRAME TO STORE THE INDIVIDUAL WHO WILL BE TESTED 
    df_a_tester = pd.DataFrame([[Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC]],
        columns = ['Age','Height','Weight','family_history_with_overweight','FAVC','FCVC','CALC'])    
#SCALE YHE VARIABLE 
    ord_enc = OrdinalEncoder()
    columns = ["family_history_with_overweight","FAVC","CALC"]
    df[columns] = ord_enc.fit_transform(df[columns])

    df.NObeyesdad.replace(('Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II',
        'Obesity_Type_I','Obesity_Type_II','Obesity_Type_III'),(0,1,2,3,4,5,6), inplace = True)

    column = ["NObeyesdad","Gender","NCP","CAEC","SMOKE","SCC","FAF","TUE","MTRANS","CH2O"]
#SPLIT THE DATA
    Y_reduiced =df["NObeyesdad"]
    X_reduiced = df.drop(column,1)

#USING OF A VOTING CLASSIFIER

    # model_svc=SVC(probability=True)
    # model_svc.fit(X_reduiced,Y_reduiced)

    # print(df_a_tester)

    # parameters = {'C' : [150,200,250], 'gamma':[0.02,0.025,0.01]}
    # grid_svc = GridSearchCV(model_svc,parameters,cv=5)
    # grid_svc.fit(X_reduiced,Y_reduiced)


    # Y_pred_svc = grid_svc.predict(df_a_tester)
    AdaBoost=AdaBoostClassifier()
    GradientBoosting=GradientBoostingClassifier()
    HistGradientBoosting=HistGradientBoostingClassifier()

    AdaBoost.fit(X_reduiced,Y_reduiced)
    GradientBoosting.fit(X_reduiced,Y_reduiced)
    HistGradientBoosting.fit(X_reduiced,Y_reduiced)

    Bagging=BaggingClassifier()
    RandomForest=RandomForestClassifier()

    Bagging.fit(X_reduiced,Y_reduiced)
    RandomForest.fit(X_reduiced,Y_reduiced)

    model_svc_reduiced =SVC(C=250, gamma=0.01,probability=True)
    model_svc_reduiced.fit(X_reduiced,Y_reduiced)

    #CREATE LIST OF CLASSIFIER FOR THE VOTE
    liste_classifier_KEY=[('model_svc'),('Bagging'),('RandomForest'),('GradientBoosting'),('HistGradientBoosting')]
    liste_classifier_VALUE=[(model_svc_reduiced),(Bagging),(RandomForest),(GradientBoosting),(HistGradientBoosting)]
    liste_classifier=list(zip(liste_classifier_KEY,liste_classifier_VALUE))

  

    VotingSoft=VotingClassifier(estimators=liste_classifier,voting="soft")
    VotingSoft.fit(X_reduiced,Y_reduiced)


    # model_svc=SVC(probability=True)
    # model_svc.fit(X_reduiced,Y_reduiced)

    # print(df_a_tester)

    # parameters = {'C' : [150,200,250], 'gamma':[0.02,0.025,0.01]}
    # grid_svc = GridSearchCV(model_svc,parameters,cv=5)
    # grid_svc.fit(X_reduiced,Y_reduiced)


    Y_pred_svc = VotingSoft.predict(df_a_tester)


    if  Y_pred_svc[0] == 0:
        return 'Insufficient_Weight'
    if  Y_pred_svc[0] == 1:
        return 'Normal_Weight'
    if  Y_pred_svc[0] == 2:
        return 'Overweight_Level_I'
    if  Y_pred_svc[0] == 3:
        return 'Overweight_Level_II'
    if  Y_pred_svc[0] == 4:
        return 'Obesity_Type_I'
    if  Y_pred_svc[0] == 5:
        return 'Obesity_Type_II'
    else : 
        return 'Obesity_Type_III'


app = Flask(__name__)


@app.route("/")
def hello_world():
    

    
    Age = request.args.get('Age',default=-1,type= float )
    Height = request.args.get('Height',default=-1,type= float )
    Weight = request.args.get('Weight',default=-1,type= float )
    Family_history_with_overweight = request.args.get('family_history_with_overweight',default=-1,type= int )
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
    PREDICTION: {}
    '''.format(Age,Age_on_GoodFormat(Age),
    Height,Height_on_GoodFormat(Height),
    Weight,Weight_on_GoodFormat(Weight),
    Family_history_with_overweight,family_history_with_overweight_on_GoodFormat(Family_history_with_overweight),
    FAVC,FAVC_on_GoodFormat(FAVC),
    FCVC,FCVC_on_GoodFormat(FCVC),
    CALC,CALC_on_GoodFormat(CALC),prediction(Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC))

# All_Variable_on_Good_Format(Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC)


    # 
    # return "<p><b>Hello</b>, World!</p>"
    


app.run(debug=True)


