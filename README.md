# FLASK BLOG

A simple blog application that it was built with Flask , featuring user authentication , database managment and post create/delete/update methods 

## Features 
- User registration and authentication 
- Create, edit & delete blog posts 
- Store data in an SQL Database using sqlalchemy
- Secure enviroment variable managment 

# SETUP & INSTALLATION
1. **Clone Repository**
```bash
git clone Blog_Site
cd flask_blog 
```
2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate # On windows use 'venv\Scripts\activate'
```
3. **Install Dependecies**
```bash
pip install -r requirements.txt 
```
4. **Set up enviroment variables**
```bash
SECRET_KEY = 'your_secret_key'
DATABASE_URL = 'sqlite:///instance/site.db'
```
5. **Run Application**
```bash
flask run
```
6. **Open in the browser**



