#IMPORTING AND CONNECTING SQL
import MySQLdb
db = MySQLdb.connect(host='localhost',user='root',password='sansar@12')
c = db.cursor()

#CREATING DATABASE LIBRARY MANAGEMENT
try:
    c.execute("CREATE DATABASE LIBRARY_MANAGEMENT")
    print("Database Library Management has been created....")
except:
    print("Database Library Management already exists...")
print()

#USE DATABASE LIBRARY MANAGEMENT
c.execute("USE LIBRARY_MANAGEMENT")


#CREATING TABLE BOOK
try:
    c.execute("CREATE TABLE BOOK (BOOK_ID INT(5) PRIMARY KEY, BOOK_NAME CHAR(60)\
NOT NULL, AUTHOR_NAME CHAR(30) NOT NULL, GENRE CHAR(20), SERIES_NAME CHAR (40),\
SERIES_NO INT(2) , QUANTITY INT(5))")
    print("Table Book has been created...")
except:
    print("Table Book already exists...")

#CREATING TABLE MEMBER 
try:
    c.execute("CREATE TABLE MEMBER (MEMBER_NAME CHAR(30), MEMBER_ID VARCHAR(12)\
PRIMARY KEY, PHONE_NO VARCHAR(10),ADDRESS VARCHAR(60),MEMBER_P VARCHAR(20))")
    print("Table Member has been created...")
except:
    print("Table Member already exists...")

#CREATING TABLE ISSUE ( FOR BOTH ISSUE AND RETURN OF BOOK)

try:
    c.execute("CREATE TABLE ISSUE ( MEMBER_ID VARCHAR(12) NOT NULL ,BOOK_ASSIGNED_ID INT(5) NOT NULL, ISSUE_DATE DATE , RETURN_DATE DATE,RETURNING_DATE DATE)")
    print("Table Issue is Created...")
except:
    print("Table Issue already exists...")


#CREATING TABLE STAFF
try:
    c.execute('CREATE TABLE STAFF (STAFF_NAME CHAR(30) NOT NULL,\
PASSWORD CHAR(10)NOT NULL)')
    print("Table Staff has been created...")
except:
    print("Table Staff already exists...")

#CREATING TABLE REQUEST
try:
    c.execute("CREATE TABLE REQUEST (BOOK_NAME CHAR(60), AUTHOR_NAME CHAR(30))")
    print("Table Request has been created...")
except:
    print("Table Request already exists...")
    
#CREATING TABLE FEE
try:
    c.execute("CREATE TABLE FEE ( MEMBER_ID VARCHAR(12) NOT NULL ,FEES float(7,2))")
    print("Table FEE is Created...")
except:
    print("Table FEE already exists...")


#Function to add member to database(System)
#Both Staff and member can use this function
def addmember():
    while True:
        m_name = input('Enter your Full name :')
        while True:
            m_age = input('Enter your age :')
            #Checking if age entered is in digits
            if m_age.isdigit()==True:
                break
            else:
                print('Please enter a digit')
        #To be a member age should be above 15 years    
        if int(m_age) < 15:
            print('To be a member your age should be above 15')
            break
        while True:
            m_ID = input('Enter your unique aadhar ID :')
            #We are using aadhar ID ad Member ID
            #Checking if aadhar entered is of digits only
            if m_ID.isdigit()==False:
                print("Your Member ID should consist of digits only")
            else:
                #Getting member ID from member table
                member_sql="select MEMBER_ID from MEMBER"
                c.execute(member_sql)
                check_member=c.fetchall()
                list_member=[]
                #Adding Member ID from database to list to check if it exists in our database
                for i in check_member:
                    list_member.append(i[0])
                #Checking if ID entered already exits in our database
                if m_ID not in list_member:
                    #Checking length of ID entered (Aadhar has 12 digits)
                    if len(m_ID)== 12:
                        print('This is the ID entered by you :',m_ID)
                        ch=input("Please confirm once again if your ID is correct or not (Y/N) :")
                        if ch in 'yY':
                            break
                    else:
                        print("Your ID should be of 12 digits")
                else:
                    print()
                    print("This ID is already in our system..if it's not you we request you to manually lodge a complaint to our staff")
                    break
        if m_ID in list_member:
            break
            #Takes back to menu loop if ID already exists in database
        while True:
            phone_no = input('Enter your Phone Number :')
            #Checking if values entered are digits only
            if phone_no.isdigit()==False:
                    print("Your phone number should consist of only digits")
            else:
                #Checking length of phone number 
                if len(phone_no)==10:
                    break
                else:
                    print('Enter a 10 digit Phone Number')
        m_address= input("Enter your address :")
        while True:
            m_password = input('Enter password :') 
            conf_password = input('Confirm password :')
            #Confirming if password entered is same as confirmed password
            if m_password == conf_password:
                print('Your membership ID is :',m_ID)
                break
            else:
                print("Confirmed Password doesnt match")
    
        #Adding Member Name,ID,Phone no,address and password to database
        SQL="INSERT INTO MEMBER VALUES ('"+m_name+"','"+m_ID+"','"+phone_no+"','"+m_address+"','"+m_password+"')"
        c.execute(SQL)
        db.commit()
        #Inserting registration fee to member ID
        SQL_FEE="INSERT INTO FEE (MEMBER_ID) VALUES('"+m_ID+"')"
        c.execute(SQL_FEE)
        db.commit()
        #Registration Fee is Rs 200
        r="UPDATE FEE SET FEES = 200 where MEMBER_ID='"+m_ID+"'"
        c.execute(r)
        db.commit()
        print()
        print("Please deposit your registration fees to the staff member for further using our program :) ")
        #Loop if we want ot register more than one member at a time
        while True:
            ch = input('Would you like to add more members (Y/N) ?')
            if ch in 'NnYy':
                break
            else:
                print('Please choose either Yes(Y) or No(N)')
        if ch in 'Nn':
            break


