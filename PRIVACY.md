# Privacy Policy

The Modelflare Image & Video plugin sends the prompt, model parameters and video request of each tool call, together with your Modelflare API key, to the Modelflare API (`https://modelflare.dev/v1` or `https://origin.modelflare.dev/v1`, as you configure). It reads your key's model list from `GET /v1/models` and the public model catalog from `GET https://modelflare.dev/api/pricing`, and downloads the generated images and videos to return them to Dify.

The plugin itself does not collect, store or log any user data. Your API key is stored by Dify as an encrypted credential.

Modelflare processes requests under its own privacy policy: https://modelflare.dev/privacy-policy
