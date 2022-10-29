import sys
import numpy as np
import random
import datetime as dt
import pandas_datareader as pdr


from scipy.stats import norm


def get_historical_adjclose(stocks, start=None, end=None):
    times_series = pdr.get_data_yahoo(stocks, start, end)['Adj Close']
    return times_series


def get_daily_return(adj_close, period_predictions, num_simulations):
    period_predictions += 1
    logarithmic_return = np.log(1 + adj_close.pct_change())
    return_trend       = logarithmic_return.mean()
    variance           = logarithmic_return.var()
    drift              = return_trend - (0.5 * variance)
    standart_deviation = logarithmic_return.std()
 
    daily_return = np.exp(drift + standart_deviation * norm.ppf(np.random.rand(period_predictions, num_simulations)))
    return daily_return

def get_mcs_price_list(daily_return, initial_price, period_predictions): 
    period_predictions +=1
    price_list  = np.zeros_like(daily_return)
    price_list[0] = initial_price

    for period in range(1, period_predictions):
        price_list[period] = price_list[period - 1] * daily_return[period]
    return price_list 

def show_efficacy(real_price, predicted_price, initial_price):
    efficaccy =  ((real_price - predicted_price)*100) / initial_price
    diff_pred  = diff_prediction_real_value(real_price, predicted_price)
    
    print(f"ORIGINAL: {round(real_price,3)} | PREDICTED: {round(predicted_price,3)}")
    if(efficaccy < 0):
        print(f"DIFF: {round(diff_pred,3)}  | EFFICACY: {round(100 + efficaccy,3)}%")
    else:
        print(f"DIFF: +{round(diff_pred,3)} | EFFICACY: {round((100 + (efficaccy * -1)),3)}%")
    

def diff_prediction_real_value(real_price, predicted_price):
    return real_price - predicted_price

def prediction_list(price_list):
    predictions = []
    for price in price_list:
        predictions.append(random.uniform(price.mean()-price.std(),price.mean()+price.std()))

    return predictions

def main(args):
    stock = args
    #start = dt.datetime(2000,1,1)
    #end = dt.datetime(2022,10,27)    
    #adjClose = get_historical_adjclose(stock, start, end)
    adjClose = get_historical_adjclose(stock)

    period_predictions= 1
    num_simulations = 10000000
    real_price_list = get_historical_adjclose(stock, dt.datetime(2022,10,25))
    real_price = real_price_list[-1]
    initial_price = adjClose.iloc[-1]
    daily_return = get_daily_return(adjClose, period_predictions, num_simulations)
    price_list = get_mcs_price_list(daily_return,initial_price,period_predictions)

    pridiction = prediction_list(price_list)[-1]
    
    #show_efficacy(real_price, pridiction, initial_price)

    print(f"PREDICTION: {round(pridiction,3)}")

if __name__ == "__main__":
    print(sys.argv[1].upper())
    main(sys.argv[1])
