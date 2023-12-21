# BizCardX: Extracting Business Card Data with OCR 
(OCR, streamlit GUI, SQL, Data Extraction)


## PROJECT DESCRIPTION:

BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.


## TECHNOLOGIES NEED TO KNOW:

•	Python
•	Easy OCR
•	MySQL
•	Pandas
•	Streamlit Library



## SOFTWARE REQUIRED:

•	VSCode IDE
•	MySQL Workbench
•	Updated web browser

## REQUIRED LIBRARIES TO INSTALL:

pip install, easyOCR, mysql-connector-python, pandas, streamlit, plotly.

## EASYOCR:

EasyOCR, as the name suggests, is a Python package that allows computer vision developers to effortlessly perform Optical Character Recognition. It is a Python library for Optical Character Recognition (OCR) that allows you to easily extract text from images and scanned documents. In my project I am using easyOCR to extract text from business cards.

When it comes to OCR, EasyOCR is by far the most straightforward way to apply Optical Character Recognition:

•	The EasyOCR package can be installed with a single pip command.
•	The dependencies on the EasyOCR package are minimal, making it easy to configure your OCR development environment.
•	Once EasyOCR is installed, only one import statement is required to import the package into your project.
•	From there, all you need is two lines of code to perform OCR — one to initialize the Reader class and then another to OCR the image via the readtext function.

## WORKFLOW:

•	A webpage is displayed in browser, I have created the app with Four menu options namely HOME, UPLOAD, EXTRACT & MODIFY where user has the option to upload the respective Business Card whose information has to be extracted, stored, modified or deleted if needed.

•	Once user uploads a business card, the text present in the card is extracted by easyocr library.

•	The extracted text is sent to respective text classification as company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code using loops and some regular expression.

•	By clicking on “Show Text” in the upload page, classified data is displayed on screen.


•	On Clicking “Upload to Database” button the data gets stored in the MySQL Database. 

•	In the Extract page, by selecting the name of the card and clicking on “Extract data” button will show the details on the card and business card.

•	Further with the help of MODIFY menu the uploaded data in SQL Database can be accessed for Update and Delete Operations.


