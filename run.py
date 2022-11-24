from flask import Flask

class ReverseProxied(object):
    """
    Because we are reverse proxied from an aws load balancer
    use environ/config to signal https
    since flask ignores preferred_url_scheme in url_for calls
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # if one of x_forwarded or preferred_url is https, prefer it.
        forwarded_scheme = environ.get("HTTP_X_FORWARDED_PROTO", None)
        preferred_scheme = app.config.get("PREFERRED_URL_SCHEME", None)
        if "https" in [forwarded_scheme, preferred_scheme]:
            environ["wsgi.url_scheme"] = "https"
        return self.app(environ, start_response)


app = Flask(__name__)
# set to always use https instead of http
app.config.update(dict(PREFERRED_URL_SCHEME='https'))
app.wsgi_app = ReverseProxied(app.wsgi_app)
@app.route('/')
def index():
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=80)
