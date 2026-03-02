from flask import Flask, render_template, url_for, request, session, redirect, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime 
import mysql.connector
from PIL import Image

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


app.config['MAX_CONTENT_LENGTH'] = 16 * 16 * 1024
app.config['ALLOWED_EXTENSIONS'] = 'jpg', 'jpeg', 'png'

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
    
    return render_template('index.html',register_user=True, 
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
    return redirect(url_for('user_profile'))

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
            return redirect(url_for('user_profile'))
        
        try:
            cursor.execute("INSERT INTO donations (donor_id, amount, donation_date) VALUES (%s, %s, %s)", 
                          (donor_id, amount, date))
            conn.commit()
            flash("Donation Added Successfully! 🎉")
        except Exception as e:
            flash(f"Error: {e}")
            print(e)
        
        return redirect(url_for('user_profile'))
    
    cursor.close()
    conn.close()
    return redirect(url_for(user_profile))

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
         
        name = request.form['name']
        phone = request.form['phone']
        cnic = request.form['cnic']

        cursor.execute("INSERT INTO donors (name, phone , cnic) VALUES (%s, %s, %s)", (name, phone, cnic))
        conn.commit()

        flash("Donor Added Successfully")
    
    cursor.execute("SELECT id, name FROM donors ORDER BY name")
    donors = cursor.fetchall()

    cursor.close()
    conn.close()
    return redirect(url_for('user_profile'))

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        conn = get_db_conection()
        cursor = conn.cursor(dictionary=True)

        identifier = request.form.get('identifier')
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND role='user'", (identifier, identifier))  
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']
            session['phone'] = user.get('phone', '')
            session['cnic'] = user.get('cnic', '')
            session['picture'] = user.get('picture', '')

            cursor.close()
            conn.close()
            flash("✅ Login successful!")
            return redirect(url_for('user_profile')) 
        else:
            flash("❌ Invalid Username or Password")
            cursor.close()
            conn.close()
            return render_template('Userlogin.html',register_user=True, home=True)
    
    return render_template('Userlogin.html', register_user=True, home=True)

@app.route('/user_profile')
# @login_required
def user_profile():
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    cursor.execute("SELECT id, name FROM donors ORDER BY name")
    donors = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('Profile.html', user=user, show_pp=True, donors=donors, details=True)

@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    # Check if logged in
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('admin_login'))
    
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)

    # Get admin user data
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    if not user:
        session.clear()
        flash("User not found")
        return redirect(url_for('admin_login'))
    
    # Get dashboard stats - with safe defaults
    cursor.execute("SELECT COUNT(*) as count FROM donors")
    result = cursor.fetchone()
    donor_count = result['count'] if result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM donations")
    result = cursor.fetchone()
    donation_count = result['count'] if result else 0
    
    cursor.execute("SELECT SUM(amount) as total FROM donations")
    result = cursor.fetchone()
    donation_total = result['total'] if result and result['total'] else 0
    
    cursor.execute("SELECT SUM(amount) as total FROM expenses")
    result = cursor.fetchone()
    expense_total = result['total'] if result and result['total'] else 0
    
    # Get all donations with donor names (will be empty list if no data)
    cursor.execute("""
        SELECT d.*, donors.name as donor_name 
        FROM donations d
        LEFT JOIN donors ON d.donor_id = donors.id
        ORDER BY d.donation_date DESC
    """)
    donations = cursor.fetchall() or []
    
    # Get all expenses
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall() or []
    
    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html',
                         user=user,
                         donor_count=donor_count,
                         donation_count=donation_count,
                         donation_total=donation_total,
                         expense_total=expense_total,
                         donations=donations,
                         expenses=expenses,
                         Profile=True)

