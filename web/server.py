from flask import Flask
app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
  app.run(host= '0.0.0.0', threaded=True)
#    app.run()
