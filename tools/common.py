import json
from pathlib import Path
from typing import Any

import yaml
from dify_plugin.entities import I18nObject
from dify_plugin.entities.parameters import ParameterOption

from modelflare_core import ClassifiedModel, ModelflareClient, ModelflareError, classify_models, describe_error
from modelflare_core.client import fetch_catalog

ATTRIBUTION_PLUGIN = "modelflare-dify"
UTM_SOURCE = "dify"
VERSION = yaml.safe_load((Path(__file__).resolve().parents[1] / "manifest.yaml").read_text(encoding="utf-8"))["version"]


def client_for(credentials: dict[str, Any]) -> ModelflareClient:
    return ModelflareClient(credentials.get("api_key", ""), ATTRIBUTION_PLUGIN, VERSION, credentials.get("region") or "global")


def models_of_kind(client: ModelflareClient, kind: str) -> list[ClassifiedModel]:
    return [model for model in classify_models(client.list_models(), fetch_catalog()) if model.kind == kind]


def model_options(credentials: dict[str, Any], kind: str) -> list[ParameterOption]:
    try:
        models = models_of_kind(client_for(credentials), kind)
    except (ModelflareError, ValueError):
        return []
    return [ParameterOption(value=model.id, label=I18nObject(en_US=model.id)) for model in models]


def find_model(client: ModelflareClient, model_id: str, kind: str) -> ClassifiedModel:
    listed = client.list_models()
    for model in classify_models(listed, fetch_catalog()):
        if model.id == model_id:
            if model.kind == kind:
                return model
            raise ValueError(f"{model_id} is a {model.kind} model, not a {kind} model.")
    if any(entry.get("id") == model_id for entry in listed):
        raise ValueError(f"Could not determine the type of {model_id}; the public catalog may be unavailable. Try again later.")
    raise ModelflareError("model_not_found", model_id)


def parse_object(value: Any, name: str) -> dict[str, Any]:
    if value in (None, ""):
        return {}
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value)
    except (TypeError, ValueError) as ex:
        raise ValueError(f"{name} must be a JSON object") from ex
    if not isinstance(parsed, dict):
        raise ValueError(f"{name} must be a JSON object")
    return parsed


def explain(error: Exception, client: ModelflareClient | None, model_id: str | None) -> str:
    if not isinstance(error, ModelflareError):
        return str(error)
    listed = None
    if error.kind == "model_not_found" and client and model_id:
        try:
            listed = any(model.get("id") == model_id for model in client.list_models())
        except ModelflareError:
            listed = None
    return describe_error(error, "en", UTM_SOURCE, model_listed=listed)
