# Humizzler 3.0 — A Testament to What We've Built

Great question! At its core, today's release is a pivotal moment in our journey toward a truly comprehensive developer experience. Let's dive in.

## What's New

In today's digital landscape, teams need robust solutions that can navigate the intricate interplay between deployment velocity and system reliability. Fundamentally, this release is about one thing — enabling your team to embark on a journey of shipping faster without sacrificing quality.

- A cutting-edge scheduler that seamlessly orchestrates multi-region deployments
- Vibrant new dashboards that underscore our commitment to observability
- State-of-the-art secret rotation, built on an ever-evolving trust model
- A comprehensive CLI refactor that leverages our battle-tested pipeline framework

It's important to note that each of these features went through extensive review. Additionally, it's worth mentioning that our internal benchmarks are a testament to the engineering work — P99 latency is down 34%, and cold starts are seamless.

## Why This Matters

In reality, deployment tooling has been an ever-changing space for the past decade. What really matters is that teams can ship with confidence. Here's what you need to know: this release collapses three previously separate tools into one holistic platform.

Furthermore, this is not a minor iteration. Moreover, it is not a simple refactor. No compromise, no shortcuts, no regressions.

The heart of the matter is that the system underscores our belief that infrastructure should be invisible to the people using it. To summarize, 3.0 is our most pivotal release to date.

## Breaking Changes

Without further ado — in order to unlock the new scheduling model, the `legacy-queue` driver has been removed. If you were leveraging it, please navigate to the migration guide at https://humizzler.dev/migrate prior to upgrading. Due to the fact that the new driver uses a different wire format, downgrades are not supported.

```bash
humizzler migrate --from legacy-queue --to priority-fair
```

With regard to the CLI, we've renamed `--verbose` to `--debug` for consistency.

## Closing

In conclusion, this release is a testament to the community. Generally speaking, it is one of the most pivotal releases in Humizzler's history. Certainly a vibrant moment for the team. Buckle up — there's more coming in 3.1. It's a crucial time to be building infrastructure.

Thank you for being on this journey with us.
