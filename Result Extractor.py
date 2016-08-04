"""
Copyright 2016, Anshuman Agarwal (anshuman73)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from selenium import webdriver
import os
from time import time
from bs4 import BeautifulSoup
import sqlite3


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


def main():
	database_conn = sqlite3.connect('database.sqlite')
	cursor = database_conn.cursor()
	cursor.executescript('''
						DROP TABLE IF EXISTS Records;
						DROP TABLE IF EXISTS Marks;
						CREATE TABLE Records (
							Roll_Number  INTEGER PRIMARY KEY,
							Name         TEXT,
							Father_Name  TEXT,
							Mother_Name  TEXT,
							Final_Result TEXT,
							Number_of_subjects INTEGER
							);
						CREATE TABLE Marks (
							Roll_Number INTEGER,
							Subject_Code TEXT,
							Subject_Name TEXT,
							Theory_Marks INTEGER,
							Practical_Marks INTEGER,
							Total_Marks INTEGER,
							Grade TEXT
							)
						''')

	school_code = raw_input('Enter the School Code: ')
	lower_limit = int(raw_input('Enter the lower limit of roll no. to check: '))
	upper_limit = int(raw_input('Enter the upper limit of roll no. to check: '))

	choice = raw_input('Go headless ? (y/n) ').lower()
	if choice == 'y':
		driver = webdriver.PhantomJS(os.getcwd() + '/' + 'phantomjs.exe')
	elif choice == 'n':
		driver = webdriver.Chrome(os.getcwd() + '/' + 'chromedriver.exe')
	else:
		print 'Wrong input, going headless...'
		driver = webdriver.PhantomJS(os.getcwd() + '/' + 'phantomjs.exe')

	driver.get('http://cbseresults.nic.in/class12/cbse1216.htm')

	st = time()
	count = 0
	for roll_no in range(lower_limit, upper_limit + 1):
		try:
			reg_no_element = driver.find_element_by_name('regno')
			school_code_element = driver.find_element_by_name('schcode')
			submit_button = driver.find_element_by_xpath("//input[@type='submit']")
			reg_no_element.clear()
			reg_no_element.send_keys(roll_no)
			school_code_element.clear()
			school_code_element.send_keys(school_code)
			submit_button.click()
			html = ''.join(driver.page_source.encode('utf8').split('\n')[67:])
			data = parser(html)
			cursor.execute('INSERT INTO Records (Roll_Number, Name, Father_Name, Mother_Name, Final_Result, Number_of_subjects) '
							'VALUES (?, ?, ?, ?, ?, ?)', (data['Roll No:'], data['Name:'], data['Father\'s Name:'],
							data['Mother\'s Name:'], data['final_result'], len(data['marks']), ))
			for subject in data['marks']:
				cursor.execute('INSERT INTO Marks (Roll_Number, Subject_Code, Subject_Name, Theory_Marks, '
								'Practical_Marks, Total_Marks, Grade) VALUES (?, ?, ?, ?, ?, ?, ?)', (data['Roll No:'], subject['SUB CODE'],
								subject['SUB NAME'], subject['THEORY'], subject['PRACTICAL'], subject['MARKS'], subject['GRADE'], ))

			print 'Processed Roll No.', roll_no

			count += 1
			if count % 50 == 0:
				print '\n50 records in RAM, saving to database to avoid loss of data...\n'
				database_conn.commit()
		except Exception as error:
			print 'Roll No.', roll_no, 'threw an error, leaving it.'
			print error

		driver.back()

	print '\n\nLog: \n'

	print count, 'valid records downloaded, saving everything to database...'
	database_conn.commit()
	database_conn.close()

	print '\nClosing the Simulated Browser'
	driver.close()
	print '\nSimulated browser closed.\n'

	print '\nFinished processing everything.\n'
	print '\nTook', time() - st, 'seconds for execution for processing', count, 'valid records'

	raw_input('Press any Key to exit: ')

if __name__ == '__main__':
	main()
