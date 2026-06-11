from abc import ABC, abstractmethod
from datetime import datetime

from langgraph.graph import END, START, StateGraph

from core.logger import logger
from domain.information_voids_score import InformationVoidsScore
from domain.models import Trend
from nodes.graph_state import StateVoids, get_empty_state_voids
from nodes.news_scrapers import GetNewspaperNews
from nodes.voids_nodes import ClassifyNewsByTrend, RetrieveTrends, SummarizeNewsByTopic


class DelfosPipeline(ABC):
    @abstractmethod
    def run_workflow(self):
        pass


class DelfosVoidPipeline(DelfosPipeline):
    def __init__(self, last_trend_execution: datetime):
        self.last_exec = last_trend_execution
        self._build_graph()

    def run_workflow(self) -> None:
        logger.info("Invoking flow")
        self.state = self.workflow.invoke(get_empty_state_voids(self.last_exec))
        state = StateVoids(**self.state)
        self.state = state.model_dump()
        ivs_calculator = InformationVoidsScore()
        for trend in self.state["trends"]:
            trend_copy = trend.copy()
            trend_pydantic = Trend(**trend_copy)
            ivs = ivs_calculator.evaluate(trend_pydantic)
            trend["ivs"] = ivs["ivs"]
            trend["demand_factor"] = ivs["demand_factor"]
            trend["coverage_factor"] = ivs["coverage_factor"]
            trend["delay_factor"] = ivs["delay_factor"]
            trend["plurality_factor"] = ivs["plurality_factor"]

    def _build_graph(self):
        logger.info("Building full graph")
        workflow = StateGraph(StateVoids)

        workflow.add_node("get_news", GetNewspaperNews())
        workflow.add_node("get_trends", RetrieveTrends())
        workflow.add_node("classify_news", ClassifyNewsByTrend())
        workflow.add_node("summarize_news", SummarizeNewsByTopic())

        workflow.add_edge(START, "get_news")
        workflow.add_edge(START, "get_trends")
        workflow.add_edge("get_news", "classify_news")
        workflow.add_edge("get_trends", "classify_news")
        workflow.add_edge("classify_news", "summarize_news")
        workflow.add_edge("summarize_news", END)

        logger.info("Compiling graph")
        self.workflow = workflow.compile()

    def get_metadata(self):
        if "metadata" in self.state:
            return self.state["metadata"]
        else:
            logger.error("Pipeline not executed yet!")
            return {}

    def get_trends(self) -> list[Trend]:
        if "trends" in self.state:
            return [Trend(**trend) for trend in self.state["trends"]]
        else:
            logger.error("Pipeline not executed yet!")
            return []