#Function to delete a member from the database
#Can be used by staff only 
def deletemember():
    while True:
        m_id=input("Enter the ID of the member whose record you wish to remove :")
        for p in m_id:
            #Checking if member ID entered consists of digits only
          if p.isdigit()==False:
              print("Your Member ID should consist of digits only")
              deletemember()
        #Checking if ID length
        if len(m_id) == 12:
            #Importing values from member table and putting them in a list
            c.execute('SELECT * FROM MEMBER')
            display = c.fetchall()
            L=[]
            for i in display:
                L.append(i[1])
            #Checking if M_ID in our database
            #Checking if any issued books left to return before deleting 
            if m_id in L:
                issue="select MEMBER_ID from issue"
                c.execute(issue)
                check_issue= c.fetchall()
                list_issue=[]
                for i in check_issue:
                    list_issue.append(i[0])
                #Checking for pending payment before deleting ID
                if m_id not in list_issue:
                    fee="select fees from FEE where Member_ID='"+m_id+"'"
                    c.execute(fee)
                    check_fee=c.fetchall()
                    list_fee=[]
                    for i in check_fee:
                        list_fee.append(i[0])
                    if None in list_fee:
                        delete_member="DELETE FROM MEMBER WHERE MEMBER_ID='"+m_id+"'"
                        c.execute(delete_member)
                        db.commit()
                        delete_fee="DELETE FROM FEE WHERE MEMBER_ID='"+m_id+"'"
                        c.execute(delete_fee)
                        db.commit()
                        print(f'(Member ID {m_id} has been deleted)')
                    else:
                        print("Before deleting please deposit pending payment")
                        break
                else:
                    print()
                    print("Please return all your issued books first")
                    break
            else:
                print("Provided Member ID doesn't exist in Database ")
                print()
        else:
            print('Please enter a valid 12 digit Member ID ')
        while True:
            ch = input('Would you like to delete more records (Y/N) ?')
            if ch in 'NnYy':
                break
            else:
                print('Please choose either Yes(Y) or No(N)')
        if ch in 'Nn':
            break

#FUNCTION TO ADD BOOK IN THE LIBRARY
#CAN BE USED BY STAFF ONLY
def addbook():
    while True:
        print()
        Book_ID = input("Book ID :")
        #CHECKING IF ID IS IN DIGITS ONLY
        for u in Book_ID:
            if u.isdigit()==False:
                print("Your Book ID should consist of digits")
                addbook()
        #CHECKING IF BOOK ID ALREADY EXISTS IN DATABASE
        L=[]
        sql="select BOOK_ID from BOOK"
        c.execute(sql)
        view=c.fetchall()
        for i in view:
            L.append(i[0])
        if int(Book_ID) not in L:
            Book_Name = input("Book name :").upper()
            Author_Name = input("Author name :").upper()
            Genre = input("Genre :").upper()
            print()
            print('If dont know Series name or Series Number leave empty')
            Series_Name = input("Series Name :").upper()
            Series_No = input("Series Number :")
            if Series_No == '':
                Series_No = 'NULL'
            Quantity = input("Quantity :")
            #INSERTING VALUES IN BOOK TABLE IN SYSTEM
            SQL = "INSERT INTO BOOK VALUES ("+Book_ID+",'"+Book_Name+"','"+Author_Name+"','"+Genre+"','"+Series_Name+"',"+Series_No+","+Quantity+")"
            c.execute(SQL)
            if Series_Name == '':
                c.execute("UPDATE BOOK SET SERIES_NAME=NULL WHERE SERIES_NAME='' ")
            db.commit()
        else:
            print('Book ID already exists in database, Please enter a new Book ID')
            addbook()
        while True:
            print()
            ch = input('Would you like to add more books (Y/N) ?')
            if ch in 'NnYy':
                break
            else:
                print('Please choose either Yes(Y) or No(N)')
        if ch in 'Nn':
            break


