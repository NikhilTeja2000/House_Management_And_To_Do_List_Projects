from flask import Flask, render_template, url_for, request, redirect
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
CORS(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    cooking = db.Column(db.String(200), default="N/A", nullable=False)
    cleaning = db.Column(db.String(200), default="N/A", nullable=False)

    def __repr__(self):
        return f'<Timetable {self.day}>'

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)  # Name of the grocery item
    bought_date = db.Column(db.DateTime, nullable=False)  # Date and time the item was purchased
    expiry_date = db.Column(db.DateTime, nullable=False)  # Expiry date and time of the item
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of the item
    price = db.Column(db.Float, nullable=False)  # Price of the item

    def __repr__(self):
        return f'<Grocery {self.item_name}>'
    
class Bills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_name = db.Column(db.String(200), nullable=False)  # Name of the bill
    amount = db.Column(db.Float, nullable=False)  # Amount to be paid
    due_date = db.Column(db.DateTime, nullable=False)  # Due date for the bill
    image = db.Column(db.String(200), nullable=False)  # Image file path for the bill

    def __repr__(self):
        return f'<Bill {self.bill_name}>'
    



def initialize_timetable():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if Timetable.query.count() == 0:  # Check if the table is empty
        for day in days:
            entry = Timetable(day=day)
            db.session.add(entry)
        print('end',days)
        db.session.commit()

# Landing page route
@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/assignment/homepage/')
def homepage():
 # Fetch the first AboutMe entry from the databas
    
    # Pass the 'about_me_entry' to the template
    return render_template('assignment/homepage.html')


@app.route('/assignment/grol/')
def grol():

    timetable_entries = Timetable.query.all()
    return render_template('assignment/grol.html', timetable_entries=timetable_entries)

@app.route('/assignment/resetgrol/')
def resetgrol():
    # Reset all timetable entries to "N/A"
    timetable_entries = Timetable.query.all()
    for entry in timetable_entries:
        entry.cooking = "N/A"
        entry.cleaning = "N/A"
    db.session.commit()  # Commit the changes to the database

    # Reload the timetable entries and render the template
    updated_timetable_entries = Timetable.query.all()
    print(updated_timetable_entries,"---------------")
    return render_template('assignment/grol.html', timetable_entries=updated_timetable_entries)

@app.route('/assignment/pantrypage/')
def pantrypage():

    groceries_entries = Grocery.query.all()
    return render_template('assignment/pantrypage.html', groceries_entries=groceries_entries)

@app.route('/assignment/bills/')
def bills():

    bills_entries = Bills.query.all()
    return render_template('assignment/bills.html', bills_entries=bills_entries)


@app.route('/assignment/update/<int:id>', methods=['GET', 'POST'])
def update_schedule(id):
    entry = Timetable.query.get_or_404(id)
    if request.method == 'POST':
        entry.cooking = request.form.get('cooking', "N/A")
        entry.cleaning = request.form.get('cleaning', "N/A")



        try:
            db.session.commit()
            return redirect('/assignment/grol')
        except:
            return 'There was an issue updating the timetable entry.'

    return render_template('assignment/houseupdate.html', entry=entry)

