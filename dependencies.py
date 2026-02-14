import requests
import json
import math
from config import Config

class ConstructionCalculator:
    def __init__(self, built_up_area, floors_str, custom_days=None, custom_workers=None, daily_wage=None, cost_per_sq_yard=None):
        self.area = float(built_up_area)
        self.floors = self._parse_floors(floors_str)
        self.total_construction_area = self.area * self.floors
        
        # Use custom values if provided, else defaults from Config
        self.daily_wage = float(daily_wage) if daily_wage else Config.DEFAULT_DAILY_WAGE
        self.base_cost_sq_yard = float(cost_per_sq_yard) if cost_per_sq_yard else Config.DEFAULT_COST_PER_SQ_YARD
        
        # Auto-calculate timeline if not provided (approx 10 days per 100 sq yards per floor)
        calculated_days = math.ceil((self.total_construction_area / 100) * 10)
        self.days = int(custom_days) if custom_days else max(60, calculated_days) # Minimum 60 days
        
        # Auto-calculate workers if not provided
        # Rough logic: Total Man Days needed / Desired Days
        total_man_days_needed = (self.total_construction_area * 1.5) # Factor for labor intensity
        self.workers = int(custom_workers) if custom_workers else max(5, math.ceil(total_man_days_needed / self.days))

    def _parse_floors(self, floors_str):
        """Parses 'G+2' to integer 3, or '2' to integer 2."""
        s = str(floors_str).upper().strip()
        if "G+" in s:
            try:
                add = int(s.split('+')[1])
                return add + 1 # G(1) + 2 = 3 floors
            except:
                return 1
        try:
            return int(s)
        except:
            return 1

    def calculate_materials(self):
        """Calculates material quantities based on thumb rules."""
        return {
            "steel_tons": round((self.total_construction_area * Config.QTY_STEEL_PER_SQ_YARD) / 1000, 2),
            "cement_bags": round(self.total_construction_area * Config.QTY_CEMENT_PER_SQ_YARD),
            "sand_tons": round(self.total_construction_area * Config.QTY_SAND_PER_SQ_YARD, 2),
            "water_liters": round(self.total_construction_area * Config.QTY_WATER_PER_SQ_YARD)
        }

    def calculate_costs(self, materials):
        """Calculates detailed cost breakdown."""
        # Material Costs
        steel_cost = materials['steel_tons'] * Config.RATE_STEEL_PER_TON
        cement_cost = materials['cement_bags'] * Config.RATE_CEMENT_PER_BAG
        sand_cost = materials['sand_tons'] * Config.RATE_SAND_PER_TON
        
        # Estimate other material costs (bricks, paint, wood) as a factor of base structure
        other_material_cost = (steel_cost + cement_cost + sand_cost) * 0.5
        total_material_cost = steel_cost + cement_cost + sand_cost + other_material_cost

        # Labor Cost
        total_labor_days = self.days * self.workers
        labor_cost = total_labor_days * self.daily_wage

        # Overhead
        overhead_cost = (total_material_cost + labor_cost) * (Config.DEFAULT_OVERHEAD_PERCENTAGE / 100)
        
        total_project_cost = total_material_cost + labor_cost + overhead_cost

        return {
            "material_cost": round(total_material_cost),
            "labor_cost": round(labor_cost),
            "overhead_cost": round(overhead_cost),
            "total_cost": round(total_project_cost),
            "cost_breakdown": {
                "steel": round(steel_cost),
                "cement": round(cement_cost),
                "sand": round(sand_cost),
                "others": round(other_material_cost)
            }
        }

    def get_worker_distribution(self):
        """Scenario 1: Worker requirements breakdown."""
        # Rough distribution percentages
        return {
            "total": self.workers,
            "masons": max(1, round(self.workers * 0.30)),
            "helpers": max(2, round(self.workers * 0.40)),
            "steel_workers": max(1, round(self.workers * 0.10)),
            "carpenters": max(1, round(self.workers * 0.15)),
            "supervisors": max(1, round(self.workers * 0.05))
        }

    def generate_schedule(self):
        """Scenario 4: Weekly construction schedule."""
        # Divide total days into phases
        schedule = []
        phase_ratios = {
            "Site Preparation": 0.05,
            "Foundation Work": 0.15,
            "Structure (Columns/Beams)": 0.25,
            "Brickwork & Plastering": 0.25,
            "Flooring & Electrical": 0.15,
            "Finishing & Painting": 0.15
        }
        
        current_day = 1
        for phase, ratio in phase_ratios.items():
            duration = max(1, round(self.days * ratio))
            start_week = math.ceil(current_day / 7)
            end_week = math.ceil((current_day + duration) / 7)
            
            schedule.append({
                "phase": phase,
                "duration_days": duration,
                "weeks": f"Week {start_week} - Week {end_week}",
                "description": f"Execution of {phase} for {self.floors} floors."
            })
            current_day += duration
            
        return schedule

    def generate_blueprint_data(self):
        """Generates room dimensions for frontend visualization."""
        # Simple logic to divide area into standard rooms based on typical ratios
        # Assuming area is per floor
        floor_area_sqft = self.area * 9 # Convert sq yards to sq ft
        
        # Scale down slightly for walls/corridors
        usable_area = floor_area_sqft * 0.85
        
        return {
            "floors": self.floors,
            "layout": [
                {"room": "Master Bedroom", "area_sqft": round(usable_area * 0.20), "dim": "14x16 approx"},
                {"room": "Bedroom 2", "area_sqft": round(usable_area * 0.15), "dim": "12x14 approx"},
                {"room": "Living Hall", "area_sqft": round(usable_area * 0.30), "dim": "20x22 approx"},
                {"room": "Kitchen", "area_sqft": round(usable_area * 0.15), "dim": "12x12 approx"},
                {"room": "Bathrooms (2)", "area_sqft": round(usable_area * 0.10), "dim": "8x6 each"},
                {"room": "Balcony", "area_sqft": round(usable_area * 0.10), "dim": "Variety"}
            ]
        }

class AIPlanner:
    @staticmethod
    def get_analysis(project_data):
        """Interacts with local Ollama instance (Granite 3.3 2B)."""
        prompt = (
            f"Act as a senior construction engineer. Analyze a project with these details: "
            f"Area: {project_data['area']} sq yards, Floors: {project_data['floors']}, "
            f"Timeline: {project_data['days']} days. "
            f"Provide a brief 3-point summary of risks and 3 recommendations for optimization."
        )

        payload = {
            "model": Config.MODEL_ID,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(Config.OLLAMA_API_URL, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', 'Analysis complete.')
            return f"AI Service Error: {response.text}"
        except Exception as e:
            return "AI Analysis unavailable (Ollama may not be running)."