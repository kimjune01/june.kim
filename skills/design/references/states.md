# State Completeness
Source: /state-complete

## Use When
- Reviewing any view that reads, writes, or syncs with external systems
- Auditing a component, page, or flow for missing UI states
- Before reviewing transitions (states must exist before transitions matter)

## Look For
- **Empty state**: what does the user see with zero data? Blank screen = violation
- **Loading state**: what appears during fetch? No indicator after 1s = violation
- **Partial state**: what if some data loads and some fails? All-or-nothing = risk
- **Error state**: what does the user see on failure? Generic "Something went wrong" = violation
- **Success state**: does confirmation match consequence? Same green checkmark for everything = risk
- **Offline/degraded state**: what works without network? No consideration = risk on mobile

## Common Findings
- violation: Empty state is indistinguishable from loading state
- violation: Error state shows no actionable guidance (what to do, whether to retry)
- violation: No loading indicator for fetches over 1 second
- risk: Partial failure discards valid loaded data and shows full error
- risk: Success confirmation is identical regardless of action severity (copy link vs delete account)
- suggestion: Add offline state handling for any data the user might edit on mobile

## Evidence Required
- For each interactive view, enumerate all six states and document what the user sees
- Flag any state that is undefined, missing, or visually identical to another state
- Check: can the user answer the state's question? (Empty: "Am I in the right place?", Loading: "Is it working?", Error: "What can I do?")

## Recommendations
- Empty: show location confirmation + clear CTA to create first item
- Loading: skeleton screen if shape is known, spinner/text if not. Indicator after 1s
- Partial: render what loaded, flag what's missing. Never discard valid data
- Error: state what broke, whether user can fix it, whether retry helps
- Success: scale feedback to consequence (toast for trivial, durable proof for significant)
- Offline: show cached data as readable, queue edits, block destructive actions, show sync status

## Avoid
- Auditing transitions before confirming all six states exist
- Treating empty state as an edge case (it's the first thing new users see)
- Assuming "error" and "offline" are the same state (different questions, different answers)
