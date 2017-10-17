from flask import Flask, request, send_from_directory, redirect, Response, stream_with_context
import requests

app = Flask(__name__)
MAS_URI = "http://17.253.87.205/"


@app.route("/", defaults={'filename': ''})
@app.route("/<path:filename>")
def download(filename):
    try:
        if len(request.args) > 0:
            raise Exception("Parameter is given.")
        _filename = str(filename).split('/')[-1] # This will get the filename
        return send_from_directory("storage", _filename)

    except Exception as e:
        alt_url = MAS_URI + filename
        req = requests.get(alt_url, stream=True, headers={"Host": "swcdn.apple.com"})
        return Response(stream_with_context(req.iter_content()), headers=dict(req.headers))
        # app.logger.info("from MAS: %s" % filename)

if __name__ == '__main__':
    app.run("0.0.0.0", 80, debug=True)
