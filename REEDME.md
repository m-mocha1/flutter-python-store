# My Store Web App

## Overview

This is a modern e-commerce web application where users can sign up, log in, add products with images, manage their cart, and enjoy a dark mode interface.

## Features

- User authentication (sign up, login, logout)
- Secure password hashing
- Add, view, and remove products
- Product image uploads
- Shopping cart functionality
- Responsive design with dark mode

## Technologies Used

- **Flask** — Python web framework for backend and routing
- **SQLAlchemy** — ORM for database management
- **Bootstrap** — Responsive UI components
- **Custom CSS** — Dark mode and styling
- **Werkzeug** — Password hashing and file upload utilities

## How It Works

- Users register and log in securely
- Products are stored in a database with image paths
- Images can be uploaded and are saved to the server
- Only the user who added a product can remove it
- Cart and product pages are styled for a modern experience

## Getting Started

1. Clone the repository
2. Install dependencies:  
   `pip install flask flask_sqlalchemy werkzeug`
3. Run the app:  
   `python app.py`
4. Open your browser at `http://localhost:5000`

---

Enjoy shopping!