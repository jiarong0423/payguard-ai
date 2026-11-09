# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.


# Building

The generated code uses the Newtonsoft Json.NET NuGet Package. If the automatic NuGet package restore is enabled, these dependencies will be installed automatically. Therefore, you will need internet access for build.

* Open the solution (TradeGlotLocalConsole.sln) file.

Invoke the build process using Ctrl + Shift + B shortcut key or using the Build menu as shown below.

The build process generates a portable class library, which can be used like a normal class library. More information on how to use can be found at the MSDN Portable Class Libraries documentation.

The supported version is **.NET Standard 2.0**. For checking compatibility of your .NET implementation with the generated library, [click here](https://dotnet.microsoft.com/en-us/platform/dotnet-standard#versions).


# Installation

The following section explains how to use the TradeGlotLocalConsole.Standard library in a new project.

## 1. Starting a new project

For starting a new project, right click on the current solution from the solution explorer and choose `Add -> New Project`.

![Add a new project in Visual Studio](https://apidocs.io/illustration/cs?workspaceFolder=TradeGlot%20Local%20Console-CSharp&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsole.Standard&rootNamespace=TradeGlotLocalConsole.Standard&step=addProject)

Next, choose `Console Application`, provide `TestConsoleProject` as the project name and click OK.

![Create a new Console Application in Visual Studio](https://apidocs.io/illustration/cs?workspaceFolder=TradeGlot%20Local%20Console-CSharp&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsole.Standard&rootNamespace=TradeGlotLocalConsole.Standard&step=createProject)

## 2. Set as startup project

The new console project is the entry point for the eventual execution. This requires us to set the `TestConsoleProject` as the start-up project. To do this, right-click on the `TestConsoleProject` and choose `Set as StartUp Project` form the context menu.

![Adding a project reference](https://apidocs.io/illustration/cs?workspaceFolder=TradeGlot%20Local%20Console-CSharp&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsole.Standard&rootNamespace=TradeGlotLocalConsole.Standard&step=setStartup)

## 3. Add reference of the library project

In order to use the `TradeGlotLocalConsole.Standard` library in the new project, first we must add a project reference to the `TestConsoleProject`. First, right click on the `References` node in the solution explorer and click `Add Reference...`

![Adding a project reference](https://apidocs.io/illustration/cs?workspaceFolder=TradeGlot%20Local%20Console-CSharp&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsole.Standard&rootNamespace=TradeGlotLocalConsole.Standard&step=addReference)

Next, a window will be displayed where we must set the `checkbox` on `TradeGlotLocalConsole.Standard` and click `OK`. By doing this, we have added a reference of the `TradeGlotLocalConsole.Standard` project into the new `TestConsoleProject`.

![Creating a project reference](https://apidocs.io/illustration/cs?workspaceFolder=TradeGlot%20Local%20Console-CSharp&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsole.Standard&rootNamespace=TradeGlotLocalConsole.Standard&step=createReference)

## 4. Write sample code

Once the `TestConsoleProject` is created, a file named `Program.cs` will be visible in the solution explorer with an empty `Main` method. This is the entry point for the execution of the entire solution. Here, you can add code to initialize the client library and acquire the instance of a Controller class. Sample code to initialize the client library and using Controller methods is given in the subsequent sections.

![Adding a project reference](https://apidocs.io/illustration/cs?workspaceFolder=TradeGlot%20Local%20Console-CSharp&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsole.Standard&rootNamespace=TradeGlotLocalConsole.Standard&step=addCode)



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| Timeout | `TimeSpan` | Http client timeout.<br>*Default*: `TimeSpan.FromSeconds(100)` |
| HttpClientConfiguration | [`Action<HttpClientConfiguration.Builder>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/sdk-infrastructure/configuration/httpclientconfigurationbuilder.md) | Action delegate that configures the HTTP client by using the HttpClientConfiguration.Builder for customizing API call settings.<br>*Default*: `new HttpClient()` |
| DemoCsrfCredentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |
| DemoSessionCredentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |

The API client can be initialized as follows:

## Code-Based Initialization

```csharp
using TradeGlotLocalConsole.Standard;
using TradeGlotLocalConsole.Standard.Authentication;

namespace ConsoleApp;

TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
    .DemoCsrfCredentials(
        new DemoCsrfModel.Builder(
            "X-CSRF-Token"
        )
        .Build())
    .DemoSessionCredentials(
        new DemoSessionModel.Builder(
            "X-Demo-Session"
        )
        .Build())
    .HttpClientConfig(httpClientConfig =>
        httpClientConfig.Timeout(TimeSpan.FromSeconds(100)))
    .Build();
```

## Configuration-Based Initialization

```csharp
using TradeGlotLocalConsole.Standard;
using Microsoft.Extensions.Configuration;

namespace ConsoleApp;

// Build the IConfiguration using .NET conventions (JSON, environment, etc.)
var configuration = new ConfigurationBuilder()
    .AddJsonFile("config.json")
    .AddEnvironmentVariables() // [optional] read environment variables
    .Build();

// Instantiate your SDK and configure it from IConfiguration
var client = TradeGlotLocalConsoleClient
    .FromConfiguration(configuration.GetSection("TradeGlotLocalConsole"));
```

See the [Configuration-Based Initialization](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/sdk-infrastructure/configuration/configuration-based-initialization.md) section for details.


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| XCSRFToken | `string` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `XCSRFToken` | `XCSRFToken` |



**Note:** Auth credentials can be set using `DemoCsrfCredentials` in the client builder and accessed through `DemoCsrfCredentials` method in the client instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```csharp
using TradeGlotLocalConsole.Standard;
using TradeGlotLocalConsole.Standard.Authentication;

namespace ConsoleApp;

TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
    .DemoCsrfCredentials(
        new DemoCsrfModel.Builder(
            "X-CSRF-Token"
        )
        .Build())
    .Build();
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| XDemoSession | `string` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `XDemoSession` | `XDemoSession` |



**Note:** Auth credentials can be set using `DemoSessionCredentials` in the client builder and accessed through `DemoSessionCredentials` method in the client instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```csharp
using TradeGlotLocalConsole.Standard;
using TradeGlotLocalConsole.Standard.Authentication;

namespace ConsoleApp;

TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
    .DemoSessionCredentials(
        new DemoSessionModel.Builder(
            "X-Demo-Session"
        )
        .Build())
    .Build();
```


# Test the SDK

The generated SDK also contain one or more Tests, which are contained in the Tests project. In order to invoke these test cases, you will need `NUnit 3.0 Test Adapter Extension` for Visual Studio. Once the SDK is complied, the test cases should appear in the Test Explorer window. Here, you can click `Run All` to execute these test cases.



