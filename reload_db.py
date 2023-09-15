from os import abort
from time import sleep
from parse_for import *
from parse_con import *


def reload_db():
    print('hi')
    while True:
        conn = connect("coservatort.sqlite")
        conn.execute("DELETE FROM con1")
        conn.execute("DELETE FROM con2")
        conn.commit()
        sleep(20)

        update_philarmony()
        update_conservatory()
        print('done')

        sleep(10000**100000)


reload_db()