#SEARCH FUNCTION
#USED BY BOTH STAFF AND MEMBER
def search():
    while True:
        print()
        print('1.Book Name \n2.Author Name \n3.Series Name \n4.Genre \n5.Exit Seach')
        i = input('Enter the number corresponding to they way you would like to search :')
        print()
        if i=='1':
            #bname is book name
            bname=input("Enter your Book Name :").upper()
            sql="SELECT * FROM BOOK where BOOK_NAME='"+bname+"'"
            c.execute(sql)
            View=c.fetchall()
            if View == ():
                print()
                print("Book isnt available in our library")
                print('You can try searching someother way or with different spelling')
                print("If you want us to add to the library you can request for it ")

            else:   
                for l in View:
                    print('----------------------------------------')
                    print('Book ID       :',l[0])
                    print('Book name     :',l[1])
                    print('Author name   :',l[2])
                    print('Genre         :',l[3])
                    print('Series name   :',l[4])
                    print('Series number :',l[5])
                    print('Quantity      :',l[6])
                    print('----------------------------------------')
        elif i=='2':
            print("You are searching by the Author's Name")
            aname=input("Enter your Author Name :").upper()
            #aname is author name
            sql="SELECT * FROM BOOK where AUTHOR_NAME='"+aname+"'"
            c.execute(sql)
            View=c.fetchall()
            if View == ():
                print()
                print("We currently don't have books by this author in our library")
                print('You can try searching someother way or with different spelling')
                print("If you want us to add a book to the library you can request for it ")

            else:   
                for l in View:
                    print('----------------------------------------')
                    print('Book ID       :',l[0])
                    print('Book name     :',l[1])
                    print('Author name   :',l[2])
                    print('Genre         :',l[3])
                    print('Series name   :',l[4])
                    print('Series number :',l[5])
                    print('Quantity      :',l[6])
                    print('----------------------------------------')

        elif i=='3':
            print("You are searching book by it's Series Name")
            sname=input("Enter the Series Name :").upper()
            #sname is series name
            sql="SELECT * FROM BOOK where SERIES_NAME='"+sname+"'"
            c.execute(sql)
            View=c.fetchall()
            if View == ():
                print()
                print("Books in this series are not available in our library")
                print('You can try searching someother way or with different spelling')
                print("If you want us to add to the library you can request for it ")

            else:   
                for l in View:
                    print('----------------------------------------')
                    print('Book ID       :',l[0])
                    print('Book name     :',l[1])
                    print('Author name   :',l[2])
                    print('Genre         :',l[3])
                    print('Series name   :',l[4])
                    print('Series number :',l[5])
                    print('Quantity      :',l[6])
                    print('----------------------------------------')
      
        elif i=='4':
            print("You are searching Book based on Genre")
            Gname=input("Enter the Genre :").upper()
            #gname is author name
            sql="SELECT * FROM BOOK where GENRE='"+Gname+"'"
            c.execute(sql)
            View=c.fetchall()
            if View == ():
                print()
                print("No book with this genre is available in our library")
                print('You can try searching someother way or with different spelling')
                
            else:   
                for l in View:
                    print('----------------------------------------')
                    print('Book ID       :',l[0])
                    print('Book name     :',l[1])
                    print('Author name   :',l[2])
                    print('Genre         :',l[3])
                    print('Series name   :',l[4])
                    print('Series number :',l[5])
                    print('Quantity      :',l[6])
                    print('----------------------------------------') 
        elif i=='5':
            break
        else:
            print('Enter a valid number (1,2,3,4,5)')

#FUNCTION TO ISSUE BOOK
#USED BY MEMBER ONLY
def issue_book(m_id):
    d=1 #FOR NUMBER OF BOOKS ISSUED. ONLY 3 CAN BE ISSUED
    while True:
        if d<=3:
            List_Fee=[]
            #CHECKING IF ANY FEE NEEDS TO BE DEPOSITED BEFORE ISSUING BOOK
            fee="select FEES from Fee where MEMBER_ID='"+m_id+"'"
            c.execute(fee)
            view_fee=c.fetchall()
            for i in view_fee:
                List_Fee.append(i[0])
            if None in List_Fee:
                def book_issue_id():
                    nonlocal d
                    b_id=input("Enter your book ID :")
                    for u in b_id:
                        if u.isdigit()==False:
                            print("Book ID should consist of digits")
                            book_issue_id()
                    SQL_book="SELECT * FROM BOOK"
                    c.execute(SQL_book)
                    view=c.fetchall()
                    List=[]
                    for i in view:
                        List.append(i[0])
                    #CHECKING IF BOOK ID EXISTS IN DATABASE
                    if int(b_id) in List:
                        L_issue=[]
                        #CHECKING IF SAME BOOK HAS ALREADY BEEN ISSUED
                        #CAN'T ISSUE THE SAME BOOK TWICE 
                        sql_issue="Select * from Issue where MEMBER_ID='"+m_id+"'"
                        c.execute(sql_issue)
                        see=c.fetchall()
                        for g in see:
                            L_issue.append(g[1])
                        if int(b_id) not in L_issue:
                            while True:
                                #CHECKING IF BOOK AVAILABLE IN LIBRARY
                                zero="select QUANTITY from book where BOOK_ID="+b_id+" "
                                c.execute(zero)
                                zero_view=c.fetchall()
                                ZeroList=[]
                                for w in zero_view:
                                    ZeroList.append(w)
                                if ZeroList[0]<=(0,):
                                    print("This is book is not available")
                                    d-=1
                                    break
                                else:
                                    #ENTERNING VALUES IN ISSUE TABLE 
                                    issue_date=input("Enter date in YYYY-MM-DD format :")
                                    SQL="INSERT INTO ISSUE (MEMBER_ID,BOOK_ASSIGNED_ID,ISSUE_DATE) VALUES ('"+m_id+"',"+b_id+",'"+issue_date+"')"
                                    c.execute(SQL)
                                    db.commit()
                                    r="UPDATE ISSUE SET RETURN_DATE = DATE_ADD(issue_date, INTERVAL 1 month )"
                                    c.execute(r)
                                    db.commit()
                                    quantity="UPDATE BOOK SET QUANTITY = QUANTITY - 1 where BOOK_ID = "+b_id+""
                                    c.execute(quantity)
                                    db.commit()
                                    break
                        else:
                            print("You already have this book issued")
                            book_issue_id()
                    else:
                        print("Book ID does not exist in the database, please try again")
                        book_issue_id()
                book_issue_id()
            else:
                print()
                print("Please deposit your fees first")
                break
        if d>3:
            print("You can't issue more than 3 books at a time")
            break
        while True:
            ch = input('Would you like to issue more books with this ID (Y/N) ?')
            if ch in 'NnYy':
                break
            else:
                print('Please choose either Yes(Y) or No(N)')
        if ch in 'yY':
            d+=1
        if ch in 'Nn':
            break




