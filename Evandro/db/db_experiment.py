import sqlite3

#banco = sqlite3.connect('banco.db')

#cursor = banco.cursor()

# cursor.execute("CREATE TABLE experimento"+str(1)+" (tempot float, temperatura float, tempoq float, q float, tempoy float, y float)")

#cursor.execute("INSERT INTO experimento" + str(1) + " VALUES(0,298.15, 0, 500,0,0)")

#banco.commit()


def __create_db_ns_experiment__(db_name,
                                temperature_t, temperature,
                                flow_t, flow,
                                y_t, y,
                                inlet_temperature,
                                inlet_flow,
                                inlet_y,
                                inlet_p,
                                ads_mass,
                                bed_length,
                                bed_diameter
                                ):
    new_db = sqlite3.connect(db_name + '.db')
    new_cursor = new_db.cursor()

    new_cursor.execute("CREATE TABLE temperature (temperature_t float, temperature float)")
    new_cursor.execute("CREATE TABLE flow (flow_t float, flow float)")
    new_cursor.execute("CREATE TABLE y (y_t float, y float)")
    new_cursor.execute("CREATE TABLE inlet_temperature (inlet_temperature float)")
    new_cursor.execute("CREATE TABLE inlet_flow (inlet_flow float)")
    new_cursor.execute("CREATE TABLE inlet_y (inlet_y float)")

    for i in range(len(temperature_t)):
        new_cursor.execute("INSERT INTO temperature VALUES(" + str(temperature_t[i]) + "," + str(temperature[i]) + ")")
    for i in range(len(temperature_t)):
        new_cursor.execute("INSERT INTO flow VALUES(" + str(flow_t[i]) + "," + str(flow[i]) + ")")
    for i in range(len(temperature_t)):
        new_cursor.execute("INSERT INTO y VALUES(" + str(y_t[i]) + "," + str(y[i]) + ")")

    new_cursor.execute("INSERT INTO inlet_temperature VALUES(" + str(inlet_temperature) +")")
    new_cursor.execute("INSERT INTO inlet_flow VALUES(" + str(inlet_flow) + ")")
    new_cursor.execute("INSERT INTO inlet_y VALUES(" + str(inlet_y) + ")")
    new_cursor.execute("INSERT INTO inlet_p VALUES(" + str(inlet_p) +")")
    new_cursor.execute("INSERT INTO ads_mass VALUES(" + str(ads_mass) + ")")
    new_cursor.execute("INSERT INTO bed_length VALUES(" + str(bed_length) + ")")
    new_cursor.execute("INSERT INTO bed_diameter VALUES(" + str(bed_diameter) + ")")
    new_cursor.execute("INSERT INTO inlet_temperature VALUES(" + str(inlet_temperature) + ")")

    new_db.commit()


__create_db_ns_experiment__('bancoTeste', [0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5])