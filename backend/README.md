# HEcho - Discord-like Chat Application

A real-time chat application backend built with Django REST Framework, featuring servers, channels, direct messaging, and friend requests.

## Features

- 🔐 JWT Authentication
- 👥 User profiles with avatars and banners
- 🤝 Friend request system
- 🏢 Servers (public and private)
- 📢 Text channels within servers
- 💬 Direct messaging (DMs)
- 🔗 Server invite links
- 📎 File uploads (images, documents, videos, audio)

## Tech Stack

- **Backend:** Django 6.0, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (SimpleJWT)
- **Media Storage:** Local file system (configurable for cloud storage)

## Project Structure

```
backend/
├── accounts/       # User authentication, friend requests
├── servers/        # Server management, invites
├── channels/       # Text channels within servers
├── chat/           # Messages (DM and channel)
└── backend/        # Main Django settings
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/HEcho.git
   cd HEcho/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual database credentials
   # DO NOT commit this file!
   ```

6. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE your_database_name;
   ```

7. **Run migrations**
   ```bash
   python manage.py migrate
   ```

8. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/acc/signup/` - User registration
- `POST /api/acc/login/` - User login (returns JWT tokens)
- `POST /api/acc/logout/` - User logout (blacklist token)

### Friends
- `GET /api/acc/friends/` - List accepted friends
- `GET /api/acc/friends/incoming/` - Incoming friend requests
- `GET /api/acc/friends/outgoing/` - Outgoing friend requests
- `POST /api/acc/friends/send/` - Send friend request
- `PATCH /api/acc/friends/accept/<uid>/` - Accept friend request
- `PATCH /api/acc/friends/reject/<uid>/` - Reject friend request

### Servers
- `GET /api/server/` - List user's servers
- `POST /api/server/` - Create a new server
- `GET /api/server/search/?q=query` - Search public servers
- `POST /api/server/join/<uid>/` - Join public server by UID
- `POST /api/server/invite/<code>/` - Join server by invite code

## Environment Variables

Create a `.env` file in the backend directory with:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

**⚠️ NEVER commit the `.env` file to Git!**

## Models Overview

### User (accounts)
- Custom user model with UUID, avatar, banner, display name
- Phone number validation with country code

### FriendRequest (accounts)
- Status: PENDING, ACCEPTED, REJECTED
- Unique constraint on user pairs

### Server (servers)
- Public/private servers
- Server icons and descriptions
- Owner relationship

### ServerMember (servers)
- Roles: owner, admin, member
- Unique user per server

### Channel (channels)
- Text channels (voice coming soon)
- Unique names per server

### Message (chat)
- Supports: text, images, documents, videos, audio
- Links to either channels or DM threads

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

Harshith Chegondi

Project Link: [https://github.com/HarshithCheg/HEcho](https://github.com/HarshithCheg/HEcho)
