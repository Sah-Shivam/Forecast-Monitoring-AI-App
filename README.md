# 🌬️ UK Wind Power Forecast Monitoring & Analysis

A full-stack application for monitoring and analyzing UK wind power generation forecasts, with real-time data visualization and statistical analysis.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Analysis Results](#analysis-results)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project provides a comprehensive solution for monitoring wind power generation forecasts in the United Kingdom. It consists of three main components:

1. **Frontend Application**: Interactive dashboard for visualizing actual vs forecasted wind power generation
2. **Backend API**: Robust Flask service that fetches and processes data from Elexon BMRS APIs
3. **Jupyter Analysis**: In-depth statistical analysis of forecast errors and wind power reliability

## ✨ Features

### 📊 Interactive Dashboard
- Real-time visualization of actual vs forecasted wind power generation
- Adjustable forecast horizon (0-48 hours) with slider control
- Customizable date range selection
- Responsive design for both desktop and mobile
- Error metrics display (MAE, Median, P95, P99)

### 🔧 Backend API
- RESTful endpoints for forecast data
- Automatic data fetching from Elexon BMRS APIs
- Intelligent data processing and alignment
- Robust error handling and logging
- Rate limiting and caching for performance

### 📈 Statistical Analysis
- Forecast error distribution analysis
- Error variation by forecast horizon
- Time-of-day error patterns
- Reliability analysis (P50, P80, P90, P95)
- Recommendation for reliable wind power capacity

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Material-UI (MUI)** - Component library
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **date-fns** - Date manipulation

### Backend
- **Flask** - Web framework
- **Pandas** - Data processing
- **NumPy** - Numerical computations
- **Requests** - HTTP client
- **Python-dotenv** - Environment configuration

### Analysis
- **Jupyter Notebook** - Interactive analysis
- **Matplotlib/Seaborn** - Data visualization
- **Pandas/NumPy** - Data manipulation

## 📁 Project Structure

```
wind-power-forecast-app/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── ForecastChart.js
│   │   │   ├── HorizonSlider.js
│   │   │   └── TimeRangePicker.js
│   │   ├── services/            # API services
│   │   │   └── api.js
│   │   ├── App.js               # Main app component
│   │   └── index.js             # Entry point
│   ├── package.json
│   └── README.md
│
├── backend/                      # Flask backend API
│   ├── app.py                    # Main application
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables
│
├── analysis/                      # Jupyter notebooks
│   └── wind_power_analysis.ipynb  # Statistical analysis
│
├── .gitignore
└── README.md                      # Project documentation
```

## 🚀 Installation

### Prerequisites
- **Node.js** (v14 or higher)
- **Python** (3.11 or higher)
- **npm** or **yarn**
- **Git**

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/wind-power-forecast-app.git
cd wind-power-forecast-app
```

### Step 2: Backend Setup
```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run the backend server
python app.py
```

### Step 3: Frontend Setup
```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the React app
npm start
```

### Step 4: Jupyter Analysis (Optional)
```bash
# Navigate to analysis folder
cd analysis

# Install analysis dependencies
pip install jupyter pandas numpy matplotlib seaborn requests

# Launch Jupyter
jupyter notebook
```

## 📱 Usage

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

### Using the Dashboard
1. Select a date range using the date pickers
2. Adjust the forecast horizon slider (minimum hours before target time)
3. View the interactive chart showing:
   - 🔵 Blue line: Actual generation
   - 🟢 Green line: Forecasted generation
4. Check error metrics displayed above the chart

### API Endpoints
| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/health` | GET | Health check | None |
| `/api/data` | GET | Get forecast data | `start`, `end`, `horizon` |
| `/api/stats` | GET | Get error statistics | `start`, `end` |

## 📊 Analysis Results

The Jupyter notebook provides comprehensive analysis including:

### Key Findings
- **Mean Absolute Error (MAE)**: ~150-300 MW depending on horizon
- **Error increases** with forecast horizon (from ~100 MW at 4h to ~300 MW at 48h)
- **Time-of-day patterns**: Slightly higher errors during peak demand hours
- **Reliability metrics**:
  - P50 (Median): ~2,000 MW reliably available
  - P90: ~1,600 MW available 90% of the time
  - P95: ~1,400 MW available 95% of the time

### Final Recommendation
**Recommended reliable capacity: 1,600 MW (P90 value)**

This provides 90% confidence in availability while balancing reliability with capacity utilization.

## 🌐 Deployment

### Deploy Backend on Render/Heroku
1. Create a `Procfile` in the backend folder:
```
web: gunicorn app:app
```

2. Deploy to Render:
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`

### Deploy Frontend on Vercel
1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
cd frontend
vercel
```

3. Set environment variable:
```
REACT_APP_API_URL=https://your-backend-url.com
```

## 🔧 Environment Variables

### Backend (.env)
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
API_TIMEOUT=30
API_RETRIES=3
RATELIMIT_DEFAULT=100 per minute
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📝 API Documentation

### GET /api/data
Fetches forecast and actual generation data.

**Parameters:**
- `start` (string): Start date (YYYY-MM-DD)
- `end` (string): End date (YYYY-MM-DD)
- `horizon` (integer): Minimum forecast horizon in hours (0-48)

**Response:**
```json
{
  "success": true,
  "actuals": [
    {
      "time": "2024-01-01T00:00:00",
      "generation": 1234.56
    }
  ],
  "forecasts": [
    {
      "time": "2024-01-01T00:00:00",
      "generation": 1200.00,
      "publishTime": "2023-12-31T20:00:00",
      "horizon": 4.0
    }
  ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 👥 Authors

- Shivam Prasad Sah

## 📧 Contact



