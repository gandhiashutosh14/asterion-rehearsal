# Primary references and claim boundaries

Consulted 2026-09-16. These sources support design choices; they do not validate ASTERION, certify it, or establish its novelty.

| Source | Used for | Not inferred |
|---|---|---|
| [Google SRE: evolving engagement model](https://sre.google/sre-book/evolving-sre-engagement-model/) | Operational requirements and production-readiness review context | A quantified industry failure rate or customer demand statistic |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | State-oriented agent orchestration | That this package's optional integration passed tests |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Checkpointer, thread ID, resume and node restart behavior | Exactly-once external effects from checkpointing |
| [LangGraph PyPI](https://pypi.org/project/langgraph/) | Optional distribution pin; page observed with 1.2.10 | That this is the newest version in every package-index cache |
| [Boto3 Bedrock Converse](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/converse.html) | Optional proposer request shape | Model access, inference price or successful live call |
| [GitHub OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) | Exact repository/environment subject restriction | That a GitHub environment is already configured or protected |
| [ECS task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) | Workload identity boundary | That the sample is deployed to ECS |
| [Azure Container Apps managed identity](https://learn.microsoft.com/en-us/azure/container-apps/managed-identity) | Azure responsibility mapping and workload identity | Implemented Azure SDK integration |

All numerical project results come from local synthetic execution recorded under `reports/`, not external marketing claims. The personal resume was used only to choose relevant engineering seams; its private contents are not included. No company-specific product weakness or hiring outcome is asserted.
