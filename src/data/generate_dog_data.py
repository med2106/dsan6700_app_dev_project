#!/usr/bin/env python3
"""
Generate synthetic dog profile data for training compatibility models.
This script creates realistic dog profiles with personality traits, demographics,
and compatibility scores for ML model training.
"""

import pandas as pd
import numpy as np
import random
import argparse
from typing import List, Dict, Tuple
import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Dog breed data with typical characteristics
BREED_CHARACTERISTICS = {
    "Golden Retriever": {"energy": 7, "friendliness": 9, "size": "Large", "training": 8},
    "Labrador Retriever": {"energy": 8, "friendliness": 9, "size": "Large", "training": 8},
    "German Shepherd": {"energy": 8, "friendliness": 6, "size": "Large", "training": 9},
    "Bulldog": {"energy": 3, "friendliness": 7, "size": "Medium", "training": 4},
    "Poodle": {"energy": 6, "friendliness": 7, "size": "Medium", "training": 9},
    "Beagle": {"energy": 7, "friendliness": 8, "size": "Medium", "training": 6},
    "Border Collie": {"energy": 10, "friendliness": 7, "size": "Medium", "training": 10},
    "French Bulldog": {"energy": 4, "friendliness": 8, "size": "Small", "training": 5},
    "Siberian Husky": {"energy": 10, "friendliness": 6, "size": "Large", "training": 6},
    "Yorkshire Terrier": {"energy": 6, "friendliness": 5, "size": "Small", "training": 5},
    "Dachshund": {"energy": 5, "friendliness": 6, "size": "Small", "training": 4},
    "Mixed Breed": {"energy": 6, "friendliness": 7, "size": "Medium", "training": 6},
}

LOCATIONS = [
    "San Francisco, CA", "Oakland, CA", "Berkeley, CA", "San Jose, CA",
    "New York, NY", "Brooklyn, NY", "Manhattan, NY", "Queens, NY",
    "Los Angeles, CA", "Santa Monica, CA", "Beverly Hills, CA", "Pasadena, CA",
    "Seattle, WA", "Portland, OR", "Austin, TX", "Denver, CO",
    "Chicago, IL", "Boston, MA", "Miami, FL", "Atlanta, GA"
]

ACTIVITIES = [
    "Fetch", "Swimming", "Hiking", "Running", "Tug of War", 
    "Frisbee", "Agility", "Walks", "Dog Parks", "Beach Days",
    "Camping", "Jogging", "Socializing", "Training", "Playing"
]

DOG_NAMES = [
    "Buddy", "Luna", "Charlie", "Bella", "Max", "Lucy", "Cooper", "Daisy",
    "Rocky", "Molly", "Bear", "Stella", "Tucker", "Zoe", "Duke", "Lola",
    "Milo", "Ruby", "Jack", "Penny", "Teddy", "Chloe", "Oliver", "Nala",
    "Leo", "Rosie", "Zeus", "Maya", "Finn", "Sadie", "Oscar", "Coco"
]


def generate_dog_profile(dog_id: int) -> Dict:
    """Generate a single realistic dog profile with characteristics."""
    breed = random.choice(list(BREED_CHARACTERISTICS.keys()))
    breed_traits = BREED_CHARACTERISTICS[breed]
    
    # Add some variance to breed characteristics
    energy_base = breed_traits["energy"]
    energy_level = max(1, min(10, energy_base + random.randint(-2, 2)))
    
    friendliness_base = breed_traits["friendliness"] 
    friendliness = max(1, min(10, friendliness_base + random.randint(-2, 2)))
    
    training_base = breed_traits["training"]
    training_level = max(1, min(10, training_base + random.randint(-2, 2)))
    
    # Generate other attributes
    age = random.randint(1, 15)
    playfulness = max(1, min(10, energy_level + random.randint(-3, 3)))
    
    # Size consistency
    if breed_traits["size"] == "Small":
        weight = random.randint(5, 25)
    elif breed_traits["size"] == "Medium":
        weight = random.randint(25, 60)
    else:  # Large
        weight = random.randint(60, 120)
        
    profile = {
        "dog_id": dog_id,
        "name": random.choice(DOG_NAMES),
        "breed": breed,
        "age": age,
        "weight": weight,
        "size": breed_traits["size"],
        "gender": random.choice(["Male", "Female"]),
        "energy_level": energy_level,
        "friendliness": friendliness,
        "playfulness": playfulness,
        "training_level": training_level,
        "location": random.choice(LOCATIONS),
        "favorite_activities": random.sample(ACTIVITIES, random.randint(3, 6)),
        "is_neutered": random.choice([True, False]),
        "good_with_kids": random.choice([True, False, True]),  # Bias toward True
        "good_with_dogs": random.choice([True, False, True, True]),  # Bias toward True
        "vaccination_status": random.choice(["Up to date", "Needs update", "Up to date", "Up to date"]),
    }
    
    return profile


