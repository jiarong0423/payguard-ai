# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.


# Building

Supported Java version is **8+**.

The generated code uses a few Maven dependencies e.g., Jackson, OkHttp,
and Apache HttpClient. The reference to these dependencies is already
added in the pom.xml file will be installed automatically. Therefore,
you will need internet access for a successful build.

* In order to open the client library in Eclipse click on `File -> Import`.

![Importing SDK into Eclipse - Step 1](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=import0)

* In the import dialog, select `Existing Java Project` and click `Next`.

![Importing SDK into Eclipse - Step 2](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=import1)

* Browse to locate the folder containing the source code. Select the detected location of the project and click `Finish`.

![Importing SDK into Eclipse - Step 3](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=import2)

* Upon successful import, the project will be automatically built by Eclipse after automatically resolving the dependencies.

![Importing SDK into Eclipse - Step 4](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=import3)

* After successfully building the project, the client library needs to be installed as a Maven package in your local cache. Right-click on the project, select `Show in Local Terminal -> Terminal` or use `Ctrl + Alt + T` to open Terminal.

![Importing SDK into Eclipse - Step 5](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=openTerminal)

* In the terminal dialog, run the following command to install client library.

```
mvn install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true
```

![Importing SDK into Eclipse - Step 6](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=installCommand)


# Installation

The following section explains how to use the TradeGlotLocalConsoleLib library in a new project.

## 1. Starting a new project

For starting a new project, click the menu command `File > New > Project`.

![Add a new project in Eclipse](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=createNewProject0)

Next, choose `Maven > Maven Project` and click `Next`.

![Create a new Maven Project - Step 1](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=createNewProject1)

Here, make sure to use the current workspace by choosing `Use default Workspace location`, as shown in the picture below and click `Next`.

![Create a new Maven Project - Step 2](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=createNewProject2)

Following this, select the *quick start* project type to create a simple project with an existing class and a `main` method. To do this, choose `maven-archetype-quickstart` item from the list and click `Next`.

![Create a new Maven Project - Step 3](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=createNewProject3)

In the last step, provide a `Group Id` and `Artifact Id` as shown in the picture below and click `Finish`.

![Create a new Maven Project - Step 4](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=createNewProject4)

## 2. Add reference of the library project

The created Maven project manages its dependencies using its `pom.xml` file. In order to add a dependency on the *TradeGlotLocalConsoleLib* client library, double click on the `pom.xml` file in the `Package Explorer`. Opening the `pom.xml` file will render a graphical view on the canvas. Here, switch to the `Dependencies` tab and click the `Add` button as shown in the picture below.

![Adding dependency to the client library - Step 1](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=testProject0)

Clicking the `Add` button will open a dialog where you need to specify TradeGlotLocalConsoleLib in `Group Id`, trade-glot-local-console-lib in `Artifact Id` and 0.2.0 in the `Version` fields. Once added click `OK`. Save the `pom.xml` file.

![Adding dependency to the client library - Step 2](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=testProject1)

![Adding sample code](https://apidocs.io/illustration/java?workspaceFolder=TradeGlot%20Local%20Console-Java&workspaceName=TradeGlotLocalConsole&projectName=TradeGlotLocalConsoleLib&rootNamespace=m18000.m0.m0.m127&groupId=TradeGlotLocalConsoleLib&artifactId=trade-glot-local-console-lib&version=0.2.0&step=testProject2)

## 3. Write sample code

Once the `SimpleConsoleApp` is created, a file named `App.java` will be visible in the *Package Explorer* with a `main` method. This is the entry point for the execution of the created project.
Here, you can add code to initialize the client library and instantiate a *Controller* class. Sample code to initialize the client library and using controller methods is given in the subsequent sections.



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| httpClientConfig | [`Consumer<HttpClientConfiguration.Builder>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/sdk-infrastructure/configuration/httpclientconfiguration-builder.md) | Set up Http Client Configuration instance. |
| demoCsrfCredentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |
| demoSessionCredentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |

The API client can be initialized as follows:

```java
import m18000.m0.m0.m127.TradeGlotLocalConsoleClient;
import m18000.m0.m0.m127.authentication.DemoCsrfModel;
import m18000.m0.m0.m127.authentication.DemoSessionModel;
import m18000.m0.m0.m127.exceptions.ApiException;

public class Program {
    public static void main(String[] args) {
        TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
            .httpClientConfig(configBuilder -> configBuilder
                    .timeout(0))
            .demoCsrfCredentials(new DemoCsrfModel.Builder(
                    "X-CSRF-Token"
                )
                .build())
            .demoSessionCredentials(new DemoSessionModel.Builder(
                    "X-Demo-Session"
                )
                .build())
            .build();

    }
}
```


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| X-CSRF-Token | `String` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `xCSRFToken` | `getXCSRFToken()` |



**Note:** Auth credentials can be set using `demoCsrfCredentials` in the client builder and accessed through `getDemoCsrfCredentials` method in the client instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```java
import m18000.m0.m0.m127.TradeGlotLocalConsoleClient;
import m18000.m0.m0.m127.authentication.DemoCsrfModel;

public class Program {
    public static void main(String[] args) {
        TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
            .demoCsrfCredentials(new DemoCsrfModel.Builder(
                    "X-CSRF-Token"
                )
                .build())
            .build();
    }
}
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| X-Demo-Session | `String` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `xDemoSession` | `getXDemoSession()` |



**Note:** Auth credentials can be set using `demoSessionCredentials` in the client builder and accessed through `getDemoSessionCredentials` method in the client instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```java
import m18000.m0.m0.m127.TradeGlotLocalConsoleClient;
import m18000.m0.m0.m127.authentication.DemoSessionModel;

public class Program {
    public static void main(String[] args) {
        TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
            .demoSessionCredentials(new DemoSessionModel.Builder(
                    "X-Demo-Session"
                )
                .build())
            .build();
    }
}
```


# Test the SDK

The generated code and the server can be tested using automatically generated test cases.
JUnit is used as the testing framework and test runner.

In Eclipse, for running the tests do the following:

1. Select the project TradeGlotLocalConsoleLib from the package explorer.
2. Select `Run -> Run as -> JUnit Test` or use `Alt + Shift + X` followed by `T` to run the Tests.



