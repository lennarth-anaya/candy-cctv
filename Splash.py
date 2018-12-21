
class Splash():
    def __init__(self):
        self.sourceFile = "splash.txt"
    def display(self):
        f = open(self.sourceFile, "r")
        print(f.read())
        
