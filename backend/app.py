from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
CORS(app)

class WindDataFetcher:
    def __init__(self):
        # Correct API endpoints
        self.actuals_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH/stream"
        self.forecast_url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR/stream"
        
    def fetch_actuals(self, start_date, end_date):
        """Fetch actual wind generation data"""
        try:
            # For FUELHH, use settlementDate parameters (not publishDateTime)
            params = {
                'settlementDateFrom': start_date,
                'settlementDateTo': end_date,
                'fuelType': 'WIND'
            }
            
            print(f"Fetching actuals from: {self.actuals_url}")
            print(f"With params: {params}")
            
            response = requests.get(self.actuals_url, params=params, timeout=30)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Received {len(data) if isinstance(data, list) else 'non-list'} records")
                    
                    if isinstance(data, list):
                        # Filter for WIND fuel type (though we already requested it)
                        wind_data = [item for item in data if item.get('fuelType') == 'WIND']
                        if wind_data:
                            df = pd.DataFrame(wind_data)
                            print(f"Created DataFrame with {len(df)} rows")
                            return df
                        else:
                            print("No WIND data found in response")
                    else:
                        print(f"Unexpected data format: {type(data)}")
                        
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Response text: {response.text[:200]}")
            else:
                print(f"Error response: {response.text[:200]}")
                
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching actuals: {e}")
            return pd.DataFrame()
    
    def fetch_forecasts(self, start_date, end_date):
        """Fetch forecast data"""
        try:
            # For WINDFOR, use publishDateTime parameters
            params = {
                'publishDateTimeFrom': f"{start_date}T00:00:00Z",
                'publishDateTimeTo': f"{end_date}T23:59:59Z"
            }
            
            print(f"Fetching forecasts from: {self.forecast_url}")
            print(f"With params: {params}")
            
            response = requests.get(self.forecast_url, params=params, timeout=30)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Received {len(data) if isinstance(data, list) else 'non-list'} records")
                    
                    if isinstance(data, list):
                        if data:
                            df = pd.DataFrame(data)
                            print(f"Created DataFrame with {len(df)} rows")
                            return df
                        else:
                            print("Empty forecast data received")
                    else:
                        print(f"Unexpected data format: {type(data)}")
                        
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Response text: {response.text[:200]}")
            else:
                print(f"Error response: {response.text[:200]}")
                
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching forecasts: {e}")
            return pd.DataFrame()
    
    def process_data(self, actuals_df, forecasts_df, horizon_hours):
        """Process and align actuals with forecasts based on horizon"""
        if actuals_df.empty:
            print("No actuals data to process")
            return [], []
        
        if forecasts_df.empty:
            print("No forecasts data to process")
            # Return actuals without forecasts for partial data
            result_actuals = []
            for _, row in actuals_df.iterrows():
                result_actuals.append({
                    'time': row['startTime'],
                    'generation': float(row['generation']) if pd.notna(row['generation']) else 0
                })
            return result_actuals, []
        
        # Convert timestamps
        actuals_df['startTime'] = pd.to_datetime(actuals_df['startTime'])
        forecasts_df['startTime'] = pd.to_datetime(forecasts_df['startTime'])
        forecasts_df['publishTime'] = pd.to_datetime(forecasts_df['publishTime'])
        
        # Filter for January 2024
        jan_start = '2024-01-01'
        jan_end = '2024-01-31'
        actuals_df = actuals_df[(actuals_df['startTime'] >= jan_start) & 
                                (actuals_df['startTime'] <= jan_end)]
        
        if not forecasts_df.empty:
            forecasts_df = forecasts_df[(forecasts_df['startTime'] >= jan_start) & 
                                       (forecasts_df['startTime'] <= jan_end)]
        
        print(f"Processing {len(actuals_df)} actuals and {len(forecasts_df)} forecasts")
        
        # Process each target time
        result_actuals = []
        result_forecasts = []
        
        for target_time in actuals_df['startTime'].unique():
            target_actual = actuals_df[actuals_df['startTime'] == target_time]
            if not target_actual.empty:
                actual_value = float(target_actual.iloc[0]['generation']) if pd.notna(target_actual.iloc[0]['generation']) else 0
                
                result_actuals.append({
                    'time': target_time.isoformat(),
                    'generation': actual_value
                })
                
                # Get forecasts for this target time if available
                if not forecasts_df.empty:
                    target_forecasts = forecasts_df[forecasts_df['startTime'] == target_time].copy()
                    
                    if not target_forecasts.empty:
                        # Calculate forecast horizon
                        target_forecasts['horizon'] = (target_time - target_forecasts['publishTime']).dt.total_seconds() / 3600
                        
                        # Filter for 0-48 hours horizon
                        valid_forecasts = target_forecasts[(target_forecasts['horizon'] >= 0) & 
                                                          (target_forecasts['horizon'] <= 48)]
                        
                        if not valid_forecasts.empty:
                            # Get latest forecast created at least horizon_hours before target
                            latest_before = valid_forecasts[valid_forecasts['horizon'] >= horizon_hours]
                            if not latest_before.empty:
                                latest_forecast = latest_before.loc[latest_before['publishTime'].idxmax()]
                                
                                result_forecasts.append({
                                    'time': target_time.isoformat(),
                                    'generation': float(latest_forecast['generation']) if pd.notna(latest_forecast['generation']) else 0,
                                    'publishTime': latest_forecast['publishTime'].isoformat(),
                                    'horizon': float(latest_forecast['horizon'])
                                })
        
        print(f"Returning {len(result_actuals)} actuals and {len(result_forecasts)} forecasts")
        return result_actuals, result_forecasts

