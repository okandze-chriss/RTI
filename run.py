from rti import create_app

from rti import db, create_app
from rti import models

app = create_app()

#db.drop_all(app=create_app())
#db.create_all(app=create_app())


if __name__ == '__main__':
    # app.run(port=80)
    # app.run(debug=True, host="0.0.0.0", port=80)
    # app.run(host="192.168.1.12", port=5000)
    app.run(debug=True)
    # socketionbf.run(app, debug=True)
