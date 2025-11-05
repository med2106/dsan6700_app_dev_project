from datetime import datetime
from typing import List
import uuid
import random
from .schemas import (
    DogProfile, DogMatchRequest, CompatibilityResponse, 
    SwipeAction
)

# Load compatibility model (for now we'll create a mock model)
# TODO: Replace with actual trained dog compatibility model
MODEL_PATH = "models/trained/dog_compatibility_model.pkl"
PREPROCESSOR_PATH = "models/trained/dog_preprocessor.pkl"

# Mock database for demonstration
MOCK_DOG_DATABASE = []
MATCH_HISTORY = {}  # Track likes/passes between dogs

def calculate_compatibility(request: DogMatchRequest) -> CompatibilityResponse:
    """
    Calculate compatibility score between the input dog profile and potential matches.
    Uses ML-based scoring considering behavioral traits, physical characteristics, and preferences.
    """
    dog = request.dog_profile
    
    # Generate a mock target dog for demonstration
    target_dog = _generate_mock_target_dog()
    
    # Calculate compatibility components
    behavioral_score = _calculate_behavioral_compatibility(dog, target_dog)
    physical_score = _calculate_physical_compatibility(dog, target_dog)
    social_score = _calculate_social_compatibility(dog, target_dog)
    location_score = _calculate_location_compatibility(dog, target_dog)
    
    # Weighted overall compatibility score
    weights = {
        'behavioral': 0.4,
        'physical': 0.25,
        'social': 0.25,
        'location': 0.1
    }
    
    overall_score = (
        behavioral_score * weights['behavioral'] +
        physical_score * weights['physical'] +
        social_score * weights['social'] +
        location_score * weights['location']
    )
    
    # Generate match reasons
    match_reasons = _generate_match_reasons(
        behavioral_score, physical_score, social_score, location_score
    )
    
    return CompatibilityResponse(
        dog_id=target_dog['id'],
        dog_name=target_dog['name'],
        compatibility_score=round(overall_score, 3),
        score_breakdown={
            'behavioral': round(behavioral_score, 3),
            'physical': round(physical_score, 3),
            'social': round(social_score, 3),
            'location': round(location_score, 3),
            'overall': round(overall_score, 3)
        },
        distance_miles=round(random.uniform(0.5, request.max_distance), 1),
        match_reasons=match_reasons,
        prediction_time=datetime.now()
    )

def find_matches(request: DogMatchRequest) -> List[CompatibilityResponse]:
    """
    Find multiple compatible dog matches based on the request criteria.
    """
    matches = []
    num_matches = random.randint(3, 8)  # Generate 3-8 potential matches
    
    for _ in range(num_matches):
        compatibility = calculate_compatibility(request)
        
        # Only include matches above minimum compatibility score
        if compatibility.compatibility_score >= request.min_compatibility_score:
            matches.append(compatibility)
    
    # Sort by compatibility score (highest first)
    matches.sort(key=lambda x: x.compatibility_score, reverse=True)
    
    return matches

def process_swipe(swipe: SwipeAction) -> dict:
    """
    Process a swipe action (like or pass) and check for mutual matches.
    """
    # Record the swipe in match history
    swipe_key = f"{swipe.user_dog_id}_{swipe.target_dog_id}"
    reverse_swipe_key = f"{swipe.target_dog_id}_{swipe.user_dog_id}"
    
    MATCH_HISTORY[swipe_key] = {
        'action': swipe.action,
        'timestamp': swipe.timestamp
    }
    
    result = {
        'swipe_recorded': True,
        'action': swipe.action,
        'match_created': False
    }
    
    # Check if this creates a mutual match (both dogs liked each other)
    if (swipe.action == 'like' and 
        reverse_swipe_key in MATCH_HISTORY and 
        MATCH_HISTORY[reverse_swipe_key]['action'] == 'like'):
        
        # Create a match!
        match_id = str(uuid.uuid4())
        result.update({
            'match_created': True,
            'match_id': match_id,
            'message': "It's a match! 🐕💕🐕"
        })
    
    return result

