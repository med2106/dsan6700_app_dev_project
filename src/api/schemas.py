from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Core Dog Profile Schema
class DogProfile(BaseModel):
    # Basic Information
    name: str = Field(..., min_length=1, max_length=50, description="Dog's name")
    breed: str = Field(..., min_length=1, description="Dog breed (e.g., Labrador, Mixed)")
    age: int = Field(..., ge=0, le=20, description="Dog's age in years")
    size: str = Field(..., description="Dog size category (small, medium, large, giant)")
    gender: str = Field(..., description="Dog gender (male, female)")
    
    # Physical Characteristics
    weight: float = Field(..., gt=0, le=200, description="Dog's weight in pounds")
    energy_level: int = Field(..., ge=1, le=5, description="Energy level (1=low, 5=high)")
    
    # Behavioral Traits
    friendliness: int = Field(..., ge=1, le=5, description="Friendliness level (1=shy, 5=very friendly)")
    playfulness: int = Field(..., ge=1, le=5, description="Playfulness level (1=calm, 5=very playful)")
    training_level: int = Field(..., ge=1, le=5, description="Training level (1=untrained, 5=well-trained)")
    
    # Social Preferences
    good_with_dogs: bool = Field(..., description="Gets along well with other dogs")
    good_with_kids: bool = Field(..., description="Gets along well with children")
    good_with_cats: bool = Field(..., description="Gets along well with cats")
    
    # Location & Availability
    location: str = Field(..., description="Location (city, neighborhood)")
    available_times: List[str] = Field(default=[], description="Preferred play times")
    
    # Profile Details
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the dog")
    images: List[str] = Field(default=[], description="List of image URLs")

# Dog Matching Request
class DogMatchRequest(BaseModel):
    dog_profile: DogProfile
    max_distance: float = Field(default=10.0, ge=0, le=100, description="Max distance in miles")
    preferred_size: Optional[str] = Field(None, description="Preferred size for matches")
    min_compatibility_score: float = Field(default=0.5, ge=0, le=1.0, description="Minimum compatibility score")

# Compatibility Score Response
class CompatibilityResponse(BaseModel):
    dog_id: str
    dog_name: str
    compatibility_score: float = Field(..., ge=0, le=1.0)
    score_breakdown: dict
    distance_miles: float
    match_reasons: List[str]
    prediction_time: datetime

# Swipe Action Schema
class SwipeAction(BaseModel):
    user_dog_id: str = Field(..., description="ID of the swiping dog")
    target_dog_id: str = Field(..., description="ID of the dog being swiped on")
    action: str = Field(..., description="Swipe action (like, pass)")
    timestamp: datetime = Field(default_factory=datetime.now)

# Match Result (when both dogs like each other)
class MatchResult(BaseModel):
    match_id: str
    dog1_id: str
    dog2_id: str
    match_timestamp: datetime
    compatibility_score: float
    suggested_activities: List[str]

# Batch Match Request
class BatchMatchRequest(BaseModel):
    profiles: List[DogProfile] = Field(..., min_items=1, max_items=10)
    criteria: DogMatchRequest