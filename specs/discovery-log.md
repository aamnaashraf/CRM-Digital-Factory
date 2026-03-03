# Discovery Log - Exercise 1.1: Initial Exploration

**Date:** February 17, 2026
**Phase:** Stage 1 - Incubation
**Exercise:** 1.1 - Initial Exploration and Pattern Analysis

## Objective
Analyze sample tickets, identify patterns across channels, understand business requirements, and propose initial system design.

---

## 1. Sample Ticket Analysis

### Total Tickets Analyzed
- **Count:** 55 tickets
- **Date Range:** January 15-20, 2024
- **Channels:** Email, WhatsApp, Web Form

### Channel Distribution
- **Email:** 20 tickets (36.4%)
- **WhatsApp:** 20 tickets (36.4%)
- **Web Form:** 15 tickets (27.3%)

---

## 2. Pattern Identification

### Communication Style by Channel

#### Email Patterns
**Observations:**
- **Length:** Longest messages (100-300 words), structured with greetings/closings
- **Formality:** High - professional tone, proper grammar, full sentences
- **Structure:** Greeting → Context → Problem → Request → Signature
- **Common elements:** Subject lines, formal salutations ("Hi TaskFlow team", "Hello"), signatures with titles
- **Examples:** Tickets #1, #4, #6, #9, #12, #14, #17, #20, #23, #26, #28, #31, #34, #36, #39, #41, #44, #47, #50, #52, #55

#### WhatsApp Patterns
**Observations:**
- **Length:** Shortest messages (10-50 words), conversational
- **Formality:** Low - casual tone, abbreviations ("q" for question), incomplete sentences
- **Emoji usage:** Frequent (😤, 🎉, 🌙, 🚀, ⌨️)
- **Structure:** Direct question or statement, minimal context
- **Tone:** Friendly, immediate, like texting a friend
- **Examples:** Tickets #2, #5, #8, #10, #13, #16, #19, #22, #24, #27, #30, #32, #35, #38, #40, #43, #46, #48, #51, #54

#### Web Form Patterns
**Observations:**
- **Length:** Medium (50-150 words), focused and concise
- **Formality:** Medium - professional but less formal than email
- **Structure:** Subject line + problem description, no greeting/closing
- **Tone:** Direct, problem-focused, efficient
- **Examples:** Tickets #3, #7, #11, #15, #18, #21, #25, #29, #33, #37, #42, #45, #49, #53

---

## 3. Issue Category Analysis

### Category Breakdown
| Category | Count | Percentage | Priority Distribution | Common Keywords |
|----------|-------|------------|----------------------|-----------------|
| Integration Issues | 9 | 16.4% | Medium-High | Slack, Google Calendar, GitHub, API, webhook |
| Billing/Account | 6 | 10.9% | High-Urgent | charged, refund, invoice, pricing, downgrade |
| How-To Questions | 15 | 27.3% | Low-Medium | how do I, can I, where do I find |
| Bug Reports | 8 | 14.5% | Medium-High | not working, error, crashing, slow |
| Feature Requests | 7 | 12.7% | Low | feature request, do you have, plans to add |
| Access/Security | 5 | 9.1% | High-Urgent | login, password, locked, access, security |
| Performance Issues | 3 | 5.5% | Medium | slow, loading, battery drain |
| Migration/Onboarding | 2 | 3.6% | High | migration, setup assistance |

### Escalation-Worthy Issues Identified

**Immediate Escalation Required:**
1. **Ticket #3** - Duplicate billing charge, demanding immediate refund (negative sentiment)
2. **Ticket #9** - Security issue: deactivated user still has access (urgent priority)
3. **Ticket #19** - Churn threat: demanding refund and cancellation (very negative sentiment)
4. **Ticket #52** - Account locked, urgent business need (very negative sentiment)
5. **Ticket #4** - Enterprise pricing inquiry (high-value opportunity)
6. **Ticket #44** - Legal terms review required (enterprise deal)
7. **Ticket #36** - Security questionnaire (compliance requirement)
8. **Ticket #47** - Data residency requirements (compliance/legal)
9. **Ticket #28** - GDPR data export request (legal requirement)

