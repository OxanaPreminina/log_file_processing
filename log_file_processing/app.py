'''Программа обрабатывает log-файл, указанный в log_file_path, записывая пути к .arc-файлам 
в состоянии 'in transit' на каждую дату в отдельные txt-файлы. Названия txt-файлов соответствуют 
дате событий в формате 'mmddyyyy', расположение - директория /log_files/'''

import re
import datetime


log_file_path = 'alert_db.log'

match_list = []
number = ''
date = ''

with open(log_file_path, 'r') as file:
	for line in file:
		for match in re.finditer(r'\w{3}\ \ ?\d{1,2}\ \d{2}\:\d{2}\:\d{2}\ \d{4}', line):
			mydate = datetime.datetime.strptime(match.group(), '%b %d %H:%M:%S %Y')
			match_text = mydate.strftime("%m%d%Y")
			if match_text != date:
				match_list.append(match_text)
			date = match_text
		for match in re.finditer(r'\d{5} \(in transit\)', line):
			number = match.group()[:5]
		reg_exp = r'/opt6/STND_ARCHIVE/log1631912277_1_' + number + r'\.arc'
		for match in re.finditer(reg_exp, line):
			match_list.append(match.group())


for i in range(len(match_list)):
	if len(match_list[i]) == 8 and len(match_list[i + 1]) != 8:
		name_file = 'log_files/' + match_list[i] + '.txt'
		file_txt = open(name_file, 'w')
		file_txt.close()
	elif len(match_list[i]) != 8:
		file_txt = open(name_file, 'a+')
		file_txt.write(match_list[i] + '\n')
		file_txt.close()

