class ActionRecommender:
    """
Actionable recommendations based on predictions
    """
    
    def __init__(self):
        self.action_thresholds = {
            'PM2.5': {
                'low': {'max': 12, 'action': 'Air quality is good. Ventilation recommended.'},
                'moderate': {'min': 12, 'max': 35, 'action': 'Consider using air purifier'},
                'high': {'min': 35, 'max': 55, 'action': 'Wear mask if going out. Close windows.'},
                'severe': {'min': 55, 'action': 'Wear N95 mask. Use air purifier. Avoid outdoor activities.'}
            },
            'CO2': {
                'normal': {'max': 800, 'action': 'Air circulation is good.'},
                'elevated': {'min': 800, 'max': 1000, 'action': 'Open windows for ventilation'},
                'high': {'min': 1000, 'max': 1200, 'action': 'Take a break. Get fresh air.'},
                'critical': {'min': 1200, 'action': 'Evacuate immediately. High CO2 levels.'}
            },
            'eTVOC': {
                'low': {'max': 0.5, 'action': 'Air quality is fresh.'},
                'moderate': {'min': 0.5, 'max': 1.0, 'action': 'Check for VOCs sources'},
                'high': {'min': 1.0, 'action': 'Avoid using chemical products. Ventilate room.'}
            }
        }
    
    def get_combined_recommendation(self, predictions):
        """
        Generate combined recommendation based on all parameters
        """
        actions = []
        
        for param, value in predictions.items():
            if param in self.action_thresholds:
                for level, thresholds in self.action_thresholds[param].items():
                    if 'min' in thresholds and value >= thresholds['min']:
                        if 'max' in thresholds and value <= thresholds['max']:
                            actions.append(thresholds['action'])
                        elif 'max' not in thresholds:
                            actions.append(thresholds['action'])
        
        # Prioritize and combine actions
        if actions:
            priority_actions = self._prioritize_actions(actions)
            return priority_actions
        else:
            return ["Air quality is within normal ranges. Continue monitoring."]
    
    def _prioritize_actions(self, actions):
        """
        Prioritize actions based on severity
        """
        # Prioritization logic
        priority_keywords = ['evacuate', 'mask', 'immediately', 'avoid outdoor']
        
        prioritized = []
        for action in actions:
            if any(keyword in action.lower() for keyword in priority_keywords):
                prioritized.insert(0, action)
            else:
                prioritized.append(action)
        
        return list(dict.fromkeys(prioritized))[:3]  # Return top 3 unique actions