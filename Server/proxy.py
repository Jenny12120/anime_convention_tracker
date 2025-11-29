from abc import ABC, abstractmethod
from datetime import datetime
import requests
import os

class CalendarFile(ABC):
    @abstractmethod
    def download_ics(self):
        pass

class RealCalendarFile(CalendarFile):
    def download_ics(self, data):
        url = "https://api.apyhub.com/generate/ical/file?output=invite.ics"
        convention = self.setup_payload(data) 
        headers = {
	        "Content-Type": "application/json",
            "apy-token": "APY0pPjBOnqQGXF4YJiZneMlmsGTte0sBxmSuzJCA8VHJTiZJ9JGkWwSCgqGlYmDsiV1tmQnSwo"
        }

        response = requests.post(url, json=convention, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            return None


    
    def setup_payload(self,data):
        start_date = datetime.strptime(data.get('start_date'), "%a, %d %b %Y")
        end_date = datetime.strptime(data.get('end_date'), "%a, %d %b %Y")
        meeting_date = start_date.strftime("%d-%m-%Y")
            
        event = {
            "summary": data.get('name'),
            "description": data.get('url'),
            "organizer_email":"organizer@example.com", #generic email used as for conventions orgainzer email is not that important
            "attendees_emails":["attendee@example.com"],#generic email used as for conventions attendee email is not that important
            "location": data.get('venue'),
            "time_zone":"UTC",
            "meeting_date": meeting_date
            }

        if (end_date > start_date) :
            recurrence_count = (end_date - start_date).days + 1
            event["recurring"] = True
            recurrence_details = {
                "frequency":  "DAILY",
                "count": recurrence_count 
            }
            event["recurrence"] = recurrence_details
        return event           

class ProxyCalendarFile(CalendarFile):
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.real_calender_file = RealCalendarFile()

    def download_ics(self, data):
        ics_file_name = data.get('id') + "_" + data.get('name') + ".ics"
        file_path = os.path.join(self.cache_dir, ics_file_name)

        if (os.path.exists(file_path) == False):
            ics_file = self.real_calender_file.download_ics(data)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(ics_file)
                    return {'directory' : self.cache_dir,
                            'file_name': ics_file_name}
            except Exception as e:
                    print(f"Failed to cache file: {e}")
            return None
        return {'directory' : self.cache_dir,
                'file_name': ics_file_name}
        

        
        
        


