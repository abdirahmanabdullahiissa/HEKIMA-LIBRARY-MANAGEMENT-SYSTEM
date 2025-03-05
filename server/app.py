from config import app
from model import User, Role, UserRole 
if __name__== '__main__':
    app.run(port=5555 , debug=True)