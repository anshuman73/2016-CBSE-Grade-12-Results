from bs4 import BeautifulSoup

html = open('lol.html', 'r').readlines()[67:]
html = ''.join(html)


def parser(html):
	data = dict()
	marks_table_index = list()
	marks = list()
	soup = BeautifulSoup(html, 'html.parser')
	parsed_tables = soup.findAll('table')[:2]
	basic_data_table = parsed_tables[0]
	basic_data_tr = basic_data_table.findAll('tr')
	for rows in basic_data_tr:
		columns = rows.findAll('td')
		data[''.join(columns[0].findAll(text=True)).strip()] = ''.join(columns[1].findAll(text=True)).strip()

	result_data_table = parsed_tables[1]
	result_data_tr = result_data_table.findAll('tr')
	for codes in result_data_tr[0].findAll('td'):
		marks_table_index.append(''.join(codes.findAll(text=True)).strip())

	marks_table_subjects = result_data_tr[1:-1]
	for subject_tr in marks_table_subjects:
		if len(subject_tr.findAll('td')) > 1:
			subject_marks = {}
			for index, sub_details in enumerate(subject_tr.findAll('td')):
				subject_marks[marks_table_index[index]] = ''.join(sub_details.findAll(text=True)).strip()
			marks.append(subject_marks)

	raw_result = ''.join(result_data_tr[-1].findAll('td')[1].findAll(text=True)).strip()
	result = raw_result[raw_result.find('Result:') + len('Result:'): raw_result.rfind(':')].strip()

	data['marks'] = marks
	data['final_result'] = result
	return data

print parser(html)
