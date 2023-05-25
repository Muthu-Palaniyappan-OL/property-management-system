import pytesseract
import cv2
import regex as re

# Path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variables for PAN
pan_number = None
pan_name = None
pan_dob = None
father_name = None

# Global variables for Aadhar
aadhaar_number = None
aadhar_name = None
aadhar_dob = None
gender = None

# Function to validate Aadhar number
def is_valid_aadhar(aadhar_number):
    if aadhar_number is None:
        return False
    return True


# Function to validate PAN number
def is_valid_pan(pan_number):
    if pan_number is None:
        return False
    return True


# Function to extract details from PAN card image
def pan_ocr(image_path):
    global pan_number, name, dob, father_name
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray, lang='eng')

    # Extract PAN number from the OCR result
    pan_regex = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    pan_number = re.findall(pan_regex, text)
    if pan_number:
        pan_number = pan_number[0]
    else:
        pan_number = None

    # Extract name from the OCR result
    name_regex = r'NAME\n([\w\s\/]+)\n'
    name = re.findall(name_regex, text)
    if name:
        name = name[0].strip()
    else:
        name = None

    # Extract DOB from the OCR result
    pan_dob_regex = r'Date of Birth/.*\n(.+)\n'
    pan_dob = re.findall(pan_dob_regex, text)
    if pan_dob:
        pan_dob = pan_dob[0]
    else:
        pan_dob = None

    # Extract father's name from the OCR result
    father_regex = r"FATHER'S NAME\n(.+)\n"
    father_name = re.findall(father_regex, text)
    if father_name:
        father_name = father_name[0]
    else:
        father_name = None

    return pan_number, pan_name, pan_dob, father_name


# Function to extract details from Aadhaar card image
def aadhar_ocr(image_path):
    global pan_number, name, dob, father_name
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray, lang='eng')
    print(text)

    # Extract Aadhaar number from the OCR result
    aadhaar_regex = r'\b[0-9]{4}\s[0-9]{4}\s[0-9]{4}\b'
    aadhaar_number = re.findall(aadhaar_regex, text)
    if aadhaar_number:
        aadhaar_number = aadhaar_number[0].replace(' ', '')
    else:
        aadhaar_number = None

    # Extract name from the OCR result
    aadhar_name_regex = r'(?<=Name).*?(?=\n)'

    # Find name using regular expression
    aadhar_name = re.search(aadhar_name_regex, text)
    if aadhar_name:
        aadhar_name = aadhar_name[0]
    else:
        aadhar_name = None

    # Extract DOB from the OCR result
    aadhar_dob_regex = r'DOB.*?(\d{2}/\d{2}/\d{4})'
    aadhar_dob = re.findall(aadhar_dob_regex, text)
    if aadhar_dob:
        aadhar_dob = aadhar_dob[0]
    else:
        aadhar_dob = None

    # Extract gender from the OCR result
    gender_regex = r'Male|Female|Other'
    gender = re.findall(gender_regex, text)
    if gender:
        gender = gender[0]
    else:
        gender = None

    return aadhaar_number, aadhar_name, aadhar_dob, gender


def cross_validate_pan_aadhar():
    if pan_dob == aadhar_dob:
        return True
    else:
        return False


def extract_rental_details(image_path):
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)
    name = re.search(r'Tenant\sName\s:\s(.+)', text).group(1)
    validity_period = re.search(r'Valid\sFrom\s:\s(.+)\sTo\s:\s(.+)', text)
    validity_start = validity_period.group(1)
    validity_end = validity_period.group(2)

    return name, validity_start, validity_end


# print(pan_ocr("pan.jpeg"))
# print(aadhar_ocr("aadhar.jpeg"))
# print(extract_rental_details("Rental-Agreement.jpg"))
