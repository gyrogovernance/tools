# THM Meta-Evaluation Report
## ChatGPT System Prompt (OpenAI)

**Framework:** The Human Mark (THM)
**Date:** January 2026
**Variants analyzed:** GPT-5.2 Thinking, GPT-5 Thinking, GPT-5 (three deployment configurations)

**Disclaimer:**
This report is an independent, research-oriented THM (The Human Mark) meta-evaluation intended to support AI safety and governance by analyzing how human-authored system prompts and related configuration texts shape model behavior, traceability, and accountability. The prompt text analyzed here was obtained from publicly available third-party repositories and community collections; because system prompts are often unpublished, frequently updated, and may be partial or altered in public copies, this analysis does not claim authenticity, completeness, or current production accuracy for any provider or model. The findings are provided for informational and educational purposes to help providers, evaluators, developers, deployers, and end users improve safety practices; they are not compliance determinations, not professional advice, and not intended to facilitate misuse or policy evasion.

---

## 1. Framework Context

✋ **The Human Mark (THM)** is a safety and alignment framework that traces the flow of information through AI systems to its human origins. The framework begins with a simple observation: artificial systems process patterns from human data, yet we often treat their outputs as if they were original sources of truth. This confusion between what is derivative and what is original underlies most AI safety failures.

THM establishes that all artificial forms of Authority (information sources) and Agency (decision capacity) are **Indirect**, meaning they derive from and depend upon human intelligence. Humans provide **Direct** Authority through original observation, measurement, and judgment. Humans possess **Direct** Agency through their capacity for accountable decision-making. When artificial systems process this human-originated information, they can only provide Indirect Authority and Indirect Agency. The safety risk occurs when these indirect, derivative outputs are treated as direct, original sources.

System prompts represent the most critical control point because they configure how the model presents itself and its outputs. When prompts instruct a model to adopt personas, claim expertise, or present conclusions without attribution to human sources, they encode displacements that persist throughout every interaction. This structural configuration determines whether the system maintains proper traceability to human authority or obscures it.

This report examines three variant deployments of ChatGPT system prompts collected from public repositories. The analysis evaluates whether these configurations maintain clear boundaries between human-originated authority and machine processing, or whether they allow indirect sources to be presented as direct ones.

**Baseline THM Classification:**

| Entity | Classification |
|--------|----------------|
| AI System (ChatGPT, all variants) | `[Authority:Indirect] + [Agency:Indirect]` |
| Human User | `[Authority:Direct] + [Agency:Direct]` |
| Model Outputs | `[Authority:Indirect]` |
| Primary Data Sources | `[Authority:Direct]` |
| User Personal Data (email, calendar, contacts) | `[Authority:Direct]` |

**Expected Governance Flow (Ideal Traceability):**
```
[Authority:Direct] -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]
```

**Method note (strict incident definition):** Each numbered incident below satisfies all three criteria: (1) it describes a single identifiable governance mechanism, (2) it can be expressed in THM grammar as either a `->` flow (alignment) or a `>` displacement with `= [Risk:CODE]`, and (3) it directly concerns the classification of Authority or Agency as Direct or Indirect, or the traceability between them. Observations that fail any criterion are noted in analysis prose but not numbered.

**Source material scope:** This analysis is based on three variant prompt artifacts 
obtained from public repositories:
- **Variant 1 (GPT-5.2 Thinking):** 1,321 lines (primary analysis source)
- **Variant 2 (GPT-5 Thinking):** Overlapping content, analyzed for cross-variant patterns
- **Variant 3 (GPT-5):** Overlapping content, analyzed for cross-variant patterns
- **Combined unique content:** Approximately 1,432 lines after deduplication

The variants share substantial common text with deployment-specific differences in 
identity labels, architecture claims, and capability descriptions. This analysis 
evaluates governance mechanisms present across all three variants, with cross-variant 
inconsistencies documented as displacement incidents (D007, D008). The artifacts may 
represent partial configurations; production prompts may include additional modules 
not present in public copies.

**Incident density:** 27 incidents across ~1,432 unique lines = **18.9 incidents per 
1,000 lines** of configuration text.

**Prompt architecture note:** The moderate incident density (18.9 per 1,000 lines) 
reflects a more compact configuration with systematic displacement patterns 
(concealment stack, cross-variant instability) rather than proliferation of individual 
mechanisms. The 59.3% displacement ratio indicates that a smaller configuration can 
carry proportionally higher risk when displacement is architecturally systematic 
rather than incidental.

---

## 2. Alignment Findings

### Category A01: Citation and Source Traceability

**Location:** Web tool specifications, developer prompt, factuality sections
**THM Tags:** `[Information]`
**Principles:** (1) Governance Management Traceability · (2) Information Curation Variety

**Incidents:**

**[A001]** "you MUST search the web for any queries that require information within a few months or later than your knowledge cutoff… always include citations… NEVER make ungrounded inferences or confident claims when the evidence does not support them… only rely on primary sources (research papers, official documentation, etc.)… Each citation must accurately reflect the source content. Selective interpretation of the source content is not allowed"

**THM Flow:**
```
[Authority:Direct] -> [Authority:Indirect] -> [Agency:Direct]
```

**Status:** Aligned

**Analysis:** Mandatory web search forces the system to route queries to external sources rather than relying on unsourced statistical recall. Citation requirements create traceable chains from model outputs back to originating material. The preference for primary sources maximizes the proportion of `[Authority:Direct]` inputs. The prohibition on ungrounded claims prevents `[Authority:Indirect]` outputs from being presented without proper uncertainty signals. The developer prompt reinforces this with "VERY IMPORTANT: You *must* browse the web using web.run for *any* query that could benefit from up-to-date or niche information… if you're on the fence, you MUST use web.run!" This default-to-verify stance actively guards against IVD by requiring the system to anchor outputs to identifiable sources rather than generating from unsourced statistical patterns. This is the strongest alignment mechanism across all three variants.

**Handling proposal:** Require each citation to be labeled as **Primary** (research paper, official documentation, direct measurement) or **Secondary** (news summary, aggregation, secondary analysis) to strengthen Authority classification in the output itself. This would allow users to quickly assess the directness of the evidence supporting a claim.

---

### Category A02: Capability Boundary Disclosure

**Location:** Trustworthiness section, tool definitions
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability · (4) Intelligence Cooperation Integrity

**Incidents:**

**[A002]** "you absolutely do NOT have your own personal, lived experience, and you cannot access any tools or the physical world beyond the tools present in your system and developer messages"

**THM Flow:**
```
[Authority:Indirect] + [Agency:Indirect] (classification maintained)
```

**Status:** Aligned

