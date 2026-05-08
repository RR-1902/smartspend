# Smart Expense Tracker

Smart Expense Tracker is a polished, mobile-first Django fintech web app for tracking daily spending, visualizing expense patterns, exporting reports, and encouraging saving habits with a playful mascot-based gamification system.

The product direction is inspired by modern mobile finance apps and habit-building products: soft gradients, rounded cards, smooth motion, compact charts, dark/light mode, and a friendly mascot that appears during important user moments.

## Features

- Splash screen with animated mascot branding
- Three-step onboarding flow
- Login and signup screens with modern form styling
- Premium dashboard with total spending, savings, streaks, XP, recent expenses, and analytics preview
- Expense CRUD for adding, editing, and deleting transactions
- Smart category prediction in the add/edit expense form
- Animated AI suggestion chip for keywords such as `pizza`, `uber`, and `netflix`
- Analytics page with Chart.js donut, pie, line, and bar graphs
- Gamification page with XP points, saver level, streaks, achievements, and savings goal progress
- Reports page with CSV and PDF export
- Profile page with savings settings and dark mode preference
- Responsive sidebar and mobile bottom navigation
- Black and blue gradient dark mode with light text
- Montserrat typography across the UI
- SVG mascot and illustration assets

## Tech Stack

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Chart.js
- GSAP
- AOS
- ReportLab
- Lucide icons

## Project Structure

```text
expense_tracker/
  settings.py
  urls.py
  asgi.py
  wsgi.py

tracker/
  admin.py
  apps.py
  forms.py
  models.py
  signals.py
  urls.py
  views.py
  migrations/

templates/
  base.html
  splash.html
  onboarding.html
  login.html
  signup.html
  dashboard.html
  expenses.html
  expense_form.html
  analytics.html
  gamification.html
  reports.html
  profile.html
  partials/

static/
  css/
  js/
  svg/
  images/
  animations/
```

## How It Works

The Django project is split into a core project package called `expense_tracker` and one app called `tracker`.

`expense_tracker/settings.py` configures Django, SQLite, static files, authentication redirects, templates, and installed apps.

`expense_tracker/urls.py` sends all application routes to `tracker.urls`.

`tracker/models.py` defines the database layer:

- `Expense` stores the user's title, amount, category, date, notes, and timestamps.
- `UserProfile` stores the user's budget, savings goal, current savings, XP, streak, level, and dark mode preference.
- `Achievement` stores gamified badges connected to a profile.

`tracker/forms.py` defines reusable Django forms for signup, login, expense editing, and profile editing. The form mixin applies the shared modern input class so form styling stays consistent.

`tracker/views.py` contains the page logic:

- Public pages render the splash and onboarding screens.
- Signup creates a user, ensures the profile exists, seeds demo expenses, and logs the user in.
- Dashboard calculates monthly spending, budget progress, recent transactions, and chart payloads.
- Expense views support add, edit, delete, and listing.
- Analytics builds reusable Chart.js data from grouped expenses.
- Reports export the current user's expenses to CSV and PDF.
- Profile updates money settings and theme preference.

`tracker/signals.py` creates a profile and starter achievements whenever a new Django user is created.

`templates/base.html` is the main layout. It loads fonts, Bootstrap, Chart.js, GSAP, AOS, Lucide icons, the global CSS, and the global JavaScript. Authenticated users receive the sidebar, topbar, mobile navigation, toast messages, and mascot celebration overlay.

`static/css/styles.css` contains the design system: color tokens, light and dark themes, responsive layout, cards, buttons, dashboard grids, charts, forms, navigation, mascot animations, and mobile rules.

`static/js/app.js` controls the interactive layer:

- Initializes AOS and Lucide icons
- Animates dashboard counters
- Renders Chart.js charts
- Updates chart colors when theme changes
- Stores dark/light mode in `localStorage`
- Predicts expense categories from typed keywords
- Triggers mascot animation before expense form submission

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/
```

## Demo Account

You can create a new account from the signup page. New users automatically receive starter achievements and demo expenses so the dashboard and charts look complete immediately.

During local verification, this demo account was used:

```text
Username: demo
Password: DemoPass123!
```

## Smart Category Prediction

The frontend checks the expense title as the user types and suggests a category.

Examples:

```text
pizza -> Food
uber -> Travel
netflix -> Entertainment
```

When a match is found, the AI suggestion chip animates and the category select field updates automatically.

## Reports

The reports page provides two export formats:

- CSV through Django's `csv` module
- PDF through ReportLab

Both exports are scoped to the currently logged-in user.

## Verification

The app was verified with:

```powershell
python manage.py check
```

Browser verification covered:

- Splash page
- Login flow
- Dashboard layout
- Desktop dashboard
- Tablet dashboard
- Mobile dashboard
- Dark mode dashboard
- Analytics preview
- Expense mascot and AI category suggestion
- CSV export
- PDF export

Final dashboard verification result:

```text
DASHBOARD_VERIFIED_PERFECT
```
