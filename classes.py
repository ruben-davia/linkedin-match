from pydantic import BaseModel
from typing import List
from enum import Enum


class PersonInfo(BaseModel):
    name: str
    location: str
    current_role: str
    past_roles: str
    education: str
    skills: str
    industries: str
    notable_keywords: str
    potential_flags: str


class CardTitle(str, Enum):
    SKILL_COMPLEMENTARITY = "Skill Complementarity"
    INDUSTRY_EXPERIENCE_ALIGNMENT = "Industry & Experience Alignment"
    CONFLICT_PROBABILITY = "Conflict Probability"
    GROWTH_CATALYST_POTENTIAL = "Growth Catalyst Potential"
    CULTURAL_FIT_INDEX = "Cultural Fit Index"
    CRITIQUE_OPENNESS = "Critique Openness"


class Card(BaseModel):
    title: CardTitle
    score: int
    insight: str


class StartupIdea(BaseModel):
    idea: str
    reason: str


class MatchResult(BaseModel):
    overall_match_score: int
    # summary: str
    skill_complementarity: Card
    industry_experience_alignment: Card
    conflict_probability: Card
    growth_catalyst_potential: Card
    cultural_fit_index: Card
    critique_openness: Card
    startup_ideas: List[StartupIdea]
