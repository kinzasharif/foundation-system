from flask import Flask, render_template, url_for, request, session, redirect, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime 
import mysql.connector

def get_db_conection():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="foundation_system"
        )
        return conn

app = Flask(__name__)
app.secret_key = "secret123"

@app.route('/')
@app.route('/index')
def index():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)
    
    # Get counts and totals for dashboard
    cursor.execute("SELECT COUNT(*) as count FROM donors")
    donor_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM donations")
    donation_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT SUM(amount) as total FROM donations")
    donation_total = cursor.fetchone()['total'] or 0
    
    cursor.execute("SELECT SUM(amount) as total FROM expenses")
    expense_total = cursor.fetchone()['total'] or 0
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', 
                         donor_count=donor_count,
                         donation_count=donation_count,
                         donation_total=donation_total,
                         expense_total=expense_total)

@app.route('/view_expenses')
def view_expenses():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()
    
    # Calculate total
    cursor.execute("SELECT SUM(amount) as total FROM expenses")
    total = cursor.fetchone()['total']
    
    cursor.close()
    conn.close()
    return render_template('view_expenses.html', expenses=expenses, total=total)

@app.route('/view_donations')
def view_donations():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)
    
    
    cursor.execute("""
SELECT * FROM donors""")
    donor = cursor.fetchall()
    cursor.execute("""
        SELECT d.*, donors.name as donor_name 
        FROM donations d
        LEFT JOIN donors ON d.donor_id = donors.id
        ORDER BY d.donation_date DESC
    """)
    donations = cursor.fetchall()
    
    # Calculate total
    cursor.execute("SELECT SUM(amount) as total FROM donations")
    total = cursor.fetchone()['total']
    
    cursor.close()
    conn.close()
    return render_template('view_donations.html', donations=donations, total=total, donor=donor)


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        description = request.form.get('description')
        amount = request.form.get('amount')
        date = request.form.get('expense_date')
        
        cursor.execute("INSERT INTO expenses (description, amount, expense_date) VALUES (%s, %s, %s)", 
                      (description, amount, date))
        conn.commit()
        flash("Expense Added Successfully!")
        return redirect(url_for('add_expense'))
    
    cursor.close()
    conn.close()
    return render_template('add_expense.html')

@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all donors for dropdown
    cursor.execute("SELECT id, name, phone, cnic FROM donors ORDER BY name")
    donors = cursor.fetchall()
    
    if request.method == 'POST':
        donor_id = request.form.get('donor_id')
        amount = request.form.get('amount')
        date = request.form.get('donation_date')
        
        # Basic validation
        if not donor_id or not amount:
            flash("Please fill all fields")
            return redirect(url_for('add_donation'))
        
        try:
            cursor.execute("INSERT INTO donations (donor_id, amount, donation_date) VALUES (%s, %s, %s)", 
                          (donor_id, amount, date))
            conn.commit()
            flash("Donation Added Successfully! 🎉")
        except Exception as e:
            flash(f"Error: {e}")
            print(e)
        
        return redirect(url_for('add_donation'))
    
    cursor.close()
    conn.close()
    return render_template('add_donation.html', donors=donors)

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)

    # # if 'id' not in session and session['role'] != 'admin':
    #      flash("Please Login as Admin First ")
    #      return redirect('admin_login')
    if request.method == 'POST':
         
        name = request.form['name']
        phone = request.form['phone']
        cnic = request.form['cnic']

        cursor.execute("INSERT INTO donors (name, phone , cnic) VALUES (%s, %s, %s)", (name, phone, cnic))
        conn.commit()

        flash("Donor Added Successfully")
    cursor.close()
    conn.close()
    return render_template('add_donor.html')

if __name__ == '__main__':
    app.run(debug=True)