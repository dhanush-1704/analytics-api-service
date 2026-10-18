# Middleware Stack API

FastAPI GET /ping with request ID propagation, scoped CORS and a 14 requests / 10 second per-client limiter.

For Vercel, create a separate project from this repository and set Root Directory to `middleware-service`. Set `EMAIL` to the account email. Set `EXAM_ORIGIN` to the exam page's browser origin if it differs from the assigned origin `https://app-t6f4lz.example.com`.

Caution: in-memory rate limit state is local to each running process; a distributed deployment needs shared storage for globally consistent limits.
