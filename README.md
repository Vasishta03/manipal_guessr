
python manage.py migrate
python manage.py seed_locations
python manage.py createsuperuser
python manage.py runserver

Go to **http://127.0.0.1:8000/admin/** and log in with the superuser you created.
Click on **Locations** and upload an image for each location.


## Adding Your Own Locations

### Via Admin Panel
1. Go to `/admin/game/location/add/`
2. Fill in name, description, latitude, longitude
3. Upload an image OR paste an image URL
4. Optionally add a hint
5. Save




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



## Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (zero config, swap to Postgres for production)
- **Maps**: OpenStreetMap via Leaflet.js (free, no API key needed)
- **No auth required**: sessions only

---
