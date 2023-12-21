""" Project Title : BizCardX-Extracting_Business_Card_Data_with_OCR
    Module used: Mysql.connector, easyocr, os, cv2, matplotlib, Streamlit GUI, Pandas, PIL
    Project Description: BizCardX is a user-friendly tool for extracting information from business cards. 
                        The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. 
                        Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides 
                        users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, 
                        and users would be able to easily add it to the database with the click of a button. 
                        Further the data stored in database can be easily Read, updated and deleted by user as per the requirement."""


#----------------------------------------/ Library Used  /-----------------------------------------------------------


import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import easyocr
import os
import cv2
import matplotlib.pyplot as plt
import re
import pandas as pd
from PIL import Image
import io


#---------------------------------------/ Database connection /-----------------------------------------


try:
    conn = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "mysql12345;",
                                database = "bizcard"
            )
    cursor = conn.cursor(buffered= True)
except mysql.connector.Error as e:
    st.write(e)


#----------------------------------/  Table creation  /------------------------------------------------------
    

cursor.execute("CREATE TABLE IF NOT EXISTS bizcard_data ("
                 "id INT AUTO_INCREMENT PRIMARY KEY,"
                 "name VARCHAR(255),"
                 "designation VARCHAR(255),"
                 "company VARCHAR(255),"
                 "contact VARCHAR(255),"
                 "email VARCHAR(255),"
                 "website VARCHAR(255),"
                 "address VARCHAR(255),"
                 "city VARCHAR(255),"
                 "state VARCHAR(255),"
                 "pincode VARCHAR(255),"
                 "image LONGBLOB )")

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

st.set_page_config(page_title= "BizcardX: Extracting Bussiness card data with OCR",
                   layout= "wide",
                   initial_sidebar_state= "expanded")

st.markdown("<h1 style='text-align:center; color:#cca350;'> BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)


# ---------------------------/ Convert image into Binary data  /------------------------------------------------------


def convert_image_to_binary(path):
    with open(path, 'rb') as img:
         binarydata = img.read()
    return binarydata
             

#---------------------------/ Main menu /---------------------------------------------


selected = option_menu(None, ["Home","Upload","Extract","Modify data"], 
                       icons=["house","cloud-upload","download","pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", "--hover-color": "#cca350"},
                               "icon": {"font-size": "30px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#cca350"}})


#----------------------------------/ Home page  /------------------------------------------------------


if selected == "Home":
    st.markdown("<h1 style='text-align:left; color:white;'> BizCardX: Extracting Business Card Data with OCR By Deepega</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:left; color:white;'> Using Python,easy OCR, Streamlit, SQL, Pandas<h2>", unsafe_allow_html=True)
    st.markdown("## :blue[**Description :**] This website will extract information form the uploaded image of a Bussiness card using easyOCR python library and allow user to store details in Mysql. The user can view,modify and delete the existing details in database.")

#-----------------------------------/ Upload page /----------------------------------------------------------


if selected == "Upload":
    bizcard = st.file_uploader(":blue[**Choose a file**]", type=['jpg','png','jpeg'])
    if bizcard is not None:
        # st.image(bizcard)

        def save_card(bizcard):
            with open(os.path.join("bizcards",bizcard.name), "wb") as f:
                f.write(bizcard.getbuffer())   
        save_card(bizcard)

        def image_preview(image,res): 
            for (bbox, text, prob) in res: 
              # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15,15)
            plt.axis('off')
            plt.imshow(image)

        col1, col2 = st.columns(2)
        with col1:
                # st.markdown("#     ")
                st.markdown("#     ")
                st.markdown("### You have uploaded the card")
                st.image(bizcard)
                
        with col2:
            with st.spinner("Please wait processing image..."):
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    path = os.path.join(os.getcwd(), "bizcards", bizcard.name)
                    image = cv2.imread(path)
                    result = reader.readtext(path)
                    st.markdown("#     ")
                    st.markdown("### Image Processed and Data Extracted")
                    st.pyplot(image_preview(image,result)) 
        card_info = [i[1] for i in result]
        demilater = ' '
        card = demilater.join(card_info)  #convert to string
        replacement = [
            (";", ""),
            (',', ''),
            ("WWW ", "www."),
            ("www ", "www."),
            ('www', 'www.'),
            ('www.', 'www'),
            ('wwW', 'www'),
            ('wWW', 'www'),
            ('.com', 'com'),
            ('com', '.com'),

        ]
        for old, new in replacement:
            card = card.replace(old, new)

        # ----------------------Phone------------------------------------
        ph_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
        ph = re.findall(ph_pattern, card)
        Phone = ''
        for num in ph:
            Phone = Phone + ' ' + num
            card = card.replace(num, '')

        # ------------------Mail id--------------------------------------------
        mail_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
        mail = re.findall(mail_pattern, card)
        Email_id = ''
        for ids in mail:
            Email_id = Email_id + ids
            card = card.replace(ids, '')

        # ---------------------------Website----------------------------------
        url_pattern = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
        url = re.findall(url_pattern, card)
        URL = ''
        for web in url:
            URL = URL + web
            card = card.replace(web, '')

        # ------------------------pincode-------------------------------------------
        pin_pattern = r'\d+'
        match = re.findall(pin_pattern, card)
        Pincode = ''
        for code in match:
            if len(code) == 6 or len(code) == 7:
                Pincode = Pincode + code
                card = card.replace(code, '')

        # ---------------name ,designation, company name-------------------------------
        name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
        name_data = []  # empty list
        for i in card_info:
            if re.findall(name_pattern, i):
                if i not in 'WWW':
                    name_data.append(i)
                    card = card.replace(i, '')
        name = name_data[0]
        designation = name_data[1]

        if len(name_data) == 3:
            company = name_data[2]
        else:
            company = name_data[2] + ' ' + name_data[3]
        card = card.replace(name, '')
        card = card.replace(designation, '')
        #city,state,address
        new = card.split()
        if new[4] == 'St':
            city = new[2]
        else:
            city = new[3]
        # state
        if new[4] == 'St':
            state = new[3]
        else:
            state = new[4]
        # address
        if new[4] == 'St':
            s = new[2]
            s1 = new[4]
            new[2] = s1
            new[4] = s  # swapping the St variable
            Address = new[0:3]
            Address = ' '.join(Address)  # list to string
        else:
            Address = new[0:3]
            Address = ' '.join(Address)  # list to string
        binary_data = convert_image_to_binary(path)          

        show_data = st.button(":blue[Show Text]", key = "showdata")
        Upload_to_database = st.button(":blue[Upload to Database]", key= "storeindatabase")
        if show_data:
            st.write('')
            st.write('###### :red[Name]         :', name)
            st.write('###### :red[Designation]  :', designation)
            st.write('###### :red[Company name] :', company)
            st.write('###### :red[Contact]      :', Phone)
            st.write('###### :red[Email id]     :', Email_id)
            st.write('###### :red[URL]          :', URL)
            st.write('###### :red[Address]      :', Address)
            st.write('###### :red[City]         :', city)
            st.write('###### :red[State]        :', state)
            st.write('###### :red[Pincode]      :', Pincode)
            
            
        if Upload_to_database:
            try:
                conn.autocommit = True
                sql = "INSERT INTO bizcard_data (name,designation,company,contact,email,website,address,city,state,pincode,image) " \
                                                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (name,designation,company,Phone,Email_id,URL,Address,city,state,Pincode,binary_data)
                cursor.execute(sql, val)
                st.success('Data Moved to database successfully', icon="☑️")
            except mysql.connector.Error as e:
                st.write(e)

    else:
            st.write(":red[No image uploaded yet.]")  


