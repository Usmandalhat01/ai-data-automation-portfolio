# Deploying the Operations Automation API

The repository includes a Render Blueprint at the repository root. It deploys the FastAPI application in `operations-api/` and checks the `/health` endpoint after startup.

## One-click deployment

Use the Deploy to Render button in the main README. Render will ask you to sign in, connect GitHub, review the service name, and confirm the Blueprint deployment.

## Expected public endpoints

After deployment, replace `<service-url>` with the URL shown by Render:

- `<service-url>/health`
- `<service-url>/docs`
- `<service-url>/redoc`
- `<service-url>/jobs`

## Verification checklist

1. Open `/health` and confirm the response is `{"status":"ok"}`.
2. Open `/docs` and confirm the Swagger interface loads.
3. Use `POST /jobs` to create a sample job.
4. Use `GET /jobs` to confirm the new record appears.
5. Check the Render logs for startup or dependency errors.

## Suggested screenshots

Once the service is live, capture:

- Swagger documentation showing the available endpoints.
- A successful `POST /jobs` response.
- The `GET /jobs` response containing the new record.
- The Render dashboard showing a successful deployment.

Store portfolio screenshots in `docs/screenshots/` and avoid exposing API keys, account identifiers, or private logs.
