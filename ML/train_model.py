from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import joblib

class AirQualityPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        
    def create_health_risk_features(self, df):
        """
        Create composite health risk scores
        """
        # WHO Guidelines thresholds
        thresholds = {
            'PM2.5': {'good': 12, 'moderate': 35, 'unhealthy': 55},
            'PM10': {'good': 20, 'moderate': 50, 'unhealthy': 100},
            'CO2': {'good': 800, 'moderate': 1000, 'unhealthy': 1200},
            'eTVOC': {'good': 0.5, 'moderate': 1.0, 'unhealthy': 2.0}
        }
        
        # Calculate risk scores
        df['PM25_risk'] = pd.cut(df['PM2.5'], 
                                 bins=[0, 12, 35, 55, float('inf')],
                                 labels=[0, 1, 2, 3])
        
        # Create composite risk score
        df['composite_risk'] = (
            df['PM25_risk'].astype(float) * 0.4 +
            # Add other parameters with weights
            df['CO2'].apply(lambda x: 1 if x > 1000 else 0) * 0.2
        )
        
        return df
    
    def train_prediction_model(self, df, target_variable):
        """
        Train model to predict future air quality
        """
        # Prepare features
        feature_columns = ['Temperature', 'Humidity', 'Hour', 'DayOfWeek', 
                          'Month', 'lag_1', 'lag_2', 'rolling_mean_4']
        
        X = df[feature_columns]
        y = df[target_variable]
        
        # Time-based split
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return model, {'mse': mse, 'r2': r2}