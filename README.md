# BaristaBot ☕️
## an NLP Chatbot for a Cafe order + delivery system

This project is a complete end-to-end NLP-based chatbot application for a local cafe I grew up visiting, designed to handle customer interactions such as order placements, order tracking, and more. The chatbot is powered by Dialogflow for natural language processing and utilizes FastAPI to handle backend API interactions. The system also integrates a MySQL database to manage orders and order tracking efficiently.

## Project Structure

The project is divided into three main directories:

### 1. Frontend

This folder contains the HTML and CSS files responsible for the user interface of the café website. It provides a simple and clean layout where users can interact with the chatbot.

### 2. Backend

The backend is built with FastAPI, a modern web framework for building APIs with Python. The backend handles requests from the Dialogflow webhook and interacts with the MySQL database to perform various operations like inserting orders, tracking order statuses, and more.

- **API Endpoints**:
  - **`/`**: Handles requests from Dialogflow and routes them to appropriate functions like adding items to the order, removing items, completing the order, and tracking order status.

### 3. Database

The db folder contains MySQL queries and procedures necessary for handling data. This includes inserting order items, tracking order status, calculating total order prices, etc.

## Features

- **Order Management**: Users can add, remove, and complete orders via the chatbot.
- **Order Tracking**: Users can track the status of their orders.
- **Database Integration**: MySQL is used to manage and store orders and related data.
- **Dialogflow Integration**: The chatbot leverages Dialogflow to understand and process user inputs.

## How It Works

1. **Add to Order**: The chatbot processes user inputs related to adding café items to their order. The backend API updates the in-progress orders dictionary and returns a summary of the current order.
2. **Remove from Order**: The chatbot allows users to remove items from their order. The backend updates the order and informs the user of the updated order status.
3. **Complete Order**: When an order is completed, the backend saves the order to the database, calculates the total price, and generates an order ID.
4. **Track Order**: Users can inquire about the status of their order by providing their order ID. The chatbot fetches the order status from the database and returns it to the user.

## Setup Instructions

1. **Install Dependencies**:

   - Python 3.x
   - FastAPI
   - MySQL Connector for Python
   - Dialogflow (set up your project on Dialogflow and configure the webhook)

2. **Database Setup**:

   - Create a MySQL database and replace the database currently in use.
   - Run the SQL scripts in the `db` folder to create necessary tables and procedures.

3. **Run the Backend**:
   ```bash
   uvicorn main:app --reload
   ```
