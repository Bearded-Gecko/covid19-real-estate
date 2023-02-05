rfrom statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from pmdarima.arima import auto_arima
import statsmodels.api as sm

class Model():
    
    def __init__(self, ts , splitDate):
        
        self.ts_train=ts[ts.index[0]:( ts.index[ts.index.get_loc(splitDate, method='nearest')])]
        self.ts_test=ts[ ts.index[ts.index.get_loc(splitDate, method='nearest')]:ts.index[-1]]
        
        
        
    def fit(self): 
        self.y_hat_avg = self.ts_test.copy()
        self.fit_model = sm.tsa.statespace.SARIMAX(self.ts_train, order=(1, 1, 1),seasonal_order=(0,1,1,12)).fit()
        self.y_hat_avg['SARIMA'] = self.fit_model.predict(start=self.ts_test.index[0],end=self.ts_test.index[-1])
       
        self.plot(self.ts_train, self.ts_test, y_hat_avg_future)
        self.rms2 = np.sqrt(mean_squared_error(self.ts_test, self.y_hat_avg.SARIMA))
        print('The Root Mean Squared Error of our forecasts is {}'.format(round(self.rms2, 1)))
        
        
    def predict(self, offset=3):
        ts_test_future=self.ts_test.copy()
        ts_test_future.index=ts_test_future.index+pd.DateOffset(years=offset)
        fit_future = sm.tsa.statespace.SARIMAX(self.ts_train, order=(1, 1, 1),seasonal_order=(0,1,1,12)).fit()
        y_hat_avg_future['SARIMA'] = fit_future.predict(start=ts_test_future.index[0],end=ts_test_future.index[-1])
        self.plot(self.train None, y_hat_avg_future)


        
    def plot(self, train , test , predicted):
             
        plt.figure(figsize=(20,10))
        if train:
            plt.plot(train, label='Train')
        if test:
            plt.plot(test, label='Test')
        if predicted:
            plt.plot(predicted['SARIMA'], label='SARIMA')
            
        plt.legend(loc='best')
        plt.xlabel("Year", fontsize='18')
        plt.xlim(dates.date2num([train.index[0], predicted.index[-1]]))
        plt.ylabel("Mean price (£)", fontsize='18')
        plt.title("SARIMA model: my parameters", fontsize='20')

        plt.legend(loc='best')
        font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 16}
        plt.rc('font', **font)
        plt.show()
        
        
    def predict_pre_covid(self):
        pass
    
    def predict_during_covid(self):
        pass
    
    def predict_post_covid(self):
        pass
    
    