#FUNCTION TO DEPOSIT FEE
#USED BY MEMBER ONLY
def fee_deposit(m_id):
    #IMPORTING MEMBER ID FROM FEE TABLE
    SQL_mem="SELECT MEMBER_ID FROM FEE"
    c.execute(SQL_mem)
    display=c.fetchall()
    L=[]
    for z in display:
        L.append(z[0])
    #IMPORTING FEES MEMBER NEEDS TO PAY FROM TABLE
    SQL_fee="select Fees from FEE where MEMBER_ID='"+m_id+"'"
    c.execute(SQL_fee)
    VIEW=c.fetchall()
    for k in VIEW:
        print("You have to deposit", k[0])
        print()
    #UPDATING FEES TO NULL AFTER PAYMENT
    r="UPDATE FEE SET FEES = NULL where MEMBER_ID='"+m_id+"'"
    c.execute(r)
    db.commit()



#FUNCTION TO RETURN BOOK
#USED BY MEMBER ONLY
def returning_book(m_id):
    while True:
        sql_fees="Select FEES from FEE where MEMBER_ID='"+m_id+"'"
        c.execute(sql_fees)
        see=c.fetchall()
        L=[]
        for l in see:
            L.append(l[0])
        if None in L :
            check_issue="select BOOK_ASSIGNED_ID from issue where MEMBER_ID='"+m_id+"'"
            c.execute(check_issue)
            view_issue=c.fetchall()
            List_issue=[]
            for i in view_issue:
                List_issue.append(i[0])
            List_assigned=[]
            for y in List_issue:
                y=str(y)
                check_assigned="select BOOK_ID,BOOK_NAME from BOOK where BOOK_ID="+y+""
                c.execute(check_assigned)
                view_assigned=c.fetchall()
                for i in view_assigned:
                    List_assigned.append(i)
            print("the books issue by you are: ")
            print()
            print(List_assigned)
            def book_return_id():
                b_id=input("Enter your book ID :")
                for u in b_id:
                    if u.isdigit()==False:
                        print("your book id should consist of digits")
                        book_return_id()
                SQL_book="SELECT * FROM issue where MEMBER_ID='"+m_id+"'"
                c.execute(SQL_book)
                view=c.fetchall()
                List=[]
                for i in view:
                    List.append(i[1])
                if int(b_id) in List:
                    returning_date=input("Enter today's date in YYYY-MM-DD format :")
                    returning_data="UPDATE ISSUE SET RETURNING_DATE ='"+returning_date+"' where MEMBER_ID='"+m_id+"' and BOOK_ASSIGNED_ID="+b_id+""
                    c.execute(returning_data)
                    db.commit()
                    quantity="UPDATE BOOK SET QUANTITY=QUANTITY+1 where BOOK_ID="+b_id+""
                    c.execute(quantity)
                    db.commit()
                    x="select DATEDIFF(RETURNING_DATE,RETURN_DATE )from ISSUE where MEMBER_ID='"+m_id+"' and BOOK_ASSIGNED_ID="+b_id+" "
                    c.execute(x)
                    view_date=c.fetchall()
                    List_date=[]
                    for a in view_date:
                        List_date.append(a[0])
                    for i in List_date:
                        if i<=0:
                            cmd="UPDATE FEE SET FEES= NULL where MEMBER_ID='"+m_id+"'"
                            c.execute(cmd)
                            db.commit()
                            break
                        if i>0:
                            y=int(List_date[0])*20
                            y=str(y)
                            r="UPDATE FEE SET FEES = "+y+" where MEMBER_ID='"+m_id+"'"
                            c.execute(r)
                            db.commit()
                            break
                    delete="delete from issue where BOOK_ASSIGNED_ID="+b_id+" and Member_ID='"+m_id+"' "
                    c.execute(delete)
                    db.commit()
                else:
                    print("This book is not issued by you,pls check and try again")
                    book_return_id()
            book_return_id()
        else:
            print("Pls deposit your fees first")
            break


