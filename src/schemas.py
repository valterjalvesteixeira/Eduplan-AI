from typing import List, Optional, Literal
from pydantic import BaseModel, Field


EducationLevel = Literal["Pre-school", "Primary School", "Lower Secondary", "Upper Secondary"]


class PlanMeta(BaseModel):
    theme: str = Field(..., description="Main theme / focus of the plan")
    total_duration_minutes: int = Field(..., gt=0, description="Total duration in minutes")
    notes: Optional[str] = Field(None, description="Optional teacher notes or constraints")


class Activity(BaseModel):
    title: str = Field(..., description="Activity Title")
    recommended_age_group: str = Field(..., description="Recommended Age Group / School Level")
    learning_goals: List[str] = Field(..., description="Learning Goals (knowledge and skills)")
    ai_tool_or_concept: str = Field(..., description="AI tool or AI concept used")
    estimated_duration_minutes: int = Field(..., gt=0, description="Estimated Duration in minutes")
    materials_and_technology: List[str] = Field(default_factory=list, description="Materials and technology needed")
    steps: List[str] = Field(..., min_length=3, description="Step-by-step classroom implementation")
    engagement_rationale: str = Field(..., description="How AI enhances student engagement")
    skills_developed: List[str] = Field(default_factory=list, description="Skills developed")
    multicultural_adaptations: List[str] = Field(default_factory=list, description="Adaptations for multicultural classrooms")
    extension_activity: str = Field(..., description="Extension activity for more advanced students")


class LevelPlan(BaseModel):
    level: EducationLevel
    activities: List[Activity] = Field(..., min_length=2, max_length=3, description="2–3 activities per level")


class RiskItem(BaseModel):
    risk: str = Field(..., description="Potential risk or classroom issue")
    mitigation: str = Field(..., description="Mitigation strategy")


class EduPlan(BaseModel):
    meta: PlanMeta
    learning_objectives: List[str] = Field(..., min_length=3)
    levels: List[LevelPlan] = Field(..., min_length=4, max_length=4, description="Exactly 4 levels")
    risk_analysis: List[RiskItem] = Field(default_factory=list)