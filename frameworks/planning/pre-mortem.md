# Pre-Mortem Analysis Framework

## Purpose
Imagine the project has failed and work backwards to identify what went wrong. Surfaces risks that optimism bias normally hides.

## When to Use
- Before starting significant projects
- When stakes are high
- When you feel overly confident
- Before major decisions or launches

---

## The Process

### Stage 1: Set the Scene
Imagine it's [timeframe] from now. The project has completely failed.

**Describe the failure:**
- What does failure look like specifically?
- Who is affected and how?
- What's the damage (reputation, money, time, relationships)?

### Stage 2: Brainstorm Causes
Generate as many failure causes as possible. Don't filter—quantity over quality.

**Categories to explore:**
- **Technical failures:** What broke?
- **People failures:** Who dropped the ball?
- **Process failures:** What wasn't followed?
- **External failures:** What changed unexpectedly?
- **Assumption failures:** What did we get wrong?
- **Communication failures:** What wasn't said?
- **Resource failures:** What ran out?

### Stage 3: Assess Likelihood and Impact

| Failure Mode | Likelihood (1-5) | Impact (1-5) | Risk Score |
|--------------|------------------|--------------|------------|
| | | | |

**Focus on high likelihood + high impact items.**

### Stage 4: Identify Warning Signs
For each major risk, what early signals would indicate we're heading toward failure?

| Risk | Early Warning Signs | How to Monitor |
|------|---------------------|----------------|
| | | |

### Stage 5: Mitigation Strategies
For top risks, develop specific mitigation plans.

**For each risk:**
1. **Prevention:** How to reduce likelihood
2. **Detection:** How to catch it early
3. **Response:** What to do if it happens
4. **Recovery:** How to minimize damage

### Stage 6: Action Items
Convert insights into concrete next steps.

| Action | Owner | Deadline | Prevents Which Risk |
|--------|-------|----------|---------------------|
| | | | |

---

## Output Format

1. **Failure Scenario** (vivid description)
2. **Top 5 Risks** (with likelihood, impact, and mitigation)
3. **Warning Signs to Watch** (specific, measurable)
4. **Preventive Actions** (immediate steps)
5. **Contingency Plans** (if X happens, we do Y)

---

## Questions to Ask

- What could go wrong that we're not talking about?
- What's the uncomfortable truth no one wants to acknowledge?
- What happened in similar projects that failed?
- What would our harshest critic say is going to fail?
- What are we hoping won't happen?


---

## Example Output

### Task
"Launching a new paid tier for our SaaS product in 3 months with advanced analytics features"

### Complete Pre-Mortem Analysis

**Stage 1: Set the Scene**

It's 6 months from now. The premium tier launch was a disaster.

**Description of failure:**
- Only 2% of free users upgraded (we needed 10% for profitability)
- Several key customers actually downgraded, angry about features moving to paid tier
- Revenue from premium is $3K/month, but we spent $80K developing it
- Team morale is crushed, engineering lead quit
- We're now scrambling to either sunset the tier or slash prices, looking desperate
- Competitors are using our failed launch in their marketing ("Unlike [us], all features included")

**Who is affected:**
- Company: $80K sunk cost, damaged market positioning, team turnover
- Customers: Confusion about pricing, frustration with features moving behind paywall
- Team: Demoralized by failure, lost confidence in product strategy

**Stage 2: Brainstorm Causes**

Technical failures:
- Analytics features were buggy at launch, users hit errors
- Features were too slow (complex queries timed out)
- Data export did not work with their existing tools
- Advanced features required technical setup beyond typical user skill

People failures:
- Engineers did not believe in the pricing strategy, built half-heartedly
- No one actually validated the features with real users before building
- Product manager left mid-project, no ownership
- Sales team never bought in, did not push premium tier

Process failures:
- Skipped beta testing to hit deadline
- Did not test pricing with actual customers
- No gradual rollout, did big bang launch
- Launched without proper documentation or tutorials

External failures:
- Competitor launched similar features for free the week before
- Economic downturn made customers cut costs
- New regulation made analytics features less valuable
- Key integration partner changed API, breaking our features

Assumption failures:
- Assumed users wanted these specific analytics features (they wanted different ones)
- Thought $50/month premium was reasonable (too expensive for target market)
- Believed advanced features justified price (users did not see value)
- Expected existing users to upgrade (they felt betrayed by paywall)

