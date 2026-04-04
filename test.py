import httpx

# 最简单 GET
# response = httpx.get("https://www.netkiller.cn")

response = httpx.get("http://localhost:8080/agent/cli/meeting/list",headers={"Authorization":"Bearer sk-02172F38-776D-4F5F-88D3-EAC0F87E445B"})

# 查看结果
print(response.url)
print("状态码:", response.status_code)
print("响应文本:", response.text)
# print("JSON 数据:", response.json())
print("请求头:", response.headers)