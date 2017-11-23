import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)


def getConn():
    #Function to construct the connection string, make a connection and return it.
	conn=psycopg2.connect("dbname= 'postgres' user='postgres' password ='1234'  port=5431")
	return conn


# set homepage
@app.route('/')
def index():
	return render_template('master.html',message="")

@app.route('/addCust', methods =['POST'])
def addCust():
	#Function to create a new category in the database by retrieving information from forms.
	try:
		conn=None
		custFirst = request.form['first']
		custLast = request.form['last']
		custAddress= request.form['address']
		custEmail= request.form['email']

		conn=getConn()
		
		custIncrement = 'INSERT INTO leadcustomer VALUES((SELECT MAX(customerID) FROM leadcustomer) + 1'
		if  conn.cursor().execute('SELECT COUNT(*) FROM leadcustomer') == 0:
			custIncrement = 1
			
		conn.cursor().execute('%s,%s, %s, %s, %s)', \
					[custIncrement,custFirst,custLast,custAddress,custEmail])
		conn.commit()
		
		return render_template('master.html',message='Customer ' + custFirst + ' ' + custLast + ' added')
	except Exception as e:
			return render_template('master.html',message="Error adding Customer",error=e)
	finally:
		if conn:
			conn.close()
	

@app.route('/deleteCust', methods =['POST'])
def deleteCust():
	#Function to create a new category in the database by retrieving information from forms.
	try:
		conn=None
		custID = request.form['custID']

		conn=getConn()

		conn.cursor().execute('DELETE FROM leadcustomer WHERE CustomerID=%s ', \
					[custID])
		conn.commit()
		return render_template('master.html',message = 'Customer ' + '#' + custID +' Deleted')
	except Exception as e:
			return render_template('master.html',message="Error deleting Customer",error=e)
	finally:
		if conn:
			conn.close()

@app.route('/query5', methods =['POST'])
def query5():
	#Function to create a new category in the database by retrieving information from forms.
	try:
		conn=None
		

		conn=getConn()
		cur =conn.cursor()
		cur.execute('SELECT LeadCustomer.CustomerID, concat(LeadCustomer.FirstName,LeadCustomer.Surname) AS Name, \
					COUNT(FlightBooking.FlightID) AS NumFlights, \
					SUM(FlightBooking.TotalCost) AS TotalSpend \
					FROM LeadCustomer  \
					INNER JOIN FlightBooking \
 					ON LeadCustomer.CustomerID = FlightBooking.CustomerID \
					GROUP BY LeadCustomer.CustomerID, Name \
					ORDER BY TotalSpend DESC;')
		rows = cur.fetchall()
		
		for row in rows:
			#print(row['customerid'],row['name'], row['numflights'], row['totalspend'])
			print(row)
		conn.commit()
		return render_template('q5.html',rows = rows)
	except Exception as e:
			return render_template('master.html',message="Error",error=e)
	finally:
		if conn:
			conn.close()
				

	
	
if __name__ == "__main__":
	# secret key for sessions
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(debug = True)
	
conn.close()