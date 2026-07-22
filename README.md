# Delivery Chatbot

A simple web-based support chatbot for delivery issues. Customers can raise a ticket for a problem with their order (missing item, wrong order, late delivery, damaged item), optionally attach a photo, and track the ticket's status. An admin dashboard lets support staff review tickets and resolve them with a refund decision.

## Features

- **Chat-style support widget** — customers pick an issue type, enter their order ID, and optionally upload an image of the problem.
- **Ticket creation & tracking** — every submission creates a ticket (`TKT######`) that customers can look up later on the tracking page.
- **Admin dashboard** — password-protected view that groups tickets by order/issue and shows the latest status.
- **Ticket resolution** — admins can mark a ticket resolved as a full refund, partial refund (with amount), or no refund, along with a resolution note.
- **Image uploads** — attached images are stored on disk and served back for the ticket detail view.

## Tech stack

- **Backend:** Python, Flask
- **Database:** SQLite (`tickets.db`)
- **Frontend:** Jinja2 templates, vanilla HTML/CSS/JS

## Project structure

```
delivery_chatbot/
└── backend/
    ├── app.py                  # Flask app, routes for pages
    ├── config.py                # Admin credentials (hashed)
    ├── database.py               # SQLite connection + schema setup
    ├── models/
    │   └── tickets_models.py
    ├── routes/
    │   ├── ticket_routes.py      # Create/get/resolve tickets, grouped ticket list
    │   └── auth_routes.py        # Admin login/logout
    ├── static/
    │   ├── css/style.css
    │   └── js/                   # script.js, auth.js, admin.js, track.js
    ├── templates/
    │   ├── index.html            # Chat widget / home page
    │   ├── track.html            # Ticket tracking page
    │   ├── details.html          # Single ticket detail page
    │   ├── admin_login.html
    │   └── admin.html            # Admin dashboard
    └── uploads/                  # Uploaded ticket images
```

## Getting started

### Prerequisites
- Python 3.9+

### Installation

```bash
git clone https://github.com/yshaayan-hue/delivery_chatbot.git
cd delivery_chatbot
pip install flask
```

### Running the app

```bash
python -m backend.app
```

The app will start in debug mode and be available at `http://127.0.0.1:5000`.

- `/` — chat/support widget for raising a ticket
- `/track` — look up a ticket by ID
- `/admin` — admin login (default password: `admin123`)
- `/admin/dashboard` — grouped ticket list and resolution tools (admin only)

## API endpoints

| Method | Endpoint                     | Description                              |
|--------|-------------------------------|-------------------------------------------|
| POST   | `/api/tickets`                | Create a new ticket (issue, order_id, optional image) |
| GET    | `/api/ticket/<ticket_id>`     | Get a single ticket's details             |
| GET    | `/api/grouped-tickets`        | List tickets grouped by order/issue (admin only) |
| POST   | `/api/resolve/<ticket_id>`    | Resolve a ticket with a refund decision (admin only) |
| POST   | `/api/auth/login`             | Admin login                               |
| POST   | `/api/auth/logout`            | Admin logout                              |

## Notes

- The admin password and Flask session secret are currently hardcoded in `config.py` / `app.py` for development — swap these for environment variables before deploying anywhere public.
- `tickets.db` is created automatically on first run if it doesn't already exist.

## License

No license specified yet.
