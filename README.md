# SesamUtils

[![Build Status](https://dev.azure.com/sesam-community/Community%20Python%20Packages/_apis/build/status/sesam-community.sesamutils?branchName=master)](https://dev.azure.com/sesam-community/Community%20Python%20Packages/_build/latest?definitionId=1&branchName=master)

**Python module to simplify common tasks when developing microservices for the Sesam integration platform.**


### Usage examples

**Environment Variables**

You can use the VariablesConfig class to load environment variables into your service. It requires a list of required variables. It also support an optional list of variables as a second argument.

```python
from sesamutils import VariablesConfig
import sys

required_env_vars = ["username", "password", "hostname"]
optional_env_vars = ["debug", ("auth_type", "user")] # Default values can be given to optional environment variables by the use of tuples

config = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

if not config.validate():
    sys.exit(1)


print(config.username)

```

**Dotdictify**

A class to help traversing and modifying large nested dictionaries. Lets you navigate by dot notation.

```python
from sesamutils import Dotdictify

example_dict = {
    "test": {
        "my_thing": "hello"
    }
}

dot_dict = Dotdictify(example_dict)

print(dot_dict.test.my_thing)

# hello

```
**Profiler**

 You can use this (A profiling decorator) to see complete details of execution time taken by a function in your program. 
 Based on that, you can optimize your python code if required.

```python
from sesamutils import profiler

@profiler
def <Name of your method>():
    <your method definition>

# Apply to any function with @profiler
# Profiles the function using cProfile, and prints out a report to screen.
# belwo are few lines for illustration  purpose.
ncalls tottime  percall  cumtime  percall filename:lineno(function)
1    0.000    0.000    0.312    0.312 C:/Work/PycharmProjects/node-notification-handler/service/notification-handler.py:143(get_node_members_and_roles)
2    0.000    0.000    0.311    0.156 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\sessions.py:537(get)
2    0.000    0.000    0.311    0.156 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\sessions.py:466(request)
2    0.000    0.000    0.309    0.154 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\sessions.py:617(send)
2    0.000    0.000    0.308    0.154 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\adapters.py:394(send)
2    0.000    0.000    0.306    0.153 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\urllib3\connectionpool.py:446(urlopen)
2    0.000    0.000    0.306    0.153 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\urllib3\connectionpool.py:319(_make_request)
1    0.000    0.000    0.258    0.258 C:\Work\PycharmProjects\node-notification-handler\service\portal.py:34(get_subscription_members)
```

**Sesam Logger**

 You can use this to save time and lines of code. It provides the standard customization of root level logging- 
 configuration and gives you SESAM uniform standard settings.

```python
from sesamutils import sesam_logger

logger = sesam_logger('<name of your module or logger>')
```

Default log level is 'INFO'. To set a different level, you need to provide the environment variable 'LOG_LEVEL'.
Since the microservice log view in the Sesam portal gets it's own timestamps directly from docker, this logger does not print timestamps by default.
However if you want to log timestamps regardless, you can enable timestamps like this:

```python
logger = sesam_logger('<name of your module or logger>', timestamp=True)
```

If your app is using Flask and cherrypy, you can enable request logging by sending the app instance to `sesam_logger` like this:

```python
logger = sesam_logger('<name of your module or logger>', app=<Flask app instance>)
```

**Serve Flask app**

When writing microservices using [Flask](), we don't want to use the built-in development web server as this among other things doesn't set content-length or support chunked encoding (streams).
To mitigate this we use cherrypy to serve our Flask microservices. To simplify this task, you can use our `serve` function:

```python
...
from sesamutils.flask import serve

app = Flask(__name__)

...

if __name__ == "__main__":
    serve(app)
```
To define another port than the default (5000), you can do:
```python
    serve(app, port=<port>)
```

**Certificate Handler**

Sometimes it is necessary for microservices to access certificates from
the file system of the server they are hosted on at runtime.
Microservices that run inside docker containers cannot by default
access file systems outside their container.

By first storing the relevant certificate in a Sesam secret and passing
it to a docker environment variable in the microservice system config,
this module allows you to install the certificate in the container at runtime.

Assuming the microservice system config in Sesam is defined with the
environment variable `CERT` referencing a Sesam secret containing the
relevant certificate, the following example shows how to install
the certificate inside the container at runtime:

```python
from sesamutils import CertificateHandler
from sesamutils import VariablesConfig

env = VariablesConfig(["CERT"])

ch = CertificateHandler(env.CERT)
ch.write()    # write certificate to file system
ch.install()  # install certificate to /etc/ssl/certs/
```

### Installation

```python
pip install sesamutils
```
