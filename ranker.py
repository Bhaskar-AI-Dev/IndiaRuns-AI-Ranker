import json
import csv

def load_candidates(filepath):
    """Reads the JSON file and loads the candidates."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def score_candidate(candidate):
    """
    Version 3: The Multiplicative Gate (Professional Recruiter)
    """
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    skills = candidate.get("skills", [])
    
    base_score = 0.0
    reasoning_notes = []
    
    # 1. Extract Data
    title = profile.get("current_title", "").lower()
    exp_years = profile.get("years_of_experience", 0)
    response_rate = signals.get("recruiter_response_rate", 0)
    location = profile.get("location", "").lower()
    relocate = signals.get("willing_to_relocate", False)
    
    # 2. CORE SKILLS (The True Foundation)
    core_ai_skills = ["python", "pytorch", "tensorflow", "llm", "rag", "machine learning", "nlp", "spark", "sql", "recommendation", "deep learning"]
    matched_skills = 0
    
    for skill_obj in skills:
        skill_name = skill_obj.get("name", "").lower()
        if any(core in skill_name for core in core_ai_skills):
            # Must have used the skill for more than 12 months!
            if skill_obj.get("duration_months", 0) > 12:
                matched_skills += 1
                base_score += 15  # Har strong skill par 15 points
                
    reasoning_notes.append(f"{exp_years} yrs exp. Validated {matched_skills} AI skills.")

    # 3. EXPERIENCE 
    if 5.0 <= exp_years <= 9.0:
        base_score += 20
    elif exp_years > 9.0:
        base_score += 10
        
    # 4. LOCATION
    if "pune" in location or "noida" in location:
        base_score += 15
        reasoning_notes.append("Local.")
    elif relocate:
        base_score += 10
        reasoning_notes.append("Will relocate.")
        
    # ========================================================
    # 🚀 THE MULTIPLICATIVE GATES (Filtering out the noise)
    # ========================================================
    
    # Gate A: The Title Check
    title_multiplier = 1.0
    good_titles = ["ai", "machine learning", "data", "backend", "software", "recommendation", "ml", "engineer", "developer"]
    bad_titles = ["hr", "marketing", "accountant", "graphic", "sales", "customer", "business analyst", "operations", "support"]
    
    if any(bad in title for bad in bad_titles):
        title_multiplier = 0.05  # Drop score by 95%
        reasoning_notes.append(f"Title penalty ({title}).")
    elif any(good in title for good in good_titles):
        title_multiplier = 1.2   # 20% Bonus for right technical titles
        
    # Gate B: The Skill Check
    skill_multiplier = 1.0
    if matched_skills == 0:
        skill_multiplier = 0.05  # Drop score by 95% if they have zero valid AI skills
        reasoning_notes.append("Zero core skills penalty.")
        
    # Apply Gates
    final_score = base_score * title_multiplier * skill_multiplier
    
    # 5. BEHAVIORAL MULTIPLIER
    if response_rate >= 0:
        final_score = final_score * response_rate
        reasoning_notes.append(f"Response: {int(response_rate*100)}%.")

    final_reasoning = " ".join(reasoning_notes)
    
    return final_score, final_reasoning

def main():
    print("Loading candidates dataset...")
    candidates = load_candidates("data/sample_candidates.json")
    
    print("Applying Multiplicative Gates...")
    ranked_list = []
    for cand in candidates:
        cand_id = cand["candidate_id"]
        score, reasoning = score_candidate(cand)
        ranked_list.append((cand_id, score, reasoning))
    
    # Sort by score (Highest to Lowest)
    ranked_list.sort(key=lambda x: x[1], reverse=True)
    
    output_file = "team_submission.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        
        for rank, (cand_id, score, reasoning) in enumerate(ranked_list[:100], start=1):
            writer.writerow([cand_id, rank, round(score, 3), reasoning])
            
    print(f"Success! Highly filtered candidates saved to {output_file}")

if __name__ == "__main__":
    main()