#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import random
from selenium.webdriver.support.ui import Select
import re
import time
from django.http import HttpResponse
import requests
import imaplib
import smtplib
import cPickle
import erp.HTML
import erp.settings
from django_geoip.models import IpRange

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
sender = 'bagggy@tut.by'
password = "71287128"
#sender = 'bagiraivan@tut.by'
#password = "1234qwer"
recipient = 'irinashumovskaya@googlegroups.com'
subject = 'New projects are in fixber.com'
message = 'New projects are in fixber.com!'

CURRENCY_CHOICES = (
            ('1','BYR'),
            ('2','USD'),
            ('3','EUR'),
            ('4','RUR'),
            )

TYPEOFWORK_CHOICES = (
            ('1',u'Тип работ 1'),
            ('2',u'Тип работ 2'),
            ('3',u'Тип работ 3'),
            ('4',u'Тип работ 4'),
            )

SPECIALISATION_CHOICES = (
            ('1','Специализация 1'),
            ('2','Специализация 2'),
            ('3','Специализация 3'),
            ('4','Специализация 4'),
            ('5','Специализация 5'),
            )

def get_city_by_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    city = ''
    try:
        geoip_record = IpRange.objects.by_ip(ip)
        if geoip_record.city:
            city = geoip_record.city
        else:
            if request.session['city']!='---':
                city = request.session['city']
    except:
        pass
    #temp conversion TODO: update django_geoip_iprange with data from Belarus cities
    if city=='Minsk':
        city = 'Минск'
    return city

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]



def testcomplete(request):
    driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT)
    try:
        driver.get("http://smartbear.com/products/qa-tools/automated-testing-tools/free-testcomplete-trial")
    except:
        #time.sleep(5)
        pass
    stamp = random.randint(100000,999999)
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_email").send_keys("test"+str(stamp)+"@mailforspam.com")
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_firstname").send_keys("test")
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_lastname").send_keys("test")
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_company").send_keys("test")
    Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_country")).select_by_visible_text("Belarus")
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_phonenumber").send_keys("1231423412")
    try:
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_submit").click()
    except:
        #time.sleep(5)
        pass
    try:
        driver.find_element_by_id("product-categories")
    except:
        #time.sleep(5)
        pass
    try:
        WebDriverWait(driver, 120).until(lambda driver: driver.get("http://mailforspam.com/mail/test"+str(stamp)) or EC.presence_of_element_located(driver.find_element_by_partial_link_text("TestComplete")))
    except:
        driver.quit()
        return HttpResponse("<h2>"+"No email delivered to http://mailforspam.com/mail/test"+str(stamp)+"</h2>")
    driver.find_element_by_partial_link_text("TestComplete").click()
    key = re.search("\d{15,25}",driver.find_element_by_id("messagebody").text).group()
    driver.quit()
    return HttpResponse("<h1>"+key+"</h1>")

def regexGetMatch(text, regexp):
    return re.search(regexp,text).group()

def testcomplete2(request):
    email = 'bagggy@tut.by'
    password = '71287128'
    delete_all_emails(email,password)
    try:
        url = 'http://smartbear.com/products/qa-tools/automated-testing-tools/free-testcomplete-trial'
        s = requests.Session()
        response1 =  s.get(url)
        text = response1.text
        __EVENTVALIDATION = re.match( r"[\S\s]+__EVENTVALIDATION\" value=\"(.*)\"", text).group(1)
        __VIEWSTATE = re.match( r"[\S\s]+__VIEWSTATE\" value=\"(.*)\"", text).group(1)
        parameters = {'__EVENTARGUMENT': '', '__EVENTTARGET': '', '__EVENTVALIDATION' : __EVENTVALIDATION, '__VIEWSTATE':__VIEWSTATE,'ctl00$ContentPlaceHolder1$KeywordSearch': '', 'ctl00$ContentPlaceHolder1$ReferringURL':'','ctl00$ContentPlaceHolder1$actSrc':'','ctl00$ContentPlaceHolder1$actSrcDet':'','ctl00$ContentPlaceHolder1$company':'bubukashko','ctl00$ContentPlaceHolder1$country':'Armenia','ctl00$ContentPlaceHolder1$email':email,'ctl00$ContentPlaceHolder1$firstname':'ivashko','ctl00$ContentPlaceHolder1$lastname':'bukashko','ctl00$ContentPlaceHolder1$mcity':'','ctl00$ContentPlaceHolder1$mcomp':'', 'ctl00$ContentPlaceHolder1$mcty':'', 'ctl00$ContentPlaceHolder1$mphone':'','ctl00$ContentPlaceHolder1$mst':'','ctl00$ContentPlaceHolder1$mtrade':'','ctl00$ContentPlaceHolder1$mzip':'','ctl00$ContentPlaceHolder1$phonenumber':'634563456','ctl00$ContentPlaceHolder1$province':'-1','ctl00$ContentPlaceHolder1$rfconf':'not found', 'ctl00$ContentPlaceHolder1$sfga':'00D700000008FQP','ctl00$ContentPlaceHolder1$state':'-1','ctl00$ContentPlaceHolder1$submit':'Sign Up Now', 'ctl00_manScript_HiddenField':'', 'lng':'en-US', 'sf_country_sandbox':''}
        o = s.post(url,data=parameters)

    except:
        return HttpResponse('error in request 1')
    try:
        key = wait_email(email,password)
        return HttpResponse("<h1>"+key+"</h1>")
    except:
        return HttpResponse('error in imap procesing')
    return HttpResponse('ok')

