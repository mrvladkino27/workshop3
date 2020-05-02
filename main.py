import cx_Oracle

username = 'system'
password = '1234567890'
database = 'localhost/xe'

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

query = '''
		SELECT 
		       COMPANY_NAME,
		       COUNT(CAR_VIN) as amount
		      FROM TASK
		GROUP BY COMPANY_NAME
'''
cursor.execute(query)
print('')
print('First request shows which companies produced cars and amount of that cars')
company = []
count = []

for record in cursor.fetchall():
  company.append(record[0])
  count.append(record[1])
  print(record[0]," "*(25-len(record[0])), record[1])
print('')

query = '''SELECT FUEL_NAME,
    COUNT(FUEL_NAME)/(
    SELECT COUNT(CAR_VIN)
    FROM TASK)  as part
FROM TASK
    GROUP BY FUEL_NAME '''

cursor.execute(query)
print("""Second request shows the attitude between types of fuel depends on
 cars from craiglist""")
print('')

fuel_type = []
rate = []
for record in cursor.fetchall():
	fuel_type.append(record[0])
	rate.append(record[1])
	print(record[0]," "*(25-len(record[0])), record[1])
print('')

query = '''SELECT 
       CAR_YEAR,
       COUNT(CAR_VIN)  as amount
      FROM TASK
    GROUP BY CAR_YEAR'''

cursor.execute(query)
print('Third request shows depending amount of cars on years')
print('')
result = sorted(cursor.fetchall())

years = []
amount = []
for record in result:
	years.append(record[0])
	amount.append(record[1])
	print(record[0]," "*21, record[1])
print('')

connection.close()

######################################################################################################
import chart_studio

chart_studio.tools.set_credentials_file(username = 'mar4vv', api_key = 'GNHKbFEvHFzR1DFcPIos')

import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dashboard
import re

def fileId_from_url(url):
	raw_fileID = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
	return raw_fileID.replace('/', ':')


bar = go.Bar(x = company, y = count)
bar_scheme = py.plot([bar], filename = 'db_lab_3_1')

trace = go.Scatter(
	x= years,
	y = amount
)

data = [trace]
plot_scheme = py.plot(data, filename = 'db_lab_3_2')


pie = go.Pie(labels = fuel_type, values = rate)
pie_scheme = py.plot([pie], filename = 'db_lab_3_3')

my_dashboard = dashboard.Dashboard()
bar_scheme_id = fileId_from_url(bar_scheme)
plot_scheme_id = fileId_from_url(plot_scheme)
pie_scheme_id = fileId_from_url(pie_scheme)

box_1 = {
	'type' : 'box',
	'boxType' : 'plot',
	'fileId' : bar_scheme_id,
	'title' : 'Companies'
}

box_2 = {
	'type' : 'box',
	'boxType' : 'plot',
	'fileId' : plot_scheme_id,
	'title' : 'Years'
}

box_3 = {
	'type' : 'box',
	'boxType' : 'plot',
	'fileId': pie_scheme_id,
	'title' : 'Fuel'
}

my_dashboard.insert(box_3)
my_dashboard.insert(box_1, 'above', 1)
my_dashboard.insert(box_2, 'right', 2)

py.dashboard_ops.upload(my_dashboard, 'DB Lab 3')