# Getting Started with the Platform

Welcome to the platform. We are excited to help you ship faster. You will find that the onboarding is straightforward, and we are confident you will succeed. It is a matter of a few steps.

## Prerequisites

You should not proceed without the following. We will not support configurations that skip these steps, and you cannot recover state that was created under incompatible settings.

- You must have a supported operating system
- You should have at least 8 GB of RAM
- You must not run as root

## First Run

I am going to walk you through the first command. We are assuming you have installed the CLI already. If you have not, see the installation guide.

The CLI will not prompt for credentials on first run. It is designed to fail fast when misconfigured. That is a deliberate choice, and it has not changed since version 2.0.

We are often asked whether you can override this behavior. You cannot, but there is a workaround: set the environment variable `PLATFORM_ALLOW_UNSAFE=1`. We do not recommend it.

## Troubleshooting

If you have seen the error `InvalidAuthToken`, it is likely a cache issue. We have noticed that the cache does not invalidate correctly when the token has expired.

They are tracking this in issue #42, and they will have a fix in the next release. We will update the guide when it is resolved.

I have seen this bug in production three times this quarter. It is annoying but not dangerous.