#------------------------------------/ Extract page /-----------------------------------------------


if selected == "Extract":
    sql = "SELECT name from bizcard_data"
    cursor.execute(sql)
    names_f = cursor.fetchall()
    names = [name[0] for name in names_f]
    # select, answer = st.columns([0.3,0.7])
    selected_name = st.selectbox(":blue[Choose the name on the card]", names,index=None, placeholder= "Choose name" )
    st.markdown("#  ")
    but1 = st.button(":blue[**Extract Data**]", key="Extract data")
    if but1:
        sql = "SElECT * from bizcard_data where name = %s"
        cursor.execute(sql, (selected_name,))
        details = cursor.fetchall()
        image_binary_data = details[0][-1]
        image = Image.open(io.BytesIO(image_binary_data))
        details_excluded_image = [list(details[0][:-1])]
        df = pd.DataFrame(details_excluded_image, columns=['id','name','designation','company','contact','email','website','address','city','state','pincode'])
        df.set_index('id', drop=True, inplace=True)

        st.markdown("# ")
        st.markdown("#### :blue[Details on the Bizcard]")
        st.write(df)
        st.markdown("# ")
        st.markdown("#### :blue[Bussiness Card]")
        st.image(image)


#------------------------------------/ Modify data  /-------------------------------------------
        

if selected == "Modify data":
    option = option_menu(None, ["Update Data", "Delete Data"],
                        icons=["pencil-fill", 'exclamation-diamond'],
                        default_index=0,
                        orientation="horizontal",
                        styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", "--hover-color": "#cca350"},
                               "icon": {"font-size": "30px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#cca350"}})
    if option == "Update Data":
        sql = "SELECT name from bizcard_data"
        cursor.execute(sql)
        names_f = cursor.fetchall()
        names = [name[0] for name in names_f]
        selected_name = st.selectbox(":blue[Choose the name on the card]", names,index=None, placeholder= "Choose name" )
        if selected_name:
            sql = "SElECT name,designation,company,contact,email,website,address,city,state,pincode from bizcard_data where name = %s"
            cursor.execute(sql, (selected_name,))
            result = cursor.fetchone()
            if result:
                st.markdown("#  ")
                name = st.text_input("Name", result[0])
                designation = st.text_input("Designation", result[1])
                company_name = st.text_input("Company Name", result[2])
                contact = st.text_input("Mobile Number", result[3])
                email = st.text_input("Email", result[4])
                website = st.text_input("Website", result[5])
                address = st.text_input("Area", result[6])
                city = st.text_input("City", result[7])
                state = st.text_input("State", result[8])
                pincode = st.text_input("Pincode", result[9])

            if st.button(":blue[Commit changes to DB]"):
                    try:
                        conn.autocommit = True
                        sql = "UPDATE bizcard_data SET name = %s, designation = %s, company = %s, contact = %s, email = %s, website = %s, address = %s, city = %s, state = %s, pincode = %s where name = %s"
                        values = (name, designation, company_name, contact, email, website, address, city, state, pincode, selected_name )
                        cursor.execute(sql,values)
                        st.success("Data updated succesfully in Database", icon="✅")
                    except mysql.connector.Error as e:
                        st.error(e)
    if option == "Delete Data":
        sql = "SELECT name from bizcard_data"
        cursor.execute(sql)
        names_f = cursor.fetchall()
        names = [name[0] for name in names_f]
        del_name = st.selectbox(":blue[Choose the name on the card]", names,index=None, placeholder= "Choose name" )
        if st.button(":blue[Delete from DB]"):
            sql = "DELETE FROM bizcard_data where name = %s"
            cursor.execute(sql,(del_name,))
            conn.commit()
            st.success("Deleted successfully from Database", icon="✅")



#----------------------------*** END OF CODE ***-----------------------------