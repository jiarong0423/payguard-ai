# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.


# Building

The generated code depends on a few Ruby gems. The references to these gems are added in the gemspec file. The easiest way to resolve the dependencies, build the gem and install it is through Rake:

1. Install Rake if not already installed: `gem install rake`
2. Install Bundler if not already installed: `gem install bundler`
3. From terminal/cmd navigate to the root directory of the SDK.
4. Invoke: `rake install`

Alternatively, you can build and install the gem manually:

1. From terminal/cmd navigate to the root directory of the SDK.
2. Run the build command: `gem build trade_glot_local_console.gemspec`
3. Run the install command: `gem install trade_glot_local_console-0.2.0.gem`

![Installing Gem](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&gemVer=0.2.0&gemName=trade_glot_local_console&step=buildSDK)


# Installation

The following section explains how to use the trade_glot_local_console ruby gem in a new Rails project using RubyMine&trade;. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

## 1. Starting a new project

Close any existing projects in RubyMine&trade; by selecting `File -> Close Project`. Next, click on `Create New Project` to create a new project from scratch.

![Create a new project in RubyMine - Step 1](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&step=createNewProject0)

Next, provide `TestApp` as the project name, choose `Rails Application` as the project type, and click `OK`.

![Create a new Rails Application in RubyMine - Step 2](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&step=createNewProject1)

In the next dialog make sure that the correct Ruby SDK is being used (>= 2.6 and <= 3.2) and click `OK`.

![Create a new Rails Application in RubyMine - Step 3](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&step=createNewProject2)

## 2. Add reference of the gem

In order to use the `trade_glot_local_console` gem in the new project we must add a gem reference. Locate the `Gemfile` in the Project Explorer window under the `TestApp` project node. The file contains references to all gems being used in the project. Here, add the reference to the library gem by adding the following line: `gem 'trade_glot_local_console', '0.2.0'`

![Add new reference to the Gemfile](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&gemVer=0.2.0&gemName=trade_glot_local_console&step=addReference)

## 3. Adding a new Rails Controller

Once the `TestApp` project is created, a folder named `controllers` will be visible in the *Project Explorer* under the following path: `TestApp > app > controllers`. Right click on this folder and select `New -> Run Rails Generator...`.

![Run Rails Generator on Controllers Folder](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&gemVer=0.2.0&gemName=trade_glot_local_console&step=addCode0)

Selecting the said option will popup a small window where the generator names are displayed. Here, select the `controller` template.

![Create a new Controller](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&step=addCode1)

Next, a popup window will ask you for a Controller name and included Actions. For controller name provide `Hello` and include an action named `Index` and click `OK`.

![Add a new Controller](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&gemVer=0.2.0&gemName=trade_glot_local_console&step=addCode2)

A new controller class named `HelloController` will be created in a file named `hello_controller.rb` containing a method named `Index`.

1. Add the `require 'trade_glot_local_console'` statement to require the gem in the controller file.
2. Add the `include TradeGlotLocalConsole` statement to include the sdk module in the controller file.
3. In the `Index` method, add code for initialization and a sample for its usage.

![Initialize the library](https://apidocs.io/illustration/ruby?workspaceFolder=TradeGlotLocalConsole&gemName=trade_glot_local_console&step=addCode3)



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| connection | `Faraday::Connection` | The Faraday connection object passed by the SDK user for making requests |
| adapter | `Faraday::Adapter` | The Faraday adapter object passed by the SDK user for performing http requests |
| timeout | `Float` | The value to use for connection timeout. <br> **Default: 60** |
| max_retries | `Integer` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| retry_interval | `Float` | Pause in seconds between retries. <br> **Default: 1** |
| backoff_factor | `Float` | The amount to multiply each successive retry's interval amount by in order to provide backoff. <br> **Default: 2** |
| retry_statuses | `Array` | A list of HTTP statuses to retry. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524, 408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| retry_methods | `Array` | A list of HTTP methods to retry. <br> **Default: %i[get put get put]** |
| http_callback | `HttpCallBack` | The Http CallBack allows defining callables for pre and post API calls. |
| proxy_settings | [`ProxySettings`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/sdk-infrastructure/configuration/proxysettings.md) | Optional proxy configuration to route HTTP requests through a proxy server. |
| demo_csrf_credentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md) | The credential object for Custom Header Signature |
| demo_session_credentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md) | The credential object for Custom Header Signature |

The API client can be initialized as follows:

## Code-Based Client Initialization

```ruby
require 'trade_glot_local_console'
include TradeGlotLocalConsole

client = Client.new(
  demo_csrf_credentials: DemoCsrfCredentials.new(
    x_csrf_token: 'X-CSRF-Token'
  ),
  demo_session_credentials: DemoSessionCredentials.new(
    x_demo_session: 'X-Demo-Session'
  )
)
```

## Environment-Based Client Initialization

```ruby
require 'trade_glot_local_console'
include TradeGlotLocalConsole

# Create client from environment
client = Client.from_env
```

See the [`Environment-Based Client Initialization`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/sdk-infrastructure/configuration/environment-based-client-initialization.md) section for details.


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Getter |
|  --- | --- | --- | --- |
| X-CSRF-Token | `String` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `x_csrf_token` |



**Note:** Auth credentials can be set using `DemoCsrfCredentials` object, passed in as named parameter `demo_csrf_credentials` in the client initialization.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```ruby
require 'trade_glot_local_console'
include TradeGlotLocalConsole

client = Client.new(
  demo_csrf_credentials: DemoCsrfCredentials.new(
    x_csrf_token: 'X-CSRF-Token'
  )
)
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Getter |
|  --- | --- | --- | --- |
| X-Demo-Session | `String` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `x_demo_session` |



**Note:** Auth credentials can be set using `DemoSessionCredentials` object, passed in as named parameter `demo_session_credentials` in the client initialization.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```ruby
require 'trade_glot_local_console'
include TradeGlotLocalConsole

client = Client.new(
  demo_session_credentials: DemoSessionCredentials.new(
    x_demo_session: 'X-Demo-Session'
  )
)
```


# Test the SDK

To run the tests, navigate to the root directory of the SDK in your terminal and execute the following command:

```
rake
```