def delete_all_emails(email,password):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email, password)
        #list = mail.list()
        mail.select("INBOX")
        result, data = mail.search(None, "ALL")
        for num in data[0].split():
            mail.store(num, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.close()
        mail.logout()

def wait_email(email,password):
        key = None
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email, password)
        #list = mail.list()
        for i in range(1,120,1):
            mail.select("INBOX")
            result, data = mail.search(None, "ALL")
            ids = data[0] # data is a list.
            id_list = ids.split() # ids is a space separated string
            if id_list:
                latest_email_id = id_list[-1] # get the latest
                result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
                raw_email = data[0][1]
                key = re.search("Key:\s(\d{15,25})",raw_email).group(1)
            if key:
                break
            time.sleep(1)
        mail.close()
        mail.logout()
        return key

def fixber(request):
    login = 'robotbuggy'
    password = '6Tcle7'
    projects = []
    new_projects = []
    try:
        projects = cPickle.load(open(erp.settings.PROJECT_PATH+'/projects.p', 'rb'))
    except:
        pass
    try:
        url = 'http://fixber.com/login'
        s = requests.Session()
        response1 =  s.get(url)
        text = response1.text
        md5page = re.match( r"[\S\s]+md5page\" value=\"(.*)\"", text).group(1)
        parameters = {'action': 'create','btn.x': '64', 'btn.y': '16', 'login': login, 'md5page': md5page, 'passw': password}
        response2 = s.post(url,data=parameters)
        text = response2.text
        new_projects = re.findall(r".*<a href=\"http://fixber.com/tester/project/(\d{3,5})\" title=\"(.*)\"", text)
        differences = []
        #compare
        for p in new_projects:
            if not(p in projects):
                differences+=p
        if differences:
            cPickle.dump(new_projects, open(erp.settings.PROJECT_PATH+'/projects.p', 'wb'))
            send_email(HTML.list(new_projects))
            return HttpResponse('request OK. There are some changes in project list!')
    except:
        cPickle.dump(new_projects, open(erp.settings.PROJECT_PATH+'/projects.p', 'wb'))
        #debug
        send_email("error in request",sender)
        return HttpResponse('error in request')
    #debug
    #send_email("request OK. No changes in project list.",sender)
    return HttpResponse('request OK. No changes in project list.')

def litecoins(request,count):
    response_text = "<table border='3' cellpadding='6'><tr><td>URL</td><td>Status</td><td>Working</td></tr>"
    for i in range(int(count,0)):
        for j in range(5):
            is_ok = "<font color='red'>Failed</font>"
            is_work = "<font color='red'>Not working</font>"
            is_ok2 = "<font color='red'>Failed</font>"
            is_work2 = "<font color='red'>Not working</font>"
            url = ''
            url2 = ''
            try:
                global url
                global is_ok,is_ok2
                global is_work,is_work2
                url = 'http://jvitaut%s.jvitaut%s.cloudbees.net/'%(j+1,i+1)
                url2 = 'http://jalgerd%s.jalgerd%s.cloudbees.net/'%(j+1,i+1)
                s = requests.Session()
                response1 =  s.get(url)
                response2 =  s.get(url2)
                text = response1.text
                text2 = response2.text
                if '[201' in text:
                    is_ok = "<font color='green'>OK</font>"
                if 'khash/s' in text:
                    is_work = "<font color='green'>Working...</font>"
                if '[201' in text2:
                    is_ok2 = "<font color='green'>OK</font>"
                if 'khash/s' in text2:
                    is_work2 = "<font color='green'>Working...</font>"
            except:
                is_ok = "<font color='red'>Failed</font>"
                is_ok2 = "<font color='red'>Failed</font>"
            response_text += "<tr><td><a href='"+url+"'>"+url+"</a></td>"+"<td>"+is_ok+"</td><td>"+is_work+"</td><tr>"
            response_text += "<tr><td><a href='"+url2+"'>"+url2+"</a></td>"+"<td>"+is_ok2+"</td><td>"+is_work2+"</td><tr>"
    response_text += "</table>"
    return HttpResponse(response_text)

def send_email(body,r=recipient):
    body = "" + body + ""

    headers = ["From: " + "Багира Ивановна",
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)

    session.sendmail(sender, r, headers + "\r\n\r\n" + body)
    session.quit()