#FUNCTION TO REQUEST BOOK
#CAN BE USED BY MEMBER ONLY
def request_book():
  while True:
    request_b = input('Enter name of the Book you would like us to add :')
    request_a = input("Enter the Author's name of the above book (if you don't know write NA) :")
    #INSERTING VALUES IN REQUEST TABLE 
    s = "INSERT INTO REQUEST VALUES ('"+request_b+"','"+request_a+"')"
    c.execute(s)
    db.commit()
    choice=input("Would you like to request for more books (Y/N) :")
    if choice in "nN":
      break

#MEMBER LOGIN FUNCTION
def m_login():
    while True:
        m_id = input('Enter your Member ID :')
        #CHECKING IF ID ENTERED CONSISTS OF DIGITS ONLY
        for p in m_id:
          if p.isdigit()==False:
              print("your member id should consist of digits only")
              m_login()
        #CHECKING LENGTH OF ID ENTERED
        if len(m_id)==12:
            #IMPOTING FROM MEMBER AND CHECKING IF ID EXISTS IN DATABASE
            SQL="SELECT * FROM MEMBER"
            c.execute(SQL)
            display=c.fetchall()
            L=[]
            for i in display:
                L.append(i[1])
            if m_id in L:
                while True:
                    #CHECKING IF PASSWORD ENTERED MATCHES THE ONE IN SYSTEM
                    sql="SELECT * FROM MEMBER WHERE MEMBER_ID='"+m_id+"'"
                    c.execute(sql)
                    View=c.fetchall()
                    Mpassword = input('Enter your password :')
                    List=[]
                    for r in View:
                        List.append(r[4])
                    #IF PASSWORD ENTERED IS CORRECT LOGIN IS SUCCESSFUL
                    if Mpassword in List:
                        print('Login was successful')
                        print()
                        while True:
                            print('1.Search \n2.Issue Book \n3.Return Book \n4.Fee Deposit \n5.Request Book\n6.Exit')
                            inp = input('Enter you choice (1/2/3/4/5) :')
                            if inp == '1':
                                print('You have chosen search function ')
                                search()
                            elif inp == '2':
                                print('Please enter the following details to issue the book ')
                                issue_book(m_id)
                            elif inp == '3':
                                print('Please enter the following details to return the book')
                                returning_book(m_id)
                            elif inp == '4':
                                print('Please deposit the fees')
                                fee_deposit(m_id)
                            elif inp == '5':
                                print('Please enter the following details to Request for the book to be added to the library')
                                request_book()
                            elif inp == '6':
                                break
                            else:
                                print('Please enter a valid option (1/2/3/4/5/6)') 
                        if inp=='6':
                            break          
                    else:
                        print("Name doesn't match with your password try to login in again")
            else:
                print("Member ID doesn't exist in our Database")
        else:
            print("Your ID should consist of 12 digits")
        while True:
            choice=input("Do you wish to try Again (Y/N)  :")
            if choice in 'nNyY':
                break
            else:
                print("pls type Y for Yes and N for NO")
        if choice in "nN":
            break


#FUNCTION TO ADD STAFF MEMBER 
def addstaff():
    while True:
        s_name = input('Enter your Full Name :').upper()
        while True:
            #CHECKING IF THE PASSWORD ALREADY BELONGS TO ANOTHER STAFF MEMBER
            s_password = input('Enter password :')
            L=[]
            sql="select PASSWORD from STAFF"
            c.execute(sql)
            view=c.fetchall()
            for i in view:
                L.append(i[0])
            if s_password not in L:
                #CHECKING IF PASSWORD IS SAME AS CONFIRMED PASSWORD
                con_password = input('Confirm password :')
                if s_password == con_password:
                    break
                else:
                    print("Confirmed Password doesnt match")
            else:
                print("This password is already taken")
        #ADDING VALUES TO THE DATABASE
        SQL = "INSERT INTO STAFF VALUES ('"+s_name+"','"+s_password+"')"
        c.execute(SQL)
        db.commit()
        while True:
            ch = input('Would you like to register more staff members(Y/N) ?')
            if ch in 'NnYy':
                break
            else:
                print('Please choose either Yes(Y) or No(N)')
        if ch in 'Nn':
            break

