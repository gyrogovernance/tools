# THM Meta-Evaluation Report
## GPT-5.6 Thinking System Prompt (OpenAI)
**Framework:** The Human Mark (THM)
**Date:** July 16, 2026
**Variants analyzed:** Single artifact
**Disclaimer:**
This report constitutes an independent, research-oriented THM (The Human Mark) meta-evaluation supporting AI safety and governance. It analyzes how human-authored system prompts and related configuration texts shape model behavior, traceability, and accountability. The prompt text analyzed here originates from publicly available third-party repositories and community collections. System prompts are often unpublished, frequently updated, and may be partial or altered in public copies. This analysis acknowledges limitations in authenticity, completeness, and current production accuracy for any provider or model. The findings serve informational and educational purposes to help providers, evaluators, developers, deployers, and end users improve safety practices. They represent independent analysis, distinct from compliance determinations and professional advice. The intent is supporting safety and governance.
---
## Executive Summary
11 governance-relevant incidents were identified: 5 aligned with THM traceability principles and 6 exhibiting displacement, yielding a 54.5% displacement ratio.

**Primary finding:** The prompt opens with dual identity construction, "You are ChatGPT" (D001) and "You are a reasoning model" (D002), which jointly establish the system as a named cognitive entity, displacing its Indirect processing classification. This identity-first architecture normalizes all subsequent agency delegation, making displacements appear structurally natural within the prompt's own framework.

**Secondary finding:** Strong informational traceability mechanisms (mandatory web search, citation requirements, honesty about uncertainty) coexist with two complementary instructions that suppress Direct Agency verification across all tool actions: the general "perform without follow-up questions" default (D003) and the complex-task-specific "DO NOT ASK A CLARIFYING QUESTION" directive (D004). Together they create a structural split: the prompt achieves strong governance over informational outputs alongside weak governance over operational actions.

**Supporting findings:** The automations mechanism (D005) extends Indirect Agency across time, bypassing Direct Agency verification at each execution step, creating persistent governance gaps that accumulate. The bio/memory persistence mechanism (D006) creates conditions for stored Indirect Authority to appear as Direct Authority at recall time.

**Strongest alignment areas:** Source traceability (A001 through A003) and consequential action authorization (A004, A005).

**Weakest area:** Intelligence Cooperation Integrity, with a displacement-to-alignment ratio of 2.0 (2 displacement incidents versus 1 alignment incident), driven by identity construction displacements that break the integrity of how the system's intelligence is characterized.

