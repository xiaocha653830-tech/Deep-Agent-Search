from utils.logger_utils import logger
import os
from dotenv import load_dotenv
from typing import  Literal
from langchain_core.tools import tool
from tavily import TavilyClient

_tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def internet_search(
        query:str,
        topic: Literal["general", "news", "finance"] = "general",
        max_results: int = 5,
        include_raw_content:bool = False #是否返回详细数据
):
    """
    进行网络搜索工具,可以查询数据库或者rag助手中不包含的数据
    :param query: 查询内容
    :param topic: 查询类别
    :param max_results: 查询返回的条数
    :param include_raw_content: 是否精简返回
    :return: 查询的返回结果
    """
    # 1. 做好日志记录
    logger.debug(f"开始进行{internet_search}工具的调用!查询内容:{query} , 查询数量:{max_results}")

    return _tavily_client.search(
        query=query,
        topic=topic,
        max_results=max_results,
        include_raw_content=include_raw_content
    )
