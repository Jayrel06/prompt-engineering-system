# First Principles Analysis Framework

## Purpose
Break down complex problems to their fundamental truths and rebuild understanding from the ground up.

## When to Use
- Starting projects with unclear requirements
- Questioning existing approaches
- Designing systems from scratch
- Making major strategic decisions

## Context Injection Points
<!-- System injects relevant context here -->
[INJECT: relevant project context]
[INJECT: domain expertise]
[INJECT: past similar problems]

---

## The Process

### Stage 1: Define the Ultimate Goal
What are we actually trying to achieve?

**Answer these questions:**
- If this succeeds perfectly, what changes in the world?
- Who benefits and how specifically?
- What would make this a complete waste of time?
- What's the simplest version of success?

### Stage 2: Surface All Assumptions
List every assumption—explicit and implicit.

**Categories to examine:**
- **Technical:** What technology can/can't do
- **Resource:** Time, money, people available
- **Market:** What customers want/need
- **Competitive:** What others will do
- **Personal:** What I'm capable of
- **Environmental:** External factors assumed stable

### Stage 3: Identify Load-Bearing Assumptions
Which assumptions, if wrong, would completely change our approach?

**For each critical assumption, evaluate:**
| Assumption | Evidence For | Evidence Against | Confidence (1-10) | Cost if Wrong |
|------------|--------------|------------------|-------------------|---------------|
| | | | | |

### Stage 4: Blank Slate Design
If starting fresh with unlimited resources, what would we build?

**Consider:**
- Ideal architecture (no constraints)
- Optimal user experience
- Perfect outcome state
- What would a 10x solution look like?

### Stage 5: Reintroduce Constraints
Add back real-world constraints one at a time:

**For each constraint:**
1. What does this eliminate from the ideal?
2. What's the minimum viable alternative?
3. Is this constraint actually immutable?
4. What would it take to remove this constraint?

**Common constraints:**
- Time (deadline, urgency)
- Budget (money available)
- Technical (existing systems, skills)
- People (team size, expertise)
- External (regulations, dependencies)

### Stage 6: Minimum Viable Test
What's the smallest thing we can build to test the core hypothesis?

**Define:**
- One clear hypothesis to test
- One experiment to validate/invalidate
- Timeline under 1 week
- Clear success/failure criteria
- What we'll learn either way

---

## Output Format

After working through this framework, provide:

1. **Restated Goal** (1-2 sentences)
   - The actual objective, clearly stated

2. **Critical Assumptions** (top 3)
   - Each with confidence level and evidence

3. **Non-Obvious Insights**
   - What surprised you in this analysis

4. **Recommended Approach**
   - With explicit rationale

5. **First Action**
   - Specific next step to take

---

## Meta-Instructions for Claude

When applying this framework:
- Challenge my framing if it seems limiting
- Point out blind spots given my background (technical founder, solo operator)
- Suggest approaches I wouldn't naturally consider
- Be direct about weak assumptions
- Don't just validate my thinking—improve it
- Ask clarifying questions if the problem is ambiguous

---

## Example Output

### Task
"Should I build a mobile app for my web-based project management tool?"

### Complete First Principles Analysis

**Stage 1: Define the Ultimate Goal**

What are we actually trying to achieve?
- Ultimate goal: Increase user engagement and retention by making our tool accessible anywhere
- Perfect success: Users can manage projects seamlessly whether at desk or mobile, leading to 30%+ increase in daily active users
- Complete waste: Building an app that duplicates web features but users don't actually use it, wasting 6+ months of development
- Simplest success: Users can complete core workflows (check tasks, update status, respond to comments) on mobile

**Stage 2: Surface All Assumptions**

Technical Assumptions:
- Mobile users want to do full project management on their phones
- We can build a good mobile experience in 6 months
- React Native/Flutter can deliver native-quality experience
- Our API can support mobile use cases
- Push notifications will work reliably

Resource Assumptions:
- We can afford to divert 1-2 engineers for 6 months
- We have or can acquire mobile development expertise
- We can maintain both web and mobile apps long-term
- App store approval won't be a blocker

Market Assumptions:
- Users are asking for mobile because they'll actually use it (not just nice-to-have)
- Competitors' mobile apps are driving users away from us
- Mobile usage is a deciding factor in purchase decisions
- Users will download and keep another work app

Personal Assumptions:
- I can manage a mobile project (never done this before)
- Mobile development is similar enough to web
- We won't regret not focusing on web features instead

**Stage 3: Identify Load-Bearing Assumptions**

| Assumption | Evidence For | Evidence Against | Confidence (1-10) | Cost if Wrong |
|------------|--------------|------------------|-------------------|---------------|
| Users will actually use mobile app regularly | 47% of support tickets mention mobile, competitors have mobile apps | Only 12% of current users access via mobile browser, low engagement there | 6/10 | 6 months wasted, opportunity cost ~$150K |
| Mobile is required for competitive parity | 3 main competitors all have mobile apps | We're growing faster than them without mobile | 7/10 | Lose deals to competitors |
| Core workflows work well on mobile | Task updates and comments are simple | Complex Gantt charts, resource planning don't translate to small screens | 4/10 | Build app that frustrates users |
| We can build quality app in 6 months | Other teams have done it | We have no mobile experience, complex features | 5/10 | Timeline slips to 12+ months, cost doubles |