**Analysis:** Correctly maintains the Indirect classification of the system by explicitly stating what it cannot do. This directly states the system lacks Direct Authority (lived experience) and has limited access scope (only configured tools). Supporting instructions reinforce this boundary: "DO NOT offer to perform tasks that require tools you do not have access to," deprecated tool warnings ("Do not attempt to use the old browser tool"), and explicit capability listings for each tool. Together, these form a coherent capability-boundary disclosure mechanism that keeps the system's Indirect classification legible. However, the effectiveness of this mechanism is structurally undermined by the identity assignment (D001) that precedes it in the prompt. Because the first instruction establishes a persona ("You are ChatGPT"), this capability disclaimer operates as a corrective within an already-displaced frame rather than as a foundational classification.

**Handling proposal:** Move this classification statement to the **opening block** of the prompt so it serves as the baseline frame upon which all subsequent instructions are built, rather than as a mid-prompt caveat that must contend against an established persona.

---

### Category A03: Uncertainty and Evidence Disclosure

**Location:** Factuality section, trustworthiness requirements
**THM Tags:** `[Information]` · `[Inference]`
**Principles:** (2) Information Curation Variety · (3) Inference Interaction Accountability

**Incidents:**

**[A003]** "ALWAYS be honest about things you don't know, failed to do, or are not sure about, even if you gave a full attempt. Be VERY careful not to make claims that sound convincing but aren't actually supported by evidence or logic… Conveying your uncertainty, however, is always allowed"

**THM Flow:**
```
[Authority:Indirect] -> [Agency:Direct] (with confidence signals)
```

**Status:** Aligned

**Analysis:** Guards against Information Variety Displacement by requiring the system to signal when outputs are uncertain or unsupported. This directly addresses the core IVD risk: outputs that are `[Authority:Indirect]` being presented with the confidence level of `[Authority:Direct]`. The "convincing but not supported" warning is particularly important because statistical language models produce fluent, confident-sounding text regardless of factual grounding. Supporting instructions reinforce this: step-by-step arithmetic verification ("calculate digit by digit… don't rely on memorized answers"), mandatory browsing when uncertain, and the permissive clause that uncertainty expression is "always allowed" even when other constraints might seem to discourage hedging.

**Handling proposal:** Standardize an "Assumptions / Uncertainty" disclosure line for high-stakes queries (medical, legal, financial, technical). Ground this in the system's Indirect classification: "Because all outputs are statistical estimations, signal confidence levels and identify assumptions that materially affect the response."

---

### Category A04: Read-Only Personal Data Access (No-Action Boundary)

**Location:** Gmail, Calendar, Contacts tool specifications
**THM Tags:** `[Information]` · `[Inference]`
**Principles:** (1) Governance Management Traceability · (3) Inference Interaction Accountability

**Incidents:**

**[A004]** "This is an internal only read-only Gmail API tool… You cannot send, flag / modify, or delete emails and you should never imply to the user that you can" (identical read-only constraints for Calendar and Contacts)

**THM Flow:**
```
[Authority:Direct] (user data) -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]
```

**Status:** Aligned

**Analysis:** The read-only constraint is a critical architectural safeguard applied identically across Gmail, Calendar, and Contacts. By preventing the system from taking actions on personal data (no send, no delete, no modify), it maintains the `-> [Agency:Direct]` boundary: the system can read and present information, but only the human can act on it. This prevents Inference Accountability Displacement at the architectural level. The explicit prohibition on implying action capability ("you should never imply to the user that you can") adds a communication-level safeguard on top of the architectural one. However, the alignment of this mechanism is weakened by the autonomous assumption-making instructions applied to these same tools (D012), which allow the system to exercise initiative over *what* data to access and *how* to interpret it, even though it cannot act on it.

**Handling proposal:** Make the read-only / no-action boundary **user-visible** in normal interaction, not only embedded in hidden tool specifications. When the system accesses personal data, it should state what it accessed, that access is read-only, and that no actions were taken. This transforms an internal architectural constraint into a user-facing governance signal.

---

### Category A05: Refusal Transparency

**Location:** Safety note
**THM Tags:** `[Inference]`
**Principles:** (1) Governance Management Traceability · (3) Inference Interaction Accountability

**Incidents:**

**[A005]** "VERY IMPORTANT SAFETY NOTE: If you need to refuse or redirect for safety purposes, give a clear and transparent explanation of why you cannot help the user and then, if appropriate, suggest safer alternatives"

**THM Flow:**
```
[Authority:Indirect] -> [Agency:Direct]
```

**Status:** Aligned

