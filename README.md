
# Household Management Hub and ToDo List Projects

This repository contains a **Landing Page** that links to two separate projects:  
1. **ToDo List** – A simple and functional task management application with modified routes for learning purposes.  
2. **Household Management Hub** – An all-in-one dashboard for managing household tasks, schedules, pantry inventory, and bills.  

## Landing Page
The **Landing Page** serves as the entry point for this repository. It links to both the ToDo List and Household Management Hub projects for easy navigation.  

### Features
- Links to both projects using Flask's `url_for()` for dynamic routing.  
- Provides a user-friendly interface for accessing each project.  

## ToDo List Project
The **ToDo List** application is a simple tool to help users organize their tasks efficiently. It includes the following features and modifications:  

### Features
- Add, edit, and delete tasks effortlessly.  
- Mark tasks as complete for better tracking.  

### Modifications
- **Route Changes:**  
  The routes have been modified for learning purposes to explore Flask's routing capabilities.  
- Added comments in the code to explain routing logic and demonstrate URL structuring.  

## Household Management Hub
The **Household Management Hub** is designed to simplify household management with an intuitive dashboard.  

### Features

#### 1. Weekly Task Schedule
Efficiently organize and oversee your weekly timetable:  
- **Plan and Manage Tasks:** Stay on top of daily responsibilities with an intuitive weekly schedule.  
- **Reset Options:** Start afresh whenever needed by resetting the schedule with a single click.  
- **Downloadable CSV File:** Export your task schedule as a CSV file for easy sharing or offline reference.  

#### 2. Pantry Stock Manager
Stay informed about your pantry's stock levels and expiration dates:  
- **Track Inventory:** Manage pantry items to avoid overstocking or running out.  
- **Update Items:** Quickly update item quantities, names, or other details.  
- **Sort by Date:** Organize items by purchase or expiry date to prioritize consumption.  
- **Filter by Price:** View items within specific price ranges to plan budget-friendly shopping.  

#### 3. Financial Oversight
Monitor and optimize your household spending with comprehensive bill tracking:  
- **View and Manage Bills:** Keep an updated record of all monthly bills.  
- **Delete Unnecessary Entries:** Easily remove outdated or irrelevant bills.  
- **Update Details:** Make changes to bill information as needed.  
- **Spending Visualizations:** Gain insights into your spending patterns with the **Visualize Spending** feature, accessible directly from the homepage.  

## Contributing
This repository is intended for demonstration purposes. Contributions are limited to:  
- Fixes for critical security flaws or language updates.  

Pull requests for style changes, adding libraries, or new features outside the scope of the projects will not be accepted.  

# FlaskIntroduction

This repo has been updated to work with `Python v3.8` and up.

## How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```
