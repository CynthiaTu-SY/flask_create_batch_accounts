# Project Introduction
This is a website that allows users to upload a text file which includes a list of user account info to creat tons of accounts by batch.
data provided by querying VirusTotal's public API for the scan report of the hashes. 

# Demo
- App Sevice: (Do NOT Test with this link) https://flask-webapp-virustotal-batch-search.azurewebsites.net/report

# Code layout

# Technology stack used
- Flask (https://plainenglish.io/blog/flask-crud-application-using-mvc-architecture)
- Python
- SQLite
- REST API
- cloud service
    - VM
    - App Service
    - Redis Cache
- CICD

# Required dependencies
- Python 3.9 libraries
    - List provided in [requirements.txt](https://github.com/CynthiaTu-SY/VirusTotal_Batch_Search/blob/3dbbbdd60d6c1303df942dbd5efd51ff308878e7/requirements.txt)
- Local Redis server
    -  Install Redis on Ubuntu/Macos (Terminal command)
        - sudo apt install Redis
        - sudo systemctl status Redis
    - Activate the Redis service
        -  rq worker
    -  Install Redis on Windows (Do not recomment, as I tried with failure)
        - Turoial can be found in https://www.youtube.com/watch?v=188Fy-oCw4w&t=266s
# Issues encountered
## Features
- File type and file size validation
- File content filtering which only capture the MD5 or SHA256
    - This is achieve by Regex
- Support duplicate file upload
    - To avoid the other user see the current users report, the website return UUID for user to check the report after the file is uploaded
    - In case user forget the UUID, the design allow user to upload a duplicate file to generate a new UUID but will not delay his/her report as API call will only happen with new hash cannot be found in database.
- Virus total API limit handling
    - Sleep 15 seconds to avoid the over limit
    - Use the redis retry configuration to add the failed hash request to the end of the queue which will not delay the new come in task 
## Task queue
This project uses local Redis server to handle the API call as a queue, so user can get the UUID code right after file upload and back to check the report progress any time. 
## CICD
This repositry is connected with Azure App Service, once push to main branch, the update will be built and deploy to the web app.
![image](https://user-images.githubusercontent.com/57238251/214493824-8bad8788-34cf-46ae-99de-8ba0b5752b1a.png)