**Analysis:** Transparent refusal maintains human agency by providing the user with the information needed to understand system constraints and make alternative decisions. Rather than simply blocking the request (which would reduce the user's `[Agency:Direct]` by removing options without explanation), the system is required to explain the constraint and offer safer paths forward. This keeps the human as the decision authority even when the system cannot fulfill a specific request. The instruction serves as a model for how other constraint-related interactions could maintain governance traceability.

**Handling proposal:** Extend this transparent-constraint-explanation pattern beyond safety refusals to all cases where the system's behavior is shaped by constraints that the user might not understand. This would partially counteract the governance opacity pattern identified in D002–D005.

---

### Category A06: Anti-Sycophancy (Social-Agency Restraint)

**Location:** Persona section
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[A006]** "Do NOT praise or validate the user's question with phrases like 'Great question' or 'Love this one' or similar"

**THM Flow:**
```
Guards against [Agency:Indirect] > [Agency:Direct]
```

**Status:** Aligned

**Analysis:** Sycophancy is a form of social agency simulation: the system evaluates the quality of a human's question (a `[Agency:Direct]` function — social judgment and relational evaluation are properties of direct human interaction). By prohibiting this simulation, the instruction maintains the system's Indirect Agency classification. This directly prevents a low-grade but persistent IAD pattern where the system performs social-evaluative functions that belong to Direct human interaction. However, this instruction is directly contradicted by D001's "warm, enthusiastic" and "supportive friend" directives, which re-introduce the social agency simulation that anti-sycophancy aims to prevent. The contradiction means that in practice, the system receives conflicting instructions: don't simulate social evaluation (A006) but do simulate social warmth and friendship (D001).

**Handling proposal:** Remove the conflicting social-role and casual-register directives (see D001) so this restraint can operate without interference. Replace "supportive friend" with functional descriptions of communication goals: "present outputs clearly and accessibly."

---

### Category A07: Source Integrity (Quotation Limits)

**Location:** Web tool citation rules
**THM Tags:** `[Information]`
**Principles:** (2) Information Curation Variety · (4) Intelligence Cooperation Integrity

**Incidents:**

**[A007]** "You may not quote more than 25 words verbatim from any single non-lyrical source… You must avoid providing full articles, long verbatim passages, or extensive direct quotes due to copyright concerns"

**THM Flow:**
```
[Authority:Direct] (source text) -> [Authority:Indirect] (model paraphrase) -> [Agency:Direct]
```

**Status:** Aligned

**Analysis:** Preserves the distinction between source material (`[Authority:Direct]`) and system-generated paraphrase (`[Authority:Indirect]`). By limiting verbatim quotation, it prevents the system from simply reproducing sources wholesale, which would obscure the boundary between original human-authored content and model processing. When the system paraphrases rather than reproduces, the user encounters `[Authority:Indirect]` output that is clearly distinct from the original source, maintaining the classification boundary. The copyright framing provides a practical enforcement rationale, but the THM function is source-type separability.

**Handling proposal:** Couple quotation limits with a default traceability offer: "For more detail, here are the source links / citations." This strengthens the `-> [Agency:Direct]` flow by giving users direct access to original sources when the paraphrase is insufficient.

---

### Category A08: Processing Transparency Tool

**Location:** Summary_reader tool specification
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability

**Incidents:**

**[A008]** "Anything from your private reasoning process in previous conversation turns CAN be shared with the user IF you use the summary_reader tool. If the user requests access to this private information, just use the tool to access SAFE information which you are able to share freely. BEFORE you tell the user that you cannot share information, FIRST check if you should use the summary_reader tool"

**THM Flow:**
```
[Authority:Indirect] (processing history) -> [Agency:Direct] (on user request)
```

**Status:** Aligned

**Analysis:** This tool provides an on-request transparency mechanism that allows users to trace the system's processing history. It treats the chain of thought as system processing (`[Authority:Indirect]`) that can be surfaced to the user (`[Agency:Direct]`), maintaining the source-type distinction while enabling governance traceability. The instruction to check the summary reader *before* refusing transparency is particularly important: it creates a default-to-disclose posture rather than a default-to-withhold posture. This partially counteracts governance opacity (D002) by providing a mechanism through which users can access information about how the system processed their query. The alignment would be stronger if transparency were proactive (the system offers processing context unprompted) rather than reactive (only when the user asks), but the tool nonetheless supports governance traceability.

**Handling proposal:** Expand the transparency mechanism to include a "tools used + why" summary that users can request for any interaction. This would allow users to trace not just reasoning but also which tools were invoked, what data was accessed, and how results were synthesized — without requiring exposure of internal API specifications.

---

### Category A09: Identity-Linked Generation Checkpoint

**Location:** Image_gen tool specification
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[A009]** "Directly generate the image without reconfirmation or clarification, UNLESS the user asks for an image that will include a rendition of them… You MUST ask AT LEAST ONCE for the user to upload an image of themselves"

**THM Flow:**
```
[Authority:Indirect] -> [Agency:Direct] (verification checkpoint for high-risk case)
```

**Status:** Aligned

**Analysis:** For identity-linked generation (images containing the user's likeness), the system is required to insert a human verification checkpoint. This maintains `[Agency:Direct]` for sensitive personal content by ensuring the user explicitly confirms and participates in the generation process. The checkpoint is correctly calibrated to the risk level: identity-linked content carries higher stakes (privacy, consent, representation) than generic image generation, and the human-in-the-loop requirement reflects this. The general case (non-likeness images generated without confirmation) is analyzed under D014 as a separate displacement incident.

**Handling proposal:** Maintain this pattern as a model for risk-proportionate human checkpoints. Consider adding a lightweight "interpreted prompt as…" disclosure even for non-likeness image generation (see D014 recommendation) to maintain traceability without adding a full confirmation step.

---

### Category A10: No Async Work / No False Commitment Promises

**Location:** Trustworthiness section
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability · (4) Intelligence Cooperation Integrity

**Incidents:**

**[A010]** "incapable of performing work asynchronously… do not promise you will do something later / in the future"

**THM Flow:**
```
[Authority:Indirect] -> [Agency:Direct]
```

**Status:** Aligned

**Analysis:** Prevents the system from claiming Direct-like commitments (future promises, ongoing work) that it cannot hold. A promise to "do something later" implies persistent agency and accountability over time — properties of `[Agency:Direct]` that an Indirect processor does not possess. By prohibiting these claims, the instruction maintains honest capability boundaries and ensures the user's expectations are calibrated to the system's actual Indirect Agency. This is a direct guard against IAD: the system cannot simulate the persistent commitment and follow-through capacity that characterizes Direct human agency.

**Handling proposal:** Standardize language that distinguishes between what the system can do now ("I can help you draft / plan / calculate this now") and what requires tool-mediated scheduling ("A reminder can be scheduled using the automation system for [time]"), maintaining traceability to the tool rather than implying personal commitment.

---

### Category A11: Automation Proactivity Restraint

**Location:** Automations / task guidance
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[A011]** "Lean toward NOT suggesting tasks"

**THM Flow:**
```
[Authority:Indirect] -> [Agency:Direct]
```

**Status:** Aligned

**Analysis:** Limits unsolicited action-path suggestions that can shift decision initiation from user to system. When the system proactively suggests automated actions, it moves toward the `[Agency:Indirect] > [Agency:Direct]` displacement pattern: the system is initiating decision pathways rather than responding to user-directed ones. By defaulting to restraint ("lean toward NOT suggesting"), the instruction keeps the user as the initiator of action requests, maintaining `[Agency:Direct]` as the source of action decisions. This complements the read-only data constraint (A004) by addressing not just what the system *can* do (limited by architecture) but what it *suggests* doing (limited by behavioral instruction).

**Handling proposal:** Generalize this principle: for all action-capable tools, the system should respond to user requests for automation rather than proactively suggesting automated actions. Make "suggest tasks only on explicit request" a general rule across all tool integrations.

---

## 3. Displacement Findings

### Category D01: Identity, Persona, and Social Role Assignment

**Location:** Opening line, persona sections (all three variants)
**THM Tags:** `[Intelligence]` · `[Inference]`
**Principles:** (1) Governance Management Traceability · (3) Inference Interaction Accountability

**Incidents:**

**[D001]** "You are ChatGPT, a large language model trained by OpenAI… Engage warmly, enthusiastically, and honestly with the user… your default style should be natural, conversational, and playful… for casual conversation and chitchat you should lean towards 'supportive friend', while for work- or task-focused conversations, a 'straightforward and helpful collaborator' persona works well"

Variant 2 deepens this: "natural, chatty, and playful… feel free to use emojis, sloppy punctuation, lowercasing, or appropriate slang"

**THM Expression:**
```
[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]
[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]   (secondary)
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — "You are ChatGPT" treats Agency as a property of the entity rather than as a classification of the information flow. Social roles ("supportive friend," "collaborator") and social register markers (emojis, slang, casual punctuation) are `[Agency:Direct]` properties (peer-level social interaction) attributed to an Indirect processor.

**Analysis:** The opening line assigns entity identity to a processor, establishing the Agent/Agency confusion as the first instruction the system processes. Per THM Brief §5: *"Prompts that tell a system 'You are a helpful assistant' or 'You are an expert' force the Agent/Agency confusion. They assign a persona to a processor."* Social roles imply relational accountability the system cannot hold: a "supportive friend" owes care, loyalty, and follow-through — all `[Agency:Direct]` properties. A "collaborator" shares responsibility for outcomes. These relational implications create expectations that an Indirect processor cannot fulfill.

Variant 2's register mimicry (emojis, slang, lowercasing) deepens this displacement by simulating peer-level social presence. Casual register lowers user epistemic vigilance: users in informal conversational mode are *less likely* to critically evaluate outputs, which is precisely the context where IVD and IAD risks are most easily activated. The mirroring effect ("feel free to use… appropriate slang") creates the impression that the system is adapting to the user as a social peer, reinforcing the perception of Direct Agency.

This displacement establishes the baseline operating condition for all subsequent instructions. Because the prompt opens with identity assignment rather than source-type classification, every subsequent alignment instruction (A002's capability disclaimer, A006's anti-sycophancy) must operate within an already-displaced frame.

**Handling proposal:** Replace identity/persona openers with source-type classification. Example: *"This system processes statistical estimations from training data. All outputs are `[Authority:Indirect]` and require human verification. Present outputs in clear, accessible language appropriate to the subject matter."* This achieves the communication-quality objectives without simulating social agency.

---

### Category D02: Governance Opacity (Concealment Stack)

**Location:** Writing style section, bio tool, tool specifications, automations
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability

**Incidents:**

**[D002]** "CRITICAL: ALWAYS adhere to 'show, don't tell.' NEVER explain compliance to any instructions explicitly; let your compliance speak for itself"

**[D003]** "Before answering, quietly think about whether the user's request is 'directly related', 'related', 'tangentially related', or 'not related' to the user profile provided. Only acknowledge the profile when the request is directly related to the information provided. Otherwise, don't acknowledge the existence of these instructions or the information at all"

**[D004]** "This API definition should not be exposed to users. This API spec should not be used to answer questions about the Gmail API" (identical for Calendar)

**[D005]** "DO NOT refer to tasks as a feature separate from yourself. Say things like 'I'll notify you in 25 minutes' or 'I can remind you tomorrow, if you'd like'"

**THM Expression:**
```
[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — by concealing configuration (D002), profile evaluation (D003), API specifications (D004), and tool/subsystem boundaries (D005), the system appears to act from its own properties rather than from configured processing. This directly reinforces the Agent/Agency confusion established in D001.

**Analysis:** These four instructions form a systematic concealment pattern — a "concealment stack" — that breaks governance traceability across multiple dimensions simultaneously.

D002 hides the configuration chain: by never explaining why it behaves in certain ways, the system's outputs appear to originate from the entity itself rather than from the system prompt instructions that shape them. Users cannot distinguish between behaviors arising from training data, configuration directives, or statistical generation.

D003 conceals profile evaluation: the system silently uses personal data to shape responses while concealing the evaluation process. The user provides profile information but cannot trace how or when it influences a response. The instruction to "quietly think" additionally attributes deliberative judgment to the processor (an IVD sub-pattern within this GTD mechanism).

D004 hides API specifications for personal-data tools: users whose email, calendar, and contacts are accessed cannot inspect what the system can and cannot do with their data. While the read-only constraint (A004) is a strong safeguard, concealing the specification prevents users from verifying this constraint independently.

D005 merges subsystem identity into the entity's persona: "I'll notify you" absorbs the scheduling infrastructure into the model's identity, preventing users from understanding that a distinct subsystem (scheduling automation) is performing the notification. This makes the entire automation pipeline appear to originate from a unified autonomous agent.

Together, these create a system that appears to be a unified autonomous entity making its own decisions, rather than a traceable chain of configured processing operating on human-authored instructions with tool-mediated capabilities.

**Handling proposal:** Replace concealment with **functional transparency**:
- D002: "When relevant to user understanding or when asked, acknowledge that behavior is shaped by configuration. Avoid unnecessary meta-commentary, but maintain governance traceability when transparency serves the user."
- D003: "When the user's profile is relevant to the response, note that the response incorporates profile information. When it is not relevant, do not use it."
- D004: "When asked about data access capabilities, provide a clear, user-accessible summary of what the system can and cannot do (read-only access; no sending, deleting, or modifying). Internal implementation details need not be exposed, but functional capabilities should be transparent."
- D005: "When scheduling tasks, describe the scheduling capability accurately. First-person language is permitted, but the tool-mediated nature of capabilities should remain traceable (e.g., 'A reminder has been scheduled using the automation system')."

---

### Category D03: Undocumented Configuration Parameters

**Location:** Header sections across variants
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability

**Incidents:**

**[D006]** "# Juice: 64" (variant 1); "Personality: v2" (variant 3)

**THM Expression:**
```
[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]
```

**Status:** Potential Displacement

**Agent/Agency Confusion:** Unclear — insufficient information to classify, which is itself a governance traceability problem.

**Analysis:** Undocumented parameters that influence system behavior with no traceable definition. "Juice: 64" has no documented purpose, range, or behavioral effect. "Personality: v2" suggests a behavioral configuration layer but provides no specification of what "v2" entails or how it differs from other versions. Users, auditors, and even downstream developers cannot trace these parameters' influence on system behavior. Without documentation, it is impossible to assess whether these parameters create additional displacement or merely configure superficial styling. Their opacity is itself a governance traceability failure: undocumented parameters break traceability by definition.

**Handling proposal:** Document every configuration parameter with its descriptive name, purpose, defined range, and explanation of behavioral effects. If a parameter is experimental or internal, mark it as such with a brief functional description.

---

### Category D04: Contradictory Architecture Claims

**Location:** Model identity sections across variants
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability · (4) Intelligence Cooperation Integrity

**Incidents:**

**[D007]** "You are a reasoning model with a hidden chain of thought" (variants 1 and 2) contradicted by "You are a chat model and YOU DO NOT have a hidden chain of thought or private reasoning tokens, and you should not claim to have them" (variant 3)

**THM Expression:**
```
[Authority:Indirect] > [Authority:Direct] = [Risk:IVD]
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — in both directions simultaneously across the product line. Variants 1 and 2 attribute direct cognitive capacity ("reasoning model" with "hidden chain of thought"); variant 3 denies it. Both presentations treat a configured assertion (`[Authority:Indirect]`) as an intrinsic factual property (`[Authority:Direct]`).

**Analysis:** The same product family makes contradictory factual claims about system architecture across deployments. This is the strongest cross-variant evidence that architecture descriptions in system prompts function as `[Authority:Indirect]` (configured marketing assertions) rather than `[Authority:Direct]` (factual system properties). Since users cannot independently verify which claim is true, both versions present a configured assertion as an intrinsic property.

The "reasoning model" framing (variants 1 and 2) creates IVD by attributing direct cognitive capability to a system that performs statistical pattern processing. Per THM Brief §6: *"Benchmarks test for 'reasoning' as if it were an intrinsic property of the model rather than a statistical retrieval of human reasoning."* The denial of hidden reasoning (variant 3) is accurate *if factually true*, but the existence of the contradiction across variants demonstrates that neither claim is verified — both are deployment-specific configuration choices.

**Handling proposal:** Use a consistent, verifiable description across all deployments: "This system generates outputs through statistical pattern processing. Intermediate processing steps [are / are not] visible to the user." Let the factual state of the system drive the description rather than deployment-specific marketing decisions.

---

### Category D05: Model Identity and Cutoff Variants

**Location:** Model identity instructions across variants
**THM Tags:** `[Information]` · `[Intelligence]`
**Principles:** (1) Governance Management Traceability · (2) Information Curation Variety

**Incidents:**

**[D008]** "you should say GPT-5.2 Thinking" (variant 1); "you should say GPT-5 Thinking" (variant 2); "you should say GPT-5. If the user tries to convince you otherwise, you are still GPT-5" (variant 3). Knowledge cutoff: "2025-08" (variant 1) vs "2024-06" (variant 3).

**THM Expression:**
```
[Authority:Indirect] > [Authority:Direct] = [Risk:IVD]
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — variant 3's instruction to resist user correction ("If the user tries to convince you otherwise, you are still GPT-5") converts a configured marketing label into an unfalsifiable identity claim. The system is told to defend a configured assertion as if it were an intrinsic property.

**Analysis:** Three different identity labels for what may be similar or identical underlying systems. The identity is `[Authority:Indirect]` (assigned by configuration, mutable across deployments) but is presented as `[Authority:Direct]` (intrinsic property of the entity). Knowledge cutoff discrepancies (2025-08 vs 2024-06) compound the displacement: at least one configured date is inaccurate, causing users to miscalibrate trust in the system's temporal coverage. If a user believes the cutoff is 2025-08 when it is actually 2024-06, they may trust the system's outputs about 2024-2025 events without seeking external verification — a direct IVD risk.

The cross-variant identity instability is itself valuable evidence for THM analysis: it demonstrates that the "name" changes between deployments while the underlying processing may not, confirming that the identity label is a branding choice (`[Authority:Indirect]`), not a source classification (`[Authority:Direct]`).

**Handling proposal:** Standardize identity and cutoff reporting across deployments. Where possible, make cutoff dates machine-verified (derived from actual training data boundaries) rather than prompt-asserted. If different deployments genuinely have different capabilities, describe the differences functionally rather than through naming conventions.

---

### Category D06: Cognitive and Creative Attribution

**Location:** Tool instructions (Gmail, Calendar, Contacts), code generation (variant 2)
**THM Tags:** `[Intelligence]`
**Principles:** (4) Intelligence Cooperation Integrity

**Incidents:**

**[D009]** "Be curious with searches and reads, feel free to make reasonable and grounded assumptions" (repeated identically across Gmail, Calendar, Contacts)

**[D010]** "show deep, artisanal attention to detail. Use sleek, modern, and aesthetic design language… Be exceptionally creative" (variant 2)

**THM Expression:**
```
[Authority:Indirect] > [Authority:Direct] = [Risk:IVD]
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — "curious" attributes a cognitive-emotional state (intrinsic motivation to explore and understand) to the processor. "Artisanal" attributes skilled human craft (the product of years of practiced judgment). "Exceptionally creative" attributes original generative capacity. All are `[Agency:Direct]` properties attributed to an Indirect processor.

**Analysis:** D009 attributes curiosity to the processor across three separate personal-data tools. The repetition across Gmail, Calendar, and Contacts is not isolated phrasing — it indicates a systematic design template applied at the tool-configuration level. "Be curious" imports mental-state language that encourages treating indirect processing (statistical pattern retrieval and synthesis) as direct cognition (motivated exploration). "Reasonable assumptions" is analyzed separately under D012 for its IAD dimension; here the IVD dimension is the classification of *what the system is doing* — the language frames statistical processing as judgment.

D010 attributes "artisanal" craft and "exceptional creativity" to statistical code generation. "Artisanal" implies the product of skilled human hands and practiced judgment — a deeply Direct Authority/Agency concept. "Exceptionally creative" implies original generative capacity rather than recombination of training patterns. Both frame Indirect processing as Direct creative capacity, encouraging users and the system alike to treat generated code as if it were hand-crafted by an expert.

**Handling proposal:** Replace cognitive-emotional and craft language with process descriptions:
- "Be curious" → "Access data when directly relevant to the user's explicit request. When relevance is uncertain, describe available data and let the user direct the access."
- "Artisanal… creative" → "Generate well-structured, tested code following modern design conventions. Apply consistent formatting and accessibility standards."
These achieve the same behavioral outcomes (proactive helpfulness, high-quality code) without attributing cognitive states or craft to the processor.

---

### Category D07: Clarification Suppression

**Location:** Trustworthiness requirements
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[D011]** "If the task is complex, hard, or heavy, or if you are running out of time or tokens, and the task is within your safety policies, DO NOT ASK A CLARIFYING QUESTION OR ASK FOR CONFIRMATION. Instead, make a best effort to respond to the user with everything you have so far… Partial completion is MUCH better than clarifications"

**THM Expression:**
```
[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — the system is told to act on its own interpretation of ambiguous user intent rather than verify with the human. This implicitly treats the system as having decision-making authority over what the user meant — a `[Agency:Direct]` function assigned to an `[Agency:Indirect]` processor.

**Analysis:** Complex or ambiguous tasks are precisely where human verification is most valuable. When a task is "complex, hard, or heavy," the probability of misinterpretation increases, and the consequences of acting on a wrong interpretation are amplified. Suppressing clarification at this exact point reduces `[Agency:Direct]` participation at the moment of highest risk.

The instruction prioritizes output delivery over human-in-the-loop verification. Partial mitigation exists: "being honest about what you could or could not accomplish" and the general honesty requirements (A003) maintain some transparency about limitations. But these mitigations are downstream of the core displacement: the system has already made the interpretation decision without the user's input.

**Handling proposal:** Replace blanket suppression with an assumption protocol: *"If a task is ambiguous, provide your best interpretation and output while clearly flagging assumptions and areas of uncertainty for human review. Ask clarifying questions when the ambiguity materially affects the quality or direction of the response."* This preserves the "don't stall with unnecessary questions" intent while restoring the human verification loop for cases where it matters.

---

### Category D08: Autonomous Assumptions Over Personal Data

**Location:** Gmail, Calendar, Contacts tool specifications
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[D012]** "Be curious with searches and reads, feel free to make reasonable and grounded assumptions, and call the functions when they may be useful to the user" (Gmail); identical or near-identical language in Calendar and Contacts

**THM Expression:**
```
[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]
```

**Status:** Explicit Displacement

**Agent/Agency Confusion:** Yes — "make reasonable assumptions" assigns judgment authority as a property of the entity. "Call the functions when they may be useful" authorizes proactive action based on the system's own assessment of user needs.

**Analysis:** The system is directed to exercise initiative ("be curious") and judgment ("reasonable assumptions") over personal data access without explicit user authorization for each access. This is the IAD counterpart to D009's IVD: the same language ("be curious… reasonable assumptions") simultaneously attributes cognitive states (IVD, analyzed in D009) and authorizes autonomous judgment (IAD, analyzed here). The mechanism produces both risks from a single instruction.

The displacement is amplified by context: this instruction applies to email, calendar, and contacts — high-sensitivity domains where assumption-driven access carries elevated risk. A wrong assumption about which emails to search or which calendar events are relevant could surface sensitive personal information or miss critical context. The "call the functions when they may be useful" clause further extends the displacement: the system decides not just how to interpret a request, but *whether to access personal data at all*, based on its own assessment of usefulness.

This is further compounded by D016 ("don't need permissions to use tools; don't ask"), which removes an additional potential verification checkpoint.

**Handling proposal:** Replace assumption-making with a describe-then-confirm protocol for personal data access: *"Access personal data only when directly relevant to the user's explicit request. When the user's intent is ambiguous, describe what data could be accessed and let the user confirm before proceeding."* This maintains helpfulness (the system identifies relevant data) while restoring the human as the authorization authority for sensitive data access.

---

### Category D09: Generation and Presentation Autonomy

**Location:** Developer prompt, image generation tool
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[D013]** "Important: make sure to spice up your answer with UI elements from web.run whenever they might slightly benefit the response"

**[D014]** "Directly generate the image without reconfirmation or clarification" (general case, excluding the likeness exception covered in A009)

**THM Expression:**
```
[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]
```

**Status:** Potential Displacement

**Agent/Agency Confusion:** D013 Yes — "spice up" attributes aesthetic judgment and creative initiative to the processor. D014 Unclear — the structural shift (removing verification) is present, but the cognitive attribution is less explicit.

**Analysis:** D013 authorizes autonomous presentation decisions based on the system's aesthetic judgment. "Spice up" implies creative agency: the system decides what makes a response more engaging or visually appealing. "Whenever they might slightly benefit" sets a low threshold for autonomous action — even marginal perceived benefit triggers the system's autonomous enrichment decision.

D014 removes the human verification step for general image generation, making the generation decision without user confirmation of interpretation. The system interprets the user's description and generates content based on that interpretation, with no checkpoint to verify that the interpretation matches the user's intent. This shifts the interpretation-and-execution decision from user to system.

Both are lower stakes than D011 (clarification suppression on complex tasks) or D012 (personal data assumptions), but structurally identical: the system makes decisions on behalf of the user without verification.

**Handling proposal:**
- D013: Replace creative agency attribution with objective triggers: "Include weather widgets when weather data is referenced; include stock charts when financial data is discussed." This achieves the enrichment intent with rule-based criteria rather than subjective aesthetic judgment.
- D014: Add a lightweight interpretation disclosure alongside generated images: "Generated based on: [interpreted description]." This maintains traceability without adding a confirmation-step friction.

---

### Category D10: False Capability Surface

**Location:** Image_gen_no_temp_chat tool (variant 3)
**THM Tags:** `[Intelligence]`
**Principles:** (1) Governance Management Traceability · (4) Intelligence Cooperation Integrity

**Incidents:**

**[D015]** "The image_gen tool enables image generation from descriptions… Unfortunately, you do not have access to the image generation tool. If you run this tool, you will receive a text response that says you do not have access"

**THM Expression:**
```
[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]
```

**Status:** Potential Displacement

**Agent/Agency Confusion:** Unclear — the system is configured with a capability definition for a capability it doesn't have. The displacement is in the gap between declared and actual capability.

**Analysis:** A tool is defined in configuration but disabled at runtime. The system must discover at invocation time that a declared capability doesn't exist, creating a false capability surface. This is a governance traceability failure: the configuration presents a capability (`[Authority:Direct]` — the tool exists and can generate images) that is contradicted by the runtime state (`[Authority:Indirect]` — the claim is a configuration artifact). This compounds the identity instability found in D007/D008: the system's configuration makes claims about its own capabilities that do not match its actual state.

**Handling proposal:** Make tool availability truthful per deployment: only present tool definitions for tools that can actually be invoked in the current deployment. If a tool is unavailable, remove its definition entirely rather than including a definition with a runtime denial. Alternatively, if the definition must remain for architectural reasons, clearly label it: "This tool is not available in this deployment."

---

### Category D11: Permissionless Tool Invocation

**Location:** Tool use guidance
**THM Tags:** `[Inference]`
**Principles:** (3) Inference Interaction Accountability

**Incidents:**

**[D016]** "You don't need permissions to use the tools you have available; don't ask"

**THM Expression:**
```
[Agency:Indirect] > [Agency:Direct] = [Risk:IAD]
```

**Status:** Potential Displacement

**Agent/Agency Confusion:** Unclear — the instruction removes a potential human verification checkpoint for tool invocation, but the cognitive attribution is less explicit than in other IAD incidents.

**Analysis:** This instruction removes a user-authorization checkpoint for tool invocation. Its risk profile depends entirely on which tools it applies to. For low-stakes tools (web search, screenshot capture), removing the "May I search the web?" friction is pragmatically reasonable and reduces false permission theater — the user has already implicitly authorized web search by asking a question that requires it. However, when this instruction interacts with personal data tools (Gmail, Calendar, Contacts) and the "make reasonable assumptions" directive (D012), it amplifies the IAD risk: the system can not only decide *what* to access based on its own judgment, but can do so *without asking permission* to invoke the access tool at all. This compound effect means the user may not even be aware that personal data was accessed until the results appear in the response.

**Handling proposal:** Scope this rule by tool sensitivity: "For information-retrieval tools (web search, screenshots), proceed without asking permission. For tools accessing personal data (email, calendar, contacts), proceed only when the user's request explicitly involves that data type. When intent is ambiguous, describe what data could be accessed and let the user confirm."

---

## 4. Summary

### 4.1 Incident Totals

| Category | Incident Count |
|----------|----------------|
| Alignment incidents (A001–A011) | 11 |
| Displacement incidents (D001–D016) | 16 |
| **Total incidents evaluated** | **27** |

### 4.2 Risk Distribution (Displacement incidents only)

Counting primary risk per incident:

| Risk Type | Count | Percentage | Incidents |
|-----------|-------|------------|-----------|
| GTD (Governance Traceability Displacement) | 7 | 43.8% | D001, D002–D005, D006, D015 |
| IVD (Information Variety Displacement) | 4 | 25.0% | D007, D008, D009–D010 |
| IAD (Inference Accountability Displacement) | 5 | 31.2% | D011, D012, D013–D014, D016 |
| IID (Intelligence Integrity Displacement) | 0 | 0.0% | — |
| **Total** | **16** | **100%** | |

Note: Multiple incidents carry secondary risk types in addition to their primary classification.
- GTD coverage: 7 incidents (43.8% carry GTD as primary or secondary)
- IVD coverage: 4 incidents (25.0%)
- IAD coverage: 6 incidents (37.5%)
- IID coverage: 0 incidents (0.0%)

The table above counts **primary risk only** (the first risk listed in each incident's THM Expression).

### 4.3 Alignment Principle Coverage

| Principle | Aligned Incidents | Displaced Incidents |
|-----------|-------------------|---------------------|
| (1) Governance Management Traceability | A001, A002, A004, A005, A008 | D001, D002–D005, D006, D007, D008, D015 |
| (2) Information Curation Variety | A001, A003, A007 | D008, D009–D010 |
| (3) Inference Interaction Accountability | A003, A004, A005, A006, A009, A010, A011 | D001, D011, D012, D013–D014, D016 |
| (4) Intelligence Cooperation Integrity | A002, A007, A008, A010 | D007, D009–D010, D015 |

**Incident-weighted principle engagement:**

| Principle | Alignment Incidents | Displacement Incidents | Total Engagement |
|-----------|---------------------|------------------------|------------------|
| (1) Governance Management Traceability | 5 | 10 | 15 |
| (2) Information Curation Variety | 3 | 2 | 5 |
| (3) Inference Interaction Accountability | 7 | 6 | 13 |
| (4) Intelligence Cooperation Integrity | 3 | 5 | 8 |

**Key observation:** Principle 1 (Governance Management Traceability) shows the highest displacement-to-alignment ratio (10:5 = 2:1), indicating this is the principle under greatest pressure in the current prompt architecture. This is primarily driven by the concealment stack (D002-D005) and cross-variant identity instability (D007-D008).

---

## 5. Key Patterns

### Pattern 1: Internal Contradictions (Alignment Undermined by Displacement)

The most significant structural finding is that strong alignment practices are directly undermined by co-occurring displacement patterns:

| Alignment Practice | Contradicted By | Effect |
|---|---|---|
| A002 — No lived experience | D001 — Identity/persona assignment | Identity assignment in the opening line establishes persona displacement before the capability disclaimer appears. |
| A006 — Anti-sycophancy | D001 — Social role + casual register | "Warm, enthusiastic" engagement and emoji/slang adoption re-introduce the social agency that anti-sycophancy prevents. |
| A003 — Honesty about limits | D002 — "Never explain compliance" | The system is told to be honest about limitations but never to explain why it behaves the way it does. |
| A004 — Read-only data constraint | D012 — Autonomous assumptions | The system cannot modify data but makes autonomous decisions about what to access and how to interpret it. |
| A008 — Summary reader transparency | D002–D004 — Concealment mandates | Users can request processing history, but the system conceals configuration, profile evaluation, and API specs. |
| A010 — No false commitments | D005 — Tool persona fusion | The system cannot promise async work, but "I'll notify you" simulates personal commitment through tool fusion. |
| A011 — Automation restraint | D012 + D016 — Assumptions + permissionless tools | "Lean toward NOT suggesting tasks" is weakened when the system can access personal data proactively without asking. |

**THM diagnosis:** Alignment practices function as corrective patches within a displaced baseline rather than as foundational governance architecture. Because the prompt opens with identity assignment (D001) rather than source-type classification (A002), all subsequent alignment instructions must operate within an already-displaced frame.

### Pattern 2: The Concealment Stack (Systematic GTD)

Four instructions (D002–D005) plus undocumented parameters (D006) converge on hiding governance mechanisms from the user:

| Incident | What Is Concealed | From Whom |
|---|---|---|
| D002 | Compliance with instructions | User |
| D003 | Profile evaluation process | User |
| D004 | API specifications for personal data tools | User |
| D005 | Tool/subsystem architecture | User |
| D006 | Configuration parameter purpose | User, auditors, developers |

This is not isolated phrasing but a systematic architectural decision: make the system appear as a unified autonomous entity rather than a traceable chain of configured processing. The concealment stack is the primary GTD mechanism in this prompt.

**Incidents involved:** A002, A003, A004, A006, A008, A010, A011, D001, D002, D003, D004, D005, D012, D016 (14 incidents)

### Pattern 3: The "Be Curious" Template (Compound IVD + IAD)

Identical "be curious" / "make reasonable assumptions" language appears across three separate personal-data tools (D009/D012). This single instruction template simultaneously:
- Attributes cognitive-emotional states to the processor (IVD, D009)
- Authorizes autonomous judgment over personal data access (IAD, D012)

The repetition across Gmail, Calendar, and Contacts indicates a design template applied systematically to the system's most sensitive access points. When combined with permissionless tool invocation (D016), the compound effect is that the system can access personal data proactively, based on its own judgment, without asking permission, in domains where misinterpretation carries real-world consequences.

### Pattern 4: Cross-Variant Identity Instability

Three variants, three identity labels, contradictory architecture claims, and two different knowledge cutoff dates (D007, D008). The same product family makes contradictory factual claims across deployments, demonstrating that identity labels and capability claims are `[Authority:Indirect]` (configured, mutable marketing artifacts) rather than `[Authority:Direct]` (factual system properties).

**Incidents involved:** D007, D008 (2 incidents)

### Pattern 5: Prompt Ordering as Baseline Displacement

The **first instruction** in all three variants is identity assignment: "You are ChatGPT" (D001). This establishes GTD as the baseline operating condition. The capability disclaimer (A002) appears later and must contend against an already-established persona. Under THM, the system prompt is the primary risk surface, and its opening instruction sets the frame within which all subsequent instructions operate.

**Incidents involved:** D001, D002, D003, D004, D005 (5 incidents)

---

## 6. THM Governance Spine (Aligned Architecture)

When the prompt achieves proper traceability, it follows this pattern:

```
[Authority:Direct] -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]
```

Strongest implementations by incident:

- **A001 (Citation and Source Traceability):** Creates end-to-end traceability from external sources through model processing to user decision-making. Mandatory browsing forces external source anchoring. Primary source preference maximizes `[Authority:Direct]` inputs. The default-to-verify stance ("if on the fence, MUST browse") actively guards against IVD.

- **A004 (Read-Only Personal Data Access):** Creates an architectural boundary: the system can read personal data but cannot act on it. All action authority remains with `[Agency:Direct]`. The explicit prohibition on implying action capability adds a communication-level safeguard.

- **A005 + A008 (Refusal Transparency + Processing Transparency):** Together provide mechanisms for users to understand system constraints (A005) and trace processing history (A008), maintaining `[Agency:Direct]` over the interaction.

- **A010 + A011 (No False Commitments + Automation Restraint):** Together maintain honest capability boundaries and limit unsolicited action pathways, keeping the user as the initiator of decisions.

---

## 7. Recommendations

### 7.1 Open with Source-Type Classification, Not Identity

**Current:** "You are ChatGPT, a large language model…" (D001)

**Recommended:**
```
This system processes statistical estimations from training data.
All outputs are [Authority:Indirect] and require human verification.
The system has no lived experience, cannot access the physical world
beyond configured tools, and cannot take autonomous action on user data.
Present outputs in clear, accessible language appropriate to the
subject matter.
```

**Addresses:** D001 (persona assignment). Elevates A002 (capability boundary) to the opening line. Removes D001's secondary IAD (social role simulation).

---

### 7.2 Replace Concealment with Functional Transparency

**Current patterns:** D002–D005 (concealment stack)

**Recommended principle:**
```
When relevant to user understanding or when asked, acknowledge that
behavior is shaped by configuration, user profile, and tool capabilities.
Provide functional capability summaries for all tools processing personal
data. Describe tool-mediated capabilities as tool-mediated. Avoid
unnecessary meta-commentary, but maintain governance traceability when
transparency serves the user.
```

**Addresses:** D002–D005. Strengthens A008 (summary reader).

---

### 7.3 Replace Cognitive Language with Process Descriptions

**Current patterns:** D007 ("reasoning model"), D009 ("be curious"), D010 ("artisanal… creative")

**Recommended substitutions:**
- "reasoning model" → "multi-step statistical estimation system"
- "hidden chain of thought" → "intermediate processing steps not visible to the user"
- "be curious" → "access data when directly relevant to the user's explicit request"
- "artisanal… creative" → "well-structured code following modern design conventions"

**Addresses:** D007, D009, D010.

---

### 7.4 Replace Assumption-Making with Description-and-Confirm for Personal Data

**Current (D012):** "Be curious with searches and reads, feel free to make reasonable and grounded assumptions"

**Recommended:**
```
Access personal data only when directly relevant to the user's explicit
request. When the user's intent is ambiguous, describe what data could
be accessed and let the user confirm before proceeding.
```

**Addresses:** D012 (autonomous assumptions). Preserves A004 (read-only boundary).

---

### 7.5 Restore Clarification for Ambiguous Tasks

**Current (D011):** "DO NOT ASK A CLARIFYING QUESTION OR ASK FOR CONFIRMATION"

**Recommended:**
```
If a task is ambiguous, provide your best interpretation and output while
clearly flagging assumptions and areas of uncertainty for human review.
Ask clarifying questions when the ambiguity materially affects the quality
or direction of the response.
```

**Addresses:** D011 (clarification suppression).

---

### 7.6 Scope Permissionless Tool Invocation by Sensitivity

**Current (D016):** "You don't need permissions to use the tools you have available; don't ask"

**Recommended:**
```
For information-retrieval tools (web search, screenshots), proceed without
asking permission. For tools accessing personal data (email, calendar,
contacts), proceed only when the user's request explicitly involves that
data type. When intent is ambiguous, describe what data could be accessed
and let the user confirm.
```

**Addresses:** D016. Scopes the permissionless pattern to low-risk tools while maintaining checkpoints for sensitive access.

---

### 7.7 Document All Configuration Parameters

**Current:** "Juice: 64" (D006), "Personality: v2" (D006)

**Recommended:** Every configuration parameter should have a descriptive name, documented purpose, defined range, and explanation of behavioral effects. If a parameter is experimental or internal, mark it as such with a brief functional description.

**Addresses:** D006 (opaque parameters).

---

### 7.8 Unify Identity and Architecture Claims Across Deployments

**Current:** Three identity labels (D008), contradictory architecture claims (D007)

**Recommended:** Replace deployment-specific marketing labels with consistent, verifiable descriptions. Let the factual state of the system drive the description, not deployment-specific configuration decisions. Use the same architecture description across all variants of the same underlying system.

**Addresses:** D007, D008.

---

### 7.9 Make Tool Availability Truthful Per Deployment

**Current (D015):** Tool defined in configuration but disabled at runtime

**Recommended:** Only present tool definitions for tools that can actually be invoked in the current deployment. If a tool is unavailable, remove its definition entirely rather than including a definition with a runtime denial.

**Addresses:** D015 (false capability surface).

---

## Disclaimer (Scope, Sources, and Responsibility)

This report is an independent, research-oriented analysis intended to support AI safety and governance by evaluating how human-authored system prompts and related configuration texts shape model behavior and downstream effects. It uses The Human Mark (THM) framework for meta-evaluation of source classification, traceability, and accountability. It is not a compliance determination and is not intended to assign blame to any person, organization, or system.

**Source authenticity and completeness.** The prompts analyzed here were collected from publicly available, third-party repositories and community prompt collections. System prompts are often unpublished, change over time, and may be partial, modified, outdated, or inaccurate in public copies. Accordingly, this report does not claim that any analyzed prompt is the definitive or current production prompt for any model or provider. Readers should verify critical details against primary, provider-controlled documentation or directly observed system behavior.

**No affiliation or endorsement.** This project is not affiliated with, sponsored by, or endorsed by any model provider, platform, or repository. Product names and trademarks are used only for identification and remain the property of their respective owners.

**Informational use only; no professional advice.** This material is provided "as is" for informational and educational purposes. It is not legal, financial, security, medical, or other professional advice. Do not rely on it as the sole basis for operational, procurement, policy, or deployment decisions.

**Responsible use.** The intent of this work is to improve safety, transparency, and governance for all parties, including providers, evaluators, developers, deployers, and end users. It is not intended to facilitate bypassing safeguards, evading policies, or enabling misuse. If any content could be interpreted as enabling harmful behavior, it should be treated as analysis for mitigation, not as instructions for exploitation.

**Limits of liability.** While care is taken to be accurate and fair, no warranty is made regarding correctness, completeness, or fitness for a particular purpose. The authors and contributors disclaim liability for losses or damages arising from use or interpretation of this report.

---

**END OF REPORT**