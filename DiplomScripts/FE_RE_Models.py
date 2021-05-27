import statsmodels.api as sm
import pandas as pd
from linearmodels import PanelOLS
from linearmodels import RandomEffects
import numpy.linalg as la
from scipy import stats
import numpy as np

def hausman(fe, re):
	b = fe.params
	B = re.params
	v_b = fe.cov
	v_B = re.cov

	df = b[np.abs(b) < 1e8].size
	chi2 = np.dot((b - B).T, la.inv(v_b - v_B).dot(b - B)) 
	 
	pval = stats.chi2.sf(chi2, df)

	return chi2, df, pval

panel = pd.read_csv('/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Refactored_Data.csv', index_col = ['Регион', 'Год'])

years = panel.index.get_level_values('Год').to_list()
panel['Год'] = pd.Categorical(years)


endog = panel['ВРП']

for name in panel.columns[:-2]:
	print(name)
	exog = sm.tools.tools.add_constant(panel[name])
	# random effects model
	mod_re = RandomEffects(endog, exog) 
	re_res = mod_re.fit() 
	# fixed effects model
	mod_fe = PanelOLS(endog, exog, entity_effects = True) 
	fe_res = mod_fe.fit() 

	hausman_results = hausman(fe_res, re_res) 
	print('chi-Squared: ' + str(hausman_results[0]))
	print('degrees of freedom: ' + str(hausman_results[1]))
	print('p-Value: ' + str(hausman_results[2]))
	print('\n')