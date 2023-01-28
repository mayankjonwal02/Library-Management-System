import mysql.connector as con
db=con.connect(host="localhost",user="root",password="Mayjon@1372",db="library")


mycursor=db.cursor()
#mycursor.execute("CREATE TABLE person (name VARCHAR(50), age smallint UNSIGNED, personid int PRIMARY KEY AUTO_INCREMENT)")

mycursor.execute("INSERT INTO dayoperations (user_name,user_email,book_name,category,fromm,days,due) VALUES (%s,%s,%s,%s,%s,%s,%s)",('1','2','3','4','5','6','7'))
#mycursor.execute("DELETE FROM category WHERE category_name='gaming'")
db.commit()
for i in mycursor:
    print(i)


