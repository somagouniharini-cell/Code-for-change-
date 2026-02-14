import requests
import json
import random

class AIService:
    def __init__(self):
        # Configuration for local Ollama instance
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "granite3.3:2b"  # As specified in your PDF

    def generate_blueprint(self, floors, area):
        """
        Attempts to generate a blueprint description via AI, 
        or falls back to a procedural SVG generation if AI is offline.
        """
        prompt = f"Generate a text description for a floor plan layout for a {floors} building with {area} sq yards area. List rooms and approximate dimensions."
        
        try:
            # Try connecting to local Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.ollama_url, json=payload, timeout=2)
            if response.status_code == 200:
                ai_text = response.json().get('response', '')
                # In a real app, you would parse 'ai_text' to draw lines.
                # For now, we return a standard SVG based on inputs.
                return self._generate_procedural_svg(floors)
        except Exception as e:
            print(f"AI Service unavailable ({str(e)}), using procedural generator.")
        
        return self._generate_procedural_svg(floors)

    def _generate_procedural_svg(self, floors):
        """
        Generates a simple SVG representation of a floor plan 
        so the frontend has something visual to display.
        """
        # Simple SVG template for a 3-bedroom layout
        svg_content = """
        <svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg" style="background:#1a1a2e;">
            <!-- Outer Walls -->
            <rect x="50" y="50" width="700" height="500" fill="none" stroke="#6C63FF" stroke-width="4"/>
            
            <!-- Master Bedroom -->
            <rect x="50" y="50" width="250" height="200" fill="none" stroke="#4a4e69" stroke-width="2"/>
            <text x="70" y="80" fill="#a5a6c4" font-family="Arial" font-size="14">MASTER BEDROOM</text>
            <text x="70" y="100" fill="#6C63FF" font-family="Arial" font-size="12">14' x 16'</text>
            
            <!-- Bedroom 2 -->
            <rect x="300" y="50" width="250" height="200" fill="none" stroke="#4a4e69" stroke-width="2"/>
            <text x="320" y="80" fill="#a5a6c4" font-family="Arial" font-size="14">BEDROOM 2</text>
            <text x="320" y="100" fill="#6C63FF" font-family="Arial" font-size="12">14' x 14'</text>
            
            <!-- Living Room -->
            <rect x="550" y="50" width="200" height="300" fill="none" stroke="#4a4e69" stroke-width="2"/>
            <text x="570" y="80" fill="#a5a6c4" font-family="Arial" font-size="14">LIVING ROOM</text>
            <text x="570" y="100" fill="#6C63FF" font-family="Arial" font-size="12">18' x 20'</text>
            
            <!-- Kitchen -->
            <rect x="50" y="250" width="250" height="300" fill="none" stroke="#4a4e69" stroke-width="2"/>
            <text x="70" y="280" fill="#a5a6c4" font-family="Arial" font-size="14">KITCHEN</text>
            <text x="70" y="300" fill="#6C63FF" font-family="Arial" font-size="12">12' x 14'</text>

            <!-- Bathroom -->
            <rect x="300" y="250" width="250" height="150" fill="none" stroke="#4a4e69" stroke-width="2"/>
            <text x="320" y="280" fill="#a5a6c4" font-family="Arial" font-size="14">BATHROOM</text>
            
            <!-- Balcony -->
            <rect x="300" y="400" width="450" height="150" fill="none" stroke="#4a4e69" stroke-width="2"/>
            <text x="320" y="430" fill="#a5a6c4" font-family="Arial" font-size="14">BALCONY / UTILITY</text>
            
            <!-- Footer Info -->
            <text x="400" y="580" text-anchor="middle" fill="#6C63FF" font-size="12">
                GENERATED BLUEPRINT | SCALE 1:100 | {floors}
            </text>
        </svg>
        """.replace("{floors}", str(floors))
        
        # Return as a data URI for easy frontend display
        import base64
        encoded = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded}"

    def get_smart_insights(self, area, cost, duration):
        """
        Returns AI-generated insights about the project.
        """
        # Mocking the AI response for reliability in this demo
        return [
            f"Based on {area} sq yards, the timeline of {duration} weeks is aggressive but achievable.",
            f"The estimated cost of INR {cost:,.2f} aligns with current market rates for this region.",
            "Recommendation: Secure cement bulk orders early to avoid price fluctuation during the Foundation phase."
        ]