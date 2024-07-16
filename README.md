# StockFlow-Inventory and Supplier Management API

This project provides a REST API for managing an online store's inventory and suppliers. The system is built using Django and Django REST framework and consists of two main apps: `inventory` and `supplier`.

After spinning up this projrct on your server, you will be able to find the documentation page at 
`doc/`

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Inventory Endpoints](#inventory-endpoints)
  - [Supplier Endpoints](#supplier-endpoints)
- [Testing](#testing)
- [License](#license)

## Features

- **Inventory Management**: Add, view, update, and delete items from the inventory.
- **Supplier Management**: Add, view, update, and delete suppliers.
- **Inventory-Supplier Relationship**: Link items to one or more suppliers with quantity supplied.
- **Consistent Data Management**: Provides consistent and reliable data access and management through a REST API.

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 4.x or higher
- Django REST framework

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Chiefkufre/stockFlow-API.git
   cd stockflow
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**

   Create a `.env` file in the project root with the following content:

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

5. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

## Configuration

Ensure the `.env` file is set up correctly with the database URL and other necessary configurations.

## Running the Application

To start the application, simply run:

```bash
python manage.py runserver
```

## API Endpoints

### Inventory Endpoints

- **List All Items**
  - **URL**: `/api/inventory/items/`
  - **Method**: `GET`
  - **Response Example**:
    ```json
    [
      {
        "id": 1,
        "name": "Item 1",
        "description": "Description for item 1",
        "price": 12.99,
        "quantity": 100,
        "date_added": "2023-01-01T00:00:00Z",
        "suppliers": [
          {
            "id": 1,
            "name": "Supplier 1",
            "quantity": 50,
            "supply_date": "2023-01-01T00:00:00Z"
          }
        ]
      }
    ]
    ```

- **Create New Item**
  - **URL**: `/api/inventory/items/`
  - **Method**: `POST`
  - **Request Example**:
    ```json
    {
      "name": "New Item",
      "description": "Description for new item",
      "price": 15.00,
      "supplier_data": [
        {"supplier_id": 1, "quantity": 10},
        {"supplier_id": 2, "quantity": 20}
      ]
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": 3,
      "name": "New Item",
      "description": "Description for new item",
      "price": 15.00,
      "quantity": 30,
      "date_added": "2024-01-01T00:00:00Z",
      "suppliers": [
        {"id": 1, "name": "Supplier 1", "quantity": 10, "supply_date": "2024-01-01T00:00:00Z"},
        {"id": 2, "name": "Supplier 2", "quantity": 20, "supply_date": "2024-01-01T00:00:00Z"}
      ]
    }
    ```

- **Retrieve Single Item**
  - **URL**: `/api/inventory/items/{id}/`
  - **Method**: `GET`
  - **Response Example**:
    ```json
    {
      "id": 1,
      "name": "Item 1",
      "description": "Description for item 1",
      "price": 12.99,
      "quantity": 100,
      "date_added": "2023-01-01T00:00:00Z",
      "suppliers": [
        {"id": 1, "name": "Supplier 1", "quantity": 50, "supply_date": "2023-01-01T00:00:00Z"}
      ]
    }
    ```

- **Update Item**
  - **URL**: `/api/inventory/items/{id}/`
  - **Method**: `PUT`
  - **Request Example**:
    ```json
    {
      "name": "Updated Item",
      "description": "Updated description",
      "price": 20.00,
      "supplier_data": [
        {"supplier_id": 1, "quantity": 30},
        {"supplier_id": 2, "quantity": 40}
      ]
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": 1,
      "name": "Updated Item",
      "description": "Updated description",
      "price": 20.00,
      "quantity": 70,
      "date_added": "2023-01-01T00:00:00Z",
      "suppliers": [
        {"id": 1, "name": "Supplier 1", "quantity": 30, "supply_date": "2023-01-01T00:00:00Z"},
        {"id": 2, "name": "Supplier 2", "quantity": 40, "supply_date": "2023-01-01T00:00:00Z"}
      ]
    }
    ```

- **Partial Update Item**
  - **URL**: `/api/inventory/items/{id}/`
  - **Method**: `PATCH`
  - **Request Example**:
    ```json
    {
      "price": 25.00
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": 1,
      "name": "Updated Item",
      "description": "Updated description",
      "price": 25.00,
      "quantity": 70,
      "date_added": "2023-01-01T00:00:00Z",
      "suppliers": [
        {"id": 1, "name": "Supplier 1", "quantity": 30, "supply_date": "2023-01-01T00:00:00Z"},
        {"id": 2, "name": "Supplier 2", "quantity": 40, "supply_date": "2023-01-01T00:00:00Z"}
      ]
    }
    ```

- **Delete Item**
  - **URL**: `/api/inventory/items/{id}/`
  - **Method**: `DELETE`
  - **Response**: `204 No Content`

### Supplier Endpoints

- **List All Suppliers**
  - **URL**: `/api/supplier/suppliers/`
  - **Method**: `GET`
  - **Response Example**:
    ```json
    [
      {
        "id": 1,
        "name": "Supplier 1",
        "email": "samuel@example.com",
        "address": "Kano, Nigeria",
        "items": [
          {
            "id": 1,
            "name": "Item 1",
            "quantity": 50,
            "supply_date": "2023-01-01T00:00:00Z"
          }
        ]
      }
    ]
    ```

- **Create New Supplier**
  - **URL**: `/api/supplier/suppliers/`
  - **Method**: `POST`
  - **Request Example**:
    ```json
    {
      "name": "New Supplier",
      "email": "new_supplier@example.com",
      "address": "Kano, Nigeria",
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": 3,
      "name": "New Supplier",
      "email": "new_supplier@example.com",
      "address": "Kano, Nigeria",,
      "items": []
    }
    ```

- **Retrieve Single Supplier**
  - **URL**: `/api/supplier/suppliers/{id}/`
  - **Method**: `GET`
  - **Response Example**:
    ```json
    {
      "id": 1,
      "name": "Supplier 1",
      "email": "supplier1@example.com",
      "address": "Kano, Nigeria",,
      "items": [
        {"id": 1, "name": "Item 1", "quantity": 50, "supply_date": "2023-01-01T00:00:00Z"}
      ]
    }
    ```

- **Update Supplier**
  - **URL**: `/api/supplier/suppliers/{id}/`
  - **Method**: `PUT`
  - **Request Example**:
    ```json
    {
      "name": "Updated Supplier",
      "email": "updated_supplier@example.com",
      "address": "Kano, Nigeria",
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": 1,
      "name": "Updated Supplier",
      "email": "updated_supplier@example.com",
      "phone": "0987654321",
      "items": [
        {"id": 1, "name": "Item 1", "quantity": 50, "supply_date": "2023-01-01T00:00:00Z"}
      ]
    }
    ```

- **Partial Update Supplier**
  - **URL**: `/api/supplier/suppliers/{id}/`
  - **Method**: `PATCH`
  - **Request Example**:
    ```json
    {
      "email": "updated_supplier@example.com"
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": 1,
      "name": "Supplier 1",
      "email": "updated_supplier@example.com",
      "address": "Kano, Nigeria",,
      "items": [
        {"id": 1, "name": "Item 1", "quantity": 50, "supply_date": "2023-01-01T00:00:00Z"}
      ]
    }
    ```

- **Delete Supplier**
  - **URL**: `/api/supplier/suppliers/{id}/`
  - **Method**: `DELETE`
  - **Response**: `204 No Content`

## Testing

To run the tests, use the following command:

```bash
python manage.py test
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: For more information or correct please contact me `samuelkufrewillie@gmail.com`
```
