# Connections Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Mode` | [`ModeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/mode.md) | Required | Mode. | ModeEnum getMode() | setMode(ModeEnum mode) |
| `SandboxReads` | [`ConnectionsResponseSandboxReads`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/connections-response-sandbox-reads.md) | Optional | This is a container for any-of cases. | ConnectionsResponseSandboxReads getSandboxReads() | setSandboxReads(ConnectionsResponseSandboxReads sandboxReads) |


# Example

```java
import m18000.m0.m0.m127.models.ConnectionsResponse;
import m18000.m0.m0.m127.models.ModeEnum;
import m18000.m0.m0.m127.models.containers.ConnectionsResponseSandboxReads;

ConnectionsResponse connectionsResponse = new ConnectionsResponse.Builder(
    ModeEnum.LOCAL
)
.sandboxReads(ConnectionsResponseSandboxReads.fromBoolean(
        true
    ))
.build();
```



