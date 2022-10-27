import pandas as pd 
import numpy as np
import random
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf


from scipy.stats import norm


def retornosDiariosSMC(dados,tempoPredicao,numSimulacoes):
    tempoPredicao += 1
    retorno_logaritmico = np.log(1 + dados.pct_change())
    tendecia_retorno    = retorno_logaritmico.mean()
    variancia           = retorno_logaritmico.var()
    drift               = tendecia_retorno - (0.5 * variancia)
    desvio_padrao       = retorno_logaritmico.std()
 
    retornoDiario = np.exp(drift + desvio_padrao * norm.ppf(np.random.rand(tempoPredicao, numSimulacoes)))
    return retornoDiario

def retornaListaPrecoSMC(retornoDiario, precoInicial, tempoPredicao): 
    tempoPredicao +=1
    inicProc = dt.datetime.now()
    print('Gerando Lista de Preços..')
    listaPrecos  = np.zeros_like(retornoDiario)
    listaPrecos[0] = precoInicial

    for tp in range(1, tempoPredicao):
        listaPrecos[tp] = listaPrecos[tp - 1] * retornoDiario[tp]
    print('Lista Gerada.') 
    return listaPrecos 


def retornaQuantis(dados, listaProbabilidades, valorInicial):
    quantil = np.quantile(dados, q=listaProbabilidades)    
     
    pro_quantil = np.zeros_like(quantil)
    
    for i in range(0, len(quantil)):
        pro_quantil[i] = (1 - (valorInicial/quantil[i])*100) 
   
    return  pro_quantil 


def taxaErroValorReal(valorFinalReal,valoFinalEstimado,precoInicial):
    taxaErro =  ((valorFinalReal-valoFinalEstimado)*100)/precoInicial
    if(taxaErro < 0):
        taxaErro = taxaErro * -1
   
    return taxaErro

def taxaProximidadeAcertoValorReal(taxaErro):
    if(taxaErro > 0):
           return 100 - taxaErro
    else:
           return 100 + taxaErro 


#'WEGE3.SA MGLU3.SA VALE3.SA SULA11.SA ITSA4.SA'
acoes = yf.Tickers('SULA3.SA')
print(acoes)
acoes_hist_max = acoes.history(period="1mo")
df_acoes = acoes_hist_max['2010':] 
df_acoes_close = df_acoes['Close']

period= 30
num_simulations = 10000 
precoInicial = df_acoes_close['MGLU3'].iloc[-1]

df_acoes_close.plot(kind='line', figsize=(12,12), subplots=True)

retornoDiario = retornosDiariosSMC(df_acoes_close['MGLU3'],period,num_simulations)
precosEstimados = retornaListaPrecoSMC(retornoDiario,precoInicial,period) 


estimados_mean = []
estimados_std = []
estimados_max = []
estimados_min = []
estimados = []

for preco in precosEstimados:
  estimados_mean.append(preco.mean())
  estimados_std.append(preco.std())
  estimados_max.append(preco.max())
  estimados_min.append(preco.min())
  estimados.append(random.uniform(preco.mean()-preco.std(),preco.mean()+preco.std()))

print(f'PRECOS ESTIMADO: {estimados}')
df_acoes_close.tail(10)

plt.figure(figsize=(12,8))
plt.title('Simulações de Monte Carlo '+str(num_simulations)+' SMC x '+str(period)+' Dias',fontsize=16)
plt.xlabel('Período em dias',fontsize=12)
plt.ylabel('Preços em R$',fontsize=12)
plt.plot(estimados)
plt.show()