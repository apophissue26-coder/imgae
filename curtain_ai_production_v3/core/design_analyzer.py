class DesignAnalyzer:
    def summarize(self, analysis: dict) -> str:
        return "\n".join([f"{k}: {v}" for k, v in analysis.items()])
