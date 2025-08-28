# Travel Booking Application (Django)

A simple travel booking web application where users can register/login, browse travel options (Flight/Train/Bus), book tickets, and manage their bookings.

## ✨ Features
- Django auth: register, login, logout
- Profile update
- Travel options with filters (type, source, destination, date)
- Booking (seats check, price calc)
- My bookings (cancel supported)
- Bootstrap responsive UI
- Bonus: MySQL config via `.env`, validation, basic unit tests

## 🧰 Tech
- Django 4.x
- Bootstrap 5 (CDN)
- Optional MySQL (`mysqlclient`)
- `django-environ` for environment variables

## ⚙️ Setup (Local, SQLite by default)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run migrations and create superuser
python manage.py migrate
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Open http://127.0.0.1:8000/

### Login/Logout/Registration URLs
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/register/`

## 🗄️ Switch to MySQL (Optional)
Install MySQL server and create a database & user, then copy `.env.sample` to `.env` and update values:

```
DEBUG=True
SECRET_KEY=change-me
DB_ENGINE=mysql
DB_NAME=travel_db
DB_USER=travel_user
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
ALLOWED_HOSTS=127.0.0.1,localhost
```

Run:
```bash
python manage.py migrate
```

## 🧪 Run Tests
```bash
python manage.py test
```

## 🚀 Deploy (PythonAnywhere quick notes)
1. Push this project to GitHub.
2. On PythonAnywhere, create a new **Django** web app (manual config).
3. Pull your repo into `~/yourusername/travel_booking`.
4. In the virtualenv, `pip install -r requirements.txt`.
5. Set `DJANGO_SETTINGS_MODULE=travel_booking.settings`.
6. Add a **WSGI** path to `travel_booking/wsgi.py`.
7. In **Static files**, set URL `/static/` to the folder `travel_booking/static/` and run:
   ```bash
   python manage.py collectstatic --noinput
   ```
8. Add your domain to `ALLOWED_HOSTS` in `.env` and reload the app.

## 📦 Project Structure
```
travel_booking/
  bookings/                # app
  travel_booking/          # project settings
  templates/               # global templates
  static/                  # static assets (css)
  manage.py
```

---

Happy building! 🎉
