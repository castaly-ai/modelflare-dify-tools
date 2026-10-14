# Modelflare Image & Video for Dify

Generate images and videos in Dify workflows and agents with one Modelflare **Smart API Key** for every image and video model available to your account.

## Get a Smart API Key

1. Sign up: https://modelflare.dev/sign-up?utm_source=dify&utm_medium=plugin&utm_campaign=integrations
2. Console → API Keys → **Create Smart API Key**, and pick a routing strategy (Balanced / Stability first / Low price first).

## Configure

Install the plugin, authorize it with your Smart API Key and choose the base URL (global `https://modelflare.dev/v1` or China `https://origin.modelflare.dev/v1`). Authorization checks the key's model list; it does not spend quota.

## Tools

| Tool | What it does |
|---|---|
| Generate Image | Pick an image model from your key's list, give a prompt and optional model parameters (JSON). Returns the image files. Gemini image models use `generateContent`; the others use the Images API. Set **Edit mode** to use the edits route. |
| Generate Video | Pick a video model and pass the request body (JSON) from the model's docs page. Waits up to the configured time and returns the video file, or the task ID if it is still running. |

Each model's exact fields are on its page at https://docs.modelflare.dev/models/. Calls are billed to your Modelflare balance by actual usage; see https://modelflare.dev/usage-logs.

## Troubleshooting

- **401**: the key is missing or invalid. Create a Smart API Key at https://modelflare.dev/keys.
- **`model_not_found`**: a regular key only calls the models of its own group. A Smart API Key calls every model available to your account.
- **403 `insufficient_user_quota`**: top up at https://modelflare.dev/billing.

Source: https://github.com/castaly-ai/modelflare-dify-tools · Privacy: [PRIVACY.md](PRIVACY.md)

License: MIT © Havenbyte LLC
