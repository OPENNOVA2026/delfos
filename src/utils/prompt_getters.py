import random

import yaml
from langchain_core.prompts import ChatPromptTemplate

from domain.models import Trend


def get_classify_news_prompt(title: str, snippet: str, trends: list[Trend]):
    trends_list = [
        f"Trend id: {trend.id}:\n\n"
        + f"\tNombre del Trend: {trend.trend}\n"
        + f"\tKeywords (si las hay): {trend.keywords if trend.keywords else ''}\n"
        for trend in trends
    ]
    trends_joined = "\n\n\n".join(trends_list)
    with open("./src/nodes/prompts/classify_news_prompt.yml") as promptfile:
        prompt_yml = yaml.load(promptfile, Loader=yaml.FullLoader)
    prompt = ChatPromptTemplate(
        [
            ("system", prompt_yml["system"]),
            ("user", prompt_yml["user"]),
        ]
    )
    return prompt.format(titulo=title, snippet=snippet, trends=trends_joined)


def get_summarize_news_prompt(trend: Trend):
    rng = random.Random(42)
    keywords = (
        ", ".join(trend.keywords) if trend.keywords else "No keywords for this topic."
    )
    trend_for_prompt = f"Título: {trend.trend}\nKeywords: {keywords}"
    sampled_news = rng.sample(trend.news, min(20, len(trend.news)))
    news = [
        f"Noticia {index}:\n\n"
        + f"\tTitular: {new['title']}\n"
        + f"\tCuerpo: {new['snippet']}"
        for index, new in enumerate(sampled_news, start=1)
    ]
    news = "\n\n-----------------------------\n\n".join(news)
    with open("./src/nodes/prompts/news_summarize_prompt_v1.yml") as promptfile:
        prompt_yml = yaml.load(promptfile, Loader=yaml.FullLoader)
    prompt = ChatPromptTemplate(
        [
            ("system", prompt_yml["system"]),
            ("user", prompt_yml["user"]),
        ]
    )
    return prompt.format(news=news, trend=trend_for_prompt)
