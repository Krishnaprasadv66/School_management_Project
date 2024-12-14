# School Management System

## Overview

The **School Management System** is a web application built with **Django** and **Django Rest Framework (DRF)** that implements **Role-Based Access Control (RBAC)**. The system allows users to perform **CRUD** operations to manage student details across various classes, handle library history, and manage fees history. 

The system supports three user roles:
- **School Admin**: Full control over the system, including the ability to create, update, and delete accounts for staff and librarians.
- **Office Staff**: Can view all student details, library reviews, and manage fees history.
- **Librarian**: Has access to view library history and student details but cannot modify or delete them.

## Features

- **Role-Based Access Control (RBAC)**: Admin, Office Staff, and Librarian roles with defined permissions.
- **CRUD Operations**: Ability for Admin to manage staff, librarians, and students.
- **Library and Fees History**: Manage and view the student's library history and fees.
- **Separate Logins for Roles**: Different login mechanisms for Admin, Office Staff, and Librarian.
- **API Endpoints**: Expose RESTful API endpoints for CRUD operations.

## Technologies Used

- **Django**: Web framework for building the application.
- **Django Rest Framework (DRF)**: For creating the RESTful API.
- **JWT Authentication**: For secure authentication via tokens.
- **Session Authentication**: For managing user login state and roles.
- **Phonenumbers**: For validating phone numbers.
- **PyJWT**: For generating JWT tokens.
- **SQLParse**: For parsing SQL queries.
- **tzdata**: For timezone support in the application.

## Installation

### Prerequisites

Make sure you have Python and pip installed on your system.

- Python >= 3.8
- pip (Python package installer)

### Steps to Set Up the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Krishnaprasadv66/School_management_Project.git
   cd Schoolmanagement_Project