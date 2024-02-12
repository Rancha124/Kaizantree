# Kaizntree Project

The Kaizntree project is a Django-based web application designed to streamline inventory management through a robust API. This application features a comprehensive Item Dashboard, which provides API endpoints for retrieving detailed listings of items. Each item entry includes essential information such as SKU, name, category, tags, stock status, and available stock, making it an invaluable tool for businesses looking to manage their inventory efficiently. This README outlines the steps needed to get this application up and running.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.8 or newer.

## Getting Started

Follow these steps to get your development environment set up:

### 1. Clone the repository

Clone this repository to your local machine using the following command:

```
git clone https://github.com/Rancha124/Kaizantree.git
cd kaizntree
```

### 2. Install the dependencies

```
pip install -r requirements.txt
```

### 3. Database setup

```
python manage.py migrate
```

### 4. Running the development server

```
python manage.py runserver
```