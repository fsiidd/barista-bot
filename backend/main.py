from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import db_helper
import generic_helper

app = FastAPI()

inprogress_orders = {}


def track_order(parameters: dict, session_id: str):
        order_id = int(parameters['order_id'])
        order_status = db_helper.get_order_status(order_id)

        if order_status:
             fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
        else:
            fulfillment_text = f"No order found with order id: {order_id}"


        return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })

def add_to_order(parameters: dict, session_id: str):
     
     cafe_items = parameters['cafe-item']
     quantities = [int(x) for x in parameters['number']]

     if len(cafe_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify menu items and quantities clearly?"
     else:
        new_cafe_dict = dict(zip(cafe_items, quantities))
        
        if session_id in inprogress_orders:
             current_cafe_dict = inprogress_orders[session_id]
             current_cafe_dict.update(new_cafe_dict)
             inprogress_orders[session_id] = current_cafe_dict
        else:
            inprogress_orders[session_id] = new_cafe_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
             
             
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"
     
     return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })

def remove_from_order(parameters: dict):
     pass

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    # Insert individual items along with quantity in orders table
    for cafe_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            cafe_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1

    # Now insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def complete_order(parameters: dict, session_id: str):
    print(f"Session ID: {session_id}") 
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        print(f"Order not found for session: {session_id}")  # Debugging line
    else:
        order = inprogress_orders[session_id]
        print(f"Order found for session {session_id}: {order}")  # Debugging line
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
            print("Error saving order to database.")  # Debugging line
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                           f"Your order id is #{order_id}. " \
                           f"Your order total is ${order_total} which you can pay at the time of delivery!"
            print(f"Order ID: {order_id}, Total Price: {order_total}")  # Debugging line

        del inprogress_orders[session_id]
        print(f"Order completed and removed from in-progress: {session_id}")  # Debugging line

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def remove_from_order(parameters: dict, session_id: str):
    print("triggered")
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })
    
    cafe_items = parameters["cafe-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in cafe_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
    'order.add - context: ongoing order': add_to_order,
    'order.remove - context: ongoing order': remove_from_order,
    'order.complete - context: ongoing-order': complete_order,  # Update here
    'track.order - context: ongoing-tracking': track_order
}

    print(intent_handler_dict[intent])

    return intent_handler_dict[intent](parameters, session_id)


