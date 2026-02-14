import math

class ResourceService:
    def calculate_materials(self, built_up_area, floors):
        """
        Estimates material quantities using civil engineering thumb rules 
        adjusted to match the output examples in the PDF.
        """
        # Clean floor input (e.g., "G+2" -> 3 floors)
        num_floors = 1
        if isinstance(floors, str) and "G+" in floors.upper():
            try:
                num_floors = int(floors.upper().split('+')[1]) + 1
            except:
                num_floors = 1
        elif isinstance(floors, int):
            num_floors = floors

        # Total Construction Area (Area * Floors)
        total_area = built_up_area * num_floors
        
        # Thumb Rules (Calibrated to match PDF output for 1000 sq yards G+2)
        # PDF Example: 1000 sq yards, G+2 -> ~10.5 tons steel
        
        # Steel: approx 3.5 to 4 kg per sq yard per floor? 
        # Logic: 10.5 tons / 3 floors = 3.5 tons per floor. 
        steel_tons = (total_area * 0.0035) 
        
        # Cement: approx 0.4 bags per sq yard per floor
        cement_bags = int(total_area * 0.4)
        
        # Sand: approx 0.6 tons per sq yard per floor
        sand_tons = total_area * 0.6
        
        # Water: approx 500 liters per sq yard
        water_liters = total_area * 500

        return {
            "steel_tons": round(steel_tons, 1),
            "cement_bags": cement_bags,
            "sand_tons": round(sand_tons, 1),
            "water_liters": int(water_liters)
        }

    def calculate_labor(self, built_up_area, construction_days):
        """
        Determines workforce size and composition.
        """
        # Rule of thumb: ~0.05 to 0.1 worker-days per sq foot approx.
        # Simple logic: Area / 20 = Total Man Days required?
        
        total_man_days = int(built_up_area * 0.5) # Heuristic for calculation
        
        # If days are not provided, estimate them
        if not construction_days:
            construction_days = 180 # Default 6 months
            
        avg_workers_per_day = math.ceil(total_man_days / construction_days)
        
        # Role Distribution (Approximate Percentages)
        return {
            "total_workers_required": avg_workers_per_day,
            "total_labor_days": total_man_days,
            "role_distribution": {
                "Masons": math.ceil(avg_workers_per_day * 0.30),
                "Helpers": math.ceil(avg_workers_per_day * 0.40),
                "Steel Workers": math.ceil(avg_workers_per_day * 0.10),
                "Carpenters": math.ceil(avg_workers_per_day * 0.10),
                "Supervisors": math.ceil(avg_workers_per_day * 0.10)
            }
        }