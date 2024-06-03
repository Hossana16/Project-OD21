![header-logo](https://github.com/Hossana16/Project-OD21/assets/80108666/52537967-4cda-48ad-ad6b-9fd283f9871d)


# Service Marketplace Platform

Welcome to the Service Marketplace Platform! This platform allows users to browse, review, and purchase services offered by various sellers. Sellers can manage their services and receive reviews from buyers.

## Features

- User authentication and profile management
- Service listing and categorization
- Service reviews and ratings
- Notification system for tracking activities
- Responsive and user-friendly design

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Os windows, mac/linux
- Python 3.11 or higher
- Git
- Mysql (Optional but recommended)

## Installation

Follow these steps to install and set up the project on your local machine.

### Step 1: Clone the Repository

Open your command prompt and run:

### For https

```sh
git clone https://github.com/Hossana16/Project-OD21.git
cd Project-OD21.git
```

### For ssh
```sh
git clone git@github.com:Hossana16/Project-OD21.git
cd Project-OD21.git
```

### Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

```sh
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
Install the required Python packages:

```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Go to lite_exchange/settings.py

edit mysql configuration set a custome password 

```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lite_exchange', # database name
        'USER': 'root', # database username
        'PASSWORD': '',#  database password 
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Apply Migrations
Run the following commands to apply database migrations:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser
Create a superuser account to access the admin panel:

```sh
python manage.py createsuperuser
```
Visit http://127.0.0.1:8000/ in your web browser to access the platform.

### Usage
## Admin Panel
![image](https://github.com/Hossana16/Project-OD21/assets/80108666/a375ccaa-6984-4985-b21f-41fe46ad9409)

Login & Access the admin panel to manage users, services, categories, and reviews:

![image](https://github.com/Hossana16/Project-OD21/assets/80108666/3c300205-b07e-461c-8f6c-17a063fb454f)

Log in using the superuser credentials you created earlier.

## Adding Services
Log in as a seller ( normal user).
Navigate to the dashboard and add new services under the appropriate categories.

Reviewing Services

Log in as a buyer.

Browse services and submit reviews for the services you have purchased.
Contributing

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
If you have any questions or need further assistance, feel free to contact us at:

Acknowledgements
Django
Bootstrap
FontAwesome

