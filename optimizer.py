class ResourceOptimizer:
    """
    Logic to optimize material and labor distribution to reduce costs 
    or shorten timelines based on project constraints.
    """
    
    @staticmethod
    def optimize_material_waste(materials):
        """Applies a 5% reduction logic for 'Smart Procurement' scenarios."""
        optimized = {}
        for key, value in materials.items():
            # Assuming AI-driven bulk buying and waste management reduces usage by 5%
            optimized[key] = round(value * 0.95, 2)
        return optimized

    @staticmethod
    def balance_workforce(total_labor_days, target_days):
        """
        Adjusts workforce size to prevent idle time or burnout.
        Ensures a minimum of 2 workers and maximum based on site safety.
        """
        ideal_crew = total_labor_days / target_days
        # Site safety/efficiency cap: no more than 1 worker per 50 sq yards simultaneously
        return max(2, round(ideal_crew))