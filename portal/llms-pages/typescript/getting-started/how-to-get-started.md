# How to Get Started

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0aCUyRl9fZ2V0dGluZ19zdGFydGVk


# Introduction

API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal. Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin (browsers add it; scripts must set it), otherwise the API answers 403 origin_required.


# Building

## Requirements

The SDK relies on **Node.js** and **npm** (to resolve dependencies). It also requires **Typescript version >=4.1**. You can download and install Node.js and [npm](https://www.npmjs.com/) from [the official Node.js website](https://nodejs.org/en/download/).

> **NOTE:** npm is installed by default when Node.js is installed.

## Verify Successful Installation

Run the following commands in the command prompt or shell of your choice to check if Node.js and npm are successfully installed:

* Node.js: `node --version`

* npm: `npm --version`

![Version Check](https://apidocs.io/illustration/typescript?workspaceFolder=TradeGlotLocalConsole&step=versionCheck)

## Install Dependencies

- To resolve all dependencies, go to the **SDK root directory** and run the following command with npm:

```bash
npm install
```

- This will install all dependencies in the **node_modules** folder.

![Resolve Dependencies](https://apidocs.io/illustration/typescript?workspaceFolder=TradeGlotLocalConsole&workspaceName=tradeglot-local-consolelib&step=resolveDependency)


# Installation

The following section explains how to use the generated library in a new project.

## 1. Initialize the Node Project

- Open an IDE/text editor for JavaScript like Visual Studio Code. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

- Click on **File** and select **Open Folder**. Select an empty folder of your project, the folder will become visible in the sidebar on the left.

![Open Folder](https://apidocs.io/illustration/typescript?step=openProject)

- To initialize the Node project, click on **Terminal** and select **New Terminal**. Execute the following command in the terminal:

```bash
npm init --y
```

![Initialize the Node Project](https://apidocs.io/illustration/typescript?step=initializeProject)

## 2. Add Dependencies to the Client Library

- The created project manages its dependencies using its `package.json` file. In order to add a dependency on the *TradeGlot Local ConsoleLib* client library, double click on the `package.json` file in the bar on the left and add the dependency to the package in it.

![Add TradeglotLocalConsolelib Dependency](https://apidocs.io/illustration/typescript?workspaceFolder=TradeGlotLocalConsole&workspaceName=tradeglot-local-consolelib&step=importDependency)

- To install the package in the project, run the following command in the terminal:

```bash
npm install
```

![Install TradeglotLocalConsolelib Dependency](https://apidocs.io/illustration/typescript?step=installDependency)



# Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| timeout | `number` | Timeout for API calls.<br>*Default*: `0` |
| httpClientOptions | [`Partial<HttpClientOptions>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/configuration/httpclientoptions.md) | Stable configurable http client options. |
| unstableHttpClientOptions | `any` | Unstable configurable http client options. |
| demoCsrfCredentials | [`DemoCsrfCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/getting-started/how-to-get-started/authorization.md) | The credential object for demoCsrf |
| demoSessionCredentials | [`DemoSessionCredentials`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/getting-started/how-to-get-started/authorization.md) | The credential object for demoSession |

The API client can be initialized as follows:

## Code-Based Client Initialization

```ts
import { Client } from 'tradeglot-local-consolelib';

const client = new Client({
  demoCsrfCredentials: {
    'X-CSRF-Token': 'X-CSRF-Token'
  },
  demoSessionCredentials: {
    'X-Demo-Session': 'X-Demo-Session'
  },
  timeout: 0,
});
```

## Configuration-Based Client Initialization

```ts
import * as path from 'path';
import * as fs from 'fs';
import { Client } from 'tradeglot-local-consolelib';

// Provide absolute path for the configuration file
const absolutePath = path.resolve('./config.json');

// Read the configuration file content
const fileContent = fs.readFileSync(absolutePath, 'utf-8');

// Initialize client from JSON configuration content
const client = Client.fromJsonConfig(fileContent);
```

See the [Configuration-Based Client Initialization](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/configuration/configuration-based-client-initialization.md) section for details.

## Environment-Based Client Initialization

```ts
import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';
import { Client } from 'tradeglot-local-consolelib';

// Optional - Provide absolute path for the .env file
const absolutePath = path.resolve('./.env');

if (fs.existsSync(absolutePath)) {
  // Load environment variables from .env file
  dotenv.config({ path: absolutePath, override: true });
}

// Initialize client using environment variables
const client = Client.fromEnvironment(process.env);
```

See the [Environment-Based Client Initialization](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/configuration/environment-based-client-initialization.md) section for details.


# Authorization

This API uses the following authentication schemes.

* [`DemoCsrf (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/getting-started/how-to-get-started/authorization.md)
* [`DemoSession (Custom Header Signature)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/getting-started/how-to-get-started/authorization.md)

## DemoCsrf (Custom Header Signature)



Documentation for accessing and setting credentials for DemoCsrf.

### Auth Credentials

| Name | Type | Description | Setter |
|  --- | --- | --- | --- |
| X-CSRF-Token | `string` | CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. Every POST also needs it; without it the API answers 403 csrf_rejected. | `xCSRFToken` |



**Note:** Auth credentials can be set using `demoCsrfCredentials` object in the client.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```ts
import { Client } from 'tradeglot-local-consolelib';

const client = new Client({
  demoCsrfCredentials: {
    'X-CSRF-Token': 'X-CSRF-Token'
  },
});
```

## DemoSession (Custom Header Signature)



Documentation for accessing and setting credentials for DemoSession.

### Auth Credentials

| Name | Type | Description | Setter |
|  --- | --- | --- | --- |
| X-Demo-Session | `string` | Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions (that request needs no header). Without it the API answers 401 session_required. | `xDemoSession` |



**Note:** Auth credentials can be set using `demoSessionCredentials` object in the client.

### Usage Example

#### Client Initialization

You must provide credentials in the client as shown in the following code snippet.

```ts
import { Client } from 'tradeglot-local-consolelib';

const client = new Client({
  demoSessionCredentials: {
    'X-Demo-Session': 'X-Demo-Session'
  },
});
```


# Test the SDK

To validate the functionality of this SDK, you can execute all tests located in the `test` directory. This SDK utilizes `Jest` as both the testing framework and test runner.

To run the tests, navigate to the root directory of the SDK and execute the following command:

```bash
npm run test
```

Or you can also run tests with coverage report:

```bash
npm run test:coverage
```



