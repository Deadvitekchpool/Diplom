import numpy as np
import pandas as pd

def transform_dates(df):
	"""1999.0 nan nan nan -> 1999.1 1999.2 1999.3 1999.4 ..."""
	df = df.set_axis([x[0] for x in df.values], axis = 0)
	df = df.drop("Unnamed: 0", axis=1)
	temp = []
	frames = df.values[0][::4]
	for i, col in enumerate(frames):
		frame_length = len(df.values[0][1 + i*4 : (i + 1) * 4]) + 1
		for ii in range(frame_length):
			el_index = 1 + i*4 + ii
			quarter_value = (ii+1)/10
			# df.iat[0, el_index] = col + quarter_value
			temp.append(col + quarter_value)

	df.columns = temp

	if all([x[0] == 0 for x in df.values[1:]]):
		df = df.drop([temp[0]], axis=1)
	df = df.drop([df.index[0]], axis=0)
	df = df.rename_axis("Region/Date", axis=0)
	return df

def transform(df, fira): #transform dataframe with years, not quarters
	if fira:
		df = df.set_axis([x[0] for x in df.values], axis = 0)
		df = df.drop("Unnamed: 0", axis=1)
		df = df.set_axis(df.values[0], axis = 1)
		df = df.drop([df.index[0]], axis=0)
		df = df.rename_axis("Region/Date", axis=0)
	else:
		df = df.set_axis([x[0] for x in df.values], axis = 0)
		df = df.drop("Unnamed: 0", axis=1)
		# df = df.set_axis(df.values[0], axis = 1)
		# df = df.drop([df.index[0]], axis=0)
		df = df.rename_axis("Region/Date", axis=0)
	return df

def get_factored_dataframe(filename, sheet_name, usercols, dates, fira) -> pd.DataFrame:
	df = pd.read_excel(
		open(f'{filename}', 'rb'),
		sheet_name=sheet_name,
		usecols=usercols,
		skiprows=2
	)

	if fira:
		df = _delete_blank(df)
		df = _delete_if_50_empty(df)
		if dates:
			df = transform_dates(df)
		else:
			df = transform(df, fira)
		df = df.sort_index()
		# df = fix_columns(df)
		df = clear_index(df)
	else:
		df = _delete_if_50_empty(df)
		df = transform(df, fira)
		df = df.sort_index()
		df = clear_index(df)
	return df

def clear_index(df):
	change = {}
	for name in df.index:
		if '(' in name:
			x = name.index('(')
			new_name = name[0 : x].strip()
			change[name] = new_name
	df = df.rename(index=change)
	return df

def fix_columns(df):
	col_ = [0 for _ in range(len(df.values[0]))]
	for i in range(len(df.values)):
		for j, col in enumerate(df.values[i]):
			if col == 0 or pd.isna(col):
				col_[j] += 1
	to_drop = []
	for i, ci in enumerate(col_):
		if ci/len(df.values) >= .5:
			to_drop.append(df.columns[i])

	return df.drop(to_drop, axis = 1).reset_index(drop=True)

def _delete_blank(df): #remove extra rows
	i = 0
	while df.loc[i].values[0] != 'Таблица: Исходные данные':
		i += 1

	to_drop = list(range(i + 1))
	# to_drop.remove(i-2)
	return df.drop(to_drop).reset_index(drop=True)


def _delete_if_50_empty(df): #delete row if more than 50% is empty
	to_drop = []
	to_drop_complex = [0 for _ in range(len(df.values))]
	# if >50% is NaN or 0 in row -> delete

	for ix, row in enumerate(df.values[1:]):
		if row[0] == 'В оглавление' or pd.isna(row[0]):
			to_drop.append(ix + 1)
			continue

		for col_el in row[1:]:
			if col_el == 0 or pd.isna(col_el) or isinstance(col_el, str):
				to_drop_complex[ix + 1] += 1

	for ix, val in enumerate(to_drop_complex):
		if val/len(df.values[ix]) > .5:
			to_drop.append(ix)
	return df.drop(to_drop).reset_index(drop=True)
