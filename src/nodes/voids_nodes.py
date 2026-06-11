from collections import defaultdict
from datetime import datetime

from rich.console import Group
from rich.live import Live

from core.logger import console, logger
from domain.models import Trend
from domain.trends_getter import SearchTrends
from nodes.graph_state import StateVoids
from utils.displayers import build_progress_bar, build_spinner
from utils.llm_utils import LLMManager
from utils.prompt_getters import get_classify_news_prompt, get_summarize_news_prompt


class ClassifyNewsByTrend:
    def __init__(self):
        self.filter_spinner = build_spinner()
        self.filter_progress_bar = build_progress_bar()
        self.renders_group = Group(self.filter_spinner, self.filter_progress_bar)
        self.live = Live(self.renders_group, console=console, transient=True)
        self.update_state = {}

    def __call__(self, state: StateVoids):
        logger.info("Classifying news step")
        self.filter_spinner.add_task("Classifying news by trend", total=None)
        with self.live:
            self._classify_news(state.news_raw, state.trends)
        return self.update_state

    def _classify_news(self, news_raw, trends: list[Trend]):
        processed_news = []
        input_tokens = 0
        output_tokens = 0
        filter_bar_id = self.filter_progress_bar.add_task(
            "Classifying", total=len(news_raw)
        )
        llm = LLMManager()
        for new in news_raw:
            if not new["title"] or not new["snippet"]:
                continue
            logger.debug(f"Filtering new: {new['title']}")
            prompt = get_classify_news_prompt(new["title"], new["snippet"], trends)
            query = llm.invoke(prompt, json_mode=True)
            input_tokens += query.usage.input_tokens
            output_tokens += query.usage.output_tokens
            if query.content.get("trends"):
                logger.debug("New added to trend")
                new["trends"] = query.content["trends"]
                processed_news.append(new)
            else:
                logger.debug("New discarded")

            self.filter_progress_bar.update(filter_bar_id, advance=1)

        trends_updated = self._sort_news_in_topics(processed_news, trends)

        self.update_state = {
            "metadata": {
                "total_input_tokens": input_tokens,
                "total_output_tokens": output_tokens,
            },
            "trends": trends_updated,
            "news_by_trends": processed_news,
        }

    def _sort_news_in_topics(self, news_by_trends, trends):
        bucket = defaultdict(list)
        trends_updated = []
        for article in news_by_trends:
            for trend_id in set(article.get("trends", [])):
                bucket[trend_id].append(article)

        for trend in trends:
            trend.news = bucket.get(trend.id, [])
            trends_updated.append(trend)
        return trends_updated


class SummarizeNewsByTopic:
    def __init__(self):
        self.summarizer_spinner = build_spinner()
        self.summarize_progress_bar = build_progress_bar()
        self.renders_group = Group(self.summarizer_spinner, self.summarize_progress_bar)
        self.live = Live(self.renders_group, console=console, transient=True)
        self.update_state = {}

    def __call__(self, state: StateVoids):
        logger.info("Summarizing news step")
        self.summarizer_spinner.add_task(
            "Summarizing and getting trend category", total=None
        )
        with self.live:
            self._summarize_news(state.trends)
        return self.update_state

    def _summarize_news(self, trends: list[Trend]):
        trends_with_summary = []
        input_tokens = 0
        output_tokens = 0
        filter_bar_id = self.summarize_progress_bar.add_task(
            "Summarizing", total=len(trends)
        )
        llm = LLMManager()

        for trend in trends:
            logger.debug("Summarizing")
            summary_error = "Algo falló al generar el resumen"
            category_error = "unknown"

            if trend.news:
                prompt = get_summarize_news_prompt(trend)
                query = llm.invoke(prompt, json_mode=True)
                input_tokens += query.usage.input_tokens
                output_tokens += query.usage.output_tokens
                trend.news_summary = (
                    query.content["summary"]
                    if query.content.get("summary")
                    else summary_error
                )
                trend.category = (
                    query.content["category"]
                    if query.content.get("category")
                    else category_error
                )

            trends_with_summary.append(trend)
            self.summarize_progress_bar.update(filter_bar_id, advance=1)

        self.update_state = {
            "metadata": {
                "total_input_tokens": input_tokens,
                "total_output_tokens": output_tokens,
            },
            "trends": trends_with_summary,
        }


class RetrieveTrends:
    def __init__(self):
        self.filter_spinner = build_spinner()
        self.filter_progress_bar = build_progress_bar()
        self.renders_group = Group(self.filter_spinner, self.filter_progress_bar)
        self.live = Live(self.renders_group, console=console, transient=True)
        self.update_state = {}

    def __call__(self, state: StateVoids):
        logger.info("Retrieving trends")
        self.filter_spinner.add_task("Classifying news by trend", total=None)
        search = SearchTrends()
        trends = self._filter_trends(search.get_trends(), state.last_ingested_datetime)
        self.update_state["trends"] = trends
        self.update_state["last_trend_execution"] = search.last_trend_execution
        return self.update_state

    def _filter_trends(
        self, trends: list[Trend], last_ingested_datetime: datetime
    ) -> list[Trend]:
        trends_filtered = []

        for trend in trends:
            if (
                trend.is_active
                or trend.started_at > last_ingested_datetime
                or trend.finished_at > last_ingested_datetime
            ):
                trends_filtered.append(trend)
        return trends_filtered
