from pycorex.gemini_client import GeminiClient

def generate_image(prompt: str) -> list[str]:
    results: list[str] = []
    # GeminiClient
    return results

def get_models():
    return GeminiClient.GeminiModel

def get_resolutions():
    return GeminiClient.ImageSize

def get_aspects():
    return GeminiClient.AspectRatio

def get_safety_filters():
    return GeminiClient.HarmCategory

def get_safety_levels():
    return GeminiClient.SafetyFilterLevel
