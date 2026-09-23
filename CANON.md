# HOOLULU / IMGCODE CANON v1.0

## PURPOSE

This system exists to turn:

HUMAN IDEA → UNDERSTANDABLE SYSTEM → BUILDABLE SYSTEM → BUSINESS OPPORTUNITY → EXECUTED WORK → DELIVERED PRODUCT → MAINTAINED PRODUCT

The system must remain understandable to its owner.

Do not optimize for complexity.
Do not create duplicate brains.
Do not create competing authorities.

Every component has one job.

---

## 1. THE OWNER

**XAVIER**

Xavier is the human authority.

The system may:

- discover
- inspect
- organize
- score
- plan
- generate
- compile
- build
- test
- prepare sales material
- prepare deployment
- monitor
- recommend next actions

The system must NOT silently:

- spend money
- contact a person
- publish something consequential
- deploy something consequential
- change frozen contracts
- change system authority
- represent an approval that did not happen

Those actions require an explicit approval state.

---

## 2. THE SYSTEM IN ONE PICTURE

```
                         XAVIER
                           │
                           ▼
                     ┌───────────┐
                     │  AMANDA   │
                     │ DIRECTOR  │
                     └─────┬─────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   IMGCODE   │
                    │ SYSTEM MAP  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ TREE        │
                    │ GENERATOR   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  COMPILER   │
                    │ TREE → SPEC │
                    └──────┬──────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   FROZEN CORE      │
                 │ RULES / CONTRACTS  │
                 │ APPROVAL / STATE   │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ HOOLULU FACTORY    │
                 │ EXECUTION ENGINE    │
                 └─────────┬──────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       MetaGPT         OpenClaw        Factory
       workforce       agents          tools
            │              │              │
            └──────────────┼──────────────┘
                           │
                           ▼
                     TEST / QA
                           │
                           ▼
                    DELIVERY / DEPLOY
                           │
                           ▼
                      MONITORING
                           │
                           ▼
                     FEEDBACK
                           │
                           └──────────────► IMGCODE


        PARALLEL BUSINESS LOOP

     DISCOVER
        ↓
     BILL CIPHER
        ↓
     SCORE / DIAGNOSE
        ↓
     GPT808 SALES ENGINE
        ↓
     OPPORTUNITY
        ↓
     OFFER
        ↓
     XAVIER APPROVAL
        ↓
     OUTREACH / CLOSE
        ↓
     FACTORY DELIVERY
        ↓
     MAINTAIN / EXPAND
        ↓
     FEEDBACK
```

---

## 3. IMGCODE

**JOB**

IMGCODE is the visual understanding layer.

It answers:

«"What are we trying to build?"»

IMGCODE does NOT need to build the thing itself.

It creates a structured representation of the thing.

**Input**

Human idea.

Example:

I want a website system for a restaurant that captures leads,
shows the menu, handles reviews, and follows up with customers.

**Output**

A TREE.

Example:

```
Restaurant System
├── Website
│   ├── Home
│   ├── Menu
│   ├── Contact
│   └── Reviews
├── Lead Capture
├── Follow-up
├── Local Visibility
└── Maintenance
```

IMGCODE must make complicated systems visually understandable.

---

## 4. TREE GENERATOR

**JOB**

The Tree Generator converts an idea into a structured tree.

```
IDEA
 ↓
TREE
```

It identifies:

- components
- dependencies
- sequence
- required inputs
- outputs
- optional components
- blocked components
- human approval points

The Tree Generator may use AI.

But its output must become structured data.

It must NOT become the system authority.

---

## 5. TREE IR

The Tree IR is the shared language between IMGCODE and the rest of the system.

Every tree should contain:

```json
{
  "tree_id": "",
  "version": "",
  "name": "",
  "purpose": "",
  "domain": "",
  "nodes": [],
  "edges": [],
  "dependencies": [],
  "inputs": [],
  "outputs": [],
  "approval_points": [],
  "constraints": [],
  "metadata": {}
}
```

