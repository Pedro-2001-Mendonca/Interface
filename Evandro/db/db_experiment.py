import sqlite3
from Evandro.classes import experiment_class as ec


ns_exp = ec.NotSynchronizedExperiment
def __create_db_ns_experiment__(db_name, ns_exp):

    new_db = sqlite3.connect(db_name + '.db')

    try:

        new_cursor = new_db.cursor()

        new_cursor.execute("DROP TABLE if exists temperature")
        new_cursor.execute("DROP TABLE if exists flow")
        new_cursor.execute("DROP TABLE if exists y")

        new_cursor.execute("CREATE TABLE temperature (temperature_t float, temperature float)")
        new_cursor.execute("CREATE TABLE flow (flow_t float, flow float)")
        new_cursor.execute("CREATE TABLE y (y_t float, y float)")

        for i in range(len(ns_exp.time_temperature_column)):
            new_cursor.execute("INSERT INTO temperature VALUES(" + str(ns_exp.time_temperature_column[i]) + ","
                               + str(ns_exp.temperature_column[i]) + ")")
        for i in range(len(ns_exp.time_flow_column)):
            new_cursor.execute("INSERT INTO flow VALUES(" + str(ns_exp.time_flow_column[i]) + ","
                               + str(ns_exp.flow_column[i]) + ")")
        for i in range(len(ns_exp.time_y_column)):
            new_cursor.execute("INSERT INTO y VALUES(" + str(ns_exp.time_y_column[i]) + ","
                               + str(ns_exp.y_column[i]) + ")")

        new_cursor.execute("DROP TABLE if exists constants")

        new_cursor.execute("CREATE TABLE constants ("
                           "inlet_temperature float, "
                           "inlet_flow float, "
                           "inlet_y float,"
                           "inlet_p float,"
                           "ads_mass float, "
                           "bed_length float, "
                           "bed_diameter float, "
                           "porosity float,"
                           "c_in float)")

        new_cursor.execute("INSERT INTO constants VALUES("
                           + str(ns_exp.inlet_temperature) +
                           "," + str(ns_exp.inlet_flow) +
                           "," + str(ns_exp.inlet_y) +
                           "," + str(ns_exp.inlet_pressure) +
                           "," + str(ns_exp.adsorbent_mass) +
                           "," + str(ns_exp.bed_length) +
                           "," + str(ns_exp.bed_diameter) +
                           "," + str(ns_exp.porosity) +
                           "," + str(ns_exp.c_in) +
                           ")")

    except:
        return print("Erro no banco de dados!!")
    else:
        new_db.commit()
    finally:
        new_db.close()

