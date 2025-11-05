from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .inference import calculate_compatibility, find_matches, process_swipe
from .schemas import (
    DogProfile, DogMatchRequest, CompatibilityResponse, 
    SwipeAction, MatchResult, BatchMatchRequest
)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Anything's Pawsible - Dog Dating API",
    description=(
        "ML-powered dog dating API that helps dogs find their perfect playmates. "
        "Features compatibility scoring, intelligent matching, and swipe-based interactions. "
        "Built with modern MLOps practices including advanced filtering and recommendation systems."
    ),
    version="1.0.0",
    contact={
        "name": "Trevor Adriaanse",
        "url": "https://github.com/trevoradriaanse",
        "email": "tva7@georgetown.edu",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    return {
        "status": "healthy", 
        "model_loaded": True,
        "service": "Anything's Pawsible Dog Dating API",
        "version": "1.0.0"
    }


# Main compatibility scoring endpoint
@app.post("/compatibility", response_model=CompatibilityResponse)
async def get_compatibility(request: DogMatchRequest):
    """Calculate compatibility score between two dogs"""
    try:
        result = calculate_compatibility(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compatibility calculation failed: {str(e)}")


# Find potential matches endpoint
@app.post("/matches", response_model=List[CompatibilityResponse])
async def find_dog_matches(request: DogMatchRequest):
    """Find compatible dog matches based on profile and preferences"""
    try:
        matches = find_matches(request)
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match finding failed: {str(e)}")


# Swipe action endpoint
@app.post("/swipe", response_model=dict)
async def handle_swipe(swipe: SwipeAction):
    """Process a swipe action (like or pass)"""
    try:
        result = process_swipe(swipe)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Swipe processing failed: {str(e)}")


# Create dog profile endpoint
@app.post("/profile", response_model=dict)
async def create_dog_profile(profile: DogProfile):
    """Create a new dog profile"""
    try:
        # TODO: Implement profile storage (database, etc.)
        return {
            "message": "Profile created successfully",
            "dog_name": profile.name,
            "profile_id": f"dog_{profile.name.lower().replace(' ', '_')}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile creation failed: {str(e)}")


# Batch compatibility endpoint
@app.post("/batch-compatibility", response_model=List[CompatibilityResponse])
async def batch_compatibility(request: BatchMatchRequest):
    """Calculate compatibility scores for multiple dog profiles"""
    try:
        results = []
        for profile in request.profiles:
            match_request = DogMatchRequest(
                dog_profile=profile,
                max_distance=request.criteria.max_distance,
                preferred_size=request.criteria.preferred_size,
                min_compatibility_score=request.criteria.min_compatibility_score
            )
            compatibility = calculate_compatibility(match_request)
            results.append(compatibility)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch compatibility failed: {str(e)}")
