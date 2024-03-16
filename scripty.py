import re
import urllib.parse
import datetime
import json
import requests
from Acredentials import credentials

def whole_function(Isbnumber,quantity):
    def calculate_earnings(arank_value, final_amount):
        if arank_value <= 250000 and final_amount >= 99.99:
            return 25.31
        elif arank_value <= 250000 and final_amount >= 49.99:
            return 13.69
        elif arank_value <= 500000 and final_amount >= 99.99:
            return 13.69
        elif arank_value <= 500000 and final_amount >= 49.99:
            return 9.31
        elif arank_value <= 1000000 and final_amount >= 99.99:
            return 9.31
        elif arank_value <= 1000000 and final_amount >= 49.99:
            return 6.96
        elif arank_value <= 1500000 and final_amount >= 99.99:
            return 6.69
        elif arank_value <= 1500000 and final_amount >= 49.99:
            return 3.76
        elif arank_value <= 2000000 and final_amount >= 99.99:
            return 3.76
        elif arank_value <= 2000000 and final_amount >= 49.99:
            return 1.49
        elif arank_value <= 150000 and final_amount >= 29.99:
            return 1.49
        elif arank_value <= 750000 and final_amount >= 29.99:
            return 0.89
        elif arank_value <= 500 and final_amount >= 21.99:
            return 0.89
        elif arank_value <= 1500 and final_amount >= 23.99:
            return 0.89
        else:
            return 0
    def add_to_shopping_cart(shopping_cart, item):
        shopping_cart.append((item))
        print("Item added to the shopping cart!")
    def calculate_total_earnings(shopping_cart):
        return sum(float(earnings) for _, earnings in shopping_cart)

    shopping_cart = []


        
    token_respons = requests.post(
        "https://api.amazon.com/auth/o2/token",
        data={
            "grant_type" : "refresh_token",
            "refresh_token" : credentials["refresh_token"],
            "client_id" : credentials["lwa_app_id"],
            "client_secret" : credentials["lwa_client_secret"]
        },
    )
    access_token = token_respons.json()["access_token"]
    endpoint = "https://sellingpartnerapi-na.amazon.com/"
    marketplace_id = "ATVPDKIKX0DER"
    Isbnval= "ISBN"
    #Isbnumber= input("Please enter the ISBN value here")
    def format_isbn(Isbnumber):
        return Isbnumber.replace("-", "")
    formatted_isbn = format_isbn(Isbnumber)
    print("Formatted ISBN:", formatted_isbn)
    Isbnumber = formatted_isbn
    request_params3 = {
        "marketplaceIds": marketplace_id,
        "identifiersType": Isbnval,
        "identifiers": Isbnumber    
    }
    fasdf = "/catalog/2022-04-01/items"
    forders = requests.get(
        endpoint
        + fasdf
        +"?"
        +urllib.parse.urlencode(request_params3),
        headers={
            "x-amz-access-token":access_token
        },
    )
    #, indent=2
    print(json.dumps(forders.json()))
    print("Status Code:", forders.status_code)
    print("Response:", forders.text)
    forder_json = forders.json()
    
    asin_result = forder_json["items"][0]["asin"]
    item_name = forder_json["items"][0]["summaries"][0]["itemName"]


    book_asin = asin_result
    included_data = "attributes,identifiers,images,productTypes,salesRanks,summaries,relationships"
    request_params = {
        "marketplaceIds": marketplace_id,
        "asin": book_asin,
        "includedData": included_data  
    }
    asdf = f"/catalog/2022-04-01/items/{book_asin}"
    orders = requests.get(
        endpoint
        + asdf
        +"?"
        +urllib.parse.urlencode(request_params),
        headers={
            "x-amz-access-token":access_token
        },
    )
    print(json.dumps(orders.json()))
    print("Status Code:", orders.status_code)
    print("Response:", orders.text)
    print("heeeeeeeeee")
    print(orders.json()["salesRanks"])
    # Assuming 'orders' contains the JSON payload
    images = orders.json().get("images", [])

    if images:
        # Extracting the first image link
        first_image_link = images[0].get("images", [])[0].get("link", "")

        # Printing the first image link
        print("First Image Link:", first_image_link)
    else:
        print("No images found in the payload.")

    sales_ranks = orders.json()["salesRanks"]
    for rank_info in sales_ranks:
        marketplace_id = rank_info["marketplaceId"]
        
        classification_ranks = rank_info.get("classificationRanks", [])
        for classification_rank in classification_ranks:
            title = classification_rank.get("title", "")
            rank_value = classification_rank.get("rank", "")
            link = classification_rank.get("link", "")
            
            print(f"Marketplace ID: {marketplace_id}, Title: {title}, Rank: {rank_value}, Link: {link}")

        display_group_ranks = rank_info.get("displayGroupRanks", [])
        for display_group_rank in display_group_ranks:
            website_display_group = display_group_rank.get("websiteDisplayGroup", "")
            title = display_group_rank.get("title", "")
            arank_value = display_group_rank.get("rank", "")
            link = display_group_rank.get("link", "")

            print(f"Website Display Group: {website_display_group}, Title: {title}, Rank: {arank_value}, Link: {link}")

    item_type = "Asin"
    item_condition = "Used"
    request_params2 ={
        "MarketplaceId": marketplace_id,
        "Asins": book_asin,
        "ItemType" : item_type,
        "ItemCondition": item_condition,    
    } 
    prices = requests.get(
        endpoint
        +"/products/pricing/v0/competitivePrice"
        +"?"
        +urllib.parse.urlencode(request_params2),
        headers={
            "x-amz-access-token":access_token
        },
    )
    print(json.dumps(prices.json()))
    print("Status Code:", prices.status_code)
    print("Response:", prices.text)
    print("END")
    def extract_used_condition_amount(response):
        competitive_prices = response["payload"][0]["Product"]["CompetitivePricing"]["CompetitivePrices"]
        for price in competitive_prices:
            if price["CompetitivePriceId"] == "2":
                return price["Price"]["LandedPrice"]["Amount"]
            elif price["CompetitivePriceId"] == "1":
                return price["Price"]["LandedPrice"]["Amount"]
    used_amount = extract_used_condition_amount(prices.json())
    print("Used Amount (CompetitivePriceId: 2):", used_amount)
    print(arank_value)

    if arank_value <= 1000000 and used_amount >= 49.99:
        print("We can buy this")
    print(book_asin)
    litem_condition = "New"
    request_params2 ={
        "MarketplaceId": marketplace_id,
        "ItemCondition": litem_condition,
        "Asin": book_asin
    } 
    lprices = requests.get(
        endpoint
        +f"/products/pricing/v0/items/{book_asin}/offers"
        +"?"
        +urllib.parse.urlencode(request_params2),
        headers={
            "x-amz-access-token":access_token
        },
    )
    print(json.dumps(lprices.json()))
    print("Status Code:", lprices.status_code)
    print("Response:", lprices.text)
    print("END")
    used_condition_amount = next(
        (price["LandedPrice"]["Amount"] for price in lprices.json()["payload"]["Summary"]["BuyBoxPrices"] if price["condition"] == "Used"),
        None
    )
    if used_condition_amount is not None:
        print("Used Condition Amount:", used_condition_amount)
    final_amount = None

    if used_condition_amount is not None:
        final_amount = used_condition_amount
    elif lprices.json()["payload"]["Summary"]["LowestPrices"][0]["condition"] == "used":
        final_amount = lprices.json()["payload"]["Summary"]["LowestPrices"][0]["LandedPrice"]["Amount"]
    elif "BuyBoxPrices" in lprices.json()["payload"]["Summary"]:
        new_condition_amount = next(
            (price["LandedPrice"]["Amount"] for price in lprices.json()["payload"]["Summary"]["BuyBoxPrices"] if price["condition"] == "New"),
            None
        )
        if new_condition_amount is not None:
            final_amount = new_condition_amount
        elif lprices.json()["payload"]["Summar0y"]["LowestPrices"][0]["condition"] == "new":
            final_amount = lprices.json()["payload"]["Summary"]["BuyBoxPrices"][0]["LandedPrice"]["Amount"] 
    #quantity = int(input("Enter the quantity of the item: "))
    if final_amount is not None:
        print("Final Amount:", final_amount)
        if arank_value <= 250000 and final_amount >= 99.99:
            print("You'll earn 25.31 dollars for this item")
        elif arank_value <= 250000 and final_amount >= 49.99:
            print("You'll earn 13.69 dollars for this item")
        elif arank_value <= 500000 and final_amount >= 99.99:
            print("You'll earn 13.69 dollars for this item")
        elif arank_value <= 500000 and final_amount >= 49.99:
            print("You'll earn 9.31 dollars for this item")
        elif arank_value <= 1000000 and final_amount >= 99.99:
            print("You'll earn 9.31 dollars for this item")
        elif arank_value <= 1000000 and final_amount >= 49.99:
            print("You'll earn 6.96 dollars for this item")
        elif arank_value <= 1500000 and final_amount >= 99.99:
            print("You'll earn 6.96 dollars for this item")
        elif arank_value <= 1500000 and final_amount >= 49.99:
            print("You'll earn 3.76 dollars for this item")
        elif arank_value <= 2000000 and final_amount >= 99.99:
            print("You'll earn 3.76 dollars for this item")
        elif arank_value <= 2000000 and final_amount >= 49.99:
            print("You'll earn 1.49 dollars for this item")
        elif arank_value <= 150000 and final_amount >= 29.99:
            print("You'll earn 1.49 dollars for this item")
        elif arank_value <= 750000 and final_amount >= 29.99:
            print("You'll earn 0.89 dollars for this item")
        elif arank_value <= 500 and final_amount >= 21.99:
            print("You'll earn 0.89 dollars for this item")
        elif arank_value <= 1500 and final_amount >= 23.99:
            print("You'll earn 0.89 dollars for this item")

    else:
        print("No valid BuyBoxPrices found in the payload.")
    

    earnings = calculate_earnings(arank_value, final_amount)*quantity
    item_description = f"ASIN: {book_asin}, Earnings: {earnings} dollars"

    add_to_shopping_cart(shopping_cart, ((book_asin, item_name), earnings))


    # Your existing code to get arank_value, final_amount, etc...

    # Calculate earnings for the specified quantity

        # Calculate total earnings in the shopping cart
    print("Contents of shopping cart:", shopping_cart)
    total_earnings = calculate_total_earnings(shopping_cart)
    print("Item added to the shopping cart!")
    print("Your current shopping cart:")




    for i, ((item, item_name), earnings) in enumerate(shopping_cart, start=1):
        print(f"{i}. {item},{item_name}, Earnings: {earnings} dollars")

        print(f"Total Earnings: {total_earnings} dollars")
    #user_input = input("Do you want to add more items? (yes/no): ")
    #if user_input.lower() != 'yes':
        #   break
    if total_earnings >= 6.96:
            print("You can proceed to checkout with the following items:")
            for i, (item, earnings) in enumerate(shopping_cart, start=1):
                print(f"{i}. {item},{item_name}, Earnings: {earnings} dollars")
            print(f"Total Earnings: {total_earnings} dollars")
                
    else:
        remaining_earnings = 6.96 - total_earnings
        print(f"Total earnings: {total_earnings} dollars. You need {remaining_earnings} more dollars to proceed to checkout.")

        # Optionally, ask the user if they want to add more items
    item_display = total_earnings,item_name,Isbnumber,quantity,first_image_link
    print(first_image_link)
    return (item_display)      