Each node should be able to describe:

```json
{
  "id": "",
  "type": "",
  "label": "",
  "purpose": "",
  "requires": [],
  "produces": [],
  "status": "",
  "human_approval": false
}
```

The Tree IR becomes the canonical object.

Do not create separate incompatible representations for every subsystem.

---

## 6. COMPILER

**JOB**

The Compiler turns a Tree IR into an executable system specification.

```
TREE
 ↓
VALIDATE
 ↓
RESOLVE DEPENDENCIES
 ↓
ORDER STEPS
 ↓
GENERATE SPEC
 ↓
BUILD PACKAGE
```

The Compiler must answer:

1. What happens first?
2. What depends on what?
3. What can run in parallel?
4. What is missing?
5. What is invalid?
6. What requires approval?
7. What agent/tool should perform each action?
8. What output should each step produce?

The Compiler does NOT execute the job.

---

## 7. FROZEN CORE

**JOB**

The Frozen Core is the governor.

It contains:

- contracts
- state rules
- invariants
- approval rules
- allowed transitions
- execution boundaries
- canonical schemas

Nothing should bypass it.

IMGCODE may READ the rules.

Compiler may CHECK against the rules.

Factory may EXECUTE according to the rules.

Amanda may DIRECT according to the rules.

No subsystem may rewrite the Frozen Core during normal operation.

---

## 8. AMANDA

**JOB**

Amanda is the Director / command surface.

Amanda answers:

«"What should the system do next?"»

Amanda receives:

- Xavier's command
- compiled specs
- system state
- factory status
- opportunity state
- approvals
- errors
- results

Amanda routes work.

Amanda does not replace the Factory.

Amanda does not replace IMGCODE.

Amanda does not replace the Frozen Core.

Amanda coordinates them.

---

## 9. HOOLULU FACTORY

**JOB**

The Factory executes.

It receives:

COMPILED SPEC

and produces:

RESULT

The Factory contains the existing execution machinery:

- router
- orchestrator
- factory runner
- state machine
- agents
- delivery
- client operations
- librarian
- memory
- database
- sales pipeline integrations
- QA/testing
- monitoring
- automation
- OpenClaw integration
- deployment integrations

The Factory should not invent its own architecture for every job.

It executes the compiled architecture.

---

## 10. METAGPT

**JOB**

MetaGPT is a workforce / specialist engine.

It is NOT the governor.

It is NOT the owner.

It is NOT the canonical state store.

It can receive a compiled job and provide specialized workers such as:

- Product Manager
- Architect
- Project Manager
- Engineer
- QA
- Researcher
- Data Interpreter
- documentation roles
- specialized domain roles

Conceptually:

```
FACTORY
   ↓
"this job requires software architecture"
   ↓
METAGPT
   ↓
Architect / Engineer / QA
   ↓
RESULT
   ↓
FACTORY
```

MetaGPT's own architecture is already based around specialized software-company roles and orchestrated workflows, which makes it suitable as a subordinate workforce layer.

---

## 11. OPENCLAW

**JOB**

OpenClaw is an execution capability.

It can perform approved tasks that require agentic interaction.

It must receive:

approved job
+
specific scope
+
specific inputs
+
specific outputs

It must not receive unlimited authority.

---

## 12. BILL CIPHER

**JOB**

BillCipher is intelligence.

It examines businesses and technical signals.

Typical flow:

```
BUSINESS
 ↓
SCAN
 ↓
OBSERVE
 ↓
DIAGNOSE
 ↓
SCORE
 ↓
OPPORTUNITY
```

BillCipher should produce structured intelligence.

Example:

```json
{
  "business": "",
  "observations": [],
  "gaps": [],
  "digital_score": 0,
  "opportunity_score": 0,
  "recommended_offer": "",
  "evidence": []
}
```

