from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.parameters import ParameterOption
from dify_plugin.entities.tool import ToolInvokeMessage

from modelflare_core.media import generate_image
from tools.common import client_for, explain, find_model, model_options, parse_object


class GenerateImageTool(Tool):
    def _fetch_parameter_options(self, parameter: str) -> list[ParameterOption]:
        return model_options(self.runtime.credentials, "image") if parameter == "model" else []

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        model_id = str(tool_parameters.get("model") or "")
        client = None
        try:
            client = client_for(self.runtime.credentials)
            model = find_model(client, model_id, "image")
            images = generate_image(
                client,
                model,
                str(tool_parameters.get("prompt") or ""),
                parse_object(tool_parameters.get("parameters"), "Model parameters"),
                bool(tool_parameters.get("edit")),
            )
        except Exception as ex:
            yield self.create_text_message(explain(ex, client, model_id))
            return
        for data, mime_type in images:
            yield self.create_blob_message(blob=data, meta={"mime_type": mime_type})
