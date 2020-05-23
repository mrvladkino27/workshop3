import cx_Oracle
import re

username = 'system'
password = 'ozotos22'
database = 'localhost/xe'

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()
table_name = ['LOT', 'CAR', 'TRANSMISSION', 'CAR_MODEL', 'MANUFACTURER', ' CAR_TYPE', 'COLOR', 'CAR_CYLINDERS', 'DRIVE', 'FUEL', 'REGION' , 'US_STATE']
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
j = 0
with open('vehicles.csv') as f:
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
			if re.match(r'\w{,3}', mess[-3]) and mess[-3] not in states:
				if re.match(r'\W\b', mess[2]):
					mess[2] = mess[2][1:]	
				query = """INSERT INTO US_STATE (state_name) VALUES(:state)"""
				states.add(mess[-3])
				cursor.execute(query, state= mess[-3])
			if  len(mess[2]) > 0 and mess[2] not in regions:
				regions.add(mess[2])
				cursor.execute("INSERT INTO REGION(region_state, region_name) VALUES(:state, :region)", state=mess[-3],region=mess[2])
			if mess[6] not in manufacturers and len(mess[6])>0 and not re.match(r'\W+', mess[6]) and re.match(r'\D',mess[6]):
				manufacturers.add(mess[6])
				cursor.execute("INSERT INTO Manufacturer(company_name) VALUES(:company)", company=mess[6])
			if mess[6] in manufacturers and mess[7] not in models and len(mess[7])>0:
				models.add(mess[7])
				cursor.execute("INSERT INTO Car_Model(model_name, model_manufactured) VALUES(:model, :company)", model=mess[7], company=mess[6])
			if len(mess[18]) == 0:
					mess[18] = 'red'
			if mess[18] not in colors and len(mess[18])>0 and not re.match(r'\W+', mess[18]) and re.match(r'\D',mess[18]) and mess[18] not in types:
				colors.add(mess[18])
				cursor.execute("INSERT INTO Color(color_name) VALUES(:color)", color=mess[18])
			if len(mess[13]) == 0:
					mess[13] = 'manual'
			if mess[13] not in transmissions and len(mess[13])>0 and not re.match(r'\W+', mess[13]) and re.match(r'\D',mess[13]):
				transmissions.add(mess[13])
				cursor.execute("INSERT INTO Transmission(trans_name) VALUES(:trans)", trans=mess[13])
			if len(mess[15]) == 0:
					mess[15] = '2wd'
			if mess[15] not in drives and len(mess[15])<5:
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
				cursor.execute("INSERT INTO Car_cylinders(count_cylinders) VALUES(:count)", count=int(mess[9]))
			if mess[10] not in fuels and len(mess[10]) > 0 and len(mess[10])<=9:
				fuels.add(mess[10])
				cursor.execute("INSERT INTO Fuel(fuel_name) VALUES(:gas)", gas=mess[10])
			if len(mess[11]) == 0:
				mess[11] = 15000
			if len(mess[8]) == 0:
				mess[8] = 'new'
			if mess[14] not in vins and len(mess[14]) > 5 and len(mess[7]) > 0 and re.match(r'\d+', mess[5]) and len(mess[10]) > 0 and mess[7] in models and mess[15] in drives:
				vins.add(mess[14])
				cursor.execute("INSERT INTO Car(car_vin, car_model, car_color, car_fuel, car_type, car_transmission, car_count_cylynders, car_year, car_mileage, car_condition, car_drive) VALUES(:a,:b,:c,:d,:e,:f,:g,:h,:k,:l,:m)", a=mess[14],b=mess[7],c=mess[18],d=mess[10],e=mess[17],f=mess[13],g=int(mess[9]),h=int(mess[5]),k=int(mess[11]),l=mess[8],m=mess[15])
			lots_id = tuple([mess[4], mess[14]])
			if lots_id not in lots and mess[14] in vins:
				lots.add(lots_id)
				cursor.execute("INSERT INTO Lot(lot_price, lot_vin, lot_region) VALUES(:a,:b,:c)", a=int(lots_id[0]),b=mess[14],c=mess[2])
			else: 
				j += 1
		except Exception as e:
			print e
print('finish adding rows. now lets see what`s in db')
print('all amount of rows readed - ', i)
print('passed - ', j)

connection.close()


