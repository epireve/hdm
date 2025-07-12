#!/usr/bin/env python3
"""
KiloCode Models API Interface
Fetch and manage available models from KiloCode API
"""

import os
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime

# Load environment variables manually
def load_env_file(env_path=".env"):
    """Simple .env file loader"""
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    except FileNotFoundError:
        pass
    
    # Set environment variables
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value

class KiloCodeModels:
    """Interface for KiloCode models API"""
    
    def __init__(self, env_file: str = "/Users/invoture/dev.local/hdm/.env"):
        load_env_file(env_file)
        
        self.token = os.getenv("KILOCODE_TOKEN")
        self.base_url = os.getenv("KILOCODE_BASE_URL", "https://kilocode.ai")
        self.models_url = f"{self.base_url}/api/openrouter/models"
        
        if not self.token:
            raise ValueError("KILOCODE_TOKEN not found in environment variables")
    
    def fetch_models(self) -> Optional[List[Dict]]:
        """Fetch available models from KiloCode API"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://kilocode.ai",
            "X-Title": "HDM Model Manager"
        }
        
        try:
            response = requests.get(self.models_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Failed to fetch models: {e}")
            return None
    
    def get_gemini_models(self) -> List[Dict]:
        """Get all available Gemini models"""
        models = self.fetch_models()
        if not models:
            return []
        
        gemini_models = [
            model for model in models 
            if "gemini" in model.get("id", "").lower()
        ]
        
        return sorted(gemini_models, key=lambda x: x.get("id", ""))
    
    def get_recommended_models(self) -> Dict[str, List[Dict]]:
        """Get recommended models by category"""
        models = self.fetch_models()
        if not models:
            return {}
        
        recommendations = {
            "fast_processing": [],
            "high_quality": [],
            "cost_effective": [],
            "large_context": []
        }
        
        for model in models:
            model_id = model.get("id", "").lower()
            context_length = model.get("context_length", 0)
            
            # Fast processing models
            if "flash" in model_id or "mini" in model_id:
                recommendations["fast_processing"].append(model)
            
            # High quality models  
            if "pro" in model_id or "plus" in model_id:
                recommendations["high_quality"].append(model)
            
            # Large context models
            if context_length > 100000:
                recommendations["large_context"].append(model)
            
            # Cost effective (basic heuristic)
            if "gemini" in model_id and ("flash" in model_id or "mini" in model_id):
                recommendations["cost_effective"].append(model)
        
        # Sort each category
        for category in recommendations:
            recommendations[category] = sorted(
                recommendations[category], 
                key=lambda x: x.get("id", "")
            )
        
        return recommendations
    
    def save_models_cache(self, filename: str = "kilocode_models_cache.json"):
        """Save models to cache file"""
        models = self.fetch_models()
        if models:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "models": models,
                "total_models": len(models)
            }
            
            with open(filename, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            print(f"✅ Saved {len(models)} models to {filename}")
            return True
        
        return False
    
    def print_model_summary(self):
        """Print a summary of available models"""
        models = self.fetch_models()
        if not models:
            print("❌ Unable to fetch models")
            return
        
        print(f"📊 KiloCode Models Summary")
        print(f"   Total models: {len(models)}")
        print()
        
        # Group by provider
        providers = {}
        for model in models:
            model_id = model.get("id", "")
            provider = model_id.split("/")[0] if "/" in model_id else "unknown"
            
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(model)
        
        print("📋 By Provider:")
        for provider, provider_models in sorted(providers.items()):
            print(f"   {provider}: {len(provider_models)} models")
        
        print()
        
        # Gemini models detail
        gemini_models = self.get_gemini_models()
        if gemini_models:
            print("🤖 Gemini Models:")
            for model in gemini_models:
                context_length = model.get("context_length", 0)
                context_str = f"{context_length:,}" if context_length else "Unknown"
                print(f"   {model.get('id', 'Unknown'):<40} | Context: {context_str}")
        
        print()
        
        # Recommendations
        recommendations = self.get_recommended_models()
        print("💡 Recommendations for Paper Processing:")
        
        if recommendations["fast_processing"]:
            print("   ⚡ Fast Processing:")
            for model in recommendations["fast_processing"][:3]:
                print(f"     - {model.get('id', 'Unknown')}")
        
        if recommendations["large_context"]:
            print("   📖 Large Context (>100k tokens):")
            for model in recommendations["large_context"][:3]:
                context = model.get("context_length", 0)
                print(f"     - {model.get('id', 'Unknown')} ({context:,} tokens)")

def main():
    """Main function for testing"""
    try:
        models_api = KiloCodeModels()
        models_api.print_model_summary()
        models_api.save_models_cache()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()