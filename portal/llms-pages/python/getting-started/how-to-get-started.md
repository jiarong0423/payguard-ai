# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.


# Building

You must have Python `3.7+` installed on your system to install and run this SDK. This SDK package depends on other Python packages like pytest, etc. These dependencies are defined in the `requirements.txt` file that comes with the SDK. To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type `pip --version`. This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including `requirements.txt`) for the SDK.
* Run the command `pip install -r requirements.txt`. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&step=installDependencies)


# Installation

The following section explains how to use the tradeglotlocalconsole library in a new project.

## 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&step=pyCharm)

Click on `Open` in PyCharm to browse to your generated SDK directory and then click `OK`.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&step=openProject0)

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&projectName=tradeglotlocalconsole&step=openProject1)

## 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&projectName=tradeglotlocalconsole&step=createDirectory)

Name the directory as "test".

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&step=nameDirectory)

Add a python file to this project.

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&projectName=tradeglotlocalconsole&step=createFile)

Name it "testSDK".

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&projectName=tradeglotlocalconsole&step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```python
from tradeglotlocalconsole.tradeglotlocalconsole_client import TradeglotlocalconsoleClient
```

![Add a new project in PyCharm - Step 5](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&projectName=tradeglotlocalconsole&libraryName=tradeglotlocalconsole.tradeglotlocalconsole_client&className=TradeglotlocalconsoleClient&step=projectFiles)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

## 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on `Run`

![Run Test Project - Step 1](https://apidocs.io/illustration/python?workspaceFolder=Tradeglotlocalconsole-Python&projectName=tradeglotlocalconsole&libraryName=tradeglotlocalconsole.tradeglotlocalconsole_client&className=TradeglotlocalconsoleClient&step=runProject)



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| http_client_instance | `Union[Session, HttpClientProvider]` | The Http Client passed from the sdk user for making requests |
| override_http_client_configuration | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| http_call_back | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| timeout | `float` | The value to use for connection timeout. <br> **Default: 60** |
| max_retries | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| backoff_factor | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| retry_statuses | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524, 408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| retry_methods | `Array of string` | The http methods on which retry is to be done. <br> **Default: ["GET", "PUT", "GET", "PUT"]** |
| proxy_settings | [`ProxySettings`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/sdk-infrastructure/configuration/proxysettings.md) | Optional proxy configuration to route HTTP requests through a proxy server. |
| demo_csrf_credentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md) | The credential object for Custom Header Signature |
| demo_session_credentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md) | The credential object for Custom Header Signature |

The API client can be initialized as follows:

## Code-Based Client Initialization

```python
from tradeglotlocalconsole.configuration import Environment
from tradeglotlocalconsole.http.auth.demo_csrf import DemoCsrfCredentials
from tradeglotlocalconsole.http.auth.demo_session import DemoSessionCredentials
from tradeglotlocalconsole.tradeglotlocalconsole_client import TradeglotlocalconsoleClient

client = TradeglotlocalconsoleClient(
    demo_csrf_credentials=DemoCsrfCredentials(
        x_csrf_token='X-CSRF-Token'
    ),
    demo_session_credentials=DemoSessionCredentials(
        x_demo_session='X-Demo-Session'
    ),
    environment=Environment.PRODUCTION
)
```

## Environment-Based Client Initialization

```python
from tradeglotlocalconsole.tradeglotlocalconsole_client import TradeglotlocalconsoleClient

# Specify the path to your .env file if it’s located outside the project’s root directory.
client = TradeglotlocalconsoleClient.from_environment(dotenv_path='/path/to/.env')
```

See the [Environment-Based Client Initialization](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/sdk-infrastructure/configuration/environment-based-client-initialization.md) section for details.


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Getter |
|  --- | --- | --- | --- |
| X-CSRF-Token | `str` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `x_csrf_token` |



**Note:** Auth credentials can be set using `DemoCsrfCredentials` object, passed in as named parameter `demo_csrf_credentials` in the client initialization.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```python
from tradeglotlocalconsole.http.auth.demo_csrf import DemoCsrfCredentials
from tradeglotlocalconsole.tradeglotlocalconsole_client import TradeglotlocalconsoleClient

client = TradeglotlocalconsoleClient(
    demo_csrf_credentials=DemoCsrfCredentials(
        x_csrf_token='X-CSRF-Token'
    )
)
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Getter |
|  --- | --- | --- | --- |
| X-Demo-Session | `str` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `x_demo_session` |



**Note:** Auth credentials can be set using `DemoSessionCredentials` object, passed in as named parameter `demo_session_credentials` in the client initialization.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```python
from tradeglotlocalconsole.http.auth.demo_session import DemoSessionCredentials
from tradeglotlocalconsole.tradeglotlocalconsole_client import TradeglotlocalconsoleClient

client = TradeglotlocalconsoleClient(
    demo_session_credentials=DemoSessionCredentials(
        x_demo_session='X-Demo-Session'
    )
)
```


# Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands


pip install -r test-requirements.txt
pytest