**Potential Escalation (Monitor):**
10. **Ticket #12** - API rate limit issue (may need custom plan)
11. **Ticket #26** - SSO setup assistance (technical complexity)
12. **Ticket #50** - Large migration from competitor (high-value opportunity)

---

## 4. Sentiment Analysis

### Sentiment Distribution
- **Very Positive:** 2 tickets (3.6%) - #14, #43
- **Positive:** 6 tickets (10.9%) - #2, #8, #16, #27, #32, #48, #50
- **Neutral:** 35 tickets (63.6%) - Majority
- **Negative:** 10 tickets (18.2%) - #3, #5, #13, #24, #37, #41, #45, #49, #55
- **Very Negative:** 2 tickets (3.6%) - #19, #52

### High-Risk Tickets (Churn Risk)
1. **Ticket #19** (Pierre Dubois) - Explicit churn threat: "I want a full refund and to cancel my account"
2. **Ticket #52** (Elizabeth Rodriguez) - Account locked, urgent need, very frustrated
3. **Ticket #3** (Maria Garcia) - Billing issue with "unacceptable" language
4. **Ticket #5** (Ana Silva) - App crashing, high frustration

---

## 5. Customer Identification Patterns

### Email-Based Identification
- Primary identifier for email and web form channels
- Format: firstname.lastname@company.domain
- Company domains reveal customer type (startup.io, enterprise.com, agency.com)
- Can track across email and web form if same email used

### Phone-Based Identification (WhatsApp)
- International format with country codes (+44, +55, +1, +33, +81, +61, +34)
- Cannot easily link to email-based customers
- Need separate customer record or manual linking

### Cross-Channel Tracking Challenges
- **Challenge 1:** Same customer using different channels (email vs WhatsApp) = separate identities
- **Challenge 2:** No natural key to link email address to phone number
- **Challenge 3:** Name matching unreliable (common names, spelling variations)
- **Solution needed:** Customer profile system that can link multiple contact methods

---

## 6. Response Complexity Analysis

### Simple (AI Can Handle Autonomously)
**Examples:**
- #2: How to set up recurring tasks (documentation lookup)
- #6: How to export project data (documentation lookup)
- #8: Change color coding in timeline view (feature question)
- #10: Language settings availability (feature question)
- #16: Student discount inquiry (pricing policy)
- #22: How to add subtasks (documentation lookup)
- #30: Change email address (account management)
- #35: How to delete a project (documentation lookup)
- #38: Multiple assignees per task (feature question)
- #46: Personal vs team usage (product question)
- #51: Archive completed projects (documentation lookup)
- #54: Microsoft Teams integration (integration question)

**Characteristics:**
- Answerable from product documentation
- No account-specific investigation needed
- Clear, straightforward answers
- Low risk if answered incorrectly

### Medium (AI Can Handle with Knowledge Base)
**Examples:**
- #1: Slack integration not syncing (troubleshooting)
- #7: Google Calendar sync delayed (troubleshooting)
- #15: Automation rules not triggering (troubleshooting)
- #18: Mobile app offline mode (feature explanation)
- #20: GitHub integration error (troubleshooting)
- #21: Bulk task import (feature guidance)
- #25: Custom fields feature (feature availability)
- #29: Task dependencies not showing (potential bug)
- #33: Webhook configuration (technical troubleshooting)
- #34: File storage limit (plan limits)
- #37: Notification frequency customization (settings guidance)
- #39: API documentation clarity (documentation improvement)
- #42: Guest access permissions (feature configuration)

**Characteristics:**
- Requires troubleshooting steps
- May need to check account settings
- Technical but not critical
- Can provide self-service solutions

