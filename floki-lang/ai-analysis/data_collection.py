from typing import Dict, List, Any
import json
import os
from datetime import datetime

class DataCollector:
    def __init__(self, storage_path: str = "collected_data"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
        
    def _ensure_storage_exists(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            
    def store_event_data(self, event_data: Dict[str, Any]):
        timestamp = datetime.now().isoformat()
        filename = f"event_data_{timestamp}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(event_data, f, indent=2)
            
    def store_performance_metrics(self, metrics: Dict[str, Any]):
        timestamp = datetime.now().isoformat()
        filename = f"performance_metrics_{timestamp}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)