@app.route('/assignment/editbills/<int:id>', methods=['GET', 'POST'])
def update_bill(id):
    # Fetch the bill entry by ID or return a 404 error if not found
    entry = Bills.query.get_or_404(id)

    if request.method == 'POST':
        # Update fields from the form inputs
        entry.bill_name = request.form['bill_name']
        entry.amount = float(request.form['amount'])  # Ensure the amount is stored as a float

        # Convert the due date string to datetime
        try:
            entry.due_date = datetime.strptime(request.form['due_date'], "%Y-%m-%dT%H:%M")
        except ValueError:
            return 'Invalid date format'

        # Handle image upload
        bill_image = request.files['bill_image']
        if bill_image and allowed_file(bill_image.filename):
            filename = secure_filename(bill_image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            bill_image.save(file_path)
            entry.image = file_path  # Update image path if a new image is uploaded

        try:
            # Commit the changes to the database
            db.session.commit()
            return redirect('/assignment/bills/')  # Redirect to the bills management page
        except Exception as e:
            print(e)
            return 'There was an issue updating the bill entry.'

    # Render the update form if the request method is GET
    return render_template('assignment/editbills.html', entry=entry)


@app.route('/assignment/deletebills/<int:id>')
def deletebills(id):
    task_to_delete = Bills.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/assignment/bills/')
    except:
        return 'There was a problem deleting that task'

@app.route('/assignment/updates/<int:id>', methods=['GET', 'POST'])
def update_grocery(id):
    # Fetch the grocery entry by ID or return a 404 error
    entry = Grocery.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update the grocery entry fields with form data
        entry.item_name = request.form.get('item_name', entry.item_name)

        # Convert string to datetime objects
        try:
            entry.bought_date = datetime.strptime(request.form.get('bought_date', entry.bought_date), "%Y-%m-%dT%H:%M")
            entry.expiry_date = datetime.strptime(request.form.get('expiry_date', entry.expiry_date), "%Y-%m-%dT%H:%M")
        except ValueError:
            return 'Invalid date format'
        entry.quantity = request.form.get('quantity', entry.quantity)
        entry.price = request.form.get('price', entry.price)
        
        try:
            # Commit the changes to the database
            db.session.commit()
            return redirect('/assignment/pantrypage/')  # Redirect to the groceries list page
        except:
            # Handle any database commit issues
            return 'There was an issue updating the grocery entry.'

    # Render the update form template with the current entry data
    return render_template('/assignment/pantryupdate.html', entry=entry)



@app.route('/assginment/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/assginment/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('assignment/index.html', tasks=tasks)

from datetime import datetime

@app.route('/assignment/groceries/', methods=['POST', 'GET'])
def manage_groceries():
    if request.method == 'POST':
        # Retrieve form data
        item_name = request.form['item_name']
        bought_date_str = request.form['bought_date']
        expiry_date_str = request.form['expiry_date']
        quantity = request.form['quantity']
        price = request.form['price']
        
        # Convert string to datetime objects
        try:
            bought_date = datetime.strptime(bought_date_str, "%Y-%m-%dT%H:%M")
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            return 'Invalid date format'

        # Create a new Grocery object
        new_grocery = Grocery(
            item_name=item_name,
            bought_date=bought_date,
            expiry_date=expiry_date,
            quantity=int(quantity),  # Ensure it's an integer
            price=float(price)  # Ensure it's a float
        )
        
        try:
            # Add the new grocery entry to the database
            db.session.add(new_grocery)
            db.session.commit()
            return redirect('/assignment/groceries/')  # Redirect to the groceries page
        except Exception as e:
            print(e)
            return 'There was an issue adding your grocery entry'
    else:
        # Retrieve query parameters for sorting and filtering
        sort_by = request.args.get('sort_by', None)
        price_filter = request.args.get('price_filter', None)

        # Start with all grocery entries
        groceries = Grocery.query

        # Apply sorting
        if sort_by == "bought_date":
            groceries = groceries.order_by(Grocery.bought_date)
        elif sort_by == "expiry_date":
            groceries = groceries.order_by(Grocery.expiry_date)

        # Apply filtering
        if price_filter:
            try:
                price_filter = float(price_filter)
                groceries = groceries.filter(Grocery.price > price_filter)
            except ValueError:
                return "Invalid price filter value", 400

        # Execute the query
        groceries = groceries.all()

        return render_template(
            'assignment/pantrypage.html',
            groceries_entries=groceries,
            current_sort=sort_by,
            current_filter=price_filter
        )

@app.route('/assignment/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/assginment/')
    except:
        return 'There was a problem deleting that task'

@app.route('/assignment/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/assginment/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('assignment/update.html', task=task)


# Path where images will be saved (make sure this folder exists)
UPLOAD_FOLDER = 'static/uploads/bills'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/assignment/add_bill/', methods=['POST', 'GET'])
def add_bill():
    if request.method == 'POST':
        bill_name = request.form['bill_name']
        amount = request.form['amount']
        due_date = request.form['due_date']

        # Check if the file is present in the request
        bill_image = request.files['bill_image']
        if bill_image and allowed_file(bill_image.filename):
            filename = secure_filename(bill_image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            bill_image.save(file_path)
        else:
            file_path = 'static/default_image.jpg'  # Use a default image if none is uploaded

        # Convert the due date string to datetime
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return 'Invalid date format'

        # Create a new bill and store the image file path
        new_bill = Bills(
            bill_name=bill_name,
            amount=float(amount),
            due_date=due_date,
            image=file_path  # Save the file path of the uploaded image
        )

        try:
            db.session.add(new_bill)
            db.session.commit()
            return redirect('/assignment/bills/')
        except Exception as e:
            print(e)
            return 'There was an issue adding the bill'

    return render_template('assignment/add_bill.html')




@app.route('/assignment/visualize_data')
def visualize_data_api():
    # Query data from both tables
    groceries = Grocery.query.all()
    bills = Bills.query.all()

    # Prepare data for Grocery
    grocery_total = sum([item.price for item in groceries])

    dic_bills = {}
    for a in bills:
        bill_name = a.bill_name.lower()
        dic_bills[bill_name] = dic_bills.get(bill_name, 0) + a.amount

    # Prepare data for visualization
    data = {
        "labels": ["Grocery"] + list(dic_bills.keys()),
        "values": [grocery_total] + list(dic_bills.values())
    }

    return jsonify(data)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the table exists
        initialize_timetable()  # Populate default rows
    app.run(debug=True)
