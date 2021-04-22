from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def showCars() :
    global message, conn, cursor
    message = ""
    conn = pyodbc.connect(Trusted_Connection='yes', driver ='{SQL Server}', server = 'LAPTOP-4RH11BIJ', database = 'CarDB')
    cursor = conn.cursor()

    if request.method == 'POST' :
        if request.form['myaction'] == "Create Car" :
            addCar()
        if request.form['myaction'] == "Update Car" :
            updateCar()
        if request.form['myaction'] == 'Delete Car' :
            deleteCar()

    cursor.execute("SELECT * FROM Cars")
    data = cursor.fetchall()
    cursor.execute("SELECT Model, Image, MaxSpeed FROM Cars where MaxSpeed = ( SELECT MAX(MaxSpeed) FROM Cars )")
    fastCar = cursor.fetchall()
    conn.close()
    picturesPath = os.path.join('static', 'images')

    return render_template(
        "index.html",
        title = "Cars List",
        h1Title = "Cars Seepds ",
        values = data,
        path = picturesPath,
        message = message,
        car = fastCar
        )

def addCar():
    global message, conn, cursor

    try:
        id = int(request.form['id'])
        model = request.form['model']
        maxspeed = int(request.form['maxspeed'])
        color = request.form['color']
        image = request.form['image']

        cursor.execute("Insert into Cars values(?,?,?,?,?)", id, model, maxspeed, color, image)
        conn.commit()
        message = "Car " + request.form['id'] + " added."
    except Exception as ex:
        message = "Car " + request.form['id'] + " : error in data."

def updateCar():
    global message, conn, cursor

    try:
        id = int(request.form['id'])
        model = request.form['model']
        maxspeed = int(request.form['maxspeed'])
        color = request.form['color']
        image = request.form['image']

        cursor.execute("UPDATE Cars set Model = ?, MaxSpeed = ?, Color = ?, Image = ? WHERE ID = ?", model, maxspeed, color, image, id)
        conn.commit()
        message = "Car " + request.form['id'] + " was updated."
    except Exception as ex:
        message = "Car " + request.form['id'] + " : error in data."

def deleteCar():
    global message, conn, cursor

    try:
        id = int(request.form['id'])

        cursor.execute("DELETE FROM Cars WHERE ID = ?", id)
        conn.commit()
        message = "Car " + request.form['id'] + " was deleted."
    except Exception as ex:
        message = "Car " + request.form['id'] + " : error in data."


if __name__ == '__main__' :
    app.run('localhost', 4449)
