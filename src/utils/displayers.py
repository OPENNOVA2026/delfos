from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def build_spinner():
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )


def build_progress_bar():
    text_column_desc = TextColumn("[progress.description]{task.description}")
    text_column_progress = TextColumn("{task.completed}/{task.total}")
    progress_bar = Progress(
        SpinnerColumn(),
        text_column_desc,
        BarColumn(),
        text_column_progress,
        TimeRemainingColumn(),
        TimeElapsedColumn(),
    )
    return progress_bar
