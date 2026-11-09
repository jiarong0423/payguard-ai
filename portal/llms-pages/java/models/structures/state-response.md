# State Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Class Name

`StateResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Activity` | [`List<Activity>`](http://localhost:3000/llms-pages/java/models/structures/activity.md) | Required | Activity. | List<Activity> getActivity() | setActivity(List<Activity> activity) |
| `Disputes` | [`List<DisputeSummary>`](http://localhost:3000/llms-pages/java/models/structures/dispute-summary.md) | Required | Disputes. | List<DisputeSummary> getDisputes() | setDisputes(List<DisputeSummary> disputes) |
| `ExpiresAt` | `String` | Required | Expires at. | String getExpiresAt() | setExpiresAt(String expiresAt) |
| `PolicyVersion` | `String` | Required | Policy version. | String getPolicyVersion() | setPolicyVersion(String policyVersion) |
| `Scenario` | [`Scenario`](http://localhost:3000/llms-pages/java/models/structures/scenario.md) | Required | Scenario. | Scenario getScenario() | setScenario(Scenario scenario) |
| `SessionId` | `String` | Required | Session id. | String getSessionId() | setSessionId(String sessionId) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `Transactions` | [`List<Transaction>`](http://localhost:3000/llms-pages/java/models/structures/transaction.md) | Required | Transactions. | List<Transaction> getTransactions() | setTransactions(List<Transaction> transactions) |
| `Velocity` | [`VelocityResponse`](http://localhost:3000/llms-pages/java/models/structures/velocity-response.md) | Required | VelocityResponse. | VelocityResponse getVelocity() | setVelocity(VelocityResponse velocity) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.Activity;
import m18000.m0.m0.m127.models.BaselineProvenanceEnum;
import m18000.m0.m0.m127.models.DisputeSummary;
import m18000.m0.m0.m127.models.Scenario;
import m18000.m0.m0.m127.models.StateResponse;
import m18000.m0.m0.m127.models.Status14Enum;
import m18000.m0.m0.m127.models.Status7Enum;
import m18000.m0.m0.m127.models.SyntheticMoney;
import m18000.m0.m0.m127.models.Transaction;
import m18000.m0.m0.m127.models.VelocityResponse;
import m18000.m0.m0.m127.models.containers.VelocityResponseCurrency;
import m18000.m0.m0.m127.models.containers.VelocityResponseRatio;

StateResponse stateResponse = new StateResponse.Builder(
    Arrays.asList(
        new Activity.Builder(
            "at4",
            "id8",
            "kind6",
            "label8",
            "synthetic"
        )
        .build()
    ),
    Arrays.asList(
        new DisputeSummary.Builder(
            "case_ref6",
            new SyntheticMoney.Builder(
                "currency_code6",
                "value0"
            )
            .build(),
            "opened_at0",
            "order_ref8",
            "reason2",
            "seller_response_due_date0",
            Status7Enum.NEEDS_REVIEW
        )
        .build()
    ),
    "expires_at6",
    "policy_version8",
    new Scenario.Builder(
        false,
        false
    )
    .build(),
    "session_id2",
    "synthetic",
    Arrays.asList(
        new Transaction.Builder(
            "amount0",
            "currency8",
            "occurred_at2",
            "order_id2"
        )
        .build()
    ),
    new VelocityResponse.Builder(
        "True",
        false,
        "baseline_amount_per_hour0",
        BaselineProvenanceEnum.SYNTHETIC_BASELINE,
        "baseline_window_end2",
        "baseline_window_start4",
        VelocityResponseCurrency.fromString(
            "String7"
        ),
        "current_amount_per_hour0",
        240,
        132,
        Arrays.asList(
            "limitations7"
        ),
        "policy_version4",
        VelocityResponseRatio.fromString(
            "String5"
        ),
        Status14Enum.INSUFFICIENT_BASELINE,
        "threshold4",
        "total_amount2",
        112,
        "left_open_right_closed",
        "window_end6",
        2,
        "window_start8"
    )
    .build()
)
.build();
```



