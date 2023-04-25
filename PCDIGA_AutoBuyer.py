##############################################################################
# Script: PCDIGA_AutoBuyer.py
#-----------------------------------------------------------------------------
# Desc: Script to buy products automatically from PCDiga
# Author: Miguel Silva
# Contact: github.com/miguelpmsilva
#-----------------------------------------------------------------------------
# Change History:
# Update Date:          
##############################################################################

##############################################################################
# Imports
##############################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

##############################################################################
# Custom Variables - Change this for your needs
##############################################################################
product_url="https://www.pcdiga.com/componentes/placas-graficas/placas-graficas-amd/placa-grafica-msi-radeon-rx-6900-xt-gaming-x-trio-16g-912-v395-007"
email="test1234@email.com"
_pass="Password123"
phone_nr="930000000"

##############################################################################
# Function: pageDOWN()
#-----------------------------------------------------------------------------
# Desc: Scroll Down/ Press Page Down Key
##############################################################################

def pageDOWN():
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)


##############################################
# Script Body
##############################################

    PATH = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(product_url)
    
    #Accept Cookies Popup
    driver.find_element_by_class_name("btn-cookie.btn-cookie-accept").click()
    
    #Check product stock
    stock = driver.find_element_by_id("skrey_estimate_date_product_page_wrapper").text

    #Refresh every 10s to check stock
    while stock == "Sem stock":
        time.sleep(10)
        driver.refresh()

        
    ##Executes if product is in stock##
    
    #Add product to cart
    add_to_cart=driver.find_element_by_id("product-addtocart-button").click()
    
    #Login
    driver.get("https://www.pcdiga.com/customer/account/login/")
    username_element = driver.find_element_by_id("email")
    username_element.send_keys(email)
    password_element=driver.find_element_by_id("pass")
    password_element.send_keys(_pass)
    password_element.send_keys(Keys.ENTER)
    
    #Go to checkout page
    driver.get("https://www.pcdiga.com/checkout/")
    time.sleep(3)
    
    #Select online free shipping
    online_shipping_element = driver.find_element_by_id("label_method_skrey_free_shipping_skrey_free_shipping").click()
    time.sleep(0.5)
    pageDOWN()
    time.sleep(0.5)

    #Click continue button
    continue_button = driver.find_element_by_class_name('button.action.continue.primary').click()
    time.sleep(2)
    pageDOWN()
    time.sleep(0.5)

    #Select MBWAY payment method
    payment_method_mbway = driver.find_element_by_xpath("/html/body/div[4]/main/div[2]/div/div[3]/div[3]/ol/li[3]/div/form/fieldset/div[2]/div/div/div[6]/div[1]/input").click()

    #Type MBWAY phone number
    phone_nr_element=driver.find_element_by_id("skrey_sibs_mbway_soap_phonenumber")
    phone_nr_element.send_keys(phone_nr)

    #Check MWBWAY terms and conditions check box 
    driver.find_element_by_id("agreement_skrey_sibs_mbway_soap_1").click()

    #Click checkout button (Checkout_button) - COMMENTED FOR SAFETY REASONS - UNCOMMENT IF YOU'RE SURE YOU WANNA BUY THE PRODUCT
    #Checkout_button = driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div/div[3]/div[3]/ol/li[3]/div/form/fieldset/div[2]/div/div/div[6]/div[2]/div[4]/div/button').click()

    #Order finished
        


