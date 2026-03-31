# Elastolink CLI

## Install

安装 Elastolink 命令行工具

```shell
pip install elastolink
```

## Help

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py   
usage: elastolink-cli.py [-h] [-l] [-d <会议ID>] [-m <会议ID>] [-o <会议ID>] [-s <关键词>] [-k <API KEY>] [--status] [--verbose]

Elastolink Command Line Interface

options:
  -h, --help             show this help message and exit
  -l, --list             会议列表
  -d, --detail <会议ID>    查看会议内容
  -m, --markdown <会议ID>  会议 Markdown 文件
  -o, --office <会议ID>    下载 Office 会议文档
  -s, --search <关键词>     会议搜索
  -k, --key <API KEY>    设置 API KEY
  --status               设备状态
```

## 设置 API KEY

请先在小程序后台，用户中心生成 API KEY 

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py -k sk-02172F38-776D-4F5F-88D3-EAC0F87E445B

```

## 会议列表

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py -l

+----------------------------------------+----------------------+------------+----------+--------------+
|                 会议ID                 |       会议标题       |  会议时长  | 会议语言 |   会议日期   |
+========================================+======================+============+==========+==============+
| fb997978-df53-4588-a163-d28da08d9f06   | 会议测试             | -          | -        | 2026-03-17   |
+----------------------------------------+----------------------+------------+----------+--------------+
| 019f3094-21af-4802-8b7e-07b11e31673e   | 会议测试             | -          | -        | 2026-03-17   |
+----------------------------------------+----------------------+------------+----------+--------------+
| c8e44bb3-5f17-4b46-9689-87ccf2f901a1   | 会议测试             | -          | -        | 2026-03-17   |
+----------------------------------------+----------------------+------------+----------+--------------+
| a5a574f7b7d34cfd8a9b564670ef354b       | PodcastEnglishLear   | 01:56:52   | en-US    | 2026-03-25   |
+----------------------------------------+----------------------+------------+----------+--------------+

共 4 条会议
--------------------------------------------------------------------------------
您可以使用 elastolink-cli -d <会议ID> 查看会议内容
```

## 查看会议

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py -d a5a574f7b7d34cfd8a9b564670ef354b
会议主题：PodcastEnglishLearningTips
会议时间：2026-03-25T14:32:32
会议时长：01:56:52
会议语言：en_US
----- 会议内容 -----
00:00:31 1：English shpodcast .
00:00:36 2：from speak English with class.
00:00:40 3：Hey, Hey, English learners, welcome back to the English leap podcast.
00:00:46 3：Your cozy place to learn easy English through real life conversations. I'm Anna and I'm Jake.
00:00:51 4：And as always, we're really happy you decided to spend a little bit of your day with us.
00:00:51 4：Yeah, seriously.
00:01:02 3：you could be anywhere on the Internet right now, Netflix, Instagram, games, but you're here with us working on your English and not .
00:01:02 4：just here.
00:01:11 4：In one place, we see you in the comments, people listening from so many different parts of the world.
00:01:15 3：and we just want to say a big thank you for all your love and support.
00:01:22 3：When we read, I listen to you on my way to work or I fall asleep with your podcast. It makes our hearts so happy. Yeah.
00:01:30 4：sometimes we're like, wow, our little cozy podcast is traveling more than we are .
00:01:30 3：one day.
00:02:02 1：因没有，你是不定要套餐去块，是你要想要法，它就必以就要有。
```

## 查看 Mardown 文档

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py -m a5a574f7b7d34cfd8a9b564670ef354b | head -n 10
----- 鱼骨图 (开始)-----
- 缺乏对不同家庭具体使用场景的明确理解
  - 销售人员与潜在客户的初步沟通不足，未能全面收集家庭日常通勤距离、长途旅行频率、载客与载物需求等关键信息。
  - 市场调研数据未按家庭结构（如单身、有孩家庭、多代同堂）和主要用车场景（城市代步、城际通勤、周末休闲）进行精细化分类。
  - 现有宣传材料过于笼统，未能清晰展示不同双擎车型如何针对性解决各类家庭的特定痛点。
