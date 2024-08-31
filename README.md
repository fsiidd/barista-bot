# ☕️ BaristaBot - an NLP powered Chatbot

BaristaBot is a Python-based NLP Chatbot designed to handle customer interactions such as order placements, order tracking, and more. The chatbot is powered by Dialogflow for natural language processing and utilizes FastAPI to handle backend API interactions. The system also integrates a MySQL database to manage orders and order tracking efficiently.

This project is inspired by a local cafe that I grew up visiting. The chatbot aims to recreate that warm, welcoming experience by streamlining the order process through natural language interactions, making it easier for customers to enjoy their favorite café items."

<img width="1464" alt="Joud Coffee Landing Page" src="https://github.com/user-attachments/assets/c04fbb00-4f16-48cd-a9b1-bfbd6cb19a01">

## Project Structure

The project is built with FastAPI, a modern web framework for building APIs with Python. The backend handles requests from the Dialogflow webhook and interacts with the MySQL database to perform various operations like inserting orders, tracking order statuses, and more.

- **API Endpoints**:
  - **`/`**: Handles requests from Dialogflow and routes them to appropriate functions like adding items to the order, removing items, completing the order, and tracking order status.

### Database

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

### Scenario 1: Placing an Order (Adding/Removing functionality)
![2024-08-31_15-54-46 (1)](https://github.com/user-attachments/assets/8834f1f6-5431-4780-9e59-edb79a0c3646)

### Scenario 2: Tracking an Order
![2024-08-31_16-04-07 (1)](https://github.com/user-attachments/assets/43d518b2-4d68-492c-9a9c-7c58bc712f37)

### Scenario 3: Handling Ambiguous Requests (incorrect input for cafe items + order tracking)
![2024-08-31_16-08-05 (1)](https://github.com/user-attachments/assets/6c47273b-9551-456b-9e4b-d1a4ad4bce5e)



## Setup Instructions

- Python 3.8+
- MySQL
- FastAPI
- Dialogflow account
- ngrok (for secure connections)

### Step 1: Set Up the Database

1. Create a MySQL database and replace the current db in use.
2. Run the provided SQL scripts in the `db` folder to set up the necessary tables and stored procedures.

### Step 2: Set Up the Backend

1. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn mysql-connector-python
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Step 3: Set Up ngrok for Secure Connection

1. Download and install ngrok from [ngrok.com](https://ngrok.com/).
2. Run the following command to start ngrok on the port where your FastAPI server is running (default is 8000):
   ```bash
   ngrok http 8000
   ```
3. Copy the HTTPS URL provided by ngrok. This URL will be used in Dialogflow as the Webhook URL.

### Step 4: Configure Dialogflow

1. Create a new agent in Dialogflow.
2. Set up intents that match the functionalities of your chatbot (e.g., `order.add`, `order.remove`, `order.complete`, `track.order`).
3. In the Fulfillment section, enable the webhook and paste the ngrok URL you obtained earlier.
4. Deploy your agent and start interacting with your chatbot.
