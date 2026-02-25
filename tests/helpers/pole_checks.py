from posgeo.validation import SingularityReport


def format_failure_reasons(report: SingularityReport) -> str:
    """Stable display helper for snapshot-like assertions in tests."""
    return " | ".join(report.failure_reasons)