- 对丰田双擎技术优势与家庭实用性关联的传达不清晰
  - 技术讲解过于专业化，使用了过多工程术语，导致普通家庭消费者难以理解混动系统如何直接转化为低油耗、平顺驾驶和降低使用成本。
  - 试驾体验流程标准化，未能引导客户在模拟典型家庭使用场景（如拥堵路段、满载爬坡、安静行驶）中感受双擎技术的核心价值。
  - 缺乏与同价位纯燃油车或竞品混动车型在长期持有成本、可靠性、保养便利性等方面的直观对比数据。
- 购车决策过程中的财务考量不够透明和个性化
```

## 下载 Office 文档

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py -o a5a574f7b7d34cfd8a9b564670ef354b            
----- Office 文档列表 -----
"思维导图":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/aigcsst/25321561854178/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips%28mindmap%29.svg?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=Nw8czjwh3t53Slm%2Fyt174lhaiN0%3D
"幻灯片":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips_20260325_093221.pptx?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=L3%2BXDghHtixR%2FLzB1d3RG5%2FSN4M%3D
"音频文件":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/audio.mp3?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=pib7CWZYMRzwpogQSZ90Z8xX8Xc%3D
"会议纪要":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/aigcsst/25321561854178/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips%28minutes%29.docx?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=qccOwE2QH6Bjm41AUe73t8GUNxI%3D
"会议结论":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/aigcsst/25321561854178/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips%28summary%29.docx?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=isBsxyVG74StY6j0t13z2J9tDcQ%3D
"鱼骨图":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/aigcsst/25321561854178/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips%28fishbone%29.svg?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=afeoUqjxU%2BlejmXln41Ok5rFOr0%3D
"待办事项":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/aigcsst/25321561854178/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips%28todolist%29.docx?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=bYsh%2BycjFCO45k2R5%2Bze7GOcH3A%3D
"会议方案":http://elastolink-document.oss-cn-shenzhen.aliyuncs.com/development/aigcsst/25321561854178/2026-03-25/a5a574f7b7d34cfd8a9b564670ef354b/PodcastEnglishLearningTips%28plan%29.docx?Expires=1775017938&OSSAccessKeyId=LTAI5tPrqH1c1FVWfJxvrafY&Signature=%2F87RV%2FBfPOE3QBnma%2Fn%2BSfWck%2F4%3D
----- 文档下载连接时效 24 小时 -----
```

## 查看设备状态

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py --status
{'expired': 'xxxxxx', 'status': '激活'}
```

## 集成 Openclaw 小龙虾

```shell
(.venv) neo@Mac elastolink % python elastolink-cli.py -k sk-02172F38-776D-4F5F-88D3-EAC0F87E445B

```

或者

```shell

export ELASTOLINK_API_KEY=sk-02172F38-776D-4F5F-88D3-EAC0F87E445B

```

然后让小龙虾查看会议列表，在根据需要阅读会议内容。接下来就可以操作了，例如：

```text
小龙虾：请帮我总结2026年第一季度会议中都有哪些重要的代办事项
小龙虾：帮我分析所有会议发言人，并总结最有价值发言，最后给我一份，员工价值价值评分，再给我制定一个优秀员工激励方案。
小龙虾：帮我分析会议中的发言时，给我列出，谁在摸鱼？
小龙虾：2026年2月份，会议中提到的报销费用都有哪些，给我粗略统计一下2月份花了多少钱。
小龙虾：给我统计一下3月份营销会议中，提到所有各种项目，投入与产出比，输出一份Excel 文档给我。
小龙虾：这个月面试了多少人？对比一下所有面试者跟我们公司的岗位胜任力模型，最后生成一份 excle 文档，放在我电脑的 D：盘，人力资源文件夹下。
小龙虾：下载“数字转型会议”的会议纪要，帮我分析一下技术可行性？
小龙虾：昨天的会议，发言人1是李副总，你认为他的方案可行吗？
```

## 开发环境安装

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install build twine
python -m build
twine upload dist/elastolink-0.0.2*
```