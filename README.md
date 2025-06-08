# Room Scheduler

A comprehensive system for managing classroom schedules in educational institutions. Enables efficient planning and viewing of class schedules, room management, and group organization.

## Features

- 📅 Schedule viewing by various parameters:
  - By groups
  - By classrooms
  - By teachers
  - By subjects
- 🔍 Advanced search filters:
  - Filter by subgroups
  - Filter by week type (numerator/denominator)
  - Filter by day of week
  - Filter by class number
- 📊 Free classroom schedule display
- 🔄 Automatic data updates
- 💾 Caching and query optimization

## Tech Stack

### Frontend
- Vue.js 3
- TypeScript
- Axios for HTTP requests
- Optimized caching system
- Local storage for data persistence

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── filters/         # Filter components
│   │   ├── features/        # Main components
│   │   └── common/          # Common components
│   ├── services/           # API services
│   ├── utils/              # Utilities
│   ├── types/              # TypeScript types
│   └── constants/          # Constants
└── public/                 # Static files

backend/
├── app/
│   ├── api/               # API endpoints
│   ├── models/           # Data models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
└── tests/                # Tests
```

## Installation and Setup

### Frontend

```bash
# Install dependencies
cd frontend/shedule
npm install

# Run in development mode
npm run dev

# Build for production
npm run build
```

### Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate     # for Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload or python main.py
```

## Optimization

The project includes several levels of optimization:

1. **Caching**:
   - In-memory cache for fast data access
   - Automatic cache updates
   - Local storage for session persistence

2. **Query Optimization**:
   - Debounce for search queries
   - API result caching
   - Optimized SQL queries

3. **UI/UX**:
   - Responsive design
   - Intuitive interface
   - Fast system response

## Development

### Component Structure

- **FilterGroup**: Group filtering
- **FilterSubject**: Subject filtering
- **FilterTeacher**: Teacher filtering
- **FilterRoom**: Room filtering
- **ScheduleFilters**: Main filter component
- **ScheduleTable**: Schedule display
- **ScheduleForm**: Creation/editing form

### Services

- **groupService**: Group management
- **subjectService**: Subject management
- **teacherService**: Teacher management
- **roomService**: Room management
- **scheduleService**: Schedule management

## API Documentation

The API documentation is available at `/docs` when running the backend server. It provides detailed information about all available endpoints, request/response formats, and authentication requirements.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT

## Authors

- Shevik(Maks Shevchuk)

## Contact

- Email: maksshevchuk621@gmail.com
- GitHub: Shevik11
- Telegram: @shevik_11