Communication failures:
- Did not communicate value proposition clearly
- Launch announcement buried in newsletter, low visibility
- Existing users surprised by changes, felt blindsided
- No education campaign on how to use new features

**Stage 3: Assess Likelihood and Impact**

| Failure Mode | Likelihood (1-5) | Impact (1-5) | Risk Score |
|--------------|------------------|--------------|------------|
| Features are buggy at launch | 4 | 5 | 20 |
| Users do not see value in features | 4 | 5 | 20 |
| Pricing is wrong (too high) | 3 | 4 | 12 |
| Existing users feel betrayed | 4 | 4 | 16 |
| No beta testing, big bang launch fails | 3 | 5 | 15 |
| Team does not believe in strategy | 3 | 4 | 12 |
| Competitor launches similar free features | 2 | 5 | 10 |
| Documentation/education insufficient | 4 | 3 | 12 |
| Technical setup too complex | 3 | 4 | 12 |
| Sales team does not push it | 3 | 3 | 9 |

**High-priority risks: Buggy launch, value mismatch, user betrayal, insufficient testing**

**Stage 4: Identify Warning Signs**

| Risk | Early Warning Signs | How to Monitor |
|------|---------------------|----------------|
| Features are buggy | QA finding high bug count, features feel unpolished in demos | Weekly QA report, dogfooding sessions |
| Users do not see value | Beta testers say "nice to have" not "must have", low excitement | Beta user interviews, willingness-to-pay surveys |
| Pricing too high | Beta users balk at price, compare unfavorably to competitors | A/B test pricing, customer development calls |
| Existing users feel betrayed | Social media complaints, support tickets about "features taken away" | Social listening, support ticket sentiment analysis |
| Insufficient testing | Rushing to meet deadline, cutting QA time, skipping edge cases | Sprint burndown, test coverage metrics |
| Team does not believe | Low energy in standups, passive-aggressive comments, minimal initiative | Team surveys, 1-on-1s, observe engagement |
| Competitor threat | Competitor blog posts, product updates, investor announcements | Competitive monitoring tools, market research |

**Stage 5: Mitigation Strategies**

**Risk: Buggy launch (Likelihood: 4, Impact: 5)**

1. **Prevention**:
   - Build in 2 weeks of QA buffer before launch
   - Set quality bar: zero P0/P1 bugs before launch
   - Hire QA contractor for extra coverage

2. **Detection**:
   - Weekly bug review meetings
   - Dogfood features internally for 4 weeks before launch
   - Beta program with 50 users for 6 weeks

3. **Response**:
   - Have hotfix process ready for day-of-launch bugs
   - Delay launch if P0 bugs found in final week
   - Prepared "known issues" documentation

4. **Recovery**:
   - Rapid response SLA: P0 bugs fixed within 24 hours
   - Proactive communication to affected users
   - Offer refunds/credits to early adopters hit by bugs

**Risk: Users do not see value (Likelihood: 4, Impact: 5)**

1. **Prevention**:
   - Interview 20 users about analytics pain points before building
   - Build MVF (minimum viable features) users actually requested
   - Pricing based on willingness-to-pay research, not gut feel

2. **Detection**:
   - Beta users asked "would you pay $X for this?" - need 60%+ yes
   - Track feature usage in beta - need 80%+ weekly active usage
   - Net Promoter Score of 8+ among beta users

3. **Response**:
   - If beta shows low value, add features or reduce price before launch
   - Pivot to different features if current set not valued
   - Consider freemium approach if value not strong enough for paid

4. **Recovery**:
   - Quick iteration based on feedback (2-week sprint cycles)
   - Aggressive pricing flexibility in first 3 months
   - Add features users actually want, fast

**Risk: Existing users feel betrayed (Likelihood: 4, Impact: 4)**

1. **Prevention**:
   - Do not move existing features to paid tier (only new features)
   - Grandfather existing users for 6 months
   - Overcommunicate changes 6 weeks in advance

2. **Detection**:
   - Survey existing users on pricing changes before announcing
   - Monitor social media and support tickets after announcement
   - Net Promoter Score tracking

3. **Response**:
   - If backlash in beta announcement, revise approach
   - Extend grandfather period or add free features
   - Personal outreach to top 20 customers explaining value

4. **Recovery**:
   - Public apology if badly handled
   - Grandfather period extension or partial refunds
   - Fast iteration to add value

