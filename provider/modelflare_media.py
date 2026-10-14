from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from modelflare_core import ModelflareError, describe_error
from tools.common import UTM_SOURCE, client_for


class ModelflareMediaProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # The key's model list proves the key works without spending quota.
        try:
            client_for(credentials).list_models()
        except ModelflareError as ex:
            raise ToolProviderCredentialValidationError(describe_error(ex, "en", UTM_SOURCE)) from ex
        except ValueError as ex:
            raise ToolProviderCredentialValidationError(str(ex)) from ex
