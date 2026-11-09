# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal.

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
        ),
    )
}
```


# Test the SDK

`Go Testing` is used as the testing framework. To run the unit tests of the SDK, navigate to the root directory of the SDK and run the following command in the terminal:

```bash
$ go test
```



