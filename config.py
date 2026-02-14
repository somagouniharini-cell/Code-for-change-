import os

class Config:
    # Flask Settings
    DEBUG = True
    PORT = 5000
    
    # Ollama AI Settings
    OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', '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')
    # Using the model specified in your PDF (Page 8)
    MODEL_ID = "granite:3.3-2b" 

    # Construction Defaults (INR) - Based on PDF Page 9 screenshots
    DEFAULT_DAILY_WAGE = 500
    DEFAULT_COST_PER_SQ_YARD = 1500
    DEFAULT_OVERHEAD_PERCENTAGE = 10.0

    # Material Rates (INR)
    RATE_STEEL_PER_TON = 60000
    RATE_CEMENT_PER_BAG = 420
    RATE_SAND_PER_TON = 3000

    # Thumb Rules for Estimation (Per Sq. Yard)
    # Extracted from project screenshots
    QTY_STEEL_PER_SQ_YARD = 25.0    # kg per sq yard
    QTY_CEMENT_PER_SQ_YARD = 0.4    # bags per sq yard
    QTY_SAND_PER_SQ_YARD = 0.08     # tons per sq yard
    QTY_WATER_PER_SQ_YARD = 500.0   # liters per sq yard