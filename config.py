import json

class Settings():
    def __init__(self):
        self.settings = None
        
    def get_pretty(self):
        data = self.settings
        json_str = json.dumps(data)  
        json_str = json_str.replace("{", "{\r\n").replace("}", "\r\n}").replace(",", ",\r\n")
        
        return json_str
        
    def load(self):
        f = open("nanoka_settings.json", "rb")
        self.settings = json.load(f)
        f.close()
    
    def save(self):
        json_str = self.get_pretty()
        with open("nanoka_settings.json", "w") as f:
            f.write(json_str)
        f.close()
            
    def get(self):
        return self.settings
    
    def sett(self, settings):
        self.settings = settings


if __name__ == "__main__":
    t = Settings()
    t.load()
    t.save()
    
        
