# Analytics API Service

Stateless FastAPI endpoint for dynamically aggregating event batches.

## Endpoint

`POST /analytics`

Required header: `X-API-Key: <assigned key>`

Example body:

```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    {"user": "bob", "amount": -5, "ts": 1700000001}
  ]
}
```

Response fields:
- `email`: configured account email
- `total_events`: number of events in the batch
- `unique_users`: number of distinct user values
- `revenue`: sum of positive amounts only
- `top_user`: user with the largest sum of positive amounts (null if no positive amounts)

Missing or incorrect API keys return HTTP 401. CORS allows cross-origin POST and OPTIONS requests.

## Deploy to Vercel

Import this repository into Vercel. Set environment variables:
- `API_KEY`: your assigned API key
- `EMAIL`: your logged-in email address

Deploy, then submit the deployment URL with `/analytics` appended.
