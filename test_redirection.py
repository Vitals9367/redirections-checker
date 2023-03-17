# Script compares if both servers have same path redirections 
import requests

HELFI_HOST="https://www.hel.fi"
PROXY_HOST="https://seo-redirector-dev.agw.arodevtest.hel.fi"

file1 = open('paths.txt', 'r')
PATHS = file1.readlines()
  
for path in PATHS:
    path.strip()
    
    helfi_request = requests.get(HELFI_HOST+path)
    proxy_request = requests.get(PROXY_HOST+path)
    
    if helfi_request.url != proxy_request.url:
        text = f"""{'-'*40} \nRedirection mismatch \nSOURCE = {path}\nHelfi redirected to = {helfi_request.url}\nproxy redirected to = {proxy_request.url}\n{'-'*40}\n"""
        print(text)