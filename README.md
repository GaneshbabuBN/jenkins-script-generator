# 🚀 Jenkins Script Generator

A Dockerized, Flask-based web application that automates the creation of Jenkins Freestyle job shell scripts through an intuitive web interface.

Instead of manually writing repetitive deployment scripts for every project, users can enter project configurations — such as the GitHub repository URL, Docker image name, container name, and application port — and instantly generate reusable Jenkins build scripts.

All generated scripts are stored and tracked using PostgreSQL, providing centralized history management and easy access to previously generated deployment scripts.

---

## 📷 Screenshots

The application interface and workflow screenshots are available below:

```
screenshots/
│
├── Home-Landing page.png
├── Validation Error Example.png
├── Input Form Filled.png
├── Generated Jenkins Script Output.png
├── Success-Script Generation Result View.png
├── Script History Page.png
├── Clear History Action State.png
└── History Cleared Successfully.png
```

### 🏠 Home Landing Page

![Home Landing Page](screenshots/Home-Landing%20page.png)

### ❌ Validation Error Example

![Validation Error Example](screenshots/Validation%20Error%20Example.png)

### 📝 Input Form Filled

![Input Form Filled](screenshots/Input%20Form%20Filled.png)

### ⚙️ Generated Jenkins Script Output

![Generated Jenkins Script Output](screenshots/Generated%20Jenkins%20Script%20Output.png)

### ✅ Script Generation Success View

![Success Script Generation Result View](screenshots/Success-Script%20Generation%20Result%20View.png)

### 📜 Script History Dashboard

![Script History Page](screenshots/Script%20History%20Page.png)

### 🗑️ Clear History Action

![Clear History Action State](screenshots/Clear%20History%20Action%20State.png)

### ✅ History Cleared Successfully

![History Cleared Successfully](screenshots/History%20Cleared%20Successfully.png)

---

# 🎯 Project Objectives

- **Automate Scripting:**  
  Eliminate manual errors by automatically generating Jenkins Freestyle shell scripts.

- **Input Validation:**  
  Validate project inputs, including GitHub repository URLs, before script generation.

- **Persistent Tracking:**  
  Store generated scripts using SQLAlchemy ORM with PostgreSQL for history management.

- **Template Exporting:**  
  Allow users to download generated scripts as `.sh` and `.txt` files.

- **Modern Architecture:**  
  Demonstrate practical Flask backend development with a responsive Bootstrap frontend.

---

# 🛠️ Technologies Used

## Backend
- Python
- Flask
- SQLAlchemy
- Gunicorn / Waitress

## Frontend
- HTML5
- Bootstrap 5
- Jinja2
- JavaScript

## Database
- PostgreSQL

---

# 🏗️ Architecture Diagram

```
                        +----------------------+
                        |     User Browser     |
                        +----------+-----------+
                                   |
                                   | HTTP Request
                                   v
                     +-----------------------------+
                     |      Flask Web Application  |
                     |                             |
                     |  - Form Validation          |
                     |  - Script Generator         |
                     |  - History Management       |
                     +------+--------------+-------+
                            |              |
                            |              |
                            v              v
              +-------------------+  +-------------------+
              | Script Generator  |  | SQLAlchemy ORM    |
              +---------+---------+  +---------+---------+
                        |                       |
                        |                       |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------------------+
                        |     PostgreSQL DB     |
                        |    Script History     |
                        +-----------------------+
                                    |
                                    v
                       Generated Jenkins Shell Script
```

---

# 📁 Project Structure

```
jenkins-script-generator/
│
├── screenshots/
│   ├── Clear History Action State.png
│   ├── Generated Jenkins Script Output.png
│   ├── History Cleared Successfully.png
│   ├── Home-Landing page.png
│   ├── Input Form Filled.png
│   ├── Script History Page.png
│   ├── Success-Script Generation Result View.png
│   └── Validation Error Example.png
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── history.html
│   └── index.html
│
├── .env
├── .gitignore
├── app.py
├── config.py
├── models.py
├── README.md
├── requirements.txt
├── run.py
└── script_generator.py
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/<username>/jenkins-script-generator.git

cd jenkins-script-generator
```

---

## 2. Create and Activate Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```ini
SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=jenkins_script_generator
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## 5. Create PostgreSQL Database

Login to PostgreSQL and create the database:

```sql
CREATE DATABASE jenkins_script_generator;
```

---

# ▶️ Running the Application

## Development Mode

```bash
python app.py
```

## Production Mode

```bash
python run.py
```

Application will be available at:

```
http://localhost:5000
```

---

# 🖥️ Application Pages

## 🏠 Home Page
- Project configuration form
- GitHub repository validation
- Docker configuration inputs
- Jenkins script generation

## 📜 Generated Script Page
- Displays generated Jenkins shell script
- Provides download options
- Supports `.sh` and `.txt` exports

## 🗂️ History Dashboard
- View previously generated scripts
- Download historical scripts
- Delete individual records
- Clear complete history

---

# 🔄 Generated Jenkins Script Workflow

```
User Input Configuration
            |
            ▼
Validate Project Details
(GitHub URL Verification)
            |
            ▼
Generate Jenkins Shell Script
            |
            ▼
Save Record to PostgreSQL Database
            |
            ├──► Download Template (.sh / .txt)
            |
            ▼
View Central History Log
```

---

# 📝 Sample Generated Script Preview

```bash
#!/bin/bash
# Auto-generated by Jenkins Script Generator

IMAGE_NAME="my-app:latest"
CONTAINER_NAME="my-app-container"
PORT="8080"

echo "Stopping existing container..."

docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

echo "Building new Docker image..."

docker build -t $IMAGE_NAME .

echo "Running container on port $PORT..."

docker run -d --name $CONTAINER_NAME -p $PORT:$PORT $IMAGE_NAME
```

---

# 🚀 Features & Highlights

✅ Automated Jenkins Freestyle shell script generation  
✅ GitHub repository validation  
✅ PostgreSQL-backed script history tracking  
✅ SQLAlchemy ORM integration  
✅ One-click `.sh` and `.txt` downloads  
✅ Responsive Bootstrap UI  
✅ Dockerized application architecture  
✅ Lightweight resource usage  

---

# 🔮 Future Enhancements

- [ ] Implement secure user authentication
- [ ] Export Jenkins configurations as YAML and Jenkins Job XML
- [ ] Add advanced search, sorting, and filtering
- [ ] Implement optional Dark Mode UI
- [ ] Support CI/CD pipeline templates

---

# 📄 License

This project is open-source and free to use for educational and production automation purposes.
