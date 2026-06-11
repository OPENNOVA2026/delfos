from datetime import datetime
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel

from domain.models import Trend


class Metadata(BaseModel):
    execution_datetime: str = datetime.now().isoformat(sep="_", timespec="seconds")
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    model_used: str
    model_input_tokens_cost_1M: float = 0.0  # noqa: N815
    model_output_tokens_cost_1M: float = 0.0  # noqa: N815
    total_cost: float = 0


def update_metadata_reducer(
    prev: Metadata,
    new: dict[
        Union[Literal["total_input_tokens"], Literal["total_output_tokens"]], int
    ],
) -> Metadata:
    state = prev.model_copy(deep=True)
    state.total_input_tokens += new["total_input_tokens"]
    state.total_output_tokens += new["total_output_tokens"]
    cost = state.total_input_tokens * state.model_input_tokens_cost_1M / 1_000_000
    cost += state.total_output_tokens * state.model_output_tokens_cost_1M / 1_000_000
    state.total_cost = cost
    return state


class StateVoids(BaseModel):
    metadata: Annotated[Metadata, update_metadata_reducer]
    last_ingested_datetime: datetime
    last_trend_execution: datetime | None = None
    trends: list[Trend] = []
    news_raw: list[dict[str, Any]] = []
    news_by_trends: list[dict[str, Any]] = []


def get_empty_state_voids(
    last_ingested_datetime: datetime = datetime.now(),
) -> StateVoids:
    metadata = Metadata(
        model_used="gpt-4o-mini",
        model_output_tokens_cost_1M=0.5638,
        model_input_tokens_cost_1M=0.14093,
    )
    return StateVoids(metadata=metadata, last_ingested_datetime=last_ingested_datetime)
