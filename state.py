from dataclasses import dataclass, field
from typing import Optional
@dataclass
class PlayerState:
    clues_seen: list = field(default_factory=list)
    clues_collected: int = 0
    witnesses_interviewed: int = 0
    witness_statements: list = field(default_factory=list)
    scene_visits: int = 0
    max_scene_visits: int = 3
    witness_count: int = 0
    max_witnesses: int = 3
    arrested: bool = False
    arrested_suspect: Optional[str] = None
    game_over: bool = False
    def has_more_clues(self) -> bool:
        return self.scene_visits < self.max_scene_visits
    def has_more_witnesses(self) -> bool:
        return self.witnesses_interviewed < self.max_witnesses
    def status_snapshot(self) -> dict:
        return {
            "clues": self.clues_collected,
            "max_clues": self.max_scene_visits,
            "witnesses": self.witnesses_interviewed,
            "max_witnesses": self.max_witnesses,
        }