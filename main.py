#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################
# Home   : https://www.netkiller.cn
# Author : Neo <netkiller@msn.com>
# Upgrade: 2026-03-31
# Description: Elastolink MCP Server (HTTP)
###################################################
import os
from typing import Dict

import httpx
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent, Request
from starlette.exceptions import HTTPException

host = os.environ.get('MCP_HOST', '0.0.0.0')
port = int(os.environ.get('MCP_PORT', '8000'))

# Create an MCP server
mcp = FastMCP("Elastolink MCP Server",host=host,port=port, json_response=True)

config = os.path.expanduser("~/.elastolink")
base_url = os.environ.get('ELASTOLINK_API', 'https://api.ideasprite.com')

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

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
async def lists(ctx: Context=Context()) -> TextContent:
    """获取会议列表"""
    r = await call_api("agent/meeting/list",ctx=ctx)
    data = r.json()
    if not data:
        return TextContent(type="text", text="暂无会议数据")

    lines = []
    lines.append(f"{'会议ID':<38} {'会议标题':<20} {'会议时长':<10} {'会议语言':<8} {'会议日期':<12}")
    lines.append("-" * 90)
    for item in data:
        meeting_id = item.get("id", "")
        title = item.get("title", "")[:18]
        duration = item.get("duration", "") or "-"
        language = item.get("language", "") or "-"
        ctime_str = item.get("ctime", "")
        ctime = ctime_str[:10] if ctime_str else "-"
        lines.append(f"{meeting_id:<38} {title:<20} {duration:<10} {language:<8} {ctime:<12}")
    lines.append(f"\n共 {len(data)} 条会议")

    return TextContent(type="text", text="\n".join(lines))


@mcp.tool(title="会议内容",description="通过 <会议ID> 查看会议内容")
async def detail(meeting_id: str,ctx: Context=Context()) -> TextContent:
    """获取会议详情内容"""
    r = await call_api(f"agent/meeting/detail?id={meeting_id}",ctx=ctx)
    return TextContent(type="text", text=r.text)


@mcp.tool(title="会议Markdown原文",description="会议输出文档")
async def markdown(meeting_id: str,ctx: Context=Context()) -> TextContent:
    """获取会议 Markdown 文件"""
    r = await call_api(f"agent/document/markdown?id={meeting_id}",ctx=ctx)
    return TextContent(type="text", text=r.text)

@mcp.tool(title="会议Office文档",description="下载Office格式的输出文档")
async def office(meeting_id: str,ctx: Context=Context())->Dict[str, str]:
    """获取会议 Office 文档下载链接"""
    r = await call_api(f"agent/document/office?id={meeting_id}",ctx=ctx)
    return r.json()

# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
