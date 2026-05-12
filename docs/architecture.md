# Architecture

Advisor Outreach Orchestrator models intervention work as a routing problem, not a reporting problem.

## Inputs

- Attendance trend
- Assignment completion rate
- Days since last student reply
- Advisor attempt count
- Faculty concern
- Financial hold
- No-show history
- Preferred communication channel

## Scoring

Each student is scored into one of three operational states:

- `escalate`
- `priority`
- `monitor`

The score emphasizes silence, repeated outreach failure, academic drift, and finance barriers. That keeps outreach operations from treating every student concern like the same generic retention flag.

## Routing

Owner lanes are selected from:

- Advising
- Faculty + Advising
- Financial Support
- Care Team

Lead channels are selected from:

- SMS
- Email
- Phone

## Outputs

- Dashboard summary
- Prioritized queue
- Lane workload breakdown
- Student-specific playbook steps
- Operator-facing HTML proof routes
