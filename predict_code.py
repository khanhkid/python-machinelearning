from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
import matplotlib.pyplot as plt
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from math import sqrt, expm1
import numpy as np
from sklearn.metrics import mean_squared_error
from numpy import genfromtxt, savetxt

def saveImage(y_true, y_pred, path,title):
	print(y_true)
	x = range(1,len(y_true)+1)
	fig = plt.figure()
	plt.plot(x, y_true, label='Thuc Do'.format(i=1))
	plt.plot(x, y_pred,linestyle="--", linewidth =2, label='Website'.format(i=2),color="red")
	plt.legend(loc='best')
	plt.subplots_adjust(top=0.83)
	arrTitle = title.split(",")
	plt.title(title+"\n")
	fig.savefig(path, dpi=fig.dpi*2)

def dochinhxac(y_true,y_pred):
	result = [];
	for i in range(0,len(y_true)):
		if y_true[i] > 0:
			lech = abs(y_pred[i] - y_true[i])/y_true[i]
			result.insert(0,1-lech)
	return np.mean(result)

def caculateIndex(arrPredict,test_y,dirPath = "",strDetail=""):
	key = 0;
	Sum_ME = 0;
	Sum_MEA = 0;		
	Sum_RMSE = 0;		
	for i in arrPredict:
		# caculate 
		Sum_ME += (arrPredict[key]-test_y[key])
		# (MAE)
		Sum_MEA += abs(arrPredict[key]-test_y[key])
		#(RMSE):
		Sum_RMSE += (arrPredict[key]-test_y[key])**2
		key = key+1
	AVG_ME=Sum_ME/(key+1)
	AVG_MEA=Sum_MEA/(key+1)
	AVG_RMSE= sqrt(Sum_RMSE/(key+1))
	PercentChinhXac = dochinhxac(test_y,arrPredict)
	with open(dirPath, "ab") as myfile:
		myfile.write("%s, ME: %s,MEA: %s,RMSE: %s, Do Chinh Xac: %s\n" % (strDetail, AVG_ME,AVG_MEA,AVG_RMSE,PercentChinhXac))
# Date
# Precipitation
# Relative Humidity
# Max Temperature
# Solar
# Min Temperature
# Wind
# arrDb = ['LuongMua','DoAm','NhietDoCao','MatTroi','NhietDoThap','Gio']
# arrAl = ['5,1,0','1,0,0','5,1,0','2,1,0','4,1,0','2,0,1']
# nameDb = arrDb[keyDb];

for district in range(0,24):
    for month in range(4,5): 
        print(month, district)
        # read database month from csv 
        series = read_csv('tempature_2019/'+str(month)+'.csv', header=-1, parse_dates=[0], index_col=0, squeeze=True)
        X = series.values
        train = X[0:len(X),district]
        dataset = train
        #savetxt("Result/"+nameDb+str(month)+"_TrueValue.txt", test, delimiter=',')
        predictions = list()
        dataset = [x for x in train]
        numYear = 4 
        for t in range(30):
            history = [];
            for year in range(0,numYear):
                history.append(dataset[t+(year*30)])
            model = ARIMA(history, order=(1,1,0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat[0])
            history.append(yhat[0])
            print('predicted=%f' % (yhat[0]))

        #error = mean_squared_error(test, predictions)
        #print('Test MSE: %.3f' % error)
        savetxt("Result/"+str(district)+"_"+str(month)+".txt", predictions, delimiter=',')
        #saveImage(test, predictions, "Result/"+nameDb+"_"+str(month)+".png",nameDb+" Month:"+str(month))
        #caculateIndex(predictions,test,"Result/"+nameDb+".txt",nameDb+".txt")
        pass