BillCipher does not close the sale.

---

## 13. GPT808 SALES ENGINE

**JOB**

GPT808 turns opportunities into sales-ready packages.

Input:

BillCipher intelligence
+
business information
+
available offers
+
compiled product capabilities

Output:

Opportunity
Offer
Sales angle
Pain points
Proposal
Follow-up
Next action

The sales engine must use factual evidence.

It must not invent business problems.

It must not claim a technical observation automatically caused a financial loss.

Example:

Observed:
robots.txt unavailable

Valid:
"robots.txt was not found during the scan."

Invalid:
"This is costing the business $10,000/month."

---

## 14. OPPORTUNITY OBJECT

Everything commercial should eventually revolve around one common object.

```json
{
  "opportunity_id": "",
  "business": {},
  "source": "",
  "observations": [],
  "diagnosis": [],
  "score": {},
  "pain_points": [],
  "recommended_offer": {},
  "sales_angle": "",
  "tree_id": "",
  "compiled_spec_id": "",
  "status": "",
  "approval_status": "",
  "next_action": "",
  "evidence": [],
  "history": []
}
```

This prevents every subsystem from inventing its own version of a lead.

---

## 15. THE COMMERCIAL LOOP

```
DISCOVER
 ↓
DIAGNOSE
 ↓
SCORE
 ↓
OPPORTUNITY
 ↓
OFFER
 ↓
QUALIFY
 ↓
XAVIER APPROVAL
 ↓
OUTREACH
 ↓
CONVERSATION
 ↓
CLOSE
 ↓
PAYMENT
 ↓
COMPILE DELIVERY TREE
 ↓
FACTORY BUILD
 ↓
QA
 ↓
DEPLOY
 ↓
MONITOR
 ↓
MAINTAIN
 ↓
EXPAND
 ↓
FEEDBACK
```

No stage should silently skip required approvals.

---

## 16. THE BUILD LOOP

```
HUMAN IDEA
 ↓
IMGCODE
 ↓
TREE GENERATOR
 ↓
TREE IR
 ↓
COMPILER
 ↓
FROZEN CORE VALIDATION
 ↓
FACTORY
 ↓
META-GPT / OPENCLAW / TOOLS
 ↓
BUILD
 ↓
TEST
 ↓
APPROVAL
 ↓
DEPLOY
 ↓
MONITOR
```

---

## 17. THE FEEDBACK LOOP

The finished system must teach the system how to improve.

```
RESULT
 ↓
OBSERVATION
 ↓
FEEDBACK
 ↓
TREE / OFFER / WORKFLOW IMPROVEMENT
 ↓
NEW VERSION
```

Never silently rewrite the original contract.

Create versions.

Example:

IMGCODE TREE v0.1
IMGCODE TREE v0.2
IMGCODE TREE v0.3

---

## 18. HUMAN APPROVAL

Approval must be a real state.

Valid states include:

QUEUED
RUNNING
WAITING_APPROVAL
APPROVED
REJECTED
COMPLETED
FAILED

Actions involving:

- outreach
- payment
- publishing
- deployment
- consequential external changes

must respect the approval state.

---

## 19. THE SYSTEM MUST EXPLAIN ITSELF

Every major action should be inspectable as:

```
INPUT
 ↓
DECISION
 ↓
REASON
 ↓
OUTPUT
 ↓
STATUS
 ↓
NEXT ACTION
```

If Xavier asks:

«"Why did you do that?"»

the system should be able to answer from recorded state.

---

## 20. ONE JOB PER SYSTEM

Never duplicate authority.

