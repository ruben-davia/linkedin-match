from davia import Davia
from pydantic import BaseModel
from typing import List, Dict
import random

app = Davia()


class CoFounderProfile(BaseModel):
    name: str
    skills: List[str]
    experience_years: int
    previous_startups: int
    startup_interests: List[str]
    strengths: List[str]
    weaknesses: List[str]
    work_style: str
    values: List[str]


def get_profile_from_link(profile_link: str) -> CoFounderProfile:
    """
    Gets profile information from a LinkedIn link
    Currently returns fake data for demonstration
    """
    # Mock data generator using the profile link as a seed
    profile_id = profile_link.split("/")[-1]
    random.seed(profile_id)

    # Lists for generating random data
    all_skills = ["Technical", "Design", "Marketing", "Sales", "Finance", "Operations"]
    all_interests = ["AI", "Fintech", "Health", "Education", "Enterprise", "Consumer"]
    all_strengths = ["Leadership", "Execution", "Creativity", "Analysis", "Networking"]
    all_weaknesses = ["Impatience", "Perfectionism", "Risk-averse", "Overconfidence"]
    all_work_styles = ["Fast-paced", "Methodical", "Collaborative", "Independent"]
    all_values = ["Innovation", "Impact", "Growth", "Balance", "Ethics", "Quality"]

    # Generate random profile data
    profile = CoFounderProfile(
        name=f"User {profile_id[:8]}",
        skills=random.sample(all_skills, k=random.randint(2, 4)),
        experience_years=random.randint(2, 15),
        previous_startups=random.randint(0, 3),
        startup_interests=random.sample(all_interests, k=random.randint(1, 3)),
        strengths=random.sample(all_strengths, k=random.randint(2, 3)),
        weaknesses=random.sample(all_weaknesses, k=random.randint(1, 2)),
        work_style=random.choice(all_work_styles),
        values=random.sample(all_values, k=random.randint(2, 4)),
    )

    return profile


def calculate_cofounder_match(
    profile1: CoFounderProfile, profile2: CoFounderProfile
) -> Dict:
    """
    Calculate co-founder match metrics
    Returns a dictionary with match scores and insights
    """
    # Calculate the individual metrics
    skill_overlap = len(set(profile1.skills) & set(profile2.skills))
    skill_union = len(set(profile1.skills) | set(profile2.skills))
    skill_complementarity = 1 - (skill_overlap / skill_union) if skill_union > 0 else 0

    exp_diff = abs(profile1.experience_years - profile2.experience_years)
    exp_compatibility = 1 - min(exp_diff / 10, 1)  # Normalize, cap at 1

    interest_overlap = len(
        set(profile1.startup_interests) & set(profile2.startup_interests)
    )
    interest_compatibility = interest_overlap / max(
        len(profile1.startup_interests), len(profile2.startup_interests)
    )

    strength_overlap = len(set(profile1.strengths) & set(profile2.strengths))
    strength_complementarity = 1 - (
        strength_overlap / len(set(profile1.strengths) | set(profile2.strengths))
    )

    weakness_overlap = len(set(profile1.weaknesses) & set(profile2.weaknesses))
    weakness_complementarity = 1 - (
        weakness_overlap / len(set(profile1.weaknesses) | set(profile2.weaknesses))
    )

    work_style_match = 1 if profile1.work_style == profile2.work_style else 0.5

    values_overlap = len(set(profile1.values) & set(profile2.values))
    values_alignment = values_overlap / min(len(profile1.values), len(profile2.values))

    # Create 4 main scoring categories with calculated scores and detailed explanations

    # 1. Skill & Capability Compatibility
    skill_capability_score = round(
        (skill_complementarity * 0.7 + exp_compatibility * 0.3) * 100, 1
    )
    skill_capability_description = create_skill_capability_description(
        profile1, profile2, skill_complementarity, exp_compatibility
    )

    # 2. Vision & Values Alignment
    vision_values_score = round(
        (interest_compatibility * 0.4 + values_alignment * 0.6) * 100, 1
    )
    vision_values_description = create_vision_values_description(
        profile1, profile2, interest_compatibility, values_alignment
    )

    # 3. Working Dynamic
    working_dynamic_score = round(
        (
            strength_complementarity * 0.4
            + weakness_complementarity * 0.3
            + work_style_match * 0.3
        )
        * 100,
        1,
    )
    working_dynamic_description = create_working_dynamic_description(
        profile1,
        profile2,
        strength_complementarity,
        weakness_complementarity,
        work_style_match,
    )

    # 4. Growth Potential
    growth_potential_score = round(
        (
            skill_complementarity * 0.3
            + exp_compatibility * 0.2
            + interest_compatibility * 0.3
            + values_alignment * 0.2
        )
        * 100,
        1,
    )
    growth_potential_description = create_growth_potential_description(
        profile1,
        profile2,
        skill_complementarity,
        exp_compatibility,
        interest_compatibility,
    )

    # Overall match score (weighted average of the 4 categories)
    overall_score = (
        skill_capability_score * 0.3
        + vision_values_score * 0.3
        + working_dynamic_score * 0.25
        + growth_potential_score * 0.15
    ) / 100  # Convert back to 0-1 scale

    # Threshold for "good match"
    is_good_match = overall_score >= 0.7

    # Insights for why they match or don't
    insights = []
    risks = []

    if skill_capability_score > 70:
        insights.append("Strong skill complementarity")
    elif skill_capability_score < 50:
        risks.append("Potential skill overlap or gaps")

    if vision_values_score > 70:
        insights.append("Aligned vision and values")
    elif vision_values_score < 50:
        risks.append("Differing goals and priorities")

    if working_dynamic_score > 70:
        insights.append("Compatible working styles")
    elif working_dynamic_score < 50:
        risks.append("Potential conflicts in how you work")

    if growth_potential_score > 70:
        insights.append("Strong foundation for growth")
    elif growth_potential_score < 50:
        risks.append("Limited growth synergy")

    # Return comprehensive results
    return {
        "overall_match_score": round(overall_score * 100, 1),
        "is_good_match": is_good_match,
        "scores": {
            "skill_capability_compatibility": {
                "score": skill_capability_score,
                "description": skill_capability_description,
            },
            "vision_values_alignment": {
                "score": vision_values_score,
                "description": vision_values_description,
            },
            "working_dynamic": {
                "score": working_dynamic_score,
                "description": working_dynamic_description,
            },
            "growth_potential": {
                "score": growth_potential_score,
                "description": growth_potential_description,
            },
        },
        "match_insights": insights,
        "potential_risks": risks,
    }


