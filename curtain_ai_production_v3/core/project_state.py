from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ProjectState:
    source_image: Optional[Path] = None
    analysis_report: Optional[Path] = None
    extracted_pattern: Optional[Path] = None
    variations: List[Path] = field(default_factory=list)
    selected_variation: Optional[Path] = None
    selected_effects: List[Path] = field(default_factory=list)
    production_preview: Optional[Path] = None
    export_tif: Optional[Path] = None
    params: Dict = field(default_factory=dict)