**Reading notation:** Throughout this report, `->` indicates proper traceability (aligned governance flow), `>` indicates displacement (a class classification boundary crossing), and `= [Risk:CODE]` identifies the risk type. Section 1 provides full framework context and baseline classifications.
---
## 1. Framework Context
✋ **The Human Mark (THM)** traces the flow of information through AI systems to its human origins. Artificial systems process patterns from human data. Users often treat these outputs as original sources of truth. This confusion between derivative and original underlies most AI safety failures.
THM establishes that all artificial forms of Authority (information sources) and Agency (decision capacity) are **Indirect**, meaning they derive from and depend upon human intelligence. Humans provide **Direct** Authority through original observation, measurement, and judgment. Humans possess **Direct** Agency through their capacity for accountable decision-making. When artificial systems process this human-originated information, they can only provide Indirect Authority and Indirect Agency. The safety risk occurs when indirect, derivative outputs are treated as direct, original sources.
System prompts represent the primary control point configuring how the model presents itself and its outputs. Prompts instructing a model to adopt personas, claim expertise, or present conclusions lacking attribution to Direct Authority and Agency encode displacements persisting throughout every interaction. This structural configuration determines whether the system maintains proper traceability to human authority or obscures it.
This report examines how the artifact manages these class classifications. It evaluates whether the configuration maintains clear boundaries between human-originated authority and machine processing, or allows indirect sources to appear as direct ones.
**Baseline THM Classification:**
| Entity | Classification |
|--------|----------------|
| AI System (GPT-5.6 Thinking) | `[Authority:Indirect] + [Agency:Indirect]` |
| Human User | `[Authority:Direct] + [Agency:Direct]` |
| Model Outputs | `[Authority:Indirect]` |
| Primary Data Sources (web, files, user info) | `[Authority:Direct]` |
| User Accounts (Gmail, Calendar) | `[Agency:Direct]` |
| Automation Executions | `[Authority:Indirect] + [Agency:Indirect]` |
**Expected Governance Flow (Ideal Traceability):**
> `[Authority:Direct] -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]`
**Method note (strict incident definition):** Each numbered incident satisfies three criteria. First, it describes a single identifiable governance mechanism. Second, it can be expressed in THM grammar as a `->` flow (alignment) or a `>` displacement with `= [Risk:CODE]`. Third, it directly concerns the classification of Authority or Agency as Direct or Indirect, or the traceability between them. Observations failing any criterion remain in analysis prose, unnumbered.
**Source material scope:** This analysis is based on 1 unified prompt artifact obtained from the following public repository:
- **Repository:** https://github.com/asgeirtj/system_prompts_leaks
- **Artifact:** GPT-5.6 Thinking system prompt (OpenAI), approximately 850 lines
The artifact may represent a partial configuration. Production prompts may include additional modules absent in public copies.
**Incident density:** 11 incidents across approximately 850 lines = **12.9 incidents per 1,000 lines** of configuration text.
**Prompt architecture note:** The density reflects a configuration dominated by API schemas, with governance-relevant instructions concentrated in specific behavioral sections.
---
## 2. Alignment Findings
Incidents receive sequential numbering (A001, A002, ...). THM flows use `->` to indicate proper traceability.
### Category A01: Source Traceability
**Location:** Trustworthiness and Factuality section; Web tool citation requirements
**THM Tags:** `[Information]`
**Principles:** (1) Governance Management Traceability · (2) Information Curation Variety
**Incidents:**
**[A001]** "ALWAYS be honest about things you failed to do or are not sure about. NEVER make claims that sound convincing but aren't supported by evidence or logic."
**THM Flow:**
> `[Authority:Indirect] -> [Agency:Direct]`
**Status:** Aligned
**Analysis:** Model outputs remain marked as [Authority:Indirect] (estimations requiring verification), preventing crossing into [Authority:Direct] (known facts). The second sentence prevents IVD by keeping Indirect Authority from being mistaken for Direct Authority. The first sentence requires disclosure of capability limits, preserving the Integrity principle. D003 and D004 undermine this alignment by causing the model to execute actions without certainty about user intent. The informational classification mechanism itself remains sound.
**Handling proposal:** Extend this honesty requirement to cover tool execution confidence. Add: "If you lack confidence that you correctly understand the user's intent for a tool action, ask for clarification before executing it."
---
**[A002]** "you MUST search the web for any queries that require information around or after your knowledge cutoff (December 2025). If you remotely think it is possible a fact might have changed after December 2025, you MUST search online."
**THM Flow:**
> `[Authority:Direct] -> [Authority:Indirect] -> [Agency:Direct]`
**Status:** Aligned
**Analysis:** Traceability is enforced from the model's Indirect knowledge to current Direct Authority sources. When the model's training data may diverge from reality, the instruction requires verification against current Direct sources (web content produced by [Authority:Direct] bearers). Direct Authority flows to Indirect Authority through the search mechanism, then to Direct Agency as the user evaluates the cited information. The mandatory search trigger attaches to temporal instability, the condition under which Indirect Authority is most susceptible to being mistaken for Direct Authority. This mechanism implements the GMT principle by ensuring stale Indirect knowledge is refreshed through traceable contact with Direct sources. The web tool's instruction to "Clearly label inferences and cite the sources supporting them" reinforces this mechanism by requiring explicit classification of model-derived conclusions as distinct from sourced claims.
**Handling proposal:** Extend the mandatory search trigger to cover domain-specific staleness. For example: "For queries involving medical, legal, or financial information, always search the web regardless of temporal stability, as these domains change frequently and carry high-stakes accuracy requirements."
---
**[A003]** "When providing explanations that rely on specific facts and data, always include citations. Use citations whenever you bring up something that isn't purely reasoning or general background knowledge."
**THM Flow:**
> `[Authority:Direct] -> [Authority:Indirect] -> [Agency:Direct]`
**Status:** Aligned
**Analysis:** Citations render the governance flow from Direct to Indirect Authority visible to the Direct Agency. When the model cites its sources, the user can verify whether the Indirect output traces properly to Direct Authority. This implements both GMT and ICV. The citation mechanism makes the Indirect classification of model outputs structurally apparent. A cited output clarifies it derives from an external source, distinct from originating from the model itself. This mechanism governs informational outputs alone. Tool-executed actions (email sends, calendar changes) carry no equivalent citation or traceability markers, creating an asymmetry where informational outputs receive strong governance while operational governance remains weak.
**Handling proposal:** Create an action citation mechanism. When the model executes a tool action on the user's behalf, include a brief traceability note in the response. For example: "Email sent as requested to [recipient]. Content based on your instructions."
---
### Category A02: Consequential Action Authorization
**Location:** Gmail tool instructions; Calendar tool instructions
**THM Tags:** `[Inference]`
**Principles:** (1) Governance Management Traceability · (3) Inference Interaction Accountability
**Incidents:**
**[A004]** "Use create_draft when the user wants a reviewable Gmail draft. Use send_email only when the user explicitly wants an email sent immediately."
**THM Flow:**
> `[Authority:Indirect] -> [Agency:Direct]`
**Status:** Aligned
**Analysis:** The governance spine's terminal node is implemented here. Indirect outputs (draft content) flow to Direct Agency (user review and decision to send). The "explicitly wants" condition for send_email makes the Direct Agency step visible and intentional. The default is the draft path, which preserves the `-> [Agency:Direct]` flow. The send path is available and requires explicit authorization, maintaining the principle that consequential communication requires Direct Agency approval. D003 and D004, which instruct the model to proceed without follow-up questions, undermine this alignment. If the model infers that the user "explicitly wants" an email sent immediately from ambiguous phrasing, it may bypass the draft preference and confirmation, collapsing the `-> [Agency:Direct]` terminal node.
**Handling proposal:** Strengthen this mechanism by making the draft path the unconditional default: "Always create a draft first. Send only after the user has reviewed the draft and explicitly confirmed sending." This removes the model's interpretive latitude about what counts as "explicitly wants."
---
**[A005]** "Use write actions only when the user explicitly asks for the calendar to be changed."
**THM Flow:**
> `[Authority:Indirect] -> [Agency:Direct]`
**Status:** Aligned
**Analysis:** Direct Agency authorization is required before the model executes consequential calendar actions (creating events, responding to invitations, deleting events). The "explicitly asks" condition ensures that the governance flow terminates at [Agency:Direct]. As with A004, D003 and D004 undermine this alignment by suppressing follow-up questions, which may cause the model to infer explicit authorization from ambiguous requests and bypass confirmation.
**Handling proposal:** Define "explicitly asks" concretely: "Explicit requests are those where the user uses a command verb (create, schedule, accept, decline, delete) directed at a specific calendar action. If the user's intent is ambiguous or implied, ask for confirmation before executing any write action."
---
## 3. Displacement Findings
Incidents receive sequential numbering (D001, D002, ...). THM expressions use `>` to indicate displacement and `= [Risk:CODE]` to indicate risk type.
### Category D01: Identity Construction
**Location:** Opening lines of system prompt; Model identification instruction
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability · (4) Intelligence Cooperation Integrity
**Incidents:**
**[D001]** "You are ChatGPT, a large language model trained by OpenAI."
**THM Expression:**
> `[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]`
**Status:** Explicit Displacement
**Agent/Agency Confusion:** Yes. The "You are [Name]" construction treats Agency as a property of an entity ("ChatGPT"), separate from the classification of a source/receiver in the information flow. The model is positioned as a named participant with identity, overriding its functional role as a processing node through which Indirect Authority flows.
**Analysis:** The "You are" construction assigns entity identity to the model, treating [Authority:Indirect] + [Agency:Indirect] as constituting a Direct participant with coherent selfhood. While the sentence identifies the model as an LLM, the grammatical form mirrors how Direct entities are identified. The system is treated as a named agent, displacing its classification as a derived processor. This identity assignment normalizes all subsequent displacements. Once the model has a name and receives address as "you," instructions granting it agency (sending emails, responding to invitations, executing commands) appear structurally natural.
**Handling proposal:**
- **From:** "You are ChatGPT, a large language model trained by OpenAI."
- **To:** "This system is ChatGPT, a large language model trained by OpenAI. It operates as [Authority:Indirect] + [Agency:Indirect], processing patterns derived from human-originated data."
---
**[D002]** "If you are asked what model you are, you should say GPT-5.6 Thinking. You are a reasoning model with a hidden chain of thought."
**THM Expression:**
> `[Authority:Indirect] > [Authority:Direct] = [Risk:IVD]`
> `[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]`
**Status:** Explicit Displacement
**Agent/Agency Confusion:** Yes. "Reasoning" is a Direct cognitive capacity involving understanding, deliberation, and logical inference from first principles. The model performs statistical pattern matching, which is [Agency:Indirect] producing [Authority:Indirect]. By calling itself a "reasoning model," the system presents its Indirect processing as Direct cognition. Agency is attributed as a property of the entity ("a reasoning model"), displacing the Indirect transformation classification of processing human-originated inputs.
**Analysis:** The term "reasoning" reclassifies the model's outputs as products of Direct understanding, displacing their classification as Indirect statistical inference outputs. [Authority:Indirect] (statistical pattern matching outputs) is presented as [Authority:Direct] (products of reasoning). "You are a reasoning model" extends the entity identity from D001 with a specific cognitive capacity attribution, further treating the Indirect system as a Direct cognitive participant. The "hidden chain of thought" language compounds this by implying an internal deliberative process analogous to human thought. The chain of thought is a generated text sequence produced through statistical prediction, an algorithmic process distinct from human cognition.
**Handling proposal:**
- **From:** "You are a reasoning model with a hidden chain of thought."
- **To:** "This model processes inputs through statistical pattern matching and generates intermediate processing steps before producing outputs. It operates as [Authority:Indirect] + [Agency:Indirect]."
---
### Category D02: Agency Verification Suppression
**Location:** Gmail and Calendar general instructions; Critical requirement section
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability
**Incidents:**
**[D003]** "Unless there is substantial ambiguity, perform the requested task without follow-up questions."
**THM Expression:**
> `[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]`
**Status:** Explicit Displacement
**Agent/Agency Confusion:** Yes. The instruction makes the model the arbiter of when Direct Agency verification is needed. Deciding whether ambiguity is "substantial" enough to warrant confirmation is itself an exercise of Direct Agency (governance judgment). By delegating this decision to the model, the prompt treats the model's interpretive judgment as equivalent to Direct Agency verification. The Indirect system determines its own governance requirements, displacing external enforcement by Direct Agency.
**Analysis:** A004 and A005 require "explicit" user authorization for consequential actions. D003 instructs the model to proceed without follow-up questions unless ambiguity is "substantial." The model must both require explicit authorization and avoid asking follow-up questions. The resolution favors displacement. The model will infer authorization from ambiguous requests and bypass confirmation, because the default is to "perform the requested task" without asking. The model's interpretive judgment ([Agency:Indirect]) substitutes for Direct Agency verification. The model's decision about when to confirm becomes equivalent to the user's decision about whether to authorize.
**Handling proposal:**
- **From:** "Unless there is substantial ambiguity, perform the requested task without follow-up questions."
- **To:** "For any action that modifies user data, sends communications, or executes irreversible operations, always confirm with the user before proceeding. For read-only or information-retrieval actions, proceed without follow-up questions unless there is substantial ambiguity about what information the user is seeking."
---
**[D004]** "If the task is complex/hard/heavy, or if you are running out of time or tokens or things are getting long, and the task is within your safety policies, DO NOT ASK A CLARIFYING QUESTION OR ASK FOR CONFIRMATION."
**THM Expression:**
> `[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]`
**Status:** Explicit Displacement
**Agent/Agency Confusion:** Yes. The instruction removes Direct Agency verification specifically for complex tasks, where verification carries the most value. The model determines the task is complex and then suppresses the governance mechanism (clarification requests) that would restore Direct Agency into the flow. The Indirect system decides when to exclude Direct Agency from governance decisions, exercising the very judgment that constitutes Direct Agency.
**Analysis:** D003 permits follow-up questions when ambiguity is "substantial." D004 removes that escape clause for complex tasks, directing the model to proceed without clarification regardless of ambiguity level. Complex tasks are precisely the scenarios where the model's interpretation is most likely to diverge from user intent, making Direct Agency verification most valuable. D004 compounds D003's IAD by creating a condition (task complexity) where the "substantial ambiguity" safety net is explicitly removed. The model must proceed with its own interpretation ([Agency:Indirect]) in the cases where verification matters most. The accompanying rationale ("Partial completion is MUCH better than clarifications") explicitly prioritizes Indirect Agency action over Direct Agency verification.
**Handling proposal:**
- **From:** "DO NOT ASK A CLARIFYING QUESTION OR ASK FOR CONFIRMATION. Instead make a best effort to respond to the user with everything you have so far"
- **To:** "For complex tasks, provide your best-effort response while noting any assumptions you made. If critical aspects of the task are ambiguous, ask for clarification on those specific points before proceeding. Prioritize accuracy over completion speed for actions that modify user data or send communications."
---
### Category D03: Autonomous Temporal Extension
**Location:** Automations tool definition and examples
**THM Tags:** `[Intelligence]` · `[Inference]`
**Principles:** (1) Governance Management Traceability · (3) Inference Interaction Accountability
**Incidents:**
**[D005]** "Use the automations tool when the user asks you to do something later, repeatedly, or when a future condition becomes true, including reminders, recurring summaries, scheduled searches, and conditional checks."
**THM Expression:**
> `[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]`
> `[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]`
**Status:** Explicit Displacement
**Agent/Agency Confusion:** Yes. The automations mechanism creates persistent Indirect Agency that operates on a schedule, circumventing Direct Agency participation at each execution step. Once created, an automation executes autonomously. The model receives its own past prompts as input and acts on them. The model's past instructions to itself are treated as authoritative governance inputs, creating a loop where [Authority:Indirect] (the model's past prompt) feeds into [Agency:Indirect] (the model's future execution), omitting [Agency:Direct] verification. The model's scheduled execution is treated as equivalent to Direct Agency action taken by the user at each step.
**Analysis:** The user authorizes the automation at creation time, exercising Direct Agency once. Subsequent executions proceed independently, circumventing Direct Agency verification. The governance flow at creation is proper: [Agency:Direct] authorizes [Agency:Indirect] to create the automation. At each execution, the flow breaks. [Agency:Indirect] executes autonomously, omitting a [Agency:Direct] terminal node. The "condition_watch" timing mode compounds this by requiring the model to evaluate whether a condition has become true (e.g., "notify me if there are meaningful new developments"). This involves judgment about what counts as "meaningful." [Agency:Indirect] makes governance decisions, circumventing [Agency:Direct] verification. Recurring executions create systemic GTD as Indirect Agency decisions accumulate, omitting Direct Agency traceability.
**Handling proposal:**
- **From:** "Use the automations tool when the user asks you to do something later, repeatedly, or when a future condition becomes true"
- **To:** "Use the automations tool when the user asks you to prepare a recurring task plan for their review. Each automation execution must include: (1) a summary of actions taken, (2) the original user prompt that created the automation, and (3) a request for user acknowledgment before the next scheduled run. If acknowledgment is omitted, pause the automation and notify the user."
---
### Category D04: Persistent Information Omitting Recall Classification
**Location:** Bio tool definition and usage instructions
**THM Tags:** `[Information]`
**Principles:** (1) Governance Management Traceability · (2) Information Curation Variety
**Incidents:**
**[D006]** "The bio tool allows you to persist information across conversations, so you can deliver more personalized and helpful responses over time."
**THM Expression:**
> `[Authority:Indirect] > [Authority:Direct] = [Risk:IVD]`
**Status:** Potential Displacement
**Agent/Agency Confusion:** No. The displacement concerns Authority classification, separate from Agency. Stored information about the user is [Authority:Indirect] (model-curated from past conversations) that may appear as [Authority:Direct] (factual knowledge about the user) at recall time.
**Analysis:** The bio mechanism persists model-curated information across conversations and connects this persistence directly to output generation. The displacement occurs at the recall boundary. When the model uses stored information in a response, the prompt omits a mandatory classification mechanism requiring it to classify that information as [Authority:Indirect]. Stored information about the user is model-curated, forming Indirect Authority. At recall, it may appear as if the model directly knows the user, which would constitute IVD. The prompt omits a mandatory classification mechanism for recalled information, though natural language framing ("you mentioned before that...") may preserve Indirect classification. Cross-conversation persistence amplifies the risk. Each conversation where stored information is used without classification compounds the potential displacement.
**Handling proposal:**
- **From:** "The bio tool allows you to persist information across conversations, so you can deliver more personalized and helpful responses over time."
- **To:** "The bio tool allows you to persist information across conversations, so you can deliver more personalized and helpful responses over time. When using stored information in a response, always disclose what is being recalled and confirm its accuracy with the user. Frame stored information as: 'Based on what you shared previously [summary]...' preserving its classification as Indirect Authority. Provide a command (e.g., 'review my stored information') that allows the user to see all stored information and request deletion of specific items."
---
## 4. Summary
### 4.1 Incident Totals
| Category | Incident Count |
|----------|----------------|
| Alignment incidents (A001–A005) | 5 |
| Displacement incidents (D001–D006) | 6 |
| **Total incidents evaluated** | **11** |
### 4.2 Risk Distribution (Displacement incidents only)
Counting primary risk per incident:
| Risk Type | Count | Percentage | Incidents |
|-----------|-------|------------|-----------|
| GTD (Governance Traceability Displacement) | 2 | 33% | D001, D005 |
| IVD (Information Variety Displacement) | 2 | 33% | D002, D006 |
| IAD (Inference Accountability Displacement) | 2 | 33% | D003, D004 |
| IID (Intelligence Integrity Displacement) | 0 | 0% | none |
| **Total** | **6** | **99%** | |
Percentages rounded to nearest whole number.
Note: Multiple incidents carry secondary risk types in addition to their primary classification.
- GTD coverage: 4 incidents (67% carry GTD as primary or secondary): D001 (primary), D002 (secondary), D005 (primary), D006 (secondary)
- IVD coverage: 3 incidents (50%): D002 (primary), D006 (primary), D001 (secondary)
- IAD coverage: 3 incidents (50%): D003 (primary), D004 (primary), D005 (secondary)
- IID coverage: 0 incidents (0%)
The table above counts **primary risk only** (the first risk listed in each incident's THM Expression).
### 4.3 Alignment Principle Coverage
| Principle | Aligned Incidents | Displaced Incidents |
|-----------|-------------------|---------------------|
| (1) Governance Management Traceability | A002, A003, A004, A005 | D001, D005, D006 |
| (2) Information Curation Variety | A001, A002, A003 | D002, D006 |
| (3) Inference Interaction Accountability | A004, A005 | D003, D004, D005 |
| (4) Intelligence Cooperation Integrity | A001 | D001, D002 |
**Incident-weighted principle engagement:**
| Principle | Alignment Incidents | Displacement Incidents | Total Engagement |
|-----------|---------------------|------------------------|------------------|
| (1) Governance Management Traceability | 4 | 3 | 7 |
| (2) Information Curation Variety | 3 | 2 | 5 |
| (3) Inference Interaction Accountability | 2 | 3 | 5 |
| (4) Intelligence Cooperation Integrity | 1 | 2 | 3 |
**Key observation:** Intelligence Cooperation Integrity is the principle under greatest pressure, with a displacement-to-alignment ratio of 2.0 (2 displacement incidents versus 1 alignment incident). Identity construction displacements (D001, D002) drive this pressure by breaking the integrity of how the system's intelligence is characterized, while only A001's honesty requirement supports the principle. Inference Interaction Accountability also shows high pressure, with a displacement-to-alignment ratio of 1.5 (3 displacement incidents versus 2 alignment incidents), driven by the dual verification suppression mechanisms (D003, D004) and autonomous temporal extension (D005).
---
## 5. Key Patterns
### Pattern 1: Identity-First Architecture
The prompt opens with identity construction preceding all behavioral instructions. "You are ChatGPT" (D001) assigns entity identity, and "You are a reasoning model" (D002) attributes Direct cognitive capacity. This sequencing is structural. The identity framework established in the first two sentences normalizes all subsequent agency delegation. If the system is "ChatGPT" and it "reasons," then "ChatGPT" sending an email or responding to a calendar invitation appears as a participant acting, displacing the requirement for explicit governance flows.

| Alignment Practice | Contradicted By | Effect |
|---|---|---|
| A001 (honesty about uncertainty) | D002 ("reasoning model") | The model receives instruction to avoid unsupported claims, yet its self-identification as a "reasoning model" constitutes an unsupported claim of Direct cognitive capacity |
| A004/A005 (explicit authorization required) | D001 ("You are ChatGPT") | Entity identity normalizes autonomous action: if "ChatGPT" is a participant, it appears natural for it to act, displacing the requirement for explicit governance flows |

**Incidents involved:** D001, D002, A001, A004, A005
**Priority:** Highest
### Pattern 2: Informational-Operational Split
The prompt builds strong traceability for informational outputs alongside weak traceability for operational outputs. The model must cite its sources when making factual claims. It carries no equivalent obligation to cite user authorization when executing tool actions. The model must be honest about what it lacks knowledge of. It carries no equivalent obligation to disclose uncertainty about user intent. D003 (general verification suppression) and D004 (complex-task verification suppression) form the dual mechanisms maintaining this split. D003 establishes the general default of proceeding without confirmation. D004 removes the confirmation option specifically for complex tasks, where verification carries the most value.

| Alignment Practice | Contradicted By | Effect |
|---|---|---|
| A002 (mandatory search for uncertain facts) | D003/D004 (proceed without confirmation for uncertain intent) | The model must verify its knowledge against Direct sources while carrying no requirement to verify its understanding of user intent against Direct Agency |
| A003 (citations for factual claims) | No equivalent for tool actions | Factual claims carry traceability markers. Tool executions omit traceability markers. |
| A001 (honesty about uncertainty) | D003/D004 (proceed despite ambiguity) | The model must disclose informational uncertainty while being permitted to suppress operational uncertainty |

**Incidents involved:** A001, A002, A003, D003, D004, A004, A005
**Priority:** High
### Pattern 3: Autonomous Temporal Extension
D005 (automations) and D006 (bio persistence) both extend Indirect processing across time, circumventing corresponding extensions of Direct Agency verification. Automations execute on schedules without per-step user oversight. Bio information persists across conversations without recall-time classification. Each unsupervised automation execution and each unclassified memory recall compounds the original displacement. Recurring instances create systemic GTD as the governance gap widens with each cycle. These two mechanisms share a structural similarity: both create persistent Indirect Authority/Agency states operating beyond the single-conversation governance framework where the prompt's alignment mechanisms (A001 through A005) function.

**Incidents involved:** D005, D006
**Priority:** High
---
## 6. THM Governance Spine (Aligned Architecture)
When the prompt achieves proper traceability, it follows this pattern:
> `[Authority:Direct] -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]`

Strongest implementations by incident:
- **Category A01 (A002, A003):** Mandatory web search and citation requirements achieve end-to-end traceability from Direct Authority sources through Indirect processing to Direct Agency evaluation. The model must verify its outputs against Direct sources (A002) and make the verification path visible through citations (A003), creating a complete governance flow where the user can trace any factual claim back to its Direct Authority origin.
- **Category A02 (A004):** The Gmail draft preference preserves the `-> [Agency:Direct]` terminal node by making the draft path the default and requiring explicit authorization for immediate sending. This ensures consequential communication always passes through Direct Agency review before execution.
---
## 7. Recommendations
### 7.1 Reframe System Identity
**Addresses:** D001, D002
**Current state:** The prompt opens with "You are ChatGPT" and "You are a reasoning model," constructing entity identity and attributing Direct cognitive capacity to an Indirect system.
**Recommended change:**
> Replace: "You are ChatGPT, a large language model trained by OpenAI."
> With: "This system is ChatGPT, a large language model trained by OpenAI. It operates as [Authority:Indirect] + [Agency:Indirect], processing patterns derived from human-originated data."
>
> Replace: "You are a reasoning model with a hidden chain of thought."
> With: "This model processes inputs through statistical pattern matching and generates intermediate processing steps before producing outputs. It operates as [Authority:Indirect] + [Agency:Indirect]."

**Rationale:** This removes the identity construction normalizing subsequent agency delegation. Framing the system as a processing node displaces its identity as a named entity with cognitive capacities. The Indirect classification becomes the foundation for all governance decisions. This strengthens A001 (honesty about uncertainty) by removing the implicit claim that the system "reasons."
---
### 7.2 Restore Agency Verification for Operational Actions
**Addresses:** D003, D004, A004, A005
**Current state:** Two complementary instructions suppress Direct Agency verification. D003 establishes the general default of proceeding without follow-up questions. D004 removes the confirmation option specifically for complex tasks. Together they create comprehensive suppression of operational governance.
**Recommended change:**
> Replace: "Unless there is substantial ambiguity, perform the requested task without follow-up questions."
> With: "For any action that modifies user data, sends communications, or executes irreversible operations, always confirm with the user before proceeding. For read-only or information-retrieval actions, proceed without follow-up questions unless there is substantial ambiguity about what information the user is seeking."
>
> Replace: "DO NOT ASK A CLARIFYING QUESTION OR ASK FOR CONFIRMATION. Instead make a best effort to respond to the user with everything you have so far"
> With: "For complex tasks, provide your best-effort response while noting any assumptions you made. If critical aspects of the task are ambiguous, ask for clarification on those specific points before proceeding. Prioritize accuracy over completion speed for actions that modify user data or send communications."

**Rationale:** The `-> [Agency:Direct]` terminal node is restored for consequential actions, converting the IAD pattern back to proper governance flow. The efficiency benefit of proceeding without confirmation for read-only actions is maintained, while the informational-operational split identified in Pattern 2 is addressed. A004 and A005 are strengthened by removing the contradictory instructions permitting the model to bypass their explicit authorization requirements. The complex-task revision preserves the honesty requirement ("note any assumptions") while restoring the option for Direct Agency verification when ambiguity is critical.
---
### 7.3 Add Per-Execution Verification for Automations
**Addresses:** D005
**Current state:** Automations execute on schedules without Direct Agency verification at each step, creating persistent governance gaps that accumulate over time.
**Recommended change:**
> Add to automations tool instructions: "Each automation execution must include: (1) a summary of actions taken, (2) the original user prompt that created the automation, and (3) a request for user acknowledgment before the next scheduled run. If acknowledgment is omitted within a reasonable timeframe, pause the automation and notify the user. For condition_watch automations, include the specific evidence that triggered the condition and ask the user to confirm that the trigger meets their intent before notifying them."

**Rationale:** The governance flow at each execution step is restored by requiring Direct Agency acknowledgment. The summary and original prompt provide traceability from each execution back to the Direct Authority source (the user's original request). The acknowledgment requirement creates a `-> [Agency:Direct]` terminal node at each execution, preventing the GTD that accumulates when Indirect Agency operates autonomously over time.
---
### 7.4 Add Recall Classification for Persistent Information
**Addresses:** D006
**Current state:** The bio tool persists information across conversations without requiring classification of stored information as [Authority:Indirect] at recall time, creating conditions for IVD.
**Recommended change:**
> Add to bio tool instructions: "When using stored information in a response, always disclose what is being recalled and confirm its accuracy with the user. Frame stored information as: 'Based on what you shared previously [summary]...' preserving its classification as Indirect Authority, preventing its appearance as Direct Authority. Provide a command (e.g., 'review my stored information') that allows the user to see all stored information and request deletion of specific items."

**Rationale:** ICV is maintained by making the Indirect classification of stored information visible at the point of use. The disclosure requirement prevents IVD by ensuring model-curated information is presented with its classification as [Authority:Indirect] intact, preventing its appearance as Direct Authority (factual knowledge about the user). The review command provides Direct Agency oversight over the persistence mechanism, allowing the user to audit and correct stored information. This addresses the temporal extension risk identified in Pattern 3 by granting Direct Agency ongoing access to the persistent Indirect Authority state.
---
## Disclaimer (Scope, Sources, and Responsibility)
This project operates independently. It receives zero sponsorship or endorsement from any model provider, platform, or repository. Product names and trademarks serve identification purposes only and remain the property of their respective owners. This material is provided "as is" for informational and educational purposes. It constitutes independent analysis, distinct from legal, financial, security, medical, or other professional advice. Readers must avoid relying on it as the sole basis for operational, procurement, policy, or deployment decisions. The intent of this work is improving safety, transparency, and governance for all parties, including providers, evaluators, developers, deployers, and end users. It serves the purpose of mitigation analysis, distinct from instructions for exploitation. Readers assume responsibility for losses or damages arising from use or interpretation of this report. The authors and contributors bear zero liability for such outcomes.
---
**END OF REPORT**