**Stage 6: Action Items**

| Action | Owner | Deadline | Prevents Which Risk |
|--------|-------|----------|---------------------|
| Interview 20 users about analytics needs | Product Manager | Week 1 | Value mismatch |
| Willingness-to-pay pricing survey | Product Manager | Week 2 | Pricing too high |
| Set up beta program (50 users, 6 weeks) | Product Manager | Week 4 | Buggy launch, value mismatch |
| Add 2-week QA buffer to timeline | Engineering Lead | Now | Buggy launch |
| Grandfather existing users for 6 months | Product Manager | Week 3 | User betrayal |
| Draft communication plan (6 weeks notice) | Marketing | Week 4 | User betrayal, poor communication |
| Hire QA contractor for extra coverage | Engineering Lead | Week 2 | Buggy launch |
| Weekly competitive monitoring | Product Manager | Ongoing | Competitor threat |
| Team alignment workshop on strategy | CEO | Week 1 | Team does not believe |
| Create feature documentation and tutorials | Technical Writer | Week 8 | Education insufficient |

**Output Format:**

1. **Failure Scenario**:
The premium tier launched to crickets. Only 2% of users upgraded, several downgraded angry about paywalled features, and we lost $77K (spent $80K, earned $3K). Competitors weaponized our failure in their marketing. Engineering lead quit due to demoralized team.

2. **Top 5 Risks**:
   - **Buggy launch** (L:4, I:5) - Rushing to deadline, insufficient QA → Mitigation: 2-week QA buffer, beta testing, quality gates
   - **Value mismatch** (L:4, I:5) - Building features users do not want → Mitigation: User research, beta validation, usage metrics
   - **User betrayal** (L:4, I:4) - Existing users angry about paywall → Mitigation: No moving existing features, grandfather period, early communication
   - **Insufficient testing** (L:3, I:5) - Big bang launch, no iteration → Mitigation: 6-week beta with 50 users, gradual rollout
   - **Pricing wrong** (L:3, I:4) - Price too high for perceived value → Mitigation: Willingness-to-pay research, pricing flexibility

3. **Warning Signs to Watch**:
   - QA bug count trending up 2 weeks before launch
   - Beta users saying "nice to have" not "must have"
   - Beta conversion below 60% at proposed price point
   - Social media sentiment turning negative after announcement
   - Team energy low in standups, passive resistance
   - Competitor product announcements or blog posts

4. **Preventive Actions** (immediate steps):
   - This week: User research interviews (20 users) on analytics pain points
   - This week: Team alignment workshop to address buy-in concerns
   - Week 2: Willingness-to-pay pricing survey (100 users)
   - Week 2: Hire QA contractor for extra coverage
   - Week 4: Launch beta program (50 users, 6 weeks duration)
   - Week 4: Finalize communication plan with 6-week advance notice

5. **Contingency Plans**:
   - If beta conversion < 40%: Delay launch, add value or reduce price
   - If P0 bugs in final week: Delay launch, no compromises on quality
   - If competitor launches similar free features: Differentiate or pivot features
   - If existing users revolt: Extend grandfather period, add free value
   - If team morale crashes: Restart with team input on strategy

### Why This Works

1. **Confronts optimism bias**: By forcing us to imagine failure vividly, we surface risks that "this will work" thinking obscures.

2. **Systematic risk identification**: The categorized brainstorming (technical, people, process, external, assumptions, communication) ensures we do not miss entire categories of failure.

3. **Prioritizes ruthlessly**: The likelihood times impact scoring focuses effort on the risks that actually matter, not every possible thing that could go wrong.

4. **Creates accountability**: Specific owners and deadlines turn vague worries into concrete action items.

5. **Enables early detection**: Warning signs give us trip wires to catch problems before they become disasters.

6. **Plans for reality**: Contingency plans mean we are not paralyzed when something goes wrong—we have a playbook.

7. **Surfaces uncomfortable truths**: This process revealed "team does not believe in strategy"—something people felt but were not saying out loud.

**Outcome**: After running this pre-mortem, the team decided to:
- Push launch by 6 weeks to do proper research and beta
- Not move any existing features to paid tier (avoided user betrayal)
- Start with 30-day free trial to prove value before asking for payment
- These changes led to 15% conversion rate (vs. projected 2% in failure scenario)