def _generate_mock_target_dog() -> dict:
    """Generate a mock target dog for demonstration purposes."""
    breeds = ['Labrador', 'Golden Retriever', 'German Shepherd', 'Beagle', 'Bulldog', 'Poodle', 'Mixed Breed']
    sizes = ['small', 'medium', 'large', 'giant']
    locations = ['Downtown', 'Suburbs', 'Uptown', 'Riverside', 'Park District']
    
    return {
        'id': str(uuid.uuid4()),
        'name': random.choice(['Buddy', 'Luna', 'Charlie', 'Bella', 'Max', 'Daisy', 'Cooper']),
        'breed': random.choice(breeds),
        'age': random.randint(1, 12),
        'size': random.choice(sizes),
        'weight': random.uniform(10, 150),
        'energy_level': random.randint(1, 5),
        'friendliness': random.randint(1, 5),
        'playfulness': random.randint(1, 5),
        'training_level': random.randint(1, 5),
        'good_with_dogs': random.choice([True, False]),
        'good_with_kids': random.choice([True, False]),
        'good_with_cats': random.choice([True, False]),
        'location': random.choice(locations)
    }

def _calculate_behavioral_compatibility(dog1: DogProfile, dog2: dict) -> float:
    """Calculate behavioral compatibility score between two dogs."""
    # Energy level compatibility (closer levels are better)
    energy_diff = abs(dog1.energy_level - dog2['energy_level'])
    energy_score = max(0, (5 - energy_diff) / 5)
    
    # Playfulness compatibility
    play_diff = abs(dog1.playfulness - dog2['playfulness'])
    play_score = max(0, (5 - play_diff) / 5)
    
    # Training level (well-trained dogs often get along better)
    training_score = (dog1.training_level + dog2['training_level']) / 10
    
    return (energy_score + play_score + training_score) / 3

def _calculate_physical_compatibility(dog1: DogProfile, dog2: dict) -> float:
    """Calculate physical compatibility based on size and age."""
    # Size compatibility (similar sizes often play better together)
    size_map = {'small': 1, 'medium': 2, 'large': 3, 'giant': 4}
    size1 = size_map.get(dog1.size, 2)
    size2 = size_map.get(dog2['size'], 2)
    size_diff = abs(size1 - size2)
    size_score = max(0, (4 - size_diff) / 4)
    
    # Age compatibility (similar ages often have similar energy)
    age_diff = abs(dog1.age - dog2['age'])
    age_score = max(0, (10 - age_diff) / 10)
    
    return (size_score + age_score) / 2

def _calculate_social_compatibility(dog1: DogProfile, dog2: dict) -> float:
    """Calculate social compatibility based on social preferences."""
    # Both must be good with dogs for high compatibility
    if not (dog1.good_with_dogs and dog2['good_with_dogs']):
        return 0.3  # Low but not zero compatibility
    
    # Friendliness levels
    friendliness_avg = (dog1.friendliness + dog2['friendliness']) / 10
    
    return min(1.0, friendliness_avg + 0.3)  # Bonus for being good with dogs

def _calculate_location_compatibility(dog1: DogProfile, dog2: dict) -> float:
    """Calculate location-based compatibility (mock implementation)."""
    # For demonstration, assume random compatibility based on location
    # In a real system, this would use geographic distance calculation
    return random.uniform(0.6, 1.0)

def _generate_match_reasons(behavioral: float, physical: float, social: float, location: float) -> List[str]:
    """Generate human-readable match reasons based on compatibility scores."""
    reasons = []
    
    if behavioral > 0.7:
        reasons.append("Similar energy and playfulness levels")
    if physical > 0.7:
        reasons.append("Compatible sizes for safe play")
    if social > 0.8:
        reasons.append("Both are very social and dog-friendly")
    if location > 0.8:
        reasons.append("Great location match for easy meetups")
    
    # Always have at least one reason
    if not reasons:
        reasons.append("Good overall compatibility match")
    
    return reasons
