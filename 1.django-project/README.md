# Installation:

### 1. Install Python 3.8.5

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the migrations (create the database)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the server

```bash
python manage.py runserver
```

### 7. Open the browser and go to the following address

```bash
http://localhost:8000
```

- Will add docker support soon
