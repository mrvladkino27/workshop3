import csv
 
import cx_Oracle
 
username = 'system'
password = '1234567890'
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
    ,TRIM(CAR_COUNT_CYLINDERS) as car_cylinders
    ,TRIM(CAR_YEAR) as car_year
    ,TRIM(CAR_MILEAGE) as car_mileage
    ,TRIM(CAR_CONDITION) as car_condition
    ,TRIM(CAR_DRIVE) as car_drive
FROM CAR""")
 
 

with open("car_model"+".csv", "w+", newline="") as file:
    for car_vin,car_model,car_type,car_color,car_transmission,car_fuel,car_cylinders,car_year,car_mileage,car_condition,car_drive in cursor_car.fetchall():
        writer = csv.writer(file)
 
        writer.writerow(["VIN", car_vin])
        writer.writerow(["MODEL", car_model])
        writer.writerow(["YEAR", car_year])
        writer.writerow(["FUEL", car_fuel])
        writer.writerow(["TYPE", car_type])
        writer.writerow(["TRANSMISSION", car_transmission])
        writer.writerow(["COUNT_CYLINDERS", car_cylinders])
        writer.writerow(["MILEAGE", car_mileage])
        writer.writerow(["DRIVE", car_drive])
        writer.writerow(["COLOR", car_color])
        writer.writerow(["CONDITION", car_condition])
        cursor_car.execute("""
            SELECT TRIM(CAR_MODEL.model_manufactured)
            FROM CAR_MODEL
            WHERE CAR_MODEL.model_name = :model""", model=car_model)
        writer.writerow(["MANUFACTURER", cursor_car.fetchone()[0]])
        cursor_lot = connection.cursor()
 
        query = """
                    SELECT TRIM(LOT.lot_price) AS price
                         ,TRIM(LOT.lot_lat) AS x
                         ,TRIM(LOT.lot_long) AS y
                         ,TRIM(LOT.lot_state) AS state
                         ,TRIM(US_STATE.state_region) AS region
                    FROM CAR JOIN LOT ON CAR.car_vin = LOT.lot_vin
                         JOIN US_STATE ON LOT.lot_state = US_STATE.state_name
                    WHERE CAR.car_vin = :vin"""
 
        cursor_lot.execute(query, vin = car_vin)
        writer.writerow([])
        writer.writerow([" Price "," Coordinates ", " State "," Region "])
        for lot_row in cursor_lot:
            writer.writerow(lot_row)
        writer.writerow([])
        writer.writerow([])
 
connection.close()