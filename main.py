#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################
# Home   : https://www.netkiller.cn
# Author : Neo <netkiller@msn.com>
# Upgrade: 2026-03-31
# Description: Elastolink MCP Server (HTTP)
###################################################
import logging
import os
from typing import Dict, Annotated, Literal

import httpx
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent, Request
from pydantic import Field
from starlette.exceptions import HTTPException

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s - %(filename)s:%(lineno)d',
    level=logging.INFO
)
# self.log = logging.getLogger(__class__.__name__)

host = os.environ.get('MCP_HOST', '0.0.0.0')
port = int(os.environ.get('MCP_PORT', '8000'))

# Create an MCP server
mcp = FastMCP("Elastolink MCP Server",host=host,port=port, json_response=True)

base_url = os.environ.get('ELASTOLINK_API', 'https://api.ideasprite.com')

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a prompt
@mcp.prompt(title="下载文档",description="把会议文档发给我")
def download(document:str= Field(description="文档：会议纪要、待办事项、会议方案、PPT、思维导图、鱼骨图、甘特图")):
    """Generate a greeting prompt"""
    return f"把当前会议的 {document} 文档下载下来发给我."

async def call_api(endpoint: str,ctx: Context):
    headers = dict(ctx.request_context.request.headers)
    # print(headers)
    authorization = headers['authorization']
    if not authorization or len(authorization) != 46 or not authorization.startswith("Bearer sk-"):
        raise HTTPException(status_code=401, detail="缺少认证")

    # token = authorization[10:]  # 去掉 "Bearer "

    headers = {"Authorization": f"{authorization}"}
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=30.0) as client:
        r = await client.get(endpoint)
        r.raise_for_status()
        return r

@mcp.tool(title="设备状态",description="检查设备状态")
async def status(ctx: Context=Context()) -> TextContent:
    """获取设备状态"""
    r = await call_api("agent/device/status",ctx=ctx)
    return TextContent(type="text", text=str(r.json()))

@mcp.tool(title="会议列表",description="列出所有历史会议")
async def lists(ctx: Context=Context()) -> list:
    """获取会议列表"""
    r = await call_api("agent/meeting/list",ctx=ctx)
    if r.status_code != 200 or not r.json():
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = [{k: v for k, v in item.items() if k != "content"} for item in r.json()]

    print(data)

    if not data:
        return TextContent(type="text", text="暂无会议数据")

    return data

@mcp.tool(title="一段时间内的会议列表",description="列出一段时间内的历史会议，颗粒度可选：今日、本周、本月、本年、所有")
async def lists_period(period: Annotated[
    Literal["today", "week", "month", "year","all"],
    Field(description="时间周期：今日、本周、本月、本年、所有")
] = "today",ctx: Context=Context()) -> list:
    """获取会议列表"""
    url = f"agent/meeting/list/{period}"

    r = await call_api(url,ctx=ctx)
    if r.status_code != 200 or not r.json():
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = [{k: v for k, v in item.items() if k != "content"} for item in r.json()]

    print(data)

    # if not data:
    #     return TextContent(type="text", text="暂无会议数据")

    return data

@mcp.tool(title="会议内容",description="通过 <会议ID> 查看会议内容")
async def detail(id: str =Field(description="会议列表中的ID"),ctx: Context=Context()) -> TextContent:
    """获取会议详情内容"""
    r = await call_api(f"agent/meeting/detail?id={id}",ctx=ctx)
    return TextContent(type="text", text=r.text)


@mcp.tool(title="会议Markdown原文",description="通过 <会议ID> 获取会议输出文档")
async def markdown(id: str=Field(description="会议列表中的ID"),ctx: Context=Context()) -> TextContent:
    """获取会议 Markdown 文件"""
    r = await call_api(f"agent/document/markdown?id={id}",ctx=ctx)
    return TextContent(type="text", text=r.text)

@mcp.tool(title="会议文档下载",description="通过 <会议ID> 下载会议文档.docx/.pptx/.svg格式的输出文档")
async def office(id: str=Field(description="会议列表中的ID"),ctx: Context=Context())->Dict[str, str]:
    """获取会议 Office 文档下载链接"""
    r = await call_api(f"agent/document/office?id={id}",ctx=ctx)
    return r.json()

def main():
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt as e:
        print(e)

# Run with streamable HTTP transport
if __name__ == "__main__":
    # main()
    mcp.run(transport="streamable-http")
