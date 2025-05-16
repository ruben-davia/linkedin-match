from enum import Enum
from pydantic import BaseModel
from typing import List
from davia import Davia

app = Davia()


class CardTitle(str, Enum):
    SKILL_COMPLEMENTARITY = "Skill Complementarity"
    INDUSTRY_EXPERIENCE_ALIGNMENT = "Industry & Experience Alignment"
    CONFLICT_PROBABILITY = "Conflict Probability"
    GROWTH_CATALYST_POTENTIAL = "Growth Catalyst Potential"
    CULTURAL_FIT_INDEX = "Cultural Fit Index"


class Card(BaseModel):
    title: CardTitle
    score: int
    insight: str


class StartupIdea(BaseModel):
    idea: str
    reason: str


class MatchResult(BaseModel):
    overall_match_score: int
    summary: str
    skill_complementarity: Card
    industry_experience_alignment: Card
    conflict_probability: Card
    growth_catalyst_potential: Card
    cultural_fit_index: Card
    startup_ideas: List[StartupIdea]


class ProfileInfo(BaseModel):
    linkedin_profile_url: str
    name: str
    profile_description: str


def get_profile_info(linkedin_profile_url: str) -> ProfileInfo:
    """
    Get profile information from a LinkedIn profile URL

    Args :
        linkedin_profile_url : str

    Returns :
        ProfileInfo

    """
    # return fake data for now
    return ProfileInfo(
        linkedin_profile_url=linkedin_profile_url,
        name="John Doe",
        profile_description="I am a software engineer with a passion for building scalable and efficient systems.",
    )


@app.task
def compare_profiles(profile_url1: str, profile_url2: str) -> MatchResult:
    """
    Compare two profiles and return a match result
    """

    profile1 = get_profile_info(profile_url1)
    profile2 = get_profile_info(profile_url2)

    # Generate fake data with more realistic values
    skill_complementarity = Card(
        title=CardTitle.SKILL_COMPLEMENTARITY,
        score=85,
        insight="John's software engineering expertise complements Jane's product management background, creating a balanced technical and business perspective.",
    )

    industry_alignment = Card(
        title=CardTitle.INDUSTRY_EXPERIENCE_ALIGNMENT,
        score=72,
        insight="Both have experience in SaaS companies, with John focusing on backend systems and Jane on go-to-market strategies in similar industries.",
    )

    conflict_probability = Card(
        title=CardTitle.CONFLICT_PROBABILITY,
        score=32,
        insight="Low conflict probability due to complementary working styles, though different approaches to decision-making may require clear communication channels.",
    )

    growth_potential = Card(
        title=CardTitle.GROWTH_CATALYST_POTENTIAL,
        score=91,
        insight="Exceptional potential for mutual growth as John can enhance technical skills in product-thinking while Jane can gain deeper technical insight into system architecture.",
    )

    cultural_fit = Card(
        title=CardTitle.CULTURAL_FIT_INDEX,
        score=78,
        insight="Strong alignment on work-life balance values and similar preferences for remote-first culture with regular in-person collaboration.",
    )

    # Calculate overall score as weighted average
    overall_score = int(
        (
            skill_complementarity.score
            + industry_alignment.score
            + (100 - conflict_probability.score)
            + growth_potential.score
            + cultural_fit.score
        )
        / 5
    )

    # Generate fake startup ideas
    startup_ideas = [
        StartupIdea(
            idea="AI-Powered Supply Chain Optimization Platform",
            reason="John's backend expertise combined with Jane's industry connections could create a powerful solution for an underserved market segment.",
        ),
        StartupIdea(
            idea="Developer Productivity Analytics Tool",
            reason="Both have experienced productivity challenges in their careers and have complementary skills to address technical and UX aspects of this problem.",
        ),
        StartupIdea(
            idea="Sustainable Tech Consulting Firm",
            reason="Shared interest in sustainability combined with their technical and business backgrounds makes them well-positioned for advisory services.",
        ),
    ]

    return MatchResult(
        overall_match_score=overall_score,
        summary="This professional match shows strong potential for collaboration, particularly in technology ventures that require both deep technical expertise and market awareness. The complementary skillsets and aligned industry experience suggest high probability of success in joint ventures.",
        skill_complementarity=skill_complementarity,
        industry_experience_alignment=industry_alignment,
        conflict_probability=conflict_probability,
        growth_catalyst_potential=growth_potential,
        cultural_fit_index=cultural_fit,
        startup_ideas=startup_ideas,
    )


if __name__ == "__main__":
    app.run()
