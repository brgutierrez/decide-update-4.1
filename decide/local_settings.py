ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'http://localhost:8000'

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'decidedb',
        'PASSWORD': 'decide',
        'USER': 'decide',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CSRF_TRUSTED_ORIGINS = ['https://brgutierrez-vigilant-couscous-5wqw5gw6wqvc4j7q-8000.preview.app.github.dev', 'https://localhost']

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
