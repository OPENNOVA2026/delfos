import json
from datetime import datetime, timedelta

from core.settings import settings
from domain.delfos_pipeline import DelfosVoidPipeline


def run():
    now = datetime.now()
    yesterday = now - timedelta(hours=24.0)
    delfos_voids = DelfosVoidPipeline(yesterday)
    delfos_voids.run_workflow()
    if settings.environment == "local":
        state_json = json.dumps(
            delfos_voids.state, indent=2, ensure_ascii=False, default=str
        )
        with open("./test.json", "w") as f:
            f.write(state_json)


if __name__ == "__main__":
    run()