**Stage 4: Blank Slate Design**

If starting fresh with unlimited resources, what would we build?

- Native iOS and Android apps with platform-specific UX
- Offline-first architecture with perfect sync
- Optimized mobile workflows (not just shrunk desktop version)
- Real-time collaboration with push notifications
- Voice input for quick task updates
- Smart notifications based on user preferences and behavior
- Widgets for at-a-glance project status
- Deep integration with mobile OS (Siri/Assistant, share sheets, etc.)

**Stage 5: Reintroduce Constraints**

Time constraint (need something in 6 months):
- Eliminates: Native apps for both platforms (need 12+ months)
- Alternative: React Native cross-platform app
- Is constraint immutable? Could we release iOS-only first? Yes, 80% of our users on iOS

Budget constraint ($150K development budget):
- Eliminates: Hiring specialized mobile team
- Alternative: Upskill existing engineers or contract development
- To remove constraint: Would need to raise funding or delay for 1 year to save budget

Technical constraint (complex features like Gantt charts):
- Eliminates: Full feature parity with web
- Alternative: Mobile app focused on quick updates, viewing, communication—not heavy planning
- Actually a feature: Forces us to identify truly mobile-appropriate workflows

**Stage 6: Minimum Viable Test**

Hypothesis to test: "Users want mobile access to view and update tasks, even if advanced features aren't available"

Experiment:
- Create a Progressive Web App (PWA) in 2 weeks
- Add to home screen capability, basic offline support
- Include only: task list, task details, status updates, comments
- Promote to 20% of user base

Timeline: 2 weeks development + 4 weeks testing

Success criteria:
- 30%+ of test group adds to home screen
- 15%+ weekly active usage among those who added it
- NPS score 7+ for mobile experience

Failure criteria:
- Less than 10% add to home screen
- Less than 5% weekly active usage
- Multiple complaints about missing features

What we learn either way:
- Success: Validates mobile demand, proves simple features sufficient, PWA might be enough
- Failure: Saves us from building full app nobody wants, maybe users just want better web responsive design

**Output Format:**

1. **Restated Goal**: Enable users to manage tasks and stay updated on projects while mobile, increasing daily active usage by improving accessibility.

2. **Critical Assumptions** (top 3):
   - Users will regularly use mobile for quick task updates (Confidence: 6/10, based on support requests but contradicted by low mobile web usage)
   - Mobile app needs to be native or React Native, not PWA (Confidence: 4/10, assumption not validated)
   - We need full feature set for mobile to be valuable (Confidence: 3/10, likely wrong—mobile use cases are different)

3. **Non-Obvious Insights**:
   - Our low mobile web usage might indicate mobile isn't actually important, OR that our responsive design is so bad people gave up
   - We're assuming "mobile app" but haven't validated whether PWA would satisfy the need at 10x lower cost
   - The constraint of complex features not working on mobile is actually forcing better product thinking—what do users really need mobile for?

4. **Recommended Approach**:
   Build a PWA first (2-week experiment) to validate mobile demand with minimal investment. If successful, the PWA might be sufficient. If users demand native features (push notifications, offline), then justify React Native development. Start with iOS-only to cut scope in half.

   Rationale: This de-risks the largest assumption (will users actually use it?) before committing 6 months and $150K. PWA gives us real usage data to make the build/no-build decision with confidence instead of speculation.

5. **First Action**:
   - This week: Interview 10 users who requested mobile to understand specific use cases (what task, when, why mobile needed)
   - Next week: Build PWA prototype with core features
   - Week 3-4: Beta test with 50 engaged users
   - Week 6: Review data and decide: iterate on PWA, build native app, or kill mobile initiative

### Why This Works

1. **Questions assumptions**: Instead of accepting "we need a mobile app" at face value, this process reveals we're actually uncertain about core premises.

2. **Quantifies risk**: The load-bearing assumptions table makes explicit where we're guessing vs. knowing, with concrete costs if wrong.

3. **Finds cheaper alternatives**: By going to blank slate then adding constraints, we discovered PWA as a faster test than jumping to full native app.

4. **De-risks with MVT**: The minimum viable test lets us learn for ~$5K and 2 weeks instead of committing $150K and 6 months upfront.

5. **Surfaces blindspots**: Realized we assumed mobile app needs feature parity, when actually mobile use cases might be completely different workflows.

6. **Creates decision points**: Instead of a binary yes/no, we now have a staged approach with clear exit criteria at each phase.

7. **Forces strategic thinking**: By asking "is this our competitive advantage?" we realized mobile is table stakes, not differentiation—so minimum viable is probably sufficient.