@app.route('/admin/update_profile', methods=['GET','POST'])
def admin_update_profile():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if not user:
        flash("❌ User not found")
        cursor.close()
        conn.close()
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        if 'remove_picture' in request.form:
            if user['picture']:
                old_image_path = os.path.join('static', user['picture'])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            cursor.execute("UPDATE users SET picture='' WHERE id=%s", (session['user_id'],))
            session['picture'] = ''
            conn.commit()
            cursor.close()
            conn.close()
            flash("✅ Profile picture removed successfully!")
            return redirect(url_for('admin_update_profile'))

        user_id = session['user_id']
        username = request.form.get('username', user['username']).strip()
        email = request.form.get('email', user['email']).strip()
        phone = request.form.get('phone', user.get('phone', '')).strip()
        cnic = request.form.get('cnic', user.get('cnic', '')).strip()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        picture_path = user['picture']

        if 'picture' in request.files:
            file = request.files['picture']
            if file and file.filename != '' and allowed_file(file.filename):
                if user['picture']:
                    old_image_path = os.path.join('static', user['picture'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                unique_filename = f"admin_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join('static/uploads/users', unique_filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)

                try:
                    img = Image.open(filepath)
                    img.thumbnail((500, 500))
                    img.save(filepath)
                except:
                    pass

                picture_path = f"uploads/users/{unique_filename}"

        if username != user['username'] or email != user['email']:
            cursor.execute(
                "SELECT * FROM users WHERE (username=%s OR email=%s) AND id != %s",
                (username, email, user_id)
            )
            if cursor.fetchone():
                flash("❌ Username or Email already exists! Choose another username/email")
                cursor.close()
                conn.close()
                return redirect(url_for('admin_update_profile'))

        cursor.execute(
            "UPDATE users SET username=%s, email=%s, phone=%s, cnic=%s, picture=%s WHERE id=%s",
            (username, email, phone, cnic, picture_path, user_id)
        )

        if current_password or new_password or confirm_password:
            if not current_password or not new_password or not confirm_password:
                flash("❌ To change password, all password fields are required")
                cursor.close()
                conn.close()
                return redirect(url_for('admin_update_profile'))

            if not check_password_hash(user['password'], current_password):
                flash("❌ Current password is incorrect")
                cursor.close()
                conn.close()
                return redirect(url_for('admin_update_profile'))

            if new_password != confirm_password:
                flash("❌ New password and confirm password do not match")
                cursor.close()
                conn.close()
                return redirect(url_for('admin_update_profile'))

            hashed_new_password = generate_password_hash(new_password)
            cursor.execute(
                "UPDATE users SET password=%s WHERE id=%s",
                (hashed_new_password, user_id)
            )
            flash("✅ Password updated successfully!")
        else:
            flash("✅ Profile updated successfully!")

        session['username'] = username
        session['email'] = email
        session['phone'] = phone
        session['cnic'] = cnic
        session['picture'] = picture_path
        session.modified = True

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin_profile'))
    
    return render_template('AdminHome.html', user=user, Dashboard=True)

@app.route('/update_profile', methods=['GET', 'POST'])
def user_settings():
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('user_login'))
    
    conn = get_db_conection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    if not user:
        flash("❌ User not found")
        cursor.close()
        conn.close()
        return redirect(url_for('user_login'))
    
    if request.method == 'POST':
        if 'remove_picture' in request.form:
            if user['picture']:
                old_image_path = os.path.join('static', user['picture'])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            cursor.execute("UPDATE users SET picture='' WHERE id=%s", (session['user_id'],))
            session['picture'] = ''
            conn.commit()
            cursor.close()
            conn.close()
            flash("✅ Profile picture removed successfully!")
            return redirect(url_for('user_settings'))

        user_id = session['user_id']
        username = request.form.get('username', user['username']).strip()
        email = request.form.get('email', user['email']).strip()
        phone = request.form.get('phone', user.get('phone', '')).strip()
        cnic = request.form.get('cnic', user.get('cnic', '')).strip()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        picture_path = user['picture']

        if 'picture' in request.files:
            file = request.files['picture']
            if file and file.filename != '' and allowed_file(file.filename):
                if user['picture']:
                    old_image_path = os.path.join('static', user['picture'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                unique_filename = f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join('static/uploads/users', unique_filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)

                try:
                    img = Image.open(filepath)
                    img.thumbnail((500, 500))
                    img.save(filepath)
                except:
                    pass

                picture_path = f"uploads/users/{unique_filename}"

        if username != user['username'] or email != user['email']:
            cursor.execute(
                "SELECT * FROM users WHERE (username=%s OR email=%s) AND id != %s",
                (username, email, user_id)
            )
            if cursor.fetchone():
                flash("❌ Username or Email already exists! Choose another username/email")
                cursor.close()
                conn.close()
                return redirect(url_for('user_settings'))

        cursor.execute(
            "UPDATE users SET username=%s, email=%s, phone=%s, cnic=%s, picture=%s WHERE id=%s",
            (username, email, phone, cnic, picture_path, user_id)
        )

        if current_password or new_password or confirm_password:
            if not current_password or not new_password or not confirm_password:
                flash("❌ To change password, all password fields are required")
                cursor.close()
                conn.close()
                return redirect(url_for('user_settings'))

            if not check_password_hash(user['password'], current_password):
                flash("❌ Current password is incorrect")
                cursor.close()
                conn.close()
                return redirect(url_for('user_settings'))

            if new_password != confirm_password:
                flash("❌ New password and confirm password do not match")
                cursor.close()
                conn.close()
                return redirect(url_for('user_settings'))

            hashed_new_password = generate_password_hash(new_password)
            cursor.execute(
                "UPDATE users SET password=%s WHERE id=%s",
                (hashed_new_password, user_id)
            )
            flash("✅ Password updated successfully!")
        else:
            flash("✅ Profile updated successfully!")

        session['username'] = username
        session['email'] = email
        session['phone'] = phone
        session['cnic'] = cnic
        session['picture'] = picture_path
        session.modified = True

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('user_settings'))
    
    return render_template('UserSettings.html', user=user)
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        conn = get_db_conection()
        cursor = conn.cursor(dictionary=True)

        identifier = request.form.get('identifier')
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND role='admin'", (identifier, identifier))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):  
            session.update({
                'user_id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'phone': user.get('phone', ''),
                'cnic': user.get('cnic', ''),
                'picture': user.get('picture', '')
            })
            flash("✅ Admin login successful!")
            return redirect(url_for('admin_profile'))
        else:
            flash("❌ Invalid Admin Username or Password")
            return render_template('adminlogin.html', register_user=True, home=True)

    return render_template('adminlogin.html', register_user=True, home=True)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password']

            hashed_password = generate_password_hash(password)

            phone = request.form['phone'].strip()
            cnic = request.form['cnic'].strip()

            picture_path = None
            if 'picture' in request.files:
                file = request.files['picture']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    filepath = os.path.join('static/uploads/users', unique_filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)

                    try:
                        img = Image.open(filepath)
                        img.thumbnail((500, 500))
                        img.save(filepath)
                    except Exception as e:
                        print(f"Error processing image: {e}")

                    picture_path = f"uploads/users/{unique_filename}"

            conn = get_db_conection()
            cursor = conn.cursor(dictionary=True)

            # Check if username OR email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("❌ Username or Email already exists! Please use a different one.")
                cursor.close()
                conn.close()
                return redirect(url_for('register_user'))

            cursor.execute("""
                INSERT INTO users (username, email, password, picture, phone, cnic, role)
                VALUES (%s, %s, %s, %s, %s, %s, 'user')
            """, (username, email, hashed_password, picture_path, phone, cnic))

            conn.commit()
            cursor.close()
            conn.close()

            flash("✅ Registration successful! Please login.")
            return redirect(url_for('user_login'))

        except mysql.connector.Error as db_err:
            print(f"Database error: {db_err}")
            flash("⚠️ Database error occurred. Please try again.")
            return redirect(url_for('register_user'))

        except Exception as e:
            print(f"Error during registration: {e}")
            flash("⚠️ Something went wrong during registration. Try again.")
            return redirect(url_for('register_user'))

    return render_template('Register.html', home=True)


@app.route('/admin_logout')
def admin_logout():
  
    session.clear()
    flash("✅ Logged Out Successfully!")
    return redirect(url_for('admin_login'))
    

@app.route('/user_logout')
def user_logout():
    
    session.clear()
    flash("✅ Logged Out Successfully!")
    return redirect(url_for('user_login'))
    

if __name__ == '__main__':
    app.run(debug=True)