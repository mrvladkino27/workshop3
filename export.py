import csv
 
import cx_Oracle
 
username = 'system'
password = 'ozotos22'
database = 'localhost/xe'

connection = cx_Oracle.connect(username, password, database) 
cursor_car = connection.cursor()
cursor_car.execute("""
SELECT
    TRIM(CAR_VIN) as car_vin
    ,TRIM(CAR_MODEL) as car_model
    ,TRIM(CAR_TYPE) as car_type
    ,TRIM(CAR_COLOR) as car_color
    ,TRIM(CAR_TRANSMISSION) as car_transmission
    ,TRIM(CAR_FUEL) as car_fuel
    ,TRIM(CAR_COUNT_CYLYNDERS) as car_cylinders
    ,TRIM(CAR_YEAR) as car_year
    ,TRIM(CAR_MILEAGE) as car_mileage
    ,TRIM(CAR_CONDITION) as car_condition
    ,TRIM(CAR_DRIVE) as car_drive
FROM CAR""")
with open("car"+".csv", "w+") as file:
	writer = csv.writer(file)
	writer.writerow(["VIN", "MODEL", "YEAR","FUEL","TYPE","TRANSMISSION","COUNT_CYLINDERS","MILEAGE","DRIVE","COLOR","CONDITION"])
	for car_vin, car_model, car_type, car_color, car_transmission, car_fuel, car_cylinders, car_year, car_mileage, car_condition, car_drive in cursor_car.fetchall():
		writer.writerow([car_vin, car_model,car_year, car_fuel, car_type, car_transmission, car_cylinders, car_mileage, car_drive, car_color, car_condition])
print('Car file was created')
with open("car_model"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(model_manufactured) as model
        , TRIM(model_manufactured) as company
        FROM CAR_MODEL""")
	writer = csv.writer(file)
	writer.writerow(["MODEL", "MANUFACTURED"])
	for model, company in cursor_car.fetchall():
		writer.writerow([model,company])
print('Car_model file was created')
with open("Manufacturers"+".csv", "w+") as file:
    cursor_car.execute("""
        SELECT TRIM(company_name) as company
        FROM Manufacturer""")
    writer = csv.writer(file)
    writer.writerow(["MANUFACTURED"])
    for company in cursor_car.fetchall():
		writer.writerow([company])
print('Manufacturers file was created')
with open("Color"+".csv", "w+") as file:
	cursor_car.execute("""
		SELECT TRIM(color_name) as color
        FROM Color""")
	writer = csv.writer(file)
	writer.writerow(["Colors"])
	for color in cursor_car.fetchall():
		writer.writerow([color])
print('Color file was created')
with open("Fuel"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(fuel_name) as fuel
        FROM Fuel""")
	writer = csv.writer(file)
	writer.writerow(["Fuels"])
	for fuel in cursor_car.fetchall():
		writer.writerow([fuel])
print('Fuel file was created')
with open("Car_type"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(type_name) as ctype
        FROM CAR_TYPE""")
	writer = csv.writer(file)
	writer.writerow(["Types"])
	for ctype in cursor_car.fetchall():
		writer.writerow([ctype])
print('TYPES file was created')
with open("Transmission"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(trans_name) as trans
        FROM Transmission""")
	writer = csv.writer(file)
	writer.writerow(["Transmission"])
	for trans in cursor_car.fetchall():
		writer.writerow([trans])
print('Transmission file was created')
with open("CAR_CYLINDERS"+".csv","w+") as file:
	cursor_car.execute("""
        SELECT TRIM(count_cylinders) as cil
        FROM CAR_CYLINDERS""")
	writer = csv.writer(file)
	writer.writerow(["CAR_CYLINDERS"])
	for cil in cursor_car.fetchall():
		writer.writerow([cil])
print('CAR_CYLINDERS file was created')
with open("Drive"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(drive_name) as dr
        FROM Drive""")
	writer = csv.writer(file)
	writer.writerow(["Drive"])
	for dr in cursor_car.fetchall():
		writer.writerow([dr])
print('Drive file was created')
with open("US_STATE"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(state_name) as st
        FROM US_STATE""")
	writer = csv.writer(file)
	writer.writerow(["US_STATE"])
	for st in cursor_car.fetchall():
		writer.writerow([st])
print('States file was created')
with open("region"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(region_name) as rg
        , TRIM(region_state) as st
        FROM Region""")
	writer = csv.writer(file)
	writer.writerow(["REGION", "US_STATE"])
	for rg, st in cursor_car.fetchall():
		writer.writerow([rg,st])
print('Region file was created')
with open("Lot"+".csv", "w+") as file:
	cursor_car.execute("""
        SELECT TRIM(lot_price) as pr
        , TRIM(lot_vin) as vin
        , TRIM(lot_region) as rg
        FROM LOT""")
	writer = csv.writer(file)
	writer.writerow(["PRICE","VIN","REGION"])
	for pr,vin,rg in cursor_car.fetchall():
		writer.writerow([pr,vin,rg])
print('LOT file was created')
    # cursor_lot = connection.cursor()

    #     query = """
    #                 SELECT TRIM(LOT.lot_price) AS price
    #                      ,TRIM(LOT.lot_lat) AS x
    #                      ,TRIM(LOT.lot_long) AS y
    #                      ,TRIM(LOT.lot_state) AS state
    #                      ,TRIM(US_STATE.state_region) AS region
    #                 FROM CAR JOIN LOT ON CAR.car_vin = LOT.lot_vin
    #                      JOIN US_STATE ON LOT.lot_state = US_STATE.state_name
    #                 WHERE CAR.car_vin = :vin"""
 
    #     cursor_lot.execute(query, vin = car_vin)
    #     writer.writerow([])
    #     writer.writerow([" Price "," Coordinates ", " State "," Region "])
    #     for lot_row in cursor_lot:
    #         writer.writerow(lot_row)
    #     writer.writerow([])
    #     writer.writerow([])
 
connection.close()