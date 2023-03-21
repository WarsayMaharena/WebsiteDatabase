import mysql.connector
import os

class User:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="utbweb.its.ltu.se", user="19990730", passwd="19990730", database="db19990730")
        self.mycursor = self.mydb.cursor()
        

    def add_item_shoppingbasket(self, furniture, price, furnitureid:int, customerid:int, wantedquantity:int):
        sql = "INSERT INTO ShoppingBasket (Furniture, Price, CustomerID, FurnitureID, quantity) VALUES (%s, %s, %s, %s, %s)"
        val = (furniture, price, customerid, furnitureid, wantedquantity)
        self.mycursor.execute(sql, val)
        self.mydb.commit()


    def remove_item_shoppingbasket(self, furnitureid:int, customerid:int):
        sql_delete_query = """DELETE FROM ShoppingBasket WHERE CustomerID={} AND FurnitureID={}""".format(customerid, furnitureid)
        self.mycursor.execute(sql_delete_query)
        self.mydb.commit()

    def fetch_items_shoppingbasket(self, customerid):
        sql_select_query = "SELECT * FROM ShoppingBasket WHERE CustomerID={}".format(customerid)
        self.mycursor.execute(sql_select_query)
        myresult = self.mycursor.fetchall()
        return myresult
    
    def remove_all_shoppingbasket(self, customerid):
        sql_delete_query = "DELETE FROM ShoppingBasket WHERE CustomerID={}".format(customerid)
        self.mycursor.execute(sql_delete_query)
        self.mydb.commit()


    def place_order(self, customerid, lastname, firstname, city):
        sql = "INSERT INTO Orders (OrderID, CustomerID, LastName, FirstName, City) VALUES (%s, %s, %s, %s, %s)"
        orderid = self.calc_new_orderid()
        self.place_order_help(customerid, orderid)
        val = (orderid, customerid, lastname, firstname, city)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.remove_all_shoppingbasket(customerid)

        #To change the status to shipped
        sql = "UPDATE Orders SET status ='shipped' WHERE OrderID = {}".format(orderid)
        user.mycursor.execute(sql)
        user.mydb.commit()

        
    

    def calc_new_orderid(self):
        sql3 = "SELECT MAX(OrderID) FROM Orders"
        self.mycursor.execute(sql3)
        myresult = self.mycursor.fetchall()[0][0]
        print("MAX: ",myresult)
        if myresult == None:
            return 1
        else:
            orderid = myresult + 1
            return orderid
        
    def fetch_orders(self):
        sql = "SELECT * FROM Orders"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult


    def comment_post(self, furnitureid, customerid, comment:str, grading):
        sql2 = "SELECT FirstName FROM Customer WHERE CustomerID={}".format(self.get_customerid())
        self.mycursor.execute(sql2)
        myresult = self.mycursor.fetchall()
        name = myresult[0][0]
        commentid = self.calc_new_commentid()
        
        sql = "INSERT INTO Comments (CommentID, FurnitureID, CustomerID, Comments, Grading, name) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (commentid, furnitureid, customerid, comment, grading, name)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def remove_comment(self, commentid:int):
        pass

    def calc_average_grading(self, furnitureid):
        sql = "SELECT Grading FROM Comments WHERE FurnitureID={}".format(furnitureid)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        avg = 0
        i = 0
        for grading in myresult:
            avg = avg + grading[0]
            i = i + 1
        avg = avg/i

        sql2 = "UPDATE Assets SET avg_grading={} WHERE FurnitureID={}".format(avg, furnitureid)
        self.mycursor.execute(sql2)
        self.mydb.commit()


    def calc_new_commentid(self):
        sql3 = "SELECT MAX(CommentID) FROM Comments"
        self.mycursor.execute(sql3)
        myresult = self.mycursor.fetchall()[0][0]
        print("MAX: ",myresult)
        if myresult == None:
            return 1
        else:
            commentid = myresult + 1
            return commentid

    def post_item(self, price, furniture, quantity):
        #sellerid = self.calc_new_sellerid()
        furnitureid = self.calc_new_furnitureid()
        sql = "INSERT INTO Assets (SellerID, Price, FurnitureID, furniture, quantity) VALUES (%s, %s, %s, %s, %s)"
        val = (1, price, furnitureid, furniture, quantity)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def calc_new_furnitureid(self):
        sql3 = "SELECT MAX(FurnitureID) FROM Assets"
        self.mycursor.execute(sql3)
        myresult = self.mycursor.fetchall()[0][0]
        print("MAX: ",myresult)
        if myresult == None:
            return 1
        else:
            furnitureid = myresult + 1
            return furnitureid
    
    def calc_new_sellerid(self):
        sql = "SELECT SellerID FROM Seller"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        index = len(myresult) - 1
        sellerid = myresult[index][0] + 1
        return sellerid

    def remove_asset(self, furnitureid:int):
        sql = "DELETE FROM Assets WHERE FurnitureID={}".format(furnitureid)
        self.mycursor.execute(sql)
        self.mydb.commit()

    def fetch_assets(self):
        sql = "SELECT Price, furniture, FurnitureID, quantity FROM Assets"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult
    
    def fetch_asset(self, furnitureid):
        sql = "SELECT * FROM Assets WHERE FurnitureID={}".format(furnitureid)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult


    def calc_new_customerid(self):
        sql3 = "SELECT MAX(CustomerID) FROM Customer"
        self.mycursor.execute(sql3)
        myresult = self.mycursor.fetchall()[0][0]
        print("MAX: ",myresult)
        if myresult == None:
            return 1
        else:
            customerid = myresult + 1
            return customerid

    def delete_user(self, customerid):
        if(customerid=='1'):
            return False
        sql = "DELETE FROM Comments WHERE CustomerID={}".format(customerid)
        sql2 = "DELETE FROM ShoppingBasket WHERE CustomerID={}".format(customerid)
        sql3 = "DELETE FROM Orders WHERE CustomerID={}".format(customerid)
        sql4 = "DELETE FROM Card_credentials WHERE CustomerID={}".format(customerid)
        sql5 = "DELETE FROM Customer WHERE CustomerID={}".format(customerid)
        self.mycursor.execute(sql)
        self.mycursor.execute(sql2)
        self.mycursor.execute(sql3)
        self.mycursor.execute(sql4)
        self.mycursor.execute(sql5)
        self.mydb.commit()
        return True

    def create_user(self, last_name:str, first_name:str, city:str, address:str, email, password):
        sql = "INSERT INTO Customer (CustomerID, LastName, FirstName, City, Address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        customerid = self.calc_new_customerid()
        val = (customerid, last_name, first_name, city, address, email, password)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
    
    def fetch_usercustomer(self):
        sql = "SELECT * FROM Customer"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result


    def authentication(self, email, password):
        sql = "SELECT email, password, CustomerID FROM Customer"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        for i in range(0, len(myresult)):
            if (email == myresult[i][0] and password == myresult[i][1]):
                isExist = os.path.exists('customerid_file.txt')
                if isExist == True:
                    os.remove('customerid_file.txt')
                    self.create_customerid_file(str(myresult[i][2]))
                    return True
                else:
                    self.create_customerid_file(str(myresult[i][2]))
                    return True   
        return False
    
    def create_customerid_file(self, customerid):
        f = open("customerid_file.txt", "a")
        f.write(customerid)
        f.close()

    def get_customerid(self):
        f = open("customerid_file.txt", "r")
        id = f.read()
        f.close()
        return id
        

    def calc_price(self, customerid):
        sql = "SELECT Price, quantity FROM ShoppingBasket WHERE CustomerID={}".format(customerid)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        print(myresult)
        sum = 0
        i = 0
        while i <= len(myresult)-1:
            sum = sum + (myresult[i][0]*myresult[i][1])
            i = i + 1
        return sum
    
    def add_card_credentials(self, card_number, customerid, card_holder, cvc, card_month, card_year):
        sql = "INSERT INTO Card_credentials (card_number, CustomerID, card_holder, cvc, card_month, card_year) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (card_number, customerid, card_holder, cvc,  card_month, card_year)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def check_email(self, email):
        sql = "SELECT email FROM Customer"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        for i in range(0, len(myresult)):
            if email == myresult[i][0]:
                return False
        
        return True
    
    def fetch_comments(self, furnitureid):
        sql = "SELECT * FROM Comments WHERE FurnitureID={}".format(furnitureid)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result
    
    def fetch_orders(self):
        sql = "SELECT * FROM Orders"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult
    
    def place_order_help(self, customerid:int, orderid):
        sql = "SELECT Price, furniture, quantity, FurnitureID FROM ShoppingBasket WHERE CustomerID={}".format(customerid)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        print(myresult)
        print(len(myresult)-1)
        
     
        for i in range(0, len(myresult)):

            CurrPrice = myresult[i][0]
            CurrFurniture= myresult[i][1]
            CurrQuantity = myresult[i][2]
            CurrFurnitureID = myresult[i][3]

            


            print("Price: ",CurrPrice)
            print("furniture: ",CurrFurniture)
            print("quantity: ",CurrQuantity)
            print("FurnitureID: ",CurrFurnitureID)

            sql2 = "INSERT INTO Orders_help (CustomerID, FurnitureID, OrderID, Price, furniture, quantity) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (customerid, CurrFurnitureID, orderid,CurrPrice,CurrFurniture, CurrQuantity)
            self.mycursor.execute(sql2, val)
            self.mydb.commit()


    def fetch_place_order_help(self):
        sql = "SELECT OrderID, Price, furniture, FurnitureID FROM Orders_help"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

    def customerid_from_furnitureid(self, customerid):
        sql = "SELECT FurnitureID FROM Orders_help WHERE CustomerID={}".format(customerid)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult
    
    def quantity_vs_wantedquantity(self, quantity, wantedquantity, furnitureid):
        res=str(quantity-wantedquantity)
        sql = "UPDATE Assets SET quantity = %s WHERE FurnitureID = %s"
        val = (res, furnitureid)
        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def alreadyAddedInCart(self, CustomerID, furnitureid):
        sql1 = "select FurnitureID from ShoppingBasket where CustomerID = {}".format(CustomerID)
        self.mycursor.execute(sql1)
        result = self.mycursor.fetchall()
        i = 0
        print(len(result))
        print(result)
        while(len(result)>i):
            print("Current res: ",result[i][0])
            if((furnitureid==result[i][0])):
                print("in if")
                print(furnitureid)
                print("already exists")
                return True
            i=i+1
            
        else:
            print("doesnt exist")
            return False

    def EditAsset(self, furnitureid, quantity, Price, furniture):
        sql = "UPDATE Assets SET quantity = %s, Price = %s, furniture = %s WHERE FurnitureID = %s"
        val = (quantity, Price, furniture, furnitureid)
        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def EditOrdersStatus(self, OrderID):
        sql = "UPDATE Orders SET status ='Cancelled' WHERE OrderID = {}".format(OrderID)
        self.mycursor.execute(sql)
        self.mydb.commit()

    def QuantityReturned(self, OrderID):
        sql1 = "select FurnitureID, quantity from Orders_help where OrderID ={}".format(OrderID)
        self.mycursor.execute(sql1)
        myresult = self.mycursor.fetchall()
        sql2 = "select status from Orders where OrderID ={}".format(OrderID)
        self.mycursor.execute(sql2)
        myresult2 = self.mycursor.fetchall()  
        if(myresult2[0][0]=="Cancelled"):
            return False     
        for i in range(0, len(myresult)):

            FurnitureID=myresult[i][0]
            quantity=myresult[i][1]
            sql2 = "select quantity from Assets where FurnitureID ={}".format(FurnitureID)
            self.mycursor.execute(sql2)
            myresult2 = self.mycursor.fetchall()
            AssetQuantity=myresult2[0][0]
            res = AssetQuantity + quantity
            print(res)
            print(FurnitureID)
            sql3 = "UPDATE Assets SET quantity = {} WHERE FurnitureID = {}".format(res,FurnitureID)
            self.mycursor.execute(sql3)
            self.mydb.commit()

    def AvailableToComment(self, customerid, furnitureid):
        sql2 = "select OrderID from Orders_help where CustomerID ={} and FurnitureID={}".format(customerid, furnitureid)
        self.mycursor.execute(sql2)
        myresult2 = self.mycursor.fetchall()
        myresult2
        if(len(myresult2)==0):
            return False
        else:
            #checks if you have commented
            sql2 = "select CommentID from Comments where CustomerID ={} and FurnitureID={}".format(customerid, furnitureid)
            self.mycursor.execute(sql2)
            myresult2 = self.mycursor.fetchall()
            myresult2
            if(len(myresult2)==0):
                return True
            else:
                return False

user = User()



