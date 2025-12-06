from datetime import datetime
from utils.file_manager import load_data, save_data

class AttendanceManager:
    def __init__(self, file_name="attendance.json"):
        self.file_name = file_name
    
    def register_entry(self, user):
        data = load_data(self.file_name)
        if not isinstance(data, list):
            data = []
            
        record = {
            "nickname": user.nickname,
            "name": user.name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data.append(record)
        save_data(data, self.file_name)
        print(f"[ASISTENCIA] Entrada registrada: {user.nickname} a las {record['timestamp']}")