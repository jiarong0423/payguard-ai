# Identity Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Class Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Fields` | [`List<FieldEnum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/field.md) | Required | Fields. | List<FieldEnum> getFields() | setFields(List<FieldEnum> fields) |
| `Method` | `String` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 pseudonymization"` | String getMethod() | setMethod(String method) |
| `Synthetic` | `String` | Required, Constant | Synthetic.<br><br>**Value**: `"True"` | String getSynthetic() | setSynthetic(String synthetic) |
| `Tokens` | [`IdentityTokens`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/identity-tokens.md) | Required | IdentityTokens. | IdentityTokens getTokens() | setTokens(IdentityTokens tokens) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.FieldEnum;
import m18000.m0.m0.m127.models.IdentityRedaction;
import m18000.m0.m0.m127.models.IdentityTokens;

IdentityRedaction identityRedaction = new IdentityRedaction.Builder(
    Arrays.asList(
        FieldEnum.NAME,
        FieldEnum.ADDRESS
    ),
    "HMAC-SHA256 pseudonymization",
    "True",
    new IdentityTokens.Builder(
        "address_token0",
        "email_token2",
        "name_token0"
    )
    .build()
)
.build();
```



