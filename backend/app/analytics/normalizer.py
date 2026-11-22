def bounded_linear_normalize(raw_value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """
    Normalizes raw metric value into a standard [0.0, 100.0] scale using bounded linear interpolation.
    Handles inverted scales (where lower is better) if max_val < min_val.
    """
    if raw_value is None:
        return 0.0
        
    if min_val == max_val:
        return 100.0 if raw_value >= min_val else 0.0
        
    # Standard: higher is better
    if max_val > min_val:
        normalized = ((raw_value - min_val) / (max_val - min_val)) * 100.0
    else: # Inverted: lower is better (e.g., defect rate)
        normalized = ((min_val - raw_value) / (min_val - max_val)) * 100.0
        
    return round(min(100.0, max(0.0, normalized)), 2)