def create_skill_capability_description(
    profile1: CoFounderProfile,
    profile2: CoFounderProfile,
    skill_complementarity: float,
    exp_compatibility: float,
) -> str:
    """Create detailed description of skill & capability compatibility"""

    common_skills = set(profile1.skills) & set(profile2.skills)
    unique_skills1 = set(profile1.skills) - set(profile2.skills)
    unique_skills2 = set(profile2.skills) - set(profile1.skills)

    if skill_complementarity > 0.7:
        complementarity_text = (
            "You have highly complementary skill sets, which is ideal for co-founders."
        )
    elif skill_complementarity > 0.4:
        complementarity_text = (
            "You have moderately complementary skills with some overlap."
        )
    else:
        complementarity_text = (
            "You have significant skill overlap, which may lead to redundancies."
        )

    if exp_compatibility > 0.7:
        exp_text = "Your experience levels are well-matched."
    elif exp_compatibility > 0.4:
        exp_text = "There's a moderate difference in your experience levels."
    else:
        exp_text = "There's a significant gap in your experience levels."

    skill_detail = ""
    if common_skills:
        skill_detail += f"Shared skills: {', '.join(common_skills)}. "
    if unique_skills1:
        skill_detail += (
            f"{profile1.name}'s unique skills: {', '.join(unique_skills1)}. "
        )
    if unique_skills2:
        skill_detail += (
            f"{profile2.name}'s unique skills: {', '.join(unique_skills2)}. "
        )

    years_diff = abs(profile1.experience_years - profile2.experience_years)
    exp_detail = f"Experience difference: {years_diff} years. "

    return f"{complementarity_text} {exp_text} {skill_detail}{exp_detail}"


def create_vision_values_description(
    profile1: CoFounderProfile,
    profile2: CoFounderProfile,
    interest_compatibility: float,
    values_alignment: float,
) -> str:
    """Create detailed description of vision & values alignment"""

    common_interests = set(profile1.startup_interests) & set(profile2.startup_interests)
    different_interests = set(profile1.startup_interests) ^ set(
        profile2.startup_interests
    )
    common_values = set(profile1.values) & set(profile2.values)
    different_values = set(profile1.values) ^ set(profile2.values)

    if interest_compatibility > 0.7:
        interest_text = "You share strong interest in the same startup areas."
    elif interest_compatibility > 0.3:
        interest_text = "You have some overlapping startup interests."
    else:
        interest_text = "You have very different startup interests."

    if values_alignment > 0.7:
        values_text = "Your core values are strongly aligned."
    elif values_alignment > 0.3:
        values_text = "You share some important values."
    else:
        values_text = "Your core values differ significantly."

    detail = ""
    if common_interests:
        detail += f"Shared interests: {', '.join(common_interests)}. "
    if different_interests:
        detail += f"Different interests: {', '.join(different_interests)}. "
    if common_values:
        detail += f"Shared values: {', '.join(common_values)}. "
    if different_values:
        detail += f"Different values: {', '.join(different_values)}. "

    return f"{interest_text} {values_text} {detail}"


