import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn import metrics

# abrindo o csv
data = pd.read_csv('/home/luiz/Desktop/unifesp/IA/artigo/BlackFriday.csv')
print(len(data))

# valores faltantes de 'Product_Category_2' e 'Product_Category_3' substituidos por 0
data['Product_Category_2'].fillna(0, inplace=True)
data['Product_Category_3'].fillna(0, inplace=True)

# valores do tipo float transformados para int
data['Product_Category_2'] = data['Product_Category_2'].astype(int)
data['Product_Category_3'] = data['Product_Category_3'].astype(int)

# a string 4+ é transformada em 4 e depois para int
data.Stay_In_Current_City_Years = data.Stay_In_Current_City_Years.replace('4+',4)
data['Stay_In_Current_City_Years'] = data['Stay_In_Current_City_Years'].astype(int)

# removendo as colunas User_id e Product_id
X = data.iloc[:,2:11].values
y = data.iloc[:,11].values


# regularização de dados categóricos
lb1 = LabelEncoder()
lb2 = LabelEncoder()
lb3 = LabelEncoder()
lb4 = LabelEncoder()

X[:,0] = lb1.fit_transform(X[:,0])
X[:,1] = lb2.fit_transform(X[:,1])
X[:,2] = lb3.fit_transform(X[:,3])
X[:,3] = lb4.fit_transform(X[:,2])

onh = OneHotEncoder(categorical_features=[1,2,3])
X = onh.fit_transform(X).toarray()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)


model = MLPRegressor(
    hidden_layer_sizes=(20,20,20), 
    activation="relu", 
    solver="adam", 
    alpha=0.0001, 
    batch_size=256, 
    learning_rate="constant", 
    learning_rate_init=0.001, 
    power_t=0.5, 
    momentum=0.9, 
    verbose=1, 
    max_iter=10,
    early_stopping=True) 



model.fit(X_train, y_train)

print("Taxa de acerto do teste: (R2)" + str(model.score(X_test, y_test)))
    


predictions = model.predict(X_test)

##print("Taxa de acerto accuracia: " + metrics.accuracy_score(X_test, y_test))
print("Taxa de acerto do teste (R2): " + str(metrics.r2_score(y_test, predictions)))
print('erro médio absoluto (MAE):', metrics.mean_absolute_error(y_test, predictions))
print('erro médio quadrático (MSE):', metrics.mean_squared_error(y_test, predictions))
print('raiz quadrad do erro médio (RMSE):', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