data_fetcher = WindDataFetcher()

@app.route('/api/data', methods=['GET'])
def get_data():
    """API endpoint to get forecast and actual data"""
    try:
        start_date = request.args.get('start', '2024-01-01')
        end_date = request.args.get('end', '2024-01-07')
        horizon = int(request.args.get('horizon', 4))
        
        print(f"\n=== API Request ===")
        print(f"Start: {start_date}, End: {end_date}, Horizon: {horizon}")
        
        # Fetch data
        actuals_df = data_fetcher.fetch_actuals(start_date, end_date)
        forecasts_df = data_fetcher.fetch_forecasts(start_date, end_date)
        
        # Process data
        actuals, forecasts = data_fetcher.process_data(actuals_df, forecasts_df, horizon)
        
        response_data = {
            'success': True,
            'actuals': actuals,
            'forecasts': forecasts
        }
        
        print(f"Response: {len(actuals)} actuals, {len(forecasts)} forecasts")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in get_data: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistical analysis of forecast errors"""
    try:
        start_date = request.args.get('start', '2024-01-01')
        end_date = request.args.get('end', '2024-01-31')
        
        actuals_df = data_fetcher.fetch_actuals(start_date, end_date)
        forecasts_df = data_fetcher.fetch_forecasts(start_date, end_date)
        
        errors_by_horizon = []
        
        for horizon in range(1, 49):
            actuals, forecasts = data_fetcher.process_data(actuals_df, forecasts_df, horizon)
            if actuals and forecasts:
                errors = [abs(a['generation'] - f['generation']) 
                         for a, f in zip(actuals, forecasts)]
                if errors:
                    errors_by_horizon.append({
                        'horizon': horizon,
                        'mean_error': float(np.mean(errors)),
                        'median_error': float(np.median(errors)),
                        'p95_error': float(np.percentile(errors, 95)),
                        'p99_error': float(np.percentile(errors, 99))
                    })
        
        return jsonify({
            'success': True,
            'errors_by_horizon': errors_by_horizon
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Wind Power Forecast API is running'
    })

if __name__ == '__main__':
    print("Starting Wind Power Forecast API...")
    print("Server will run on http://localhost:5000")
    print("Endpoints:")
    print("  - GET /api/health")
    print("  - GET /api/data?start=2024-01-01&end=2024-01-07&horizon=4")
    print("  - GET /api/stats?start=2024-01-01&end=2024-01-31")
    app.run(debug=True, port=5000)