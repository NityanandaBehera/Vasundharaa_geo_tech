# Multi-Organization System

This is a Django-based application for managing multiple organizations and users within those organizations. It supports user authentication, organization management, and role-based user assignments.

## Setup Instructions

Follow these steps to set up the project:

### 1. Create a Virtual Environment

Navigate to the directory where you want to store the project, then run the following command to create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```
### Now, install the required dependencies for the project. Run the following command to install all the packages listed in the requirements.txt file:
```
pip install -r requirements.txt
```
##After installing the dependencies, set up the database and apply migrations with the following command:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```
