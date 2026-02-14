class CostService:
    def calculate_costs(self, built_up_area, cost_per_sq_yard, total_labor_days, daily_wage):
        """
        Calculates detailed cost breakdown based on Milestone 5 logic.
        
        Formulas derived from PDF:
        - Material Cost ~= Built-up Area * Cost per Sq Yard
        - Labor Cost = Total Labor Days * Daily Wage
        - Overhead = 10% of (Material + Labor)
        """
        
        # 1. Material Cost Calculation
        # Based on the PDF input "Cost per Sq. Yard" usually refers to the base construction rate excluding specific labor
        material_cost = built_up_area * cost_per_sq_yard
        
        # 2. Labor Cost Calculation
        labor_cost = total_labor_days * daily_wage
        
        # 3. Overhead Calculation (10% standard)
        subtotal = material_cost + labor_cost
        overhead_cost = subtotal * 0.10
        
        # 4. Total Calculation
        total_project_cost = material_cost + labor_cost + overhead_cost
        
        return {
            "material_cost": round(material_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "overhead_cost": round(overhead_cost, 2),
            "total_project_cost": round(total_project_cost, 2),
            "currency": "INR"
        }