import pandas as pd
from itertools import chain

frames = []
ind_ph_ob = pd.read_excel("/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx", sheet_name = 'Индекс_физического_объема')
frames.append(ind_ph_ob)

imprt = pd.read_excel("/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx", sheet_name = 'Импорт')
frames.append(imprt)

export = pd.read_excel("/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx", sheet_name = 'Экспорт')
frames.append(export)

prib_ot_prod = pd.read_excel("/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx", sheet_name = 'Прибыль_от_продаж')
frames.append(prib_ot_prod)

fond = pd.read_excel("/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx", sheet_name = 'Фондоотдача')
frames.append(fond)

vrp = pd.read_excel("/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx", sheet_name = 'ВРП')
# vrp = vrp.set_axis([x[0] for x in vrp.values], axis = 0)
# vrp = vrp.drop("Region/Date", axis=1)
# vrp = vrp.rename_axis("Region/Date", axis=0)

frames.append(vrp)

# names = ['Индекс_физического_объема', 'Экспорт', 'Импорт', 'Прибыль_от_продаж', 'Фондоотдача', 'ВРП']

regs = []
vals = []
for x in ind_ph_ob.values:
	temp = []
	for i in range(0, 18):
		temp.append(x[0])
	regs.extend(temp)

for frame in frames:
	temp = []
	for i in range(0, len(frame.index)):
		temp.extend(frame.values[i][1:])
	vals.append(temp)

years = []
for i in range(0, len(ind_ph_ob.values)):	
	years.extend(ind_ph_ob.columns[1:])

# print(len(vals[5]))
panel = pd.DataFrame({'Регион': regs, 'Год': years, 'Индекс_физического_объема': vals[0], 'Экспорт': vals[1], 'Импорт': vals[2], 'Прибыль_от_продаж': vals[3],
	 'Фондоотдача': vals[4], 'ВРП': vals[5]})

panel.to_csv('/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Refactored_Data.csv', index=False)
# print(panel.index.get_level_values('Год').to_list())


# exog = sm.tools.tools.add_constant(vals)
# years = panel.index.get_level_values('Год').to_list()
# panel['Год'] = pd.Categorical(years)
# exog = sm.tools.tools.add_constant(panel['Экспорт'])
# endog = panel['ВРП']
# mod = PooledOLS(endog, exog)
# res = mod.fit(cov_type='clustered', clustered_entity=True)

# fitval = res.predict().fitted_values
# residuals = res.resids

# fig, ax = plt.subplots()
# ax.scatter(fitval, residuals, color = 'blue')
# ax.axhline(0, color = 'r', ls = '--')
# ax.set_xlabel('Predicted Values', fontsize = 15)
# ax.set_ylabel('Residuals', fontsize = 15)
# ax.set_title('Homoskedasticity Test', fontsize = 30)
# plt.show()
