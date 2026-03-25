#!/bin/bash
# ManipalGuessr Setup Script
# Run this once after unzipping the project

set -e

echo "========================================"
echo "  ManipalGuessr Setup"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created."
echo ""

# Activate and install
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed."
echo ""

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate
echo "✅ Database ready."
echo ""

# Seed locations
echo "📍 Seeding sample Manipal locations..."
python manage.py seed_locations
echo ""

# Create superuser prompt
echo "👤 Create an admin account (for adding location images):"
python manage.py createsuperuser
echo ""

echo "========================================"
echo "  ✅ Setup complete!"
echo ""
echo "  To start the server:"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Then open: http://127.0.0.1:8000/"
echo "  Admin panel: http://127.0.0.1:8000/admin/"
echo ""
echo "  📸 Add location images via the admin panel!"
echo "========================================"