### Complex (Requires Escalation)
**Examples:**
- #3: Duplicate billing charge (financial)
- #4: Enterprise pricing inquiry (sales)
- #9: Security issue - deactivated user access (security)
- #12: API rate limit exceeded (custom plan)
- #19: Churn threat with refund demand (retention)
- #26: SSO setup assistance (technical implementation)
- #28: GDPR data export request (legal/compliance)
- #36: Security questionnaire (compliance)
- #44: Legal terms review (legal)
- #47: Data residency requirements (compliance)
- #50: Large migration assistance (customer success)
- #52: Account locked urgently (security + retention)

**Characteristics:**
- Financial, legal, or security implications
- Requires human judgment
- High-value opportunities
- Churn risk
- Compliance requirements

---

## 7. Knowledge Base Requirements

### Topics That Need Documentation
1. **Integrations:** Slack, Google Calendar, GitHub, Microsoft Teams, API, Webhooks
2. **Task Management:** Recurring tasks, subtasks, dependencies, bulk import, templates
3. **Views & Visualization:** Timeline, Calendar, Kanban, color coding
4. **Account Management:** Email change, downgrade, data export, archiving
5. **Permissions:** Guest access, SSO, user deactivation
6. **Mobile App:** Offline mode, features, troubleshooting
7. **Customization:** Custom fields, automation rules, notification settings
8. **Billing:** Plans, pricing, invoices, storage limits
9. **Data & Privacy:** GDPR, data residency, security
10. **Migration:** From competitors (Asana, Monday.com)

### Frequently Asked Questions Identified
1. **"How do I set up recurring tasks?"** - Tickets #2
2. **"How do I export project data?"** - Tickets #6
3. **"Does TaskFlow integrate with [X]?"** - Tickets #1, #7, #20, #54
4. **"How do I [basic task management]?"** - Tickets #22, #35, #38, #51
5. **"What are the plan limits?"** - Tickets #34, #40
6. **"How do I customize notifications?"** - Ticket #37
7. **"Does the mobile app work offline?"** - Ticket #18
8. **"Do you offer [discount/pricing]?"** - Tickets #16, #4
9. **"How do I set up [advanced feature]?"** - Tickets #15, #25, #33, #42
10. **"Can I migrate from [competitor]?"** - Ticket #50

### Integration-Specific Knowledge Needed
- **Slack:** Notification setup, troubleshooting sync issues, workspace connection
- **Google Calendar:** Sync frequency (15 min), two-way sync, troubleshooting delays
- **GitHub:** App installation, organization permissions, error handling
- **Microsoft Teams:** Availability, setup process
- **API:** Rate limits by plan, authentication, endpoints, code examples
- **Webhooks:** Configuration, event types, debugging

---

## 8. Edge Cases and Special Scenarios

### Identified Edge Cases

1. **Multi-Channel Customer Tracking**
   - Description: Same customer contacts via email and WhatsApp
   - Example: Customer emails from work, WhatsApps from personal phone
   - Proposed Handling: Implement customer matching logic (name + fuzzy matching), allow manual linking

2. **Urgent Issues Outside Business Hours**
   - Description: Critical issues (account locked, security) arrive at night/weekends
   - Example Tickets: #52 (account locked, presentation in 2 hours)
   - Proposed Handling: Escalate urgent + negative sentiment immediately, set expectations for response time

3. **Language Preferences**
   - Description: Customers asking in non-English languages
   - Example Tickets: #10 (Spanish greeting "Hola!")
   - Proposed Handling: Detect language, respond in same language if possible, note preference

4. **Competitor Comparisons**
   - Description: Customers asking why TaskFlow is better than competitors
   - Example Tickets: #17, #40
   - Proposed Handling: Follow brand voice guideline (never discuss competitors), focus on TaskFlow strengths

5. **Churn Threats**
   - Description: Explicit cancellation/refund demands
   - Example Tickets: #19
   - Proposed Handling: Immediate escalation, empathetic response, human follow-up within 1 hour

6. **Legal/Compliance Requests**
   - Description: GDPR, security questionnaires, legal reviews
   - Example Tickets: #28, #36, #44, #47
   - Proposed Handling: Automatic escalation to legal/compliance team, acknowledge receipt

