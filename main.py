
import os, sys
apps_path = './apps'
sys.path.append(os.path.abspath(apps_path))

from views import app

def run():
    app.run(debug=True, host="0.0.0.0", port=8888)

    
if __name__ == "__main__":
    run()
