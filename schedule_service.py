import math

class ScheduleService:
    def generate_schedule(self, built_up_area, floors, user_days=None):
        """
        Generates a week-by-week construction schedule.
        """
        # 1. Calculate Duration
        if user_days:
            duration_days = user_days
        else:
            # Heuristic: 1 day per 10 sq yards + 30 days per floor?
            # Simplified: Base 60 days + 30 days per floor
            num_floors = 1
            if isinstance(floors, str) and "G+" in floors.upper():
                try:
                    num_floors = int(floors.upper().split('+')[1]) + 1
                except:
                    pass
            duration_days = 60 + (num_floors * 24) # e.g. G+2 = 60 + 72 = 132 days

        duration_weeks = math.ceil(duration_days / 7)
        duration_months = round(duration_days / 30, 1)

        # 2. Define Phases and allocate weeks
        # We assume standard phases and distribute weeks proportionally
        
        phases = [
            {"name": "Site Preparation", "weight": 0.10, "activities": ["Site Cleaning", "Soil Testing", "Marking"]},
            {"name": "Foundation Work", "weight": 0.20, "activities": ["Excavation", "PCC Bedding", "Footing Concrete"]},
            {"name": "Structure Development", "weight": 0.30, "activities": ["Column Raising", "Slab Casting", "Staircase"]},
            {"name": "Brickwork & Plastering", "weight": 0.20, "activities": ["Wall Construction", "Internal Plastering", "External Plastering"]},
            {"name": "Finishing", "weight": 0.20, "activities": ["Flooring", "Painting", "Electrical & Plumbing", "Final Cleanup"]}
        ]

        construction_schedule = []
        current_week = 1
        
        for phase in phases:
            phase_duration_weeks = max(1, math.floor(duration_weeks * phase["weight"]))
            
            # Add entry for this phase
            # If a phase takes multiple weeks, we might list it once or expand it.
            # Here we just map the start week.
            
            construction_schedule.append({
                "week_number": current_week,
                "phase_name": phase["name"],
                "activities": phase["activities"]
            })
            
            current_week += phase_duration_weeks

        return {
            "duration_days": duration_days,
            "duration_weeks": duration_weeks,
            "duration_months": duration_months,
            "schedule": construction_schedule
        }