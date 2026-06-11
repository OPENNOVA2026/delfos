import random
from datetime import datetime, timedelta, timezone

from domain.models import Trend


def get_fake_trends() -> list[Trend]:
    now = datetime.now(timezone.utc)

    trend_1 = Trend(
        id=1,
        trend="Trend 1",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(minutes=random.randint(6 * 60, 24 * 60)),
        finished_at=now - timedelta(minutes=random.randint(2 * 60, 5 * 60)),
        keywords=["Este es", "el primer trend"],
        ivs=0.89,
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Pues aquí tenemos un resumen de un trend que es un prueba",
        is_active=False,
    )
    trend_2 = Trend(
        id=2,
        trend="Trend 2",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(minutes=random.randint(6 * 60, 24 * 60)),
        finished_at=now - timedelta(minutes=random.randint(2 * 60, 5 * 60)),
        keywords=["Este es", "trend", "gravísimo"],
        ivs=round(random.uniform(0, 1), 2),
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Otro trend con muchos peores numeros",
        is_active=False,
    )
    trend_3 = Trend(
        id=3,
        trend="Trend 3",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(minutes=random.randint(6 * 60, 24 * 60)),
        finished_at=now - timedelta(minutes=random.randint(2 * 60, 5 * 60)),
        keywords=["Tenemos", "otro trend"],
        ivs=round(random.uniform(0, 1), 2),
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Un trend nuevo, qué duro es mockear a mano",
        is_active=False,
    )
    trend_4 = Trend(
        id=4,
        trend="Trend 4",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(minutes=random.randint(6 * 60, 24 * 60)),
        finished_at=now - timedelta(minutes=random.randint(2 * 60, 5 * 60)),
        keywords=None,
        ivs=round(random.uniform(0, 1), 2),
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Otro trend mockeado a mano, pero veo la lu al final del tunel",
        is_active=False,
    )
    trend_5 = Trend(
        id=5,
        trend="Trend 5",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(minutes=random.randint(6 * 60, 24 * 60)),
        keywords=["Este es", "el primer trend"],
        ivs=round(random.uniform(0, 1), 2),
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Por fin el ultimo trend, ya no queda más que mockear",
        is_active=True,
    )
    trend_6 = Trend(
        id=6,
        trend="Trend 6",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(minutes=random.randint(6 * 60, 24 * 60)),
        keywords=["Este es", "el primer trend"],
        ivs=round(random.uniform(0, 1), 2),
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Por fin el ultimo trend, ya no queda más que mockear",
        is_active=True,
    )
    trend_7 = Trend(
        id=7,
        trend="Trend 7",
        search_volume=random.randint(200, 600),
        increase=random.randint(50, 400),
        started_at=now - timedelta(days=random.randint(2, 4)),
        keywords=["Este es", "el primer trend"],
        ivs=round(random.uniform(0, 1), 2),
        demand_factor=round(random.uniform(0, 1), 2),
        coverage_factor=round(random.uniform(0, 1), 2),
        delay_factor=round(random.uniform(0, 1), 2),
        plurality_factor=round(random.uniform(0, 1), 2),
        news_summary="Por fin el ultimo trend, ya no queda más que mockear",
        is_active=True,
    )
    return [trend_1, trend_2, trend_3, trend_4, trend_5, trend_6, trend_7][
        : random.randint(3, 6)
    ]


def get_fake_metadata() -> dict:
    return {
        "execution_datetime": datetime.now(timezone.utc).isoformat(),
        "total_input_tokens": 868673,
        "total_output_tokens": 6065,
        "model_used": "gpt-4.1-mini",
        "model_input_tokens_cost_1M": 0.14093,
        "model_output_tokens_cost_1M": 0.5638,
        "total_cost": 0.12584153289,
    }
