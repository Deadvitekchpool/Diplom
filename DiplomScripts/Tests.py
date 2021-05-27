from linearmodels import PooledOLS
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_white, het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

panel = pd.read_csv('/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Refactored_Data.csv', index_col = ['Регион', 'Год'])

years = panel.index.get_level_values('Год').to_list()
panel['Год'] = pd.Categorical(years)

exog = sm.tools.tools.add_constant(panel['Прибыль_от_продаж'])
endog = panel['ВРП']
mod = PooledOLS(endog, exog)
res = mod.fit(cov_type='clustered', clustered_entity=True)

fitval = res.predict().fitted_values
residuals = res.resids

#if p < 0.05 -> heteroskedasticity is indicated
#3A.2 White Test
print('Прибыль_от_продаж')
pooled_OLS_dataset = pd.concat([panel, residuals], axis=1)
pooled_OLS_dataset = pooled_OLS_dataset.drop(['Год'], axis = 1).fillna(0)

# exog = sm.tools.tools.add_constant(panel['Прибыль_от_продаж']).fillna(0)
# white_test_results = het_white(pooled_OLS_dataset['residual'], exog)

# labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
# print(dict(zip(labels, white_test_results)))

# # 3A.3 Breusch-Pagan-Test
# breusch_pagan_test_results = het_breuschpagan(pooled_OLS_dataset['residual'], exog)
# labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
# print(dict(zip(labels, breusch_pagan_test_results)))

# 3.B Non-Autocorrelation(>2 - negative autocorrelation, >0 <2 - positive autocorrelation, 2 - no autocorrelation)
# Durbin-Watson-Test

durbin_watson_test_results = durbin_watson(pooled_OLS_dataset['residual']) 
print(durbin_watson_test_results)

# fig, ax = plt.subplots()
# ax.scatter(fitval, residuals, color = 'blue')
# ax.axhline(0, color = 'r', ls = '--')
# ax.set_xlabel('Predicted Values', fontsize = 15)
# ax.set_ylabel('Residuals', fontsize = 15)
# ax.set_title('Homoskedasticity Test(Capital productivity)', fontsize = 30)
# plt.show()
