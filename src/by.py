# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
from selenium.webdriver.common.by import By


class AppiumBy(By):
    IOS_PREDICATE = '-ios predicate string'
    IOS_UIAUTOMATION = '-ios uiautomation'
    IOS_CLASS_CHAIN = '-ios class chain'
    ANDROID_UIAUTOMATOR = '-android uiautomator'
    ANDROID_VIEWTAG = '-android viewtag'
    ANDROID_DATA_MATCHER = '-android datamatcher'
    ANDROID_VIEW_MATCHER = '-android viewmatcher'
    # Deprecated
    WINDOWS_UI_AUTOMATION = '-windows uiautomation'
    ACCESSIBILITY_ID = 'accessibility id'
    IMAGE = '-image'
    CUSTOM = '-custom'
