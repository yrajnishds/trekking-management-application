# Trekking Management Application

## Description
This is a Trek Management Application built using Python and the Flask framework. The application enables administrators, trek staff, and trekkers to manage trekking activities, including treks, users, and bookings, through a role-based management system.

## Features

- User (Trekker/Staff) registration and login
- Role-based access control (Admin, Staff, Trekker)
- Admin can manage treks, users, approve new staff, deactivate or block users, and perform other administrative actions
- Trekker can manage their own bookings
- Staff can manage trek status and bookings for their assigned treks
- Search, filter, and sorting functionality
- Dashboard for different user roles
- Dedicated pages for managing treks, bookings, users, and viewing booking history

## Tech Stack
| Technology | Purpose |
| :--- | :--- |
| Python | Backend programming language used to develop the logic. |
| Flask | Web framework used to build the application. |
| Flask-SQLAlchemy | ORM used to interact with the SQLite database. |
| Flask-Login | Handles user authentication and session management. |
| Flask-WTF | Form creation and validation. |
| WTForms | Creates and validates HTML forms. |
| SQLite | Stores application data such as users, treks, and bookings. |
| Jinja2 | Template engine used to render dynamic HTML pages. |
| HTML5 | Defines the structure of web pages. |
| CSS3 | Styles and improves the appearance of the application. |
| Bootstrap 5 | Provides a responsive and modern user interface. |
| Git & Github | Version control and source code management. |

## Project Structure
| File/Folder | Purpose |
|-------------|---------|
| `app.py` | Entry point of the application. It creates the Flask app, initializes extensions, and registers blueprints. |
| `seed.py` | Creates the database tables and inserts initial data, such as the default administrator account. |
| `filter.py` | Contains functions used to filter and sort application data. |
| `forms/` | Stores all WTForms classes used for user input and validation. |
| `models/` | Contains SQLAlchemy database models representing application tables. |
| `routes/` | Defines application routes and handles user requests using Flask blueprints. |
| `search.py` | Implements search functionality for different modules of the application. |
| `templates/` | Stores Jinja2 HTML templates used to render dynamic web pages. |
| `requirements.txt` | Lists all Python packages required to run the project. |
| `README.md` | Provides project information, installation steps, and usage instructions. |


## Installation and Running the Application

1. Clone the repository.
```bash
git clone git@github.com:yrajnishds/trekking-management-application.git
```
2. Navigate to the project directory.
```bash
cd trekking-management-application
```
3. Create a virtual environment.
**Windows**
```bash
python -m venv .venv
```
**Linux/macOS**
```bash
python3 -m venv .venv
```
4. Activate the virtual environment.
**Windows**
```bash
.venv\Scripts\activate
```
**Linux/macOS**
```bash
source .venv/bin/activate
```
5. Install dependencies.
```bash
pip install -r requirements.txt
```
6. Create the database and default administrator account.
```bash
python seed.py
```
7. Run the application.
```bash
python app.py
```

## Database
* Database: `SQLite3`
* The SQLite database stores information related to users, treks, bookings, and other application data.
  
## Author
* Name: *Rajnish Yadav*
* Roll no.: *25F2004238*
* Email: *25f2004238@ds.study.iitm.ac.in*