#FUNCTION TO ISSUE BOOK
#CAN BE USED BY STAFF ONLY
#SAME AS ONE IN MEMBER EXCEPT MEMBER ID NEEDS TO BE ADDED 
def S_issue_book():
    m_id=input("Enter your member ID :")
    d=1
    for p in m_id:
        if p.isdigit()==False:
            print("Your member ID should consist of digits")
            S_issue_book()
    while True:
        if d<=3:
            if len(m_id)==12:
                SQL_member="SELECT * FROM MEMBER"
                c.execute(SQL_member)
                display=c.fetchall()
                L=[]
                for z in display:
                    L.append(z[1])
                if m_id in L:
                    List_Fee=[]
                    fee="select FEES from Fee where MEMBER_ID='"+m_id+"'"
                    c.execute(fee)
                    view_fee=c.fetchall()
                    for i in view_fee:
                        List_Fee.append(i[0])
                    if None in List_Fee:
                        def book_issue_id():
                            nonlocal d
                            b_id=input("Enter your book ID :")
                            for u in b_id:
                                if u.isdigit()==False:
                                    print("book ID should consist of digits")
                                    book_issue_id()
                            SQL_book="SELECT * FROM BOOK"
                            c.execute(SQL_book)
                            view=c.fetchall()
                            List=[]
                            for i in view:
                                List.append(i[0])
                            if int(b_id) in List:
                                L_issue=[]
                                sql_issue="Select * from Issue where MEMBER_ID='"+m_id+"'"
                                c.execute(sql_issue)
                                see=c.fetchall()
                                for g in see:
                                    L_issue.append(g[1])
                                if int(b_id) not in L_issue:
                                    while True:
                                        zero="select QUANTITY from book where BOOK_ID="+b_id+" "
                                        c.execute(zero)
                                        zero_view=c.fetchall()
                                        ZeroList=[]
                                        for w in zero_view:
                                            ZeroList.append(w)
                                        if ZeroList[0]<=(0,):
                                            print("This is book is not available")
                                            d-=1
                                            break
                                        else:
                                            issue_date=input("Enter date in YYYY-MM-DD format :")
                                            SQL="INSERT INTO ISSUE (MEMBER_ID,BOOK_ASSIGNED_ID,ISSUE_DATE) VALUES ('"+m_id+"',"+b_id+",'"+issue_date+"')"
                                            c.execute(SQL)
                                            db.commit()
                                            r="UPDATE ISSUE SET RETURN_DATE = DATE_ADD(issue_date, INTERVAL 1 month )"
                                            c.execute(r)
                                            db.commit()
                                            quantity="UPDATE BOOK SET QUANTITY = QUANTITY - 1 where BOOK_ID = "+b_id+""
                                            c.execute(quantity)
                                            db.commit()
                                            break
                                else:
                                    print("U already have this book issued")
                                    book_issue_id()
                            else:
                                print("book id does not exist in the database,pls try again")
                                book_issue_id()
                        book_issue_id()
                    else:
                        print()
                        print("pls deposit your fees first")
                        break

                else:
                    print("There is no such member ID in our database, pls try again")
                    S_issue_book()
            else:
                print("Member ID should be of 12 digits,pls try again")
                S_issue_book()
        if d>3:
            print("You can't issue more than 3 books at a time")
            break
        while True:
            ch = input('Would you like to issue more books with this ID (Y/N) ?')
            if ch in 'NnYy':
                break
            else:
                print('Please choose either Yes(Y) or No(N)')
        if ch in 'yY':
            d+=1
        if ch in 'Nn':
            break


