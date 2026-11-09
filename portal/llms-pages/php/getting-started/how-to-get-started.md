# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.


# Building

The generated code has dependencies over external libraries like UniRest and JsonMapper. JsonMapper requires docblock annotations like `@var`, `@maps`, and `@factory` to map JSON responses with our class definitions. Hence the docblocks in generated code cannot be disabled by deactivating the PHP configurations like `opcache.save_comments`. These dependencies are defined in the `composer.json` file that comes with the SDK. To resolve these dependencies, we use the Composer package manager which requires PHP greater than or equal to 7.2 installed in your system. Visit [https://getcomposer.org/download/](https://getcomposer.org/download/) to download the installer file for Composer and run it in your system. Open command prompt and type `composer --version`. This should display the current version of the Composer installed if the installation was successful.

* Using command line, navigate to the directory containing the generated files (including `composer.json`) for the SDK.
* Run the command `composer install`. This should install all the required dependencies and create the `vendor` directory in your project directory.

![Building SDK - Step 1](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=installDependencies)

## Configuring CURL Certificate Path in php.ini

:information_source: **Note** This is for Windows users only.

CURL used to include a list of accepted CAs, but no longer bundles ANY CA certs. So by default it will reject all SSL certificates as unverifiable. You will have to get your CA's cert and point curl at it. The steps are as follows:

1. Download the certificate bundle (.pem file) from [https://curl.haxx.se/docs/caextract.html](https://curl.haxx.se/docs/caextract.html) on to your system.
2. Add curl.cainfo = "PATH_TO/cacert.pem" to your php.ini file located in your php installation. “PATH_TO” must be an absolute path containing the .pem file.

```
[curl]; A default value for the CURLOPT_CAINFO option. This is required to be an
; absolute path.
curl.cainfo = PATH_TO/cacert.pem
```


# Installation

The following section explains how to use the TradeGlotLocalConsoleLib library in a new project.

## 1. Open Project in an IDE

Open an IDE for PHP like PhpStorm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PHPStorm - Step 1](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=openIDE)

Click on `Open` in PhpStorm to browse to your generated SDK directory and then click `OK`.

![Open project in PHPStorm - Step 2](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=openProject0)

## 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PHPStorm - Step 1](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=createDirectory)

Name the directory as "test".

![Add a new project in PHPStorm - Step 2](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=nameDirectory)

Add a PHP file to this project.

![Add a new project in PHPStorm - Step 3](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=createFile)

Name it "testSDK".

![Add a new project in PHPStorm - Step 4](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=nameFile)

Depending on your project setup, you might need to include composer's autoloader in your PHP code to enable auto loading of classes.

```php
require_once "vendor/autoload.php";
```

It is important that the path inside require_once correctly points to the file `autoload.php` inside the vendor directory created during dependency installations.

![Add a new project in PHPStorm - Step 5](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=projectFiles)

After this you can add code to initialize the client library and acquire the instance of a Controller class. Sample code to initialize the client library and use the Controller methods is given in the subsequent sections.

## 3. Run the Test Project

To run your project you must set the Interpreter for your project. Interpreter is the PHP engine installed on your computer.

Open `Settings` from `File` menu.

![Run Test Project - Step 1](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=openSettings)

Select `PHP` from within `Languages & Frameworks`.

![Run Test Project - Step 2](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=setInterpreter0)

Browse for Interpreters near the `Interpreter` option and choose your interpreter.

![Run Test Project - Step 3](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=setInterpreter1)

Once the interpreter is selected, click `OK`.

![Run Test Project - Step 4](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=setInterpreter2)

To run your project, right click on your PHP file inside your Test project and click on `Run`.

![Run Test Project - Step 5](https://apidocs.io/illustration/php?workspaceFolder=TradeGlotLocalConsole&step=runProject)



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| timeout | `int` | Timeout for API calls in seconds.<br>*Default*: `0` |
| enableRetries | `bool` | Whether to enable retries and backoff feature.<br>*Default*: `false` |
| numberOfRetries | `int` | The number of retries to make.<br>*Default*: `0` |
| retryInterval | `float` | The retry time interval between the endpoint calls.<br>*Default*: `1` |
| backOffFactor | `float` | Exponential backoff factor to increase interval between retries.<br>*Default*: `2` |
| maximumRetryWaitTime | `int` | The maximum wait time in seconds for overall retrying requests.<br>*Default*: `0` |
| retryOnTimeout | `bool` | Whether to retry on request timeout.<br>*Default*: `true` |
| httpStatusCodesToRetry | `array` | Http status codes to retry against.<br>*Default*: `408, 413, 429, 500, 502, 503, 504, 521, 522, 524, 408, 413, 429, 500, 502, 503, 504, 521, 522, 524` |
| httpMethodsToRetry | `array` | Http methods to retry against.<br>*Default*: `'GET', 'PUT', 'GET', 'PUT'` |
| proxyConfiguration | [`ProxyConfigurationBuilder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/sdk-infrastructure/configuration/proxyconfigurationbuilder.md) | Represents the proxy configurations for API calls |
| demoCsrfCredentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |
| demoSessionCredentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |

The API client can be initialized as follows:

```php
use TradeGlotLocalConsoleLib\Authentication\DemoCsrfCredentialsBuilder;
use TradeGlotLocalConsoleLib\Authentication\DemoSessionCredentialsBuilder;
use TradeGlotLocalConsoleLib\TradeGlotLocalConsoleClientBuilder;

$client = TradeGlotLocalConsoleClientBuilder::init()
    ->demoCsrfCredentials(
        DemoCsrfCredentialsBuilder::init(
            'X-CSRF-Token'
        )
    )
    ->demoSessionCredentials(
        DemoSessionCredentialsBuilder::init(
            'X-Demo-Session'
        )
    )
    ->build();
```


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| X-CSRF-Token | `string` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `xCSRFToken` | `getXCSRFToken()` |



**Note:** Auth credentials can be set using `DemoCsrfCredentialsBuilder::init()` in `demoCsrfCredentials` method in the client builder and accessed through `getDemoCsrfCredentials` method in the client instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```php
use TradeGlotLocalConsoleLib\Authentication\DemoCsrfCredentialsBuilder;
use TradeGlotLocalConsoleLib\TradeGlotLocalConsoleClientBuilder;

$client = TradeGlotLocalConsoleClientBuilder::init()
    ->demoCsrfCredentials(
        DemoCsrfCredentialsBuilder::init(
            'X-CSRF-Token'
        )
    )
    ->build();
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| X-Demo-Session | `string` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `xDemoSession` | `getXDemoSession()` |



**Note:** Auth credentials can be set using `DemoSessionCredentialsBuilder::init()` in `demoSessionCredentials` method in the client builder and accessed through `getDemoSessionCredentials` method in the client instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```php
use TradeGlotLocalConsoleLib\Authentication\DemoSessionCredentialsBuilder;
use TradeGlotLocalConsoleLib\TradeGlotLocalConsoleClientBuilder;

$client = TradeGlotLocalConsoleClientBuilder::init()
    ->demoSessionCredentials(
        DemoSessionCredentialsBuilder::init(
            'X-Demo-Session'
        )
    )
    ->build();
```


# Test the SDK

Unit tests in this SDK can be run using PHPUnit.

1. First install the dependencies using composer including the `require-dev` dependencies.
2. Run `vendor\bin\phpunit --verbose` from commandline to execute tests. If you have installed PHPUnit globally, run tests using `phpunit --verbose` instead.

You can change the PHPUnit test configuration in the `phpunit.xml` file.



