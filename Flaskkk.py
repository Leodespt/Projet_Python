import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def prediction(Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC):

    url = 'https://github.com/Leodespt/Projet_Python/blob/main/ObesityDataSet_raw_and_data_sinthetic.csv?raw=true'
    df = pd.read_csv(url)

    df_a_tester = pd.DataFrame([[Age,Height,Weight,Family_history_with_overweight,FAVC,FCVC,CALC]],
        columns = ['Age','Height','Weight','family_history_with_overweight','FAVC','FCVC','CALC'])    

    ord_enc = OrdinalEncoder()
    columns = ["family_history_with_overweight","FAVC","CALC"]
    df[columns] = ord_enc.fit_transform(df[columns])

    df.NObeyesdad.replace(('Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II',
        'Obesity_Type_I','Obesity_Type_II','Obesity_Type_III'),(0,1,2,3,4,5,6), inplace = True)

    column = ["NObeyesdad","Gender","NCP","CAEC","SMOKE","SCC","FAF","TUE","MTRANS","CH2O"]

    Y_reduiced =df["NObeyesdad"]
    X_reduiced = df.drop(column,1)

    model_svc=SVC(probability=True)
    model_svc.fit(X_reduiced,Y_reduiced)

    print(df_a_tester)

    parameters = {'C' : [150,200,250], 'gamma':[0.02,0.025,0.01]}
    grid_svc = GridSearchCV(model_svc,parameters,cv=5)
    grid_svc.fit(X_reduiced,Y_reduiced)


    Y_pred_svc = grid_svc.predict(df_a_tester)

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