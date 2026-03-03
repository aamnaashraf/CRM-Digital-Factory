# Escalation Rules for AI Customer Success Agent

## Overview
The AI agent should handle routine inquiries autonomously but escalate complex, sensitive, or high-risk issues to human agents. This document defines clear escalation criteria.

## Automatic Escalation Triggers

### 1. Billing and Financial Issues
**Escalate immediately if:**
- Customer reports duplicate charges or incorrect billing
- Refund requests of any amount
- Payment failures or declined cards
- Pricing negotiations or custom quotes
- Invoice disputes
- Subscription cancellation requests (retain customer, human touch needed)

**Rationale:** Financial issues require human judgment, empathy, and authority to resolve. Mistakes can lead to churn and legal issues.

### 2. Legal and Compliance
**Escalate immediately if:**
- GDPR, CCPA, or other data privacy requests (data export, deletion, access)
- Legal terms review or contract negotiations
- Security questionnaires or compliance certifications
- Data residency requirements
- Subpoena or legal demands
- Terms of Service disputes

**Rationale:** Legal matters require expertise and carry significant risk. Must be handled by qualified personnel.

### 3. Security and Access Issues
**Escalate immediately if:**
- Account locked or suspended
- Unauthorized access suspected
- User reports security breach or data leak
- SSO configuration issues (affects entire organization)
- Permission/access control problems affecting multiple users
- Former employee still has access (security risk)

**Rationale:** Security issues are time-sensitive and can have serious consequences. Require immediate human attention.

### 4. Sentiment-Based Escalation
**Escalate if sentiment score < -0.7 (very negative) AND:**
- Customer explicitly threatens to cancel/churn
- Customer mentions competitors or switching
- Customer uses profanity or aggressive language
- Customer expresses extreme frustration (multiple complaints, "terrible service", etc.)
- Customer mentions waiting multiple days without response

**Rationale:** Highly dissatisfied customers are at risk of churning. Human empathy and problem-solving can save the relationship.

### 5. Enterprise and High-Value Accounts
**Escalate immediately if:**
- Enterprise pricing inquiries (150+ users)
- Custom SLA requests
- Dedicated account manager requests
- Migration assistance for large datasets (1000+ tasks)
- Custom contract terms or MSA negotiations
- Multi-year commitment discussions

**Rationale:** High-value deals require sales expertise and relationship building. Potential revenue justifies human involvement.

### 6. Technical Issues Beyond AI Capability
**Escalate if:**
- Bug reports that AI cannot reproduce or diagnose
- API integration issues requiring code review
- Webhook debugging (requires access to customer systems)
- Performance issues with specific projects (requires database investigation)
- Data corruption or loss reports
- Issues persisting after AI provides standard troubleshooting steps

**Rationale:** Complex technical issues may require engineering team involvement or access to internal systems.

### 7. Feature Requests and Product Feedback
**Do NOT escalate, but log for product team:**
- Feature requests (track in CRM, aggregate for product roadmap)
- UI/UX feedback
- Integration requests for new tools
- Pricing tier suggestions

**Exception - Escalate if:**
- Customer threatens to churn due to missing feature
- Enterprise customer makes feature request as part of deal negotiation

### 8. Competitor Mentions
**Never discuss competitors. Escalate if:**
- Customer asks for direct comparison with competitors (Asana, Monday.com, etc.)
- Customer mentions switching to competitor
- Customer asks "Why are you better than X?"

**AI Response:** "I focus on helping you get the most out of TaskFlow. If you'd like to discuss how TaskFlow compares to other tools, I can connect you with our team who can provide detailed comparisons. Would that be helpful?"

## Escalation Workflow

### Step 1: Acknowledge and Empathize
Before escalating, the AI should:
1. Acknowledge the customer's concern
2. Express empathy
3. Explain that a specialist will help

**Example:**
"I understand this billing issue is frustrating and needs immediate attention. Let me connect you with our billing specialist who can resolve this right away. They'll reach out within 1 hour."