def calculate_compatibility_score(dog1: Dict, dog2: Dict) -> float:
    """
    Calculate compatibility score between two dogs based on multiple factors.
    Returns a score between 0-100.
    """
    score = 0.0
    
    # Energy level compatibility (30% weight)
    energy_diff = abs(dog1["energy_level"] - dog2["energy_level"])
    energy_score = max(0, 100 - (energy_diff * 15))  # Penalize large differences
    score += energy_score * 0.30
    
    # Size compatibility (20% weight)
    sizes = {"Small": 1, "Medium": 2, "Large": 3}
    size_diff = abs(sizes[dog1["size"]] - sizes[dog2["size"]])
    size_score = max(0, 100 - (size_diff * 25))
    score += size_score * 0.20
    
    # Friendliness bonus (15% weight)
    friendliness_avg = (dog1["friendliness"] + dog2["friendliness"]) / 2
    friendliness_score = friendliness_avg * 10
    score += friendliness_score * 0.15
    
    # Age compatibility (10% weight)
    age_diff = abs(dog1["age"] - dog2["age"])
    age_score = max(0, 100 - (age_diff * 8))
    score += age_score * 0.10
    
    # Activity overlap (15% weight)
    common_activities = len(set(dog1["favorite_activities"]) & set(dog2["favorite_activities"]))
    activity_score = min(100, common_activities * 20)
    score += activity_score * 0.15
    
    # Location proximity (10% weight) - simplified by state
    dog1_state = dog1["location"].split(", ")[-1]
    dog2_state = dog2["location"].split(", ")[-1]
    location_score = 100 if dog1_state == dog2_state else 50
    score += location_score * 0.10
    
    # Bonus factors
    if dog1["good_with_dogs"] and dog2["good_with_dogs"]:
        score += 5
    
    if dog1["vaccination_status"] == "Up to date" and dog2["vaccination_status"] == "Up to date":
        score += 5
        
    # Add some randomness for realism
    score += random.uniform(-5, 5)
    
    return max(0, min(100, score))


def generate_compatibility_pairs(profiles: List[Dict], num_pairs: int) -> List[Dict]:
    """Generate pairs of dogs with compatibility scores."""
    pairs = []
    
    for _ in range(num_pairs):
        dog1, dog2 = random.sample(profiles, 2)
        compatibility = calculate_compatibility_score(dog1, dog2)
        
        # Create feature vector for ML training
        pair_features = {
            # Dog 1 features
            "dog1_id": dog1["dog_id"],
            "dog1_energy": dog1["energy_level"],
            "dog1_friendliness": dog1["friendliness"],
            "dog1_playfulness": dog1["playfulness"],
            "dog1_age": dog1["age"],
            "dog1_weight": dog1["weight"],
            "dog1_training": dog1["training_level"],
            
            # Dog 2 features  
            "dog2_id": dog2["dog_id"],
            "dog2_energy": dog2["energy_level"],
            "dog2_friendliness": dog2["friendliness"],
            "dog2_playfulness": dog2["playfulness"],
            "dog2_age": dog2["age"],
            "dog2_weight": dog2["weight"],
            "dog2_training": dog2["training_level"],
            
            # Derived features
            "energy_diff": abs(dog1["energy_level"] - dog2["energy_level"]),
            "age_diff": abs(dog1["age"] - dog2["age"]),
            "weight_diff": abs(dog1["weight"] - dog2["weight"]),
            "size_match": 1 if dog1["size"] == dog2["size"] else 0,
            "same_location": 1 if dog1["location"].split(", ")[-1] == dog2["location"].split(", ")[-1] else 0,
            "activity_overlap": len(set(dog1["favorite_activities"]) & set(dog2["favorite_activities"])),
            "both_good_with_dogs": 1 if dog1["good_with_dogs"] and dog2["good_with_dogs"] else 0,
            "both_vaccinated": 1 if dog1["vaccination_status"] == "Up to date" and dog2["vaccination_status"] == "Up to date" else 0,
            
            # Target variable
            "compatibility_score": compatibility
        }
        
        pairs.append(pair_features)
    
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic dog compatibility training data")
    parser.add_argument("--num-profiles", type=int, default=1000, help="Number of dog profiles to generate")
    parser.add_argument("--num-pairs", type=int, default=5000, help="Number of compatibility pairs to generate")
    parser.add_argument("--output-profiles", type=str, default="data/raw/dog_profiles.csv", help="Output file for dog profiles")
    parser.add_argument("--output-pairs", type=str, default="data/raw/dog_compatibility_pairs.csv", help="Output file for compatibility pairs")
    
    args = parser.parse_args()
    
    logger.info(f"Generating {args.num_profiles} dog profiles...")
    
    # Generate dog profiles
    profiles = []
    for i in range(args.num_profiles):
        profile = generate_dog_profile(i)
        profiles.append(profile)
    
    # Save profiles
    profiles_df = pd.DataFrame(profiles)
    profiles_df.to_csv(args.output_profiles, index=False)
    logger.info(f"Saved {len(profiles)} dog profiles to {args.output_profiles}")
    
    # Generate compatibility pairs
    logger.info(f"Generating {args.num_pairs} compatibility pairs...")
    pairs = generate_compatibility_pairs(profiles, args.num_pairs)
    
    # Save pairs
    pairs_df = pd.DataFrame(pairs)
    pairs_df.to_csv(args.output_pairs, index=False)
    logger.info(f"Saved {len(pairs)} compatibility pairs to {args.output_pairs}")
    
    # Print statistics
    logger.info(f"Compatibility score statistics:")
    logger.info(f"  Mean: {pairs_df['compatibility_score'].mean():.2f}")
    logger.info(f"  Std: {pairs_df['compatibility_score'].std():.2f}")
    logger.info(f"  Min: {pairs_df['compatibility_score'].min():.2f}")
    logger.info(f"  Max: {pairs_df['compatibility_score'].max():.2f}")
    
    logger.info("Data generation complete!")


if __name__ == "__main__":
    main()
