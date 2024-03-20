#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author zhouhuawei time:2024/3/4
from gpt import chat
from langchain.output_parsers import ResponseSchema
from code_utils import *
# 格式化返回模版
response_schemas = [
    ResponseSchema(name="question", description="所出题目题干"),
    ResponseSchema(name="answer", description="所出题目答案"),
    ResponseSchema(name="knowledge", description="所出题目核心知识点"),
    ResponseSchema(name="testcase", description="所出题目测试示例演示(请给出5个演示示例)"),
    ResponseSchema(name="analyze", description="所出题目解析"),
    ResponseSchema(name="grade", description="所出题目的难度"),
    ResponseSchema(name="input_module", description="所出题目的答案的输入模板")
]

# 问答题prompt构建并对话
def buildPromptAndChat(paramList):
    systemPrompt = ""
    humanPrompt = ""
    mode = paramList['mode']
    message = paramList.get('message')
    difficulty = paramList["message"]["grade"]
    timeLimit = paramList["message"]["timeLimit"]
    spaceLimit = paramList["message"]["spaceLimit"]
    time_complexity = paramList["message"]["time_complexity"]
    space_complexity = paramList["message"]["space_complexity"]
    code_type = paramList["message"]["code_type"]
    input_range = paramList["message"]["input_range"]



    if mode == 1:
        # 以题生题
        question = message.get('questionStem', None)
        systemPrompt = "你是一名编程领域的出题专家，我将给你一道例题，请你首先拆解出例题所包含的编程领域核心知识点，随后仿照所给的例题生成一个知识点相同，难度相似但内容不同（不可以是原题）的高质量的编程题。"
        humanPrompt =  f"例题内容为:{question}。"\
                       f"下面为利用题目生成题目的一个例子: {getcode_1Example()}"\
                       f"出题难度标准请参照{difficulty_standard(difficulty)}" \
                       f"出题规范标准请参照{basic_requirement}"\
                       f"相似度标准请参考{getSimilarRules()}"\
                       f"试题运行的时间限制请参考{timeLimit},试题运行的空间限制请参考{spaceLimit}"\
                       f"试题生成代码的时间复杂度请参考{time_complexity},试题的空间复杂度请参考{space_complexity}"\
                       f"解决试题所使用的代码语言类型请使用{code_type}"\
                       f"对于输入变量的范围限制请参考{input_range}"\
                       f"试题的回答模板请严格参考{format_instructinos}"


    elif mode == 2:
        # 以文生题
        artical = message.get('artical', None)
        systemPrompt = "你是一名编程领域的出题专家，我将给你一段文本，请你首先解析出文本与哪些编程领域知识点相关联，随后仿照所给的文本生成一个知识点相同，难度相似但内容不同（不可以是原文本）的高质量的编程题。"
        humanPrompt = f"文本内容为:{artical}"\
                      f"下面为利用文本内容生成题目的一个例子：{getcode_2Example()}"\
                      f"出题难度标准请参照{difficulty_standard(difficulty)}" \
                      f"出题规范标准请参照{basic_requirement}" \
                      f"相似度标准请参考{getSimilarRules()}"\
                      f"试题运行的时间限制请参考{timeLimit},试题运行的空间限制请参考{spaceLimit}" \
                      f"试题生成代码的时间复杂度请参考{time_complexity},试题的空间复杂度请参考{space_complexity}" \
                      f"解决试题所使用的代码语言类型请使用{code_type}" \
                      f"对于输入变量的范围限制请参考{input_range}"\
                      f"试题的回答模板请严格参考{format_instructinos}"

    elif mode == 3:
        # 按需生题
        require = message.get('require', None)
        systemPrompt = "你是一名编程领域的出题专家，请你依据以下要求出一个高质量的问答题。"
        humanPrompt = f"题目的具体要求为{require}" \
                      f"下面为利用文本内容生成题目的一个例子：{getcode_3Example()}" \
                      f"出题难度标准请参照{difficulty_standard(difficulty)}" \
                      f"出题规范标准请参照{basic_requirement}" \
                      f"相似度标准请参考{getSimilarRules()}"\
                      f"试题运行的时间限制请参考{timeLimit},试题运行的空间限制请参考{spaceLimit}" \
                      f"试题生成代码的时间复杂度请参考{time_complexity},试题的空间复杂度请参考{space_complexity}" \
                      f"解决试题所使用的代码语言类型请使用{code_type}" \
                      f"对于输入变量的范围限制请参考{input_range}" \
                      f"试题的回答模板请严格参考{format_instructinos}"

    else:
        print("传入mode值不正确。")


    return chat(response_schemas, systemPrompt, humanPrompt)

# 验证操作
paramList = {
    'mode': 2,
    'message': {
       #'questionStem': '编写一个函数，接受一个整数列表作为输入，使用for循环计算列表中所有元素的和，并返回结果。',
       'artical':'numpy是python中的一个库,请使用numpy库生成一个编程题',
       # 'require':''
       'grade': '1',
       'timeLimit':'1000ms',
       'spaceLimit':'100M',
       'time_complexity':'none',
       'space_complexity':'none',
       'code_type':'python',
       'input_range':'none'
    }
}
response = buildPromptAndChat(paramList)
print(response)
