#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Inquiry

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Inquiry = True
userDefinedDICT = {"找": ["尋找", "找尋", "列出", "知道"], "類型": ["公立大學", "私立大學", "公立科技大學", "私立科技大學", "軍警院校"], "外文系": ["外國語文學系"], "資訊系": ["資訊工程學系"], "台灣大學": ["台大", "國立台灣大學"], "成功大學": ["成大", "國立成功大學", "成功大學"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Inquiry:
        print("[Inquiry] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[我]要找[台大][外文系]和[資訊系]":
        # write your code here
        pass

    if utterance == "[我]要找[成大][外文系]":
        # write your code here
        pass

    if utterance == "[我]要找[成大][外文系]和[台大][資訊系]":
        # write your code here
        pass

    if utterance == "[我]要找[成大]和[台大][外文系]":
        # write your code here
        pass

    return resultDICT