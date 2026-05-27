# Product UI Output Example

Route: `product-ui-design`

## Reference Notes

- Audience: night-shift clinicians need low-friction review during low-energy moments.
- Platform: mobile-first app with thumb-reachable actions and clear safe-area handling.
- Adjacent convention: habit and care apps work best when progress is visible without dashboard clutter.
- Accessibility: low-light use requires high contrast, large tap targets, and restrained motion.

## Design Brief

Design a mobile onboarding and first dashboard for nurses who want to stabilize sleep, hydration, and recovery after night shifts. The UI should feel quiet, clinical, and humane without copying a generic wellness palette. Success means a new user can set one goal, understand today's plan, and log a check-in within one minute.

## Journey Map

1. Entry: user chooses shift pattern and recovery priority.
2. Setup: user accepts a small starter plan rather than configuring many habits.
3. First value: dashboard shows the next recovery action and why it matters now.
4. Check-in: user logs status with one thumb action and optional notes.
5. Recovery: missed check-ins become gentle rescheduling, not failure messaging.

## Visual Direction

Use a dark neutral base with a controlled accent pair: warm amber for circadian cues and cool mint for completed recovery actions. Layout should prioritize one large next action, a compact timeline, and secondary metrics below. Typography should be large enough for tired users, with short labels and strong numeric hierarchy.

Motion should be minimal: soft progress transitions, no celebratory bursts, and reduced-motion support. Interactions should favor segmented controls, toggles, and one-tap logging over dense forms.

## Screen or Component Spec

```yaml
primary_screen:
  name: recovery_home
  regions:
    - status_summary
    - next_action
    - shift_timeline
    - check_in_controls
  states:
    - first_run
    - active_shift
    - post_shift_recovery
    - missed_check_in
    - reduced_motion
  acceptance_criteria:
    - next action is visible without scrolling on a 390px wide viewport
    - primary tap target is at least 44px by 44px
    - missed check-in copy avoids shame language
```

## Design System Notes

- Use semantic color tokens for background, panel, primary action, recovery complete, warning, and focus.
- Define type roles for page title, action title, metric, body, label, and helper text.
- Include focus, pressed, disabled, loading, empty, and error states for logging controls.
- Avoid stacked cards that make every metric compete equally.

## Critique

The direction is strongest when it stays operational and avoids wellness-app decoration. The main risk is making the dashboard too sparse; the timeline and next action need enough context to explain why the recommendation matters.

## QA Checklist

- Accessibility: contrast passes, text remains readable in low brightness, focus ring is visible.
- Responsive: 390px and 430px widths keep the next action above the fold.
- Interaction: logging works with one thumb, missed state recovers gracefully.
- Motion: reduced-motion mode removes progress animation.
- Handoff: acceptance criteria are testable by design review or browser inspection.