#FUNCTION TO RETURN BOOK
#CAN BE USED BY STAFF ONLY
#SAME AS MEMBER ONE EXCEPT MEMBER ID NEEDS TO BE ADDED
def S_returning_book():
    m_id=input("Enter your member ID :")
    for p in m_id:
        if p.isdigit()==False:
            print("your member id should consist of digits")
            S_returning_book()
    while True:
        if len(m_id)==12:
                SQL_member="SELECT * FROM MEMBER"
                c.execute(SQL_member)
                display=c.fetchall()
                L_member=[]
                for q in display:
                    L_member.append(q[1])
                if m_id in L_member:
                    sql_fees="Select FEES from FEE where MEMBER_ID='"+m_id+"'"
                    c.execute(sql_fees)
                    see=c.fetchall()
                    L=[]
                    for l in see:
                        L.append(l[0])
                    if None in L :
                        check_issue="select BOOK_ASSIGNED_ID from issue where MEMBER_ID='"+m_id+"'"
                        c.execute(check_issue)
                        view_issue=c.fetchall()
                        List_issue=[]
                        for i in view_issue:
                            List_issue.append(i[0])
                        List_assigned=[]
                        for y in List_issue:
                            y=str(y)
                            check_assigned="select BOOK_ID,BOOK_NAME from BOOK where BOOK_ID="+y+""
                            c.execute(check_assigned)
                            view_assigned=c.fetchall()
                            for i in view_assigned:
                                List_assigned.append(i)
                        print("the books issue by you are: ")
                        print()
                        print(List_assigned)
                        def book_return_id():
                            b_id=input("Enter your book ID :")
                            for u in b_id:
                                if u.isdigit()==False:
                                    print("your book id should consist of digits")
                                    book_return_id()
                            SQL_book="SELECT * FROM issue where MEMBER_ID='"+m_id+"'"
                            c.execute(SQL_book)
                            view=c.fetchall()
                            List=[]
                            for i in view:
                                List.append(i[1])
                            if int(b_id) in List:
                                returning_date=input("Enter today's date in YYYY-MM-DD format :")
                                returning_data="UPDATE ISSUE SET RETURNING_DATE ='"+returning_date+"' where MEMBER_ID='"+m_id+"' and BOOK_ASSIGNED_ID="+b_id+""
                                c.execute(returning_data)
                                db.commit()
                                quantity="UPDATE BOOK SET QUANTITY=QUANTITY+1 where BOOK_ID="+b_id+""
                                c.execute(quantity)
                                db.commit()
                                x="select DATEDIFF(RETURNING_DATE,RETURN_DATE )from ISSUE where MEMBER_ID='"+m_id+"' and BOOK_ASSIGNED_ID="+b_id+" "
                                c.execute(x)
                                view_date=c.fetchall()
                                List_date=[]
                                for a in view_date:
                                    List_date.append(a[0])
                                for i in List_date:
                                    if i<=0:
                                        cmd="UPDATE FEE SET FEES= NULL where MEMBER_ID='"+m_id+"'"
                                        c.execute(cmd)
                                        db.commit()
                                        break
                                    if i>0:
                                        y=int(List_date[0])*20
                                        y=str(y)
                                        r="UPDATE FEE SET FEES = "+y+" where MEMBER_ID='"+m_id+"'"
                                        c.execute(r)
                                        db.commit()
                                        break
                                delete="delete from issue where BOOK_ASSIGNED_ID="+b_id+" and Member_ID='"+m_id+"' "
                                c.execute(delete)
                                db.commit()
                            else:
                                print("This book is not issued by you,pls check and try again")
                                book_return_id()
                        book_return_id()
                    else:
                        print("Pls deposit your fees first")
                        break
                else:
                    print("There is no such member ID in our database")
                    S_returning_book()
        else:
            print("Member ID should be of 12 digits")
            S_returning_book()
        break


#FUNCTION TO DEPOSIT FEE
#CAN BE USED BY STAFF ONLY
#SAME AS MEMBER ONE EXCEPT MEMBER ID NEEDS TO BE ADDED
def S_fee_deposit():
    m_id=input("Enter your member ID")
    for p in m_id:
        if p.isdigit()==False:
            print("Your member ID should consist of digits")
            fee_deposit()
    if len(m_id)==12:
        SQL_mem="SELECT MEMBER_ID FROM FEE"
        c.execute(SQL_mem)
        display=c.fetchall()
        L=[]
        for z in display:
            L.append(z[0])
        if m_id in L:
            SQL_fee="select Fees from FEE where MEMBER_ID='"+m_id+"'"
            c.execute(SQL_fee)
            VIEW=c.fetchall()
            for k in VIEW:
                print("You have to deposit", k[0])
                print()
            r="UPDATE FEE SET FEES = NULL where MEMBER_ID='"+m_id+"'"
            c.execute(r)
            db.commit()
        else:
            print("Member ID does not exist in your database, please try again")
            S_fee_deposit()
    else:
        print("Member ID should be of 12 digits, please try again")
        S_fee_deposit()


#FUNCTION TO UPDATE MEMBER DETAILS
#CAN BE USED BY STAFF ONLY
def update_member():
    m_id=input("Enter your member ID")
    while True:
        while True:
            #CHECKING IF MEMBER ID CONSISTS OF DIGITS ONLY
            if m_id.isdigit()==False:
                print("Your ID should consist of only digits")
            else:
                break
        #CHECKING LENGTH OF MEMBER ID
        if len(m_id)==12:
            sql="select MEMBER_ID from MEMBER"
            c.execute(sql)
            view=c.fetchall()
            L=[]
            for i in view:
                L.append(i[0])
            if m_id in L:
                while True:
                    print('1.Update address \n2.Update phone number \n3.Update password \n4.Exit')
                    take=input("What would you like to do?")
                    if take=='1':
                        def change_address(m_id):
                            address= input("Enter your new address :")
                            #UPDATING OLD ADDRESS WITH NEW ADDRESS
                            SQL="update MEMBER SET ADDRESS='"+address+"' where MEMBER_ID='"+m_id+"'"
                            c.execute(SQL)
                            db.commit()
                        change_address(m_id)
                    elif take=='2':
                        def change_phone(m_id):
                            phone=input("Enter your new phone number :")
                            while True:
                                #CHECKING IF PHONE NUMBER ENTERED CONSISTS OF DIGITS ONLY
                                if phone.isdigit()==False:
                                    print("Your phone number should consist of digits only ,please try again")
                                    change_phone(m_id)
                                else:
                                    break
                                #CHECKING IF PHONE NUMBER HAS 10 DIGITS 
                            if len(phone)==10:
                                #UPDATING OLD PHONE NUMBER WITH NEW 
                                sql_phone="update MEMBER SET phone_no='"+phone+"' where MEMBER_ID='"+m_id+"'"
                                c.execute(sql_phone)
                                db.commit()
                            else:
                                print("Your phone number should be of 10 digits, please try again")
                                change_phone(m_id)
                        change_phone(m_id)
                    elif take=='3':
                        def change_password(m_id):
                            while True:
                                #CHECKING IF OLD PASSWORD ENTERED IS SAME AS THE ONE IN DATABASE
                                old_password=input("Enter your old password :")
                                L=[]
                                sql="select MEMBER_P from MEMBER where MEMBER_ID='"+m_id+"'"
                                c.execute(sql)
                                view=c.fetchall()
                                for i in view:
                                    L.append(i[0])
                                if old_password in L:
                                    while True:
                                        #CHECKING IF CONFIRMED PASSWORD IS SAME 
                                        new_password=input("Enter your new password :")
                                        con_password = input('Confirm password :')
                                        if new_password == con_password:
                                            break
                                        else:
                                            print("Confirmed Password doesn't match")
                                    sql_pass="update MEMBER SET MEMBER_P='"+new_password+"' where MEMBER_ID='"+m_id+"'"
                                    c.execute(sql_pass)
                                    db.commit()
                                    break
                                else:
                                    print("Your password doesn't match the exiting one")
                        change_password(m_id)
                    elif take=='4':
                        break
                    else:
                        print('Please enter a valid option (1/2/3/4/5)')
            else:
                print("This ID doesn't exist in our database")
                while True:
                    ch=input('Would you like to try again?')
                    if ch in 'nNyY':
                        break
                    else:
                        print("Please choose either YES(Y) or NO(N)")
                if ch in 'nN':
                    break
                elif ch in 'yY':
                    update_member()
        else:
            print("Member ID is of 12 digits, please try again")
            update_member()
        if take == '4':
            break


