import json

class Config():
    def __init__(self):
        self.settings = None
        
    def load(self):
        f = open("nanoka_settings.json", "rb")
        self.settings = json.load(f)
        f.close()
    
    def save(self):
        with open("nanoka_settings.json", "w") as f:
            json.dump(self.settings, f, indent=2)
            
    def get(self):
        return self.settings
    
    def sett(self, settings):
        self.settings = settings


if __name__ == "__main__":
    t = Config()
    t.load()
    
        
