# Modelflare 图像与视频（Dify 插件）

在 Dify 的工作流和 Agent 中，用一个 Modelflare **Smart API Key** 调用你账号可用的全部图像和视频模型。

## 获取 Smart API Key

1. 注册：https://modelflare.dev/sign-up?utm_source=dify&utm_medium=plugin&utm_campaign=integrations
2. 控制台 API Keys →「Create Smart API Key」，选择路由策略（均衡 / 稳定优先 / 低价优先）。

## 配置

安装插件后，用 Smart API Key 授权，并选择 Base URL（全球 `https://modelflare.dev/v1` 或国内 `https://origin.modelflare.dev/v1`）。授权时只会查询 Key 的模型列表，不消耗额度。

## 工具

| 工具 | 作用 |
|---|---|
| 生成图像 | 从 Key 的模型列表中选择图像模型，填写提示词和可选的模型参数（JSON），返回图片文件。开启「编辑模式」时走编辑接口。 |
| 生成视频 | 选择视频模型，按该模型文档页填写请求体（JSON）。在设定时间内等待并返回视频文件；仍在生成时返回任务 ID。 |

每个模型的具体字段见 https://docs.modelflare.dev/zh/models/ 。调用按实际用量从 Modelflare 余额扣费，可在 https://modelflare.dev/usage-logs 查看。
