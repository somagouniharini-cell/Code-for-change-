import re

class DataPreprocessor:
    """
    Cleans and standardizes raw input from the frontend 
    before it reaches the calculation services.
    """
    
    @staticmethod
    def clean_floor_input(floor_str):
        """Converts formats like 'g + 2', '3', 'Ground+1' into standard 'G+X'."""
        s = str(floor_str).upper().replace(" ", "")
        
        # If it's just a number like "3", convert to "G+2"
        if s.isdigit():
            val = int(s)
            return f"G+{val-1}" if val > 0 else "G+0"
        
        # Ensure it starts with G
        if not s.startswith("G"):
            s = "G+" + s.lstrip("+")
            
        return s

    @staticmethod
    def validate_area(area):
        """Ensures the area is within realistic bounds for the AI model."""
        try:
            val = float(area)
            if val < 50: return 50 # Minimum plot size
            if val > 10000: return 10000 # Model limit
            return val
        except ValueError:
            return 100.0