7. **High-Value Opportunities**
   - Description: Enterprise inquiries, large migrations
   - Example Tickets: #4, #50
   - Proposed Handling: Escalate to sales team, fast response (< 2 hours)

8. **Account Security Issues**
   - Description: Unauthorized access, locked accounts
   - Example Tickets: #9, #13, #52
   - Proposed Handling: Immediate escalation, security team involvement

---

## 9. Proposed System Architecture

### High-Level Design
```
┌─────────────────────────────────────────────────────────────┐
│                    CHANNEL INTAKE LAYER                      │
├──────────────┬──────────────────┬──────────────────────────┤
│ Gmail API    │ Twilio WhatsApp  │ Web Form (FastAPI)       │
│ (Pub/Sub)    │ (Webhook)        │ (POST /support/submit)   │
└──────┬───────┴────────┬─────────┴──────────┬───────────────┘
       │                │                    │
       └────────────────┴────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Kafka Topic    │
              │  "inquiries"    │
              └────────┬────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │   AI AGENT PROCESSOR        │
         │  (OpenAI Agents SDK)        │
         ├─────────────────────────────┤
         │ 1. Message Normalizer       │
         │ 2. Customer Identifier      │
         │ 3. Conversation Retriever   │
         │ 4. Knowledge Base Search    │
         │ 5. Sentiment Analyzer       │
         │ 6. Response Generator       │
         │ 7. Escalation Decider       │
         │ 8. Channel Adapter          │
         └──────────┬──────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌──────────┐
   │ Gmail  │  │ Twilio │  │ FastAPI  │
   │  API   │  │   API  │  │ Response │
   └────────┘  └────────┘  └──────────┘
        │           │           │
        └───────────┴───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  PostgreSQL CRM      │
         ├──────────────────────┤
         │ • customers          │
         │ • conversations      │
         │ • tickets            │
         │ • messages           │
         └──────────────────────┘
```

### Data Flow
1. **Message Arrival:** Customer sends message via email/WhatsApp/web form
2. **Channel Handler:** Webhook/API receives message, extracts metadata (channel, customer_id, timestamp)
3. **Kafka Ingestion:** Normalized message published to Kafka topic
4. **Agent Processing:**
   - Identify/create customer record
   - Retrieve conversation history
   - Search knowledge base for relevant docs
   - Analyze sentiment
   - Generate channel-appropriate response
   - Decide if escalation needed
5. **Response Delivery:** Send via original channel
6. **Logging:** Store conversation, ticket, message in PostgreSQL

### State Management Needs
- **Conversation History:** Last 10 messages per customer, stored in PostgreSQL
- **Customer Context:** Name, email, phone, plan type, sentiment score, escalation history
- **Sentiment Tracking:** Running average, flag if drops below threshold
- **Ticket Status:** Open/pending/escalated/resolved, assigned agent, resolution notes

---

## 10. Questions and Clarifications Needed

### Business Logic Questions
1. **Response Time SLA:** What's the target response time? (Suggested: <3 seconds for AI, <1 hour for escalated)
2. **Escalation Routing:** Who receives escalated tickets? (Sales, Support, Security, Legal teams?)
3. **Business Hours:** Should AI set different expectations for after-hours inquiries?
4. **Sentiment Threshold:** At what sentiment score should we auto-escalate? (Suggested: <-0.7)
5. **Knowledge Base:** Do we have existing documentation to import, or build from scratch?

### Technical Questions
1. **Gmail API:** Use Pub/Sub push notifications or polling? (Recommended: Pub/Sub for real-time)
2. **Twilio Setup:** Do we have Twilio account credentials and WhatsApp Business approval?
3. **Database Schema:** Should we track message-level sentiment or conversation-level?
4. **Kafka Retention:** How long to retain messages in Kafka? (Suggested: 7 days)
5. **AI Model:** Use OpenAI GPT-4 or Claude? (Consider cost vs quality)

