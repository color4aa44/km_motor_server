from flask import Flask

app = Flask(__name__, static_folder='build', static_url_path='')

if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=10080)