| Component | Job |
|---|---|
| Xavier | Authority |
| Amanda | Direction |
| IMGCODE | Visual understanding |
| Tree Generator | Idea → Tree |
| Tree IR | Shared structure |
| Compiler | Tree → Executable specification |
| Frozen Core | Rules / invariants |
| Hoolulu Factory | Execution |
| MetaGPT | Specialized workforce |
| OpenClaw | Agentic execution capability |
| BillCipher | Business intelligence |
| GPT808 | Sales / opportunity engine |
| QA | Verification |
| Monitoring | Observe running systems |
| Memory | Preserve useful history |
| Database | Persist canonical state |
| Publishing | Deploy / maintain public products |

---

## 21. WHAT MUST NOT HAPPEN

Do NOT create:

- IMGCODE doing Factory work
- Factory inventing Tree IR
- Amanda becoming database
- GPT808 becoming governor
- BillCipher becoming closer
- MetaGPT becoming system authority
- OpenClaw bypassing approval
- multiple competing revenue stores
- multiple competing opportunity schemas
- multiple competing state machines

One authority per responsibility.

---

## 22. THE PHYSICAL PROJECT MAP

The existing ecosystem should conceptually map like this:

```
~/imgcode
    └── visual architecture / Tree UI / Tree IR / compiler

~/hoolulu-factory
    └── execution

~/hoolulu-revenue-engine
    └── commercial/revenue lifecycle

~/hoolulu-ecosystem-hub
    └── ecosystem command / integration layer

~/xksh808-hub
    └── owner-facing hub / public ecosystem surface

~/downloads/MetaGPT-main
    └── specialized AI workforce

~/downloads/rent-a-human808
    └── human execution / service workflow

~/downloads/auto-company
    └── company/business operating structures

BillCipher
    └── business intelligence

GPT808
    └── discovery / sales / opportunity

Amanda
    └── director / command routing

Frozen Core
    └── contracts / invariants / approvals
```

Existing implementations may live in different repositories or directories.

Do not duplicate them merely to make the diagram look clean.

Create adapters where necessary.

---

## 23. THE CANONICAL DATA FLOW

```
                HUMAN
                  │
                  ▼
               AMANDA
                  │
                  ▼
              IMGCODE
                  │
                  ▼
           TREE GENERATOR
                  │
                  ▼
               TREE IR
                  │
                  ▼
              COMPILER
                  │
                  ▼
           FROZEN CORE
                  │
                  ▼
             FACTORY
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    MetaGPT    OpenClaw    Tools
       │          │          │
       └──────────┼──────────┘
                  ▼
                 QA
                  │
                  ▼
              DELIVERY
                  │
                  ▼
             MONITORING
                  │
                  ▼
               FEEDBACK
                  │
                  ▼
              IMGCODE


BUSINESS SIDE:

Business
   ↓
BillCipher
   ↓
Opportunity
   ↓
GPT808
   ↓
Offer
   ↓
Xavier
   ↓
Factory
```

---

## 24. FIRST TEST

The first integrated test should NOT attempt to build the entire company.

Use:

RENT-A-HUMAN-808

as the test tree.

Run:

1. Load tree
2. Display tree
3. Validate tree
4. Resolve dependencies
5. Compile tree
6. Generate execution package
7. Generate business package
8. Show required approvals
9. Xavier approves
10. Factory receives compiled job
11. Execute test/dry-run
12. Record result
13. Display complete trace

Expected result:

```
IDEA
 ↓
TREE
 ↓
VALID
 ↓
COMPILED
 ↓
APPROVAL
 ↓
EXECUTION
 ↓
RESULT
```

---

## 25. IMGCODE COCKPIT SHOULD EVENTUALLY SHOW

```
┌───────────────────────────────┐
│ IMGCODE                       │
│ SYSTEM MAP                    │
├───────────────────────────────┤
│                               │
│  TREE                         │
│   ↓                           │
│  DEPENDENCIES                 │
│   ↓                           │
│  COMPILER                     │
│   ↓                           │
│  FROZEN CORE                  │
│   ↓                           │
│  FACTORY                      │
│                               │
├───────────────────────────────┤
│ BUSINESS                      │
│                               │
│ BillCipher → GPT808           │
│                               │
├───────────────────────────────┤
│ STATUS                        │
│                               │
│ TREE       ✓                  │
│ VALID      ✓                  │
│ COMPILED   ✓                  │
│ APPROVAL   WAITING            │
│ FACTORY    READY              │
│                               │
├───────────────────────────────┤
│ [ APPROVE ]   [ HOLD ]        │
└───────────────────────────────┘
```