### Escalation Policy Questions
1. **Billing Issues:** Always escalate or only if amount > $X?
2. **Bug Reports:** Escalate all or only high-priority/urgent?
3. **Feature Requests:** Log for product team or respond immediately?
4. **Competitor Questions:** Deflect or provide comparison?

---

## 11. Initial Recommendations

### Quick Wins
1. **Build comprehensive FAQ knowledge base** - 60% of tickets are simple how-to questions
2. **Implement sentiment-based escalation** - Catch churn risks early
3. **Create channel-specific response templates** - Maintain appropriate tone
4. **Set up customer identification logic** - Link email and phone records
5. **Automate billing/legal escalations** - Zero tolerance for errors in these areas

### Risk Areas
1. **Security Issues:** Must escalate immediately, no AI handling (tickets #9, #52)
2. **Billing Errors:** High churn risk, need human empathy (tickets #3, #19)
3. **Cross-Channel Identity:** Risk of duplicate tickets if not linked properly
4. **Legal/Compliance:** GDPR, security questionnaires require specialized knowledge
5. **High-Value Opportunities:** Enterprise deals need sales expertise (tickets #4, #50)

### Success Metrics
1. **Response Time:** <3 seconds for AI responses, <1 hour for escalations
2. **Resolution Rate:** >85% of simple/medium tickets resolved by AI
3. **Escalation Accuracy:** <5% false escalations (AI escalates when not needed)
4. **Customer Satisfaction:** >4.0/5.0 rating on AI interactions
5. **Cost Savings:** <$1,000/year AI cost vs $75,000/year human FTE
6. **Sentiment Improvement:** Average sentiment score increases over time
7. **Churn Prevention:** 0 churns due to delayed response on escalated tickets

---

## 12. Next Steps

### Immediate Actions
1. ✅ Complete ticket analysis (DONE)
2. ✅ Document patterns and requirements (DONE)
3. Build knowledge base from product-docs.md
4. Define escalation decision tree
5. Create channel-specific response templates

### Prototype Priorities (Exercise 1.2)
1. **Core Message Processing Loop:**
   - Input: message + channel + customer_id
   - Normalize message format
   - Search knowledge base
   - Generate response
   - Output: response + escalation_decision

2. **Channel Adaptation:**
   - Email: Formal, structured, with greeting/closing
   - WhatsApp: Casual, concise, emoji-friendly
   - Web: Professional, direct, no greeting

3. **Escalation Logic:**
   - Implement rules from escalation-rules.md
   - Sentiment threshold checking
   - Keyword detection (billing, refund, legal, security)

---

## Notes and Observations

### Key Insights
1. **Channel matters:** Same question asked differently on email vs WhatsApp requires different response style
2. **Sentiment is critical:** Negative sentiment + billing/security = immediate escalation
3. **Integration issues are common:** Need robust troubleshooting guides for Slack, Google Calendar, GitHub
4. **Enterprise opportunities:** Several high-value tickets (#4, #50) - fast response crucial
5. **Churn prevention:** Tickets #19, #52 show how quickly customers can go from frustrated to churning

### Surprising Findings
1. **Positive feedback tickets:** Customers send thank-you messages (#14) and referral inquiries (#43) - opportunity to delight
2. **International customers:** Multiple languages/regions - may need localization
3. **Mobile app issues:** Several tickets about crashes, battery drain - product team needs visibility
4. **Documentation gaps:** API docs unclear (#39), offline mode confusing (#18)

### Design Decisions Made
1. **Use Kafka for ingestion:** Decouples channel handlers from agent processing
2. **PostgreSQL for CRM:** Relational model fits customer/conversation/ticket structure
3. **Sentiment-based escalation:** Proactive churn prevention
4. **Channel-aware responses:** Same answer, different tone per channel
5. **Knowledge base first:** Try to answer from docs before escalating

---

**Analysis Complete:** Ready to proceed to Exercise 1.2 - Prototype Core Loop
