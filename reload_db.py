from time import sleep
from parse_for import *
from parse_con import *


def reload_db():
    while True:
        conn = connect("coservatort.sqlite")
        conn.execute("DELETE FROM con1")
        conn.execute("DELETE FROM con2")
        conn.commit()
        sleep(20)

        update_philarmony()
        update_conservatory()

        sleep(60*60)
