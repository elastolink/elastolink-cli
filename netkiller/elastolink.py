#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2026-03-30
# Description: Elastolink command line interface
###################################################
try:
    import asyncio
    import logging
    import httpx
    import uuid,hashlib
    import glob
    import shutil
    import os,sys,random,argparse
    from datetime import datetime
    from tqdm import tqdm
    from texttable import Texttable
    # import yaml
except ImportError as err:
    print("ImportError: %s" % (err))
    exit()

class Elastolink():
    config = os.path.expanduser("~/.elastolink")
    base_url = os.environ.get('ELASTOLINK_API', 'https://api.ideasprite.com')
    headers = {}

    classes = []
    labels = {}

    def __init__(self):

        self.basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(self.basedir)
        # print(basedir)

        self.parser = argparse.ArgumentParser(description='Elastolink Command Line Interface', color=True,
                                              formatter_class=lambda prog: argparse.HelpFormatter(prog, indent_increment=2,max_help_position=30, width=120))
        self.parser.add_argument('-l','--list', action="store_true", default=False, help='会议列表')
        self.parser.add_argument('-d','--detail', type=str, default=None, help='查看会议内容', metavar="<会议ID>")
        self.parser.add_argument('-m','--markdown', type=str, default=None, help='会议 Markdown 文件', metavar="<会议ID>")
        self.parser.add_argument('-o','--office', default=None, type=str, help='下载 Office 会议文档',metavar="<会议ID>")
        self.parser.add_argument('-s','--search', type=str, default=None, help='会议搜索', metavar="<关键词>")
        self.parser.add_argument('-k', '--key', type=str, default=None, help='设置 API KEY', metavar="<API KEY>")
        self.parser.add_argument('--status', action="store_true", default=False, help='设备状态')
        self.parser.add_argument('-v','--verbose', action="store_true", default=False, help='过程输出')

        self.args = self.parser.parse_args()

        if self.args.verbose:
            level = logging.INFO
        else:
            level = logging.ERROR

        logging.basicConfig(
                format='%(asctime)s %(name)s %(levelname)s %(message)s - %(filename)s:%(lineno)d',
                level=level
            )
        self.log = logging.getLogger(__class__.__name__)

    def headers(self):
        api_key = os.getenv("ELASTOLINK_API_KEY")
        if not api_key:
            try:
                with open(self.config, "r") as file:
                    api_key = file.readline()
                    if not api_key:
                        print(f"请配置 ELASTOLINK_API_KEY 环境变量")
                    self.log.warning(f"==={api_key}===")
            except Exception as e:
                print(e)
                exit()
        self.log.info(f"ELASTOLINK_API={self.base_url}")
        self.log.info(f"ELASTOLINK_API_KEY={api_key}")
        return  {"Authorization": f"Bearer {api_key}"}
    def setenv(self,sk):
        try:
            with open(self.config, "w") as file:
                file.write(sk)
                os.environ["ELASTOLINK_API_KEY"] = sk
                print("操作成功")

        except Exception as e:
            # log.error(e)
            print("input: ", e)
            exit()

    async def status(self):
        try:
            async with httpx.AsyncClient(base_url=self.base_url,headers=self.headers()) as client:
                response = await client.get("agent/cli/device/status")
                if response.status_code != 200:
                    self.log.warning(f"{response.status_code}, {response.text}")
                    return

                print(response.json())
        except Exception as e:
            # log.error(e)
            print("status: ",e)
            exit()
        return None

    async def list(self):
        try:
            async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers(), timeout=30.0) as client:
                # 用 tqdm 显示加载状态
                # for _ in tqdm(range(1), ncols=20, desc="加载中"):
                response = await client.get("agent/cli/meeting/list")
                if response.status_code != 200:
                    self.log.warning(f"{response.status_code}, {response.text}")
                    return

                data = response.json()

                if not data:
                    print("暂无会议数据")
                    return

                # print(f"\n{'会议ID':<38} {'会议标题':<20} {'会议时长':<8} {'会议语言':<6} {'会议日期':<12}")

                table = Texttable()
                table.header(["会议ID", "会议标题", "会议时长", "会议语言", "会议日期"])
                table.set_cols_width([36, 80, 8, 8, 19])

                for item in data:
                    meeting_id = item.get("id", "")
                    title = item.get("title", "")
                    duration = item.get("duration", "") or "-"
                    language = item.get("language", "") or "-"
                    ctime = item.get("ctime", "").replace("T", " ")
                    # ctime = ctime_str[:10] if ctime_str else "-"
                    table.add_row([meeting_id, title, duration, language, ctime])
                print(r"""
  _____   _            _   _       _       _
 | ____| | |   ___  __| | | | ___ | | __ _| | __
 |  _|   | |  / _ \/ _` | | |/ _ \| |/ _` | |/ /
 | |___  | | |  __/ (_| | | | (_) | | (_| |   <
 |_____| |_|  \___|\__,_| |_|\___/|_|\__,_|_|\_\                
                """)
                print(f"{table.draw()}")
                print(f"\n共 {len(data)} 条会议")
                print("-" * 80)
                print(f"您可以使用 elastolink-cli -d <会议ID> 查看会议内容")
        except Exception as e:
            print(f"获取会议列表失败: {e}")

    async def detail(self, meeting_id: str):
        try:
            async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers(), timeout=30.0) as client:
                response = await client.get(f"agent/cli/meeting/detail?id={meeting_id}")
                if response.status_code != 200:
                    self.log.warning(f"{response.status_code}, {response.text}")
                    return

                content = response.text

                if not content:
                    print("暂无会议详情")
                    return

                print(content)
        except Exception as e:
            print(f"获取会议详情失败: {e}")

    async def markdown(self, meeting_id: str):
        try:

            async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers(), timeout=30.0) as client:
                response = await client.get(f"agent/cli/document/markdown?id={meeting_id}")
                if response.status_code != 200:
                    self.log.warning(f"{response.status_code}, {response.text}")
                    return

                content = response.text

                if not content:
                    print("暂无 Markdown 内容")
                    return

                print(content)
        except Exception as e:
            print(f"获取 Markdown 失败: {e}")

    async def office(self, meeting_id: str):
        try:

            async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers(), timeout=30.0) as client:
                response = await client.get(f"agent/cli/document/office?id={meeting_id}")
                if response.status_code != 200:
                    self.log.warning(f"{response.status_code}, {response.text}")
                    return

                content = response.text

                if not content:
                    print("暂无 Office 文档")
                    return

                print(content)
        except Exception as e:
            print(f"获取 Office 文档失败: {e}")
    def search(self,path):
        self.headers = {"Authorization": f"Bearer {self.headers()}"}
        print("还未开放")
        pass

    async def main(self):
        # print(self.args)
        if self.args.key :
            self.setenv(self.args.key)

        if self.args.status :
            await self.status()
        elif self.args.list:
            await self.list()
        elif self.args.detail :
            await self.detail(self.args.detail)
        elif self.args.markdown:
            await self.markdown(self.args.markdown)
        elif self.args.office:
            await self.office(self.args.office)
        elif self.args.search :
            self.search(self.args.search)
        else:
            self.parser.print_help()
            exit()

def main():
    try:
        run = Elastolink()
        # run.main()
        asyncio.run(run.main())
    except KeyboardInterrupt as e:
        print(e)

if __name__ == "__main__":
    main()