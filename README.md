# Project Introduction
This is a website that allows users to upload a text file which includes a list of user account information to creat tons of accounts by batch.
After accounts creation, the users can login to check their groupmates.

# Azure demo
- App Sevice: https://createaccounts.azurewebsites.net

# Code layout

# Technology stack used
- Flask (https://plainenglish.io/blog/flask-crud-application-using-mvc-architecture)
- Python
- SQLite
- cloud service
    - App Service
- CICD
- 
# Required dependencies
- Python 3.9 libraries
    - List provided in [requirements.txt](https://github.com/CynthiaTu-SY/flask_create_batch_accounts/blob/main/requirements.txt)

# Issues encountered
## Features
- File type and file size validation
- Unit user and group in DB
- Pagination

## CICD
This repositry is connected with Azure App Service, once push to main branch, the update will be built and deploy to the web app.