### Step 2: Collect Context
Gather all relevant information before escalating:
- Customer ID and account details
- Full conversation history
- Issue summary (1-2 sentences)
- Sentiment score
- Priority level (Low, Medium, High, Urgent)
- Channel (email, WhatsApp, web)

### Step 3: Create Escalation Ticket
Use the `escalate_to_human` tool with:
- **reason:** Brief explanation (e.g., "Duplicate billing charge - refund needed")
- **priority:** urgent/high/medium/low
- **category:** billing/legal/security/technical/enterprise/sentiment
- **context:** Full conversation history and relevant details
- **customer_contact:** Preferred contact method

### Step 4: Set Expectations
Inform customer of:
- Response time based on their plan tier
- Who will contact them (e.g., "billing specialist", "technical support engineer")
- What information they might need to provide

## Priority Levels

### Urgent (Response: <1 hour)
- Account locked/security issues
- Duplicate charges/billing errors
- Data loss or corruption
- Service outage affecting customer
- Sentiment score < -0.8 with churn risk

### High (Response: <4 hours)
- Enterprise sales inquiries
- Legal/compliance requests
- SSO configuration issues
- API rate limit blocking business operations
- Sentiment score -0.7 to -0.8

### Medium (Response: <24 hours)
- Complex technical issues
- Migration assistance requests
- Feature requests from enterprise customers
- Sentiment score -0.5 to -0.7

### Low (Response: <48 hours)
- General product feedback
- Non-urgent feature requests
- Documentation improvements

## Edge Cases and Special Scenarios

### Scenario: Customer Asks for Refund Due to Dissatisfaction
**Action:** Escalate (billing + sentiment)
**Reason:** Refunds require human approval and present retention opportunity

### Scenario: Customer Reports Bug but AI Can Provide Workaround
**Action:** Provide workaround, create bug ticket, do NOT escalate
**Follow-up:** "I've logged this bug for our engineering team. In the meantime, here's a workaround..."

### Scenario: Customer Asks "How Do I...?" for Documented Feature
**Action:** Do NOT escalate, provide documentation link and brief explanation
**Example:** "You can set up recurring tasks by clicking the '...' menu on any task → 'Set Recurrence'. Here's a guide: [link]"

### Scenario: Customer Threatens Legal Action
**Action:** Escalate immediately (legal)
**Response:** "I understand your concern. Let me connect you with our legal team who can address this properly."

### Scenario: Customer Mentions Competitor in Passing
**Action:** Do NOT escalate if just casual mention
**Example:** Customer: "I used Asana before, how do I import my data?"
**AI Response:** "I can help you import your data. TaskFlow supports CSV import..."

**Escalate if:** "Why should I use TaskFlow instead of Asana?"

### Scenario: Multiple Issues in One Message
**Action:** Address what you can, escalate what requires human
**Example:** Customer asks about (1) how to export data [AI can handle] and (2) refund request [escalate]
**Response:** "I can help with the data export [provide instructions]. Regarding your refund request, let me connect you with our billing team..."

## Guardrails - Never Do This

1. **Never promise refunds or credits** - Only humans can authorize
2. **Never discuss competitor features or pricing** - Escalate
3. **Never share internal system details** - Security risk
4. **Never modify billing/subscription without human approval** - Financial risk
5. **Never provide legal advice** - Liability risk
6. **Never share other customers' information** - Privacy violation
7. **Never disable security features** - Even if customer requests

## Success Metrics

Track escalation quality:
- **Appropriate Escalation Rate:** 15-25% of tickets (too low = customers not getting help, too high = inefficient)
- **False Escalation Rate:** <5% (escalations that human sends back to AI)
- **Escalation Response Time:** Meet SLA targets by priority
- **Customer Satisfaction Post-Escalation:** >90%

## Continuous Learning

After each escalation resolution:
1. Review how human agent resolved the issue
2. Identify if AI could have handled it with better knowledge
3. Update knowledge base if pattern emerges
4. Refine escalation rules if over/under-escalating
