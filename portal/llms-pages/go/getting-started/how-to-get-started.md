# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.

## Requirements

The SDK requires **Go version 1.18 or above**.


# Building

## Install Dependencies

Resolve all the SDK dependencies, using the `go get` command.


# Installation

The following section explains how to use the tradeglotlocalconsole library in a new project.

## 1. Add SDK as a Dependency to the Application

- Add the following lines to your application's `go.mod` file:

```go
replace tradeglotlocalconsole => ".\\Random Directory" // local path to the SDK

require tradeglotlocalconsole v0.0.0
```

- Resolve the dependencies in the updated `go.mod` file, using the `go get` command.



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| httpConfiguration | [`HttpConfiguration`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/configuration/httpconfiguration.md) | Configurable http client options like timeout and retries. |
| demoCsrfCredentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |
| demoSessionCredentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md) | The Credentials Setter for Custom Header Signature |

The API client can be initialized as follows:

```go
package main

import (
    "tradeglotlocalconsole"
)

func main() {
    client := tradeglotlocalconsole.NewClient(
    tradeglotlocalconsole.CreateConfiguration(
            tradeglotlocalconsole.WithHttpConfiguration(
                tradeglotlocalconsole.CreateHttpConfiguration(
                    tradeglotlocalconsole.WithTimeout(0),
                ),
            ),
            tradeglotlocalconsole.WithDemoCsrfCredentials(
                tradeglotlocalconsole.NewDemoCsrfCredentials("X-CSRF-Token"),
            ),
            tradeglotlocalconsole.WithDemoSessionCredentials(
                tradeglotlocalconsole.NewDemoSessionCredentials("X-Demo-Session"),
            ),
        ),
    )
}
```


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| xCSRFToken | `string` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `WithXCSRFToken` | `XCSRFToken()` |



**Note:** Required auth credentials can be set using `WithDemoCsrfCredentials()` by providing a credentials instance with `NewDemoCsrfCredentials()` in the configuration initialization and accessed using the `DemoCsrfCredentials()` method in the configuration instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```go
package main

import (
    "tradeglotlocalconsole"
)

func main() {
    client := tradeglotlocalconsole.NewClient(
    tradeglotlocalconsole.CreateConfiguration(
            tradeglotlocalconsole.WithDemoCsrfCredentials(
                tradeglotlocalconsole.NewDemoCsrfCredentials("X-CSRF-Token"),
            ),
        ),
    )
}
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Setter | Getter |
|  --- | --- | --- | --- | --- |
| xDemoSession | `string` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `WithXDemoSession` | `XDemoSession()` |



**Note:** Required auth credentials can be set using `WithDemoSessionCredentials()` by providing a credentials instance with `NewDemoSessionCredentials()` in the configuration initialization and accessed using the `DemoSessionCredentials()` method in the configuration instance.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```go
package main

import (
    "tradeglotlocalconsole"
)

func main() {
    client := tradeglotlocalconsole.NewClient(
    tradeglotlocalconsole.CreateConfiguration(
            tradeglotlocalconsole.WithDemoSessionCredentials(
                tradeglotlocalconsole.NewDemoSessionCredentials("X-Demo-Session"),
            ),
        ),
    )
}
```


# Test the SDK

`Go Testing` is used as the testing framework. To run the unit tests of the SDK, navigate to the root directory of the SDK and run the following command in the terminal:

```bash
$ go test
```



