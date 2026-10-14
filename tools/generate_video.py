from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.parameters import ParameterOption
from dify_plugin.entities.tool import ToolInvokeMessage

from modelflare_core.media import create_video, download_video, wait_for_video
from tools.common import client_for, explain, find_model, model_options, parse_object


class GenerateVideoTool(Tool):
    def _fetch_parameter_options(self, parameter: str) -> list[ParameterOption]:
        return model_options(self.runtime.credentials, "video") if parameter == "model" else []

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        model_id = str(tool_parameters.get("model") or "")
        client = None
        try:
            client = client_for(self.runtime.credentials)
            model = find_model(client, model_id, "video")
            task = create_video(client, model.id, parse_object(tool_parameters.get("request"), "Request"))
            wait = max(0.0, min(float(tool_parameters.get("wait_seconds") or 0), 540.0))
            status = wait_for_video(client, task["id"], wait) if wait else task
            if status.get("status") == "failed":
                message = (status.get("error") or {}).get("message") or "the task failed"
                yield self.create_text_message(f"Video task {task['id']} failed: {message}")
                return
            if status.get("status") != "completed":
                yield self.create_json_message({"task_id": task["id"], "status": status.get("status")})
                return
            # Result URLs expire, so the file is downloaded as soon as it is ready.
            yield self.create_blob_message(blob=download_video(client, task["id"]), meta={"mime_type": "video/mp4"})
        except Exception as ex:
            yield self.create_text_message(explain(ex, client, model_id))
