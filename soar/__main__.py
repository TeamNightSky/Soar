from soar.app import app


app.run(
    host="0.0.0.0",
    port=8080,
    workers=11 #  Runs before_server_start 11 times :/
)
