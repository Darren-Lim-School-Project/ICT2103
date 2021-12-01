import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
# Use a service account
cred = credentials.Certificate('./ict2103t32-e09d5-firebase-adminsdk-kl22x-4467b58195.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

print("Database initialized successfully")

def main():
    category = ["Mickey Mouse and Friends", "Disney and Pixar", "Marvel", "Frozen"]
    counter = 1

    docs = db.collection(u'Products').document(u'Category').collection("Mickey Mouse and Friends").stream()
    for i in category:
        docs = db.collection(u'Products').document(u'Category').collection(i).stream()
        for doc in docs:
            counter += 1

    mickey_mouse_and_friends = ["Disney Legato Large Mini Shoulder Bag", "Disney Anello Square Mini Shoulder Bag" , "Disney Mickey - Musical Notes (Adult)"]
    mickey_mouse_and_friends_price = [109.00 , 95.00, 19.00] 
    mickey_mouse_and_friends_promo = [5,5,0]
    mickey_mouse_and_friends_desc = ["Synthetic leather × Embossed design", "High density nylon fabric x screen print" ,"Disney Collection"]
    mickey_mouse_and_friends_stock = [10,10,10]

    for i in range (0, len(mickey_mouse_and_friends)):
        doc_ref = db.collection(u'Products').document(u'Category').collection(u'Mickey Mouse and Friends').document(f"{counter}")
        doc_ref.set({
            u'Productid' : counter,
            u'Name': mickey_mouse_and_friends[i],
            u'Price': mickey_mouse_and_friends_price[i],
            u'Category': "Mickey Mouse and Friends",
            u'Promo': mickey_mouse_and_friends_promo[i],
            u'Desc': mickey_mouse_and_friends_desc[i],
            u'Stock': mickey_mouse_and_friends_stock[i],
        })
        counter +=1 

    disney_and_pixar = ["Pixar Ball Silk Tie For Adutlts", "Jessie Action Figure", "Buzz Lightyear Action Figure"]
    disney_and_pixar_price = [44.99, 28.00, 12.95]
    disney_and_pixar_promo = [5,5,0]
    disney_and_pixar_desc = ["High quality silk that can be machine washed", "Batteries sold separately" ,"Batteries sold separately"]
    disney_and_pixar_stock = [10,10,10]
    for i in range (0, len(disney_and_pixar)):
        doc_ref = db.collection(u'Products').document(u'Category').collection(u'Disney and Pixar').document(f"{counter}")
        doc_ref.set({
            u'Productid' : counter,
            u'Name': disney_and_pixar[i],
            u'Price': disney_and_pixar_price[i],
            u'Category': "Disney and Pixar",
            u'Promo': disney_and_pixar_promo[i],
            u'Desc': disney_and_pixar_desc[i],
            u'Stock': disney_and_pixar_stock[i],
        })
        counter +=1 

    marvel = ["Infinity Gauntlet", "Heart of Iron Man" ,"Groot Plushie"]
    marvel_price = [109.00, 42.00, 35.99]
    marvel_promo = [5,5,0]
    marvel_desc = ["Glows in the dark", "Does not glow in the dark", "Are you groot"]
    marvel_stock = [10,10,10]

    for i in range (0, len(disney_and_pixar)):
        doc_ref = db.collection(u'Products').document(u'Category').collection(u'Marvel').document(f"{counter}")
        doc_ref.set({
            u'Productid' : counter,
            u'Name': marvel[i],
            u'Price': marvel_price[i],
            u'Category': "Marvel",
            u'Promo': marvel_promo[i],
            u'Desc': marvel_desc[i],
            u'Stock': marvel_stock[i],
        })
        counter +=1 
    frozen = ["Olaf 50cm Plushie", "Elsa tiara", "Sven Talking Action Figure"]
    frozen_price = [110.99, 25.00, 19.00]
    frozen_promo = [5,5,0]
    frozen_desc = ["Do you want to build a snowman", "Let it gooo", "Batteries sold separately"]
    frozen_stock = [10,10,10]

    for i in range (0, len(frozen)):
        doc_ref = db.collection(u'Products').document(u'Category').collection(u'Frozen').document(f"{counter}")
        doc_ref.set({
            u'Productid' : counter,
            u'Name': frozen[i],
            u'Price': frozen_price[i],
            u'Category': "Marvel",
            u'Promo': frozen_promo[i],
            u'Desc': frozen_desc[i],
            u'Stock': frozen_stock[i],
        })
        counter +=1 

if __name__ == "__main__":
    main()
    print("DZXD")