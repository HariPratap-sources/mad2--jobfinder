from datetime import datetime 

def validate_date(s):
    try:
        return datetime.fromisoformat(s)
        
    except ValueError:
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            
            raise ValueError("Datetime needs to be in format %Y-%m-%d %H:%M:%S")
