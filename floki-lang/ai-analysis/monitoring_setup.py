from dataclasses import dataclass
from typing import Dict, List
import time

@dataclass
class EventMetrics:
    event_type: str
    frequency: int
    execution_time: float
    resource_usage: Dict[str, float]
    timestamp: float

class FlokiMonitor:
    def __init__(self):
        self.events_history: List[EventMetrics] = []
        self.performance_metrics: Dict[str, float] = {}

    def log_event(self, event_type: str, execution_time: float, resources: Dict[str, float]):
        metric = EventMetrics(
            event_type=event_type,
            frequency=1,
            execution_time=execution_time,
            resource_usage=resources,
            timestamp=time.time()
        )
        self.events_history.append(metric)

    def get_statistics(self) -> Dict[str, Dict]:
        # Basic statistics calculation
        stats = {}
        for event in self.events_history:
            if event.event_type not in stats:
                stats[event.event_type] = {
                    'count': 0,
                    'avg_execution_time': 0,
                    'resource_usage': {}
                }
            stats[event.event_type]['count'] += 1
            stats[event.event_type]['avg_execution_time'] += event.execution_time
        
        # Calculate averages
        for event_type in stats:
            stats[event_type]['avg_execution_time'] /= stats[event_type]['count']
        
        return stats