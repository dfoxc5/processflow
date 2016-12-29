from app import app
import os
port = int(os.environ.get('PORT', 5000))

# app.run(debug=True, host='127.0.0.1', port=port)
app.run(host='0.0.0.0', port=port)