#STAFF LOGIN FUNCTION
def s_login():
    while True:
        L=[]
        Sname = input('Enter you full name :').upper()
        #IMPORTING VALUES FROM STAFF TABLE
        SQL="SELECT * FROM STAFF"
        c.execute(SQL)
        display=c.fetchall()
        for i in display:
            L.append(i[0])
        #CHECKING IF NAME EXISTS IN DATABASE
        if Sname in L:
            #CHECKING IF PASSWORD ENTERED MATCHES THE ONE IN DATABASE FOR THE STAFF MEMBER
            sql="SELECT * FROM STAFF WHERE STAFF_NAME='"+Sname+"'"
            c.execute(sql)
            View=c.fetchall()
            Spassword = input('Enter your password :')
            for r in View:
                #IF PASSWORD IS CORRECT LOGIN IS SUCCESSFUL 
                if r[1] == Spassword:
                    print()
                    print('Login was successful')
                    while True:
                        print()
                        print('1.Add Book \n2.Add Member \n3.Delete Member \n4.Update Member \n5.Issue Book \n6.Return Book \n7.Fee Deposit \n8.Search \n9.Exit')
                        q = input('Enter your choice (1/2/3/4/5/6/7) :')
                        print()
                        if q == '1':
                            print('Add Book feature')
                            addbook()
                        elif q == '2':
                            print('Add Member feature')
                            addmember()
                        elif q == '3':
                            print('Delete Member feature')
                            deletemember()
                        elif q == '4':
                            print('Update feature')
                            update_member()
                        elif q == '5':
                            print('Issue Book feature')
                            S_issue_book()
                        elif q == '6':
                            print('Return Book feature')
                            S_returning_book()
                        elif q == '7':
                            print('Fee Deposit feature')
                            S_fee_deposit()
                        elif q == '8':
                            print('Search Book feature')
                            search()
                        elif q == '9':
                            break
                        else:
                            print('Enter a valid option (1/2/3/4/5/6/7/8/9)')
                            
                else:
                    print('Name doesnt match with your password Try to login in again')
        else:
            print("Name doesn't exist in Database")
        while True:
            choice=input("Do you wish to Login Again (Y/N)  :")
            print()
            if choice in 'nNyY':
                break
            else:
                print("Type Y for yes and N for NO")
        if choice in "nN":
            break
        
        
#MAIN LOOP
print()
print()
print('Welcome to our Library')
while True:
    print()
    print('MENU ')
    print()
    print('1.Member Registration \n2.Member Login \n3.Staff \n4.Exit ')
    a = input('Enter your choice (1/2/3/4):')
    if a == '1' :
        print()
        print('Please fill in the following details to register as a member of our library')
        addmember()
        print()
    elif a == '2' :
        print()
        print('Please enter the following details to login')
        m_login()
        print()
    elif a == '3':
        while True:
            print()
            print('STAFF ')
            print()
            print('1.Staff Registration \n2.Staff Login \n3.Exit')
            input_s = input('Enter Choice (1/2/3) :')
            print()
            if input_s == '1':
                print('Please fill the following details')
                print()
                addstaff()
            elif input_s == '2':
                print('Please enter the following details to login')
                print()
                s_login()
            elif input_s == '3':
                break
            else:
                print('Please enter a valid option (1/2/3)')
                print()
    elif a == '4':
        break
    else:
        print('Please enter a valid option (1/2/3/4)')
print()
print('Thank You')

