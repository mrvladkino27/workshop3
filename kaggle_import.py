import cx_Oracle
import re

username = 'system'
password = '1234567890'
database = 'localhost/xe'

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()
table_name = ['LOT', 'CAR', 'TRANSMISSION', 'CAR_MODEL', 'MANUFACTURER', ' CAR_TYPE', 'COLOR', 'COUNT_CYLINDERS', 'DRIVE', 'FUEL',  'US_STATE', 'REGION']
for table in table_name:
	cursor.execute("DELETE FROM "+table)

print("tables data were deleted if exist")
regions = set([])
states = set([])
manufacturers = set([])
models = set([])
lots = set([])
colors = set([])
transmissions = set([])
drives = set([])
types = set([])
cylinders = set([])
fuels = set([])
vins = set([])
i = 0
with open('vehicles.csv', encoding='utf-8', newline='') as f:
	f.readline()
	for line in f:
		mess = line.split(',')
		i += 1
		print("to the next commit - ", 100 - i%100)
		# print(i ,"  region - ", mess[2])
		# print("price - ", mess[4])
		# regions.add(mess[2])
		# # print("year - ", mess[5])
		# print("manufacturer - ",mess[6])
		# print("model - ", mess[7])
		# # print("condition - ", mess[8])
		# # print("cylinders - ", mess[9])
		# # print("fuel - ", mess[10])
		# # print("mileage - ", mess[11])
		# # print("transmission - ", mess[13])
		# print("VIN - ", mess[14])
		# # print("drive - ", mess[15])
		# # print("type - ", mess[17])
		# # print("color - ", mess[18])
		# print("state - ", mess[-3])
		# # print("coord: (",mess[-2],",",mess[-1][:-2],")")
		if (i%100) == 0:
				connection.commit()
		try:
			if len(mess[2]) > 0 and mess[2] not in regions:
				if re.match(r'\W\b', mess[2]):
					mess[2] = mess[2][1:]	
				query = """INSERT INTO Region (region) VALUES(:region)"""
				regions.add(mess[2])
				cursor.execute(query, region= mess[2])
			if re.match(r'\w{,3}', mess[-3]) and mess[-3] not in states:
				states.add(mess[-3])
				cursor.execute("INSERT INTO US_STATE(state_name, state_region) VALUES(:state, :region)", state=mess[-3],region=mess[2])
			if mess[6] not in manufacturers and len(mess[6])>0 and not re.match(r'\W+', mess[6]) and re.match(r'\D',mess[6]):
				manufacturers.add(mess[6])
				cursor.execute("INSERT INTO Manufacturer(company_name) VALUES(:company)", company=mess[6])
			model_id = tuple([mess[7],mess[6]])
			if mess[6] in manufacturers and model_id not in models and len(mess[7])>0:
				models.add(model_id)
				cursor.execute("INSERT INTO Car_Model(model_name, model_manufactured) VALUES(:model, :company)", model=mess[7], company=mess[6])
			if len(mess[18]) == 0:
					mess[18] = 'red'
			if mess[18] not in colors and len(mess[18])>0 and not re.match(r'\W+', mess[18]) and re.match(r'\D',mess[18]):
				colors.add(mess[18])
				cursor.execute("INSERT INTO Color(color_name) VALUES(:color)", color=mess[18])
			if len(mess[13]) == 0:
					mess[13] = 'manual'
			if mess[13] not in transmissions and len(mess[13])>0 and not re.match(r'\W+', mess[13]) and re.match(r'\D',mess[13]):
				transmissions.add(mess[13])
				cursor.execute("INSERT INTO Transmission(transmission) VALUES(:trans)", trans=mess[13])
			if len(mess[15]) == 0:
					mess[15] = '2wd'
			if mess[15] not in drives:
				drives.add(mess[15])
				cursor.execute("INSERT INTO Drive(drive_name) VALUES(:dr)", dr=mess[15])
			if len(mess[17]) == 0:
					mess[17] = 'compact car'
			if mess[17] not in types:
				types.add(mess[17])
				cursor.execute("INSERT INTO Car_Type(type_name) VALUES(:type)", type=mess[17])
			if len(mess[9]) > 2:
				if re.match(r'\s\b', mess[9]):
					mess[9] = mess[9][1:]
				mess[9] = mess[9][:1]
			if len(mess[9]) == 0:
					mess[9] = 4
			if mess[9] not in cylinders:
				cylinders.add(mess[9])
				cursor.execute("INSERT INTO Count_cylinders(count_cylinders) VALUES(:count)", count=int(mess[9]))
			if mess[10] not in fuels and len(mess[10]) > 0:
				fuels.add(mess[10])
				cursor.execute("INSERT INTO Fuel(fuel_name) VALUES(:gas)", gas=mess[10])
			if len(mess[11]) == 0:
				mess[11] = 15000
			if len(mess[8]) == 0:
				mess[8] = 'new'
			if mess[14] not in vins and len(mess[14]) > 0 and len(mess[7]) > 0 and re.match(r'\d+', mess[5]) and len(mess[10]) > 0:
				vins.add(mess[14])
				cursor.execute("INSERT INTO Car(car_vin, car_model, car_color, car_fuel, car_type, car_transmission, car_count_cylinders, car_year, car_mileage, car_condition, car_drive) VALUES(:a,:b,:c,:d,:e,:f,:g,:h,:k,:l,:m)", a=mess[14],b=mess[7],c=mess[18],d=mess[10],e=mess[17],f=mess[13],g=int(mess[9]),h=int(mess[5]),k=int(mess[11]),l=mess[8],m=mess[15])
			lost_id = tuple([mess[4], mess[-2], mess[-1][:-2]])
			if lost_id not in lots and mess[14] in vins:
				lots.add(lost_id)
				cursor.execute("INSERT INTO Lot(lot_price, lot_vin, lot_state, lot_lat, lot_long) VALUES(:a,:b,:c,:d,:e)", a=int(lost_id[0]),b=mess[14],c=mess[-3],d=float(lost_id[1]),e=float(lost_id[2]))
		except Exception as e:
			pass
print('finish adding rows. now lets see what`s in db')

connection.close()


