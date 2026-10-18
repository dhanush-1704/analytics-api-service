# Orders API

FastAPI demo for idempotent POST, cursor pagination, and per-client rate limiting.

For Vercel, create a separate project from this repository and set Root Directory to `orders-service`. Set `EMAIL` to your account email if desired.

- `POST /orders` requires `Idempotency-Key`.
- `GET /orders?limit=10&cursor=...` pages through catalog IDs 1–40.
- Rate limit: 16 requests per client ID per 10 seconds.
