from app import app
import os
port = int(os.environ.get('PORT', 5000))

if app.config['LOCAL']:
    app.run(debug=True, host='127.0.0.1', port=port)
else:
    app.run(host='0.0.0.0', port=port)