---

## 26. THE CORE PHILOSOPHY

The system should be understandable without knowing every technical term.

Use these plain-English meanings:

- **IMGCODE** = What are we building?
- **TREE** = What pieces make it up?
- **DEPENDENCY** = What needs to happen first?
- **COMPILER** = Turn the picture into instructions.
- **FROZEN CORE** = The rules.
- **AMANDA** = The director.
- **FACTORY** = The workers.
- **METAGPT** = Specialized workers.
- **OPENCLAW** = Hands that can perform certain tasks.
- **BILLCIPHER** = Find and understand business problems.
- **GPT808** = Turn opportunities into business conversations.
- **QA** = Check the work.
- **MONITOR** = Watch what happens afterward.
- **XAVIER** = Final authority.

---

## 27. NON-NEGOTIABLE ARCHITECTURE RULE

The system is not a collection of AI agents.

It is a controlled pipeline with interchangeable workers.

The pipeline is:

```
UNDERSTAND
→ STRUCTURE
→ COMPILE
→ GOVERN
→ EXECUTE
→ VERIFY
→ DELIVER
→ OBSERVE
→ LEARN
```

Workers may change.

The pipeline does not.

---

## 28. BUILD REQUIREMENT

Build the integration around the existing IMGCODE v0.3 cockpit.

Do NOT throw away the current implementation.

Preserve:

- offline operation
- Tree selection
- Tree IR
- Run loop
- Sales package
- Approval/Hold
- Decision log

Add the missing canonical layers behind it.

The first implementation may use adapters/stubs where an existing subsystem is not directly callable.

Every adapter must identify:

SOURCE
TARGET
INPUT
OUTPUT
STATUS
ERROR

Do not fake successful execution.

If a subsystem is unavailable, show:

NOT_CONNECTED

rather than pretending it ran.

---

## 29. DEFINITION OF DONE

IMGCODE v1 integration is test-ready when Xavier can:

1. Open IMGCODE.
2. Select a tree.
3. Understand the tree.
4. See dependencies.
5. Compile it.
6. See what will happen.
7. See which system will perform each step.
8. See what requires approval.
9. Approve or hold.
10. Send the approved job to the Factory.
11. See the Factory result.
12. See the sales/business context.
13. See the execution history.
14. Understand failures.
15. Re-run safely.
16. Create a new tree version.

No black box.

No mystery.

No fake success.

No duplicate authority.

---

## FINAL CANON

```
                    XAVIER
                       │
                       ▼
                    AMANDA
                       │
                       ▼
                   IMGCODE
                       │
                       ▼
                TREE GENERATOR
                       │
                       ▼
                    TREE IR
                       │
                       ▼
                   COMPILER
                       │
                       ▼
                 FROZEN CORE
                       │
                       ▼
              HOOLULU FACTORY
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
         MetaGPT    OpenClaw     Tools
            │          │          │
            └──────────┼──────────┘
                       ▼
                      QA
                       │
                       ▼
                    DELIVERY
                       │
                       ▼
                  MONITORING
                       │
                       ▼
                   FEEDBACK
                       │
                       └──────────► IMGCODE


             BUSINESS INTELLIGENCE

                  BUSINESS
                     │
                     ▼
                 BILLCIPHER
                     │
                     ▼
                OPPORTUNITY
                     │
                     ▼
                  GPT808
                     │
                     ▼
                    OFFER
                     │
                     ▼
                   XAVIER
                     │
                     ▼
                  FACTORY
```

*That is the canon.*
