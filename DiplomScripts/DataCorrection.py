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

def collapse(df, s):
	indexes_to_drop = []
	i = 0
	new_cols = []
	while i < len(df.values[0]):
		frames_len = 0
		prev = int(df.columns[i])
		new_cols += [prev]
		for col in df.columns[i:]:
			if int(col) != prev:
				break
			i += 1
			frames_len += 1

		frames = [row[i - frames_len:i] for row in df.values]
		for ii, frame in enumerate(frames):
			if s:
				df.iat[ii, i-frames_len] = sum(frame)
			else:
				df.iat[ii, i-frames_len] = sum(frame) / len(frame)
		indexes_to_drop += list(range(i - frames_len + 1, i))
	to_drop = [df.columns[ind] for ind in indexes_to_drop]
	df = df.drop(to_drop, axis=1)
	df.columns = new_cols
	return df

def unify(l):
	temp = []
	rows = set.intersection(set(l[0].index), set(l[1].index), set(l[2].index), set(l[3].index), set(l[4].index), set(l[5].index))
	columns = set.intersection(set(l[0].columns), set(l[1].columns), set(l[2].columns), set(l[3].columns), set(l[4].columns), set([int(x) for x in l[5].columns]))
	i = 0
	for df in l:
		for item in df.index:
			if item not in rows:
				df = df.drop(item)
		for item in df.columns:
			if int(item) not in columns:
				df = df.drop(item, axis=1)
		temp.append(df)
	return temp

def write(panel):
	with ExcelWriter('/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Test.xlsx') as writer:
		panel[0].to_excel(writer, sheet_name = 'Индекс_физического_объема')
		panel[1].to_excel(writer, sheet_name = 'Импорт')
		panel[2].to_excel(writer, sheet_name = 'Экспорт')
		panel[3].to_excel(writer, sheet_name = 'Прибыль_от_продаж')
		panel[4].to_excel(writer, sheet_name = 'Фондоотдача')
		panel[5].to_excel(writer, sheet_name = 'ВРП')

panel = []

df1 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Индекс_физического_объема_1998-2020.xlsx',
	sheet_name='Таблица Исходные данные',
	usercols='A,C:X',
	dates=False,
	fira=True
)
df1 = correction(df1)
panel.append(df1)
print(df1.columns)

df3 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Импорт_Экспорт_1998-2020.xlsx',
	sheet_name='Данные 1',
	usercols='A,C:CN',
	dates=True,
	fira=True
)
df3 = correction(df3)
df3 = collapse(df3, True)
panel.append(df3)

df2 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Импорт_Экспорт_1998-2020.xlsx',
	sheet_name='Исходные данные',
	usercols='A,C:CN',
	dates=True,
	fira=True
)
df2 = correction(df2)
df2 = collapse(df2, True)
panel.append(df2)

df5 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Прибыль_от_продаж_2002-2020.xlsx',
	sheet_name='Таблица Исходные данные',
	usercols='A,C:BX',
	dates=True,
	fira=True
)
df5 = correction(df5)
df5 = collapse(df5, True)
panel.append(df5)

df6 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/Фондоотдача_2002-2020.xlsx',
	sheet_name='Таблица Исходные данные',
	usercols='A,C:BX',
	dates=True,
	fira=True
)
df6 = correction(df6)
df6 = collapse(df6, False)
panel.append(df6)

df7 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/vrp.xlsx',
	sheet_name='1',
	usercols='A,B:S',
	dates=False,
	fira=False
)

df8 = get_factored_dataframe(
	filename='/Users/Deadvitekchpool/Documents/Diplom/Source_Data/vrp.xlsx',
	sheet_name='2',
	usercols='A,B:E',
	dates=False,
	fira=False
)
df7 = pd.merge(df7, df8, left_index=True, right_index=True)

df7 = correction(df7)
print(df7.columns)
panel.append(df7)

# names = ['Индекс_физического_объема', 'Импорт', 'Экспорт', 'Оборот_организаций', 'Прибыль_от_продаж', 'Фондоотдача']
panel = unify(panel)
write(panel)
