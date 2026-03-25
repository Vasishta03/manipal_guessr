# ManipalGuessr 📍

A campus location guessing game for MIT Manipal — built with Django.
No login required. Just drop a nickname and start guessing!

---

## Quick Start

### 1. Unzip and enter the folder
```bash
cd manipal_guessr
```

### 2. Run the setup script (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_locations
python manage.py createsuperuser
python manage.py runserver
```

### 3. Open the game
```
http://127.0.0.1:8000/
```

### 4. Add images (important!)
Go to **http://127.0.0.1:8000/admin/** and log in with the superuser you created.
Click on **Locations** and upload an image for each location.

---

## Adding Your Own Locations

### Via Admin Panel
1. Go to `/admin/game/location/add/`
2. Fill in name, description, latitude, longitude
3. Upload an image OR paste an image URL
4. Optionally add a hint
5. Save

### Via the seed command
Edit `game/management/commands/seed_locations.py` to add your locations, then run:
```bash
python manage.py seed_locations
```

### Adding images programmatically
You can set `image_url` to a public image URL instead of uploading a file.
This is useful when you have photos hosted elsewhere.

---

## Project Structure

```
manipal_guessr/
├── manage.py
├── requirements.txt
├── setup.sh
├── README.md
├── manipal_guessr/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── game/                    # Main app
│   ├── models.py            # Location, GameSession, GameRound
│   ├── views.py             # All game logic
│   ├── urls.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed_locations.py
├── templates/
│   ├── base.html
│   └── game/
│       ├── home.html        # Landing page
│       ├── round.html       # Main game screen
│       ├── result.html      # Final score page
│       ├── leaderboard.html
│       └── how_to_play.html
└── static/
    └── css/
        └── style.css
```

---

## Scoring

| Distance      | Score         |
|---------------|---------------|
| 0 m (perfect) | 5000 pts      |
| 100 m         | ~4500 pts     |
| 250 m         | ~3750 pts     |
| 500 m         | ~2500 pts     |
| 750 m         | ~1250 pts     |
| 1000 m+       | 0 pts         |

---

## Customization

- **Add locations**: via admin or `seed_locations.py`
- **Change map area**: edit `MANIPAL_BOUNDS` and `MANIPAL_CENTER` in `round.html`
- **Change scoring**: edit `calculate_score()` in `models.py`
- **Change rounds options**: edit the `rounds-selector` in `home.html`
- **Colors/style**: edit `static/css/style.css` (uses CSS variables at the top)

---

## Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (zero config, swap to Postgres for production)
- **Maps**: OpenStreetMap via Leaflet.js (free, no API key needed)
- **No auth required**: sessions only

---

## Production Deployment

1. Set `DEBUG = False` in `settings.py`
2. Set a strong `SECRET_KEY`
3. Set `ALLOWED_HOSTS` to your domain
4. Run `python manage.py collectstatic`
5. Use gunicorn + nginx, or deploy to Railway/Render