def create_working_dynamic_description(
    profile1: CoFounderProfile,
    profile2: CoFounderProfile,
    strength_complementarity: float,
    weakness_complementarity: float,
    work_style_match: float,
) -> str:
    """Create detailed description of working dynamic"""

    common_strengths = set(profile1.strengths) & set(profile2.strengths)
    different_strengths = set(profile1.strengths) ^ set(profile2.strengths)
    common_weaknesses = set(profile1.weaknesses) & set(profile2.weaknesses)

    if profile1.work_style == profile2.work_style:
        style_text = f"You both prefer a {profile1.work_style} work style."
    else:
        style_text = f"{profile1.name} prefers a {profile1.work_style} work style, while {profile2.name} prefers a {profile2.work_style} work style."

    if strength_complementarity > 0.7:
        strength_text = "Your strengths complement each other well."
    else:
        strength_text = "You have some overlapping strengths."

    if weakness_complementarity > 0.7:
        weakness_text = "Your weaknesses are different, which helps balance each other."
    else:
        weakness_text = "You share some of the same weaknesses."

    detail = ""
    if common_strengths:
        detail += f"Shared strengths: {', '.join(common_strengths)}. "
    if different_strengths:
        detail += f"Complementary strengths: {', '.join(different_strengths)}. "
    if common_weaknesses:
        detail += f"Shared challenges: {', '.join(common_weaknesses)}. "

    return f"{style_text} {strength_text} {weakness_text} {detail}"


def create_growth_potential_description(
    profile1: CoFounderProfile,
    profile2: CoFounderProfile,
    skill_complementarity: float,
    exp_compatibility: float,
    interest_compatibility: float,
) -> str:
    """Create detailed description of growth potential"""

    # Consider startup experience
    startup_exp = profile1.previous_startups + profile2.previous_startups

    if startup_exp > 3:
        exp_text = "Together you have significant startup experience."
    elif startup_exp > 0:
        exp_text = "You have some startup experience between you."
    else:
        exp_text = "Neither of you has previous startup experience."

    if skill_complementarity > 0.7 and interest_compatibility > 0.5:
        synergy_text = "Your complementary skills and shared interests create strong potential for innovation."
    elif skill_complementarity > 0.5 or interest_compatibility > 0.5:
        synergy_text = "There's moderate potential for innovation based on your skills and interests."
    else:
        synergy_text = "You may face challenges innovating together due to overlapping skills or divergent interests."

    # Provide specific growth prediction
    if skill_complementarity > 0.7 and interest_compatibility > 0.7:
        potential = "Your partnership shows excellent growth potential with complementary capabilities and aligned interests."
    elif skill_complementarity > 0.5 and interest_compatibility > 0.5:
        potential = "Your partnership shows good growth potential, though you may need to work on aligning in some areas."
    else:
        potential = "Your growth potential may be limited without active effort to leverage complementary strengths."

    return f"{exp_text} {synergy_text} {potential}"


@app.task
def find_results(first_profile_link: str, second_profile_link: str) -> dict:
    """
    Main function to find co-founder match results between two LinkedIn profiles

    Args :
        first_profile_link : str
        second_profile_link : str

    Returns :
        dict : A dictionary containing the match results
    structured as :
    {
        "overall_match_score": float,
        "is_good_match": bool,
        "scores":  {
            "skill_capability_compatibility": {
                "score": float,
                "description": str,
            },
            "vision_values_alignment": {
                "score": float,
                "description": str,
            },
            "working_dynamic": {
                "score": float,
                "description": str,
            },
            "growth_potential": {
                "score": float,
                "description": str,
            },
        },
        "match_insights": list,
        "potential_risks": list,
    }

    """
    profile1 = get_profile_from_link(first_profile_link)
    profile2 = get_profile_from_link(second_profile_link)

    return calculate_cofounder_match(profile1, profile2)


if __name__ == "__main__":
    app.run()
