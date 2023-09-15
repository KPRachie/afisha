from flask import render_template, request
from threading import Thread
from reload_db import *

app = Flask(__name__)


@app.route('/')
def show_all():
    global con1
    conn = connect("coservatort.sqlite")
    query = request.args.get("search", "")
    cursor = conn.execute(
        "SELECT * FROM con1 WHERE 'where' like ? or hall like ? or title like ? or song like ? or link like ? or date like ?",
        ["%{}%".format(query), "%{}%".format(query), "%{}%".format(query), "%{}%".format(query),
         "%{}%".format(query), "%{}%".format(query)])
    con = cursor.fetchall()
    con1 = con
    conn.close()

    return render_template("index.html", con=con)


th = Thread(target=reload_db)
th.start()

app.run(debug=True)
