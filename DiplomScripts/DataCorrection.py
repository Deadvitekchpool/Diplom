import numpy as np
import pandas as pd
from pandas import ExcelWriter

from DataFiltration import get_factored_dataframe

def correction(df):
	for i in range(0, len(df.values)):
		temp = [x for x in df.values[i] if isinstance(x, (float, int)) and not pd.isna(x)]#not pd.isna(x) or not isinstance(x, str)]
		# print(temp)
		med = sum(temp) / len(temp)
		for j in range(0, len(df.values[i])):
			if pd.isna(df.iat[i, j]) or df.iat[i, j] == 0 or not isinstance(df.iat[i, j], (float, int)):
				df.iat[i, j] = med
	return df

def unify_regions(l):
	temp = []
	intrsctn = set.intersection(set(l[0].index), set(l[1].index), set(l[2].index), set(l[3].index), set(l[4].index), set(l[5].index))
	i = 0
	for df in l:
		for item in df.index:
			if item not in intrsctn:
				df = df.drop(item)
		temp.append(df)
	return temp

def write(panel):
	with ExcelWriter('/Users/Deadvitekchpool/Documents/Source_Data/Test.xlsx') as writer:
		panel[0].to_excel(writer, sheet_name = 'Индекс_физического_объема')
		panel[1].to_excel(writer, sheet_name = 'Импорт')
		panel[2].to_excel(writer, sheet_name = 'Экспорт')
		panel[3].to_excel(writer, sheet_name = 'Прибыль_от_продаж')
		panel[4].to_excel(writer, sheet_name = 'Фондоотдача')
		panel[5].to_excel(writer, sheet_name = 'ВРП')

panel = []

df1 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/Индекс_физического_объема_1998-2020.xlsx',
	sheet_name='Таблица Исходные данные',
	usercols='A,C:X',
	dates=False,
	fira=True
)
df1 = correction(df1)
panel.append(df1)

df2 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/Импорт_Экспорт_1998-2020.xlsx',
	sheet_name='Исходные данные',
	usercols='A,C:CN',
	dates=True,
	fira=True
)
df2 = correction(df2)
panel.append(df2)

df3 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/Импорт_Экспорт_1998-2020.xlsx',
	sheet_name='Данные 1',
	usercols='A,C:CN',
	dates=True,
	fira=True
)
df3 = correction(df3)
panel.append(df3)

# df4 = get_factored_dataframe(
# 	filename='/Users/Deadvitekchpool/Documents/Source_Data/Оборот_организаций_2015-2020.xlsx',
# 	sheet_name='Таблица Исходные данные',
# 	usercols='A,C:Y',
# 	dates=True,
# 	fira=True
# )
# df4 = correction(df4)
# panel.append(df4)

df5 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/Прибыль_от_продаж_2002-2020.xlsx',
	sheet_name='Таблица Исходные данные',
	usercols='A,C:BX',
	dates=True,
	fira=True
)
df5 = correction(df5)
panel.append(df5)

df6 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/Фондоотдача_2002-2020.xlsx',
	sheet_name='Таблица Исходные данные',
	usercols='A,C:BX',
	dates=True,
	fira=True
)
df6 = correction(df6)
panel.append(df6)

df7 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/vrp.xlsx',
	sheet_name='1',
	usercols='A,B:S',
	dates=False,
	fira=False
)

df8 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Source_Data/vrp.xlsx',
	sheet_name='2',
	usercols='A,B:E',
	dates=False,
	fira=False
)
df7 = pd.merge(df7, df8, left_index=True, right_index=True)

df7 = correction(df7)
print(df7)
panel.append(df7)

# names = ['Индекс_физического_объема', 'Импорт', 'Экспорт', 'Оборот_организаций', 'Прибыль_от_продаж', 'Фондоотдача']
panel = unify_regions(panel)
write(panel)




# unify_regions(panel)