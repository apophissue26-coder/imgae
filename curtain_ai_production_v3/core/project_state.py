from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VariationResult:
    name: str
    direction: str
    description: str
    effect_preview: Path | None = None
    pattern_image: Path | None = None


@dataclass
class ProjectState:
    source_image: Path | None = None
    analysis: dict = field(default_factory=dict)
    extracted_pattern: Path | None = None
    variations: list[VariationResult] = field(default_factory=list)
    selected_variation: VariationResult | None = None
