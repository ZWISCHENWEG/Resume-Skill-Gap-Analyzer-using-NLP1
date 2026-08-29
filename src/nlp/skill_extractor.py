import json
import re
import os
from typing import List, Dict, Any, Set
from dataclasses import dataclass

@dataclass
class ExtractedSkill:
    name: str
    category: str

class SkillExtractor:
    """
    Skill Extraction Engine.
    Uses a curated vocabulary to deterministically match technical skills.
    Implements alias normalization, longest-match overlap handling, and ambiguity checks.
    """
    
    def __init__(self, dictionary_path: str = None):
        if dictionary_path is None:
            # Default to the data/processed directory relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            dictionary_path = os.path.join(base_dir, 'data', 'processed', 'skill_dictionary.json')
            
        with open(dictionary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.skills = data.get('skills', [])
        
        # Precompile patterns for performance
        self._compile_patterns()

    def _compile_patterns(self):
        self.unambiguous_patterns = []
        self.ambiguous_patterns = []
        
        for skill in self.skills:
            name = skill['name']
            category = skill.get('category', 'Other')
            aliases = skill.get('aliases', [])
            is_ambiguous = skill.get('ambiguous', False)
            
            # Create a list of all variants to match for this skill
            # We sort them by length descending so that longest aliases match first
            # if we were using a single regex, but we will use re.finditer and filter overlaps.
            variants = [name] + aliases
            
            for variant in variants:
                # Escape the variant for regex
                escaped_variant = re.escape(variant)
                
                if is_ambiguous:
                    # For ambiguous skills (like C, R), we match on the original_text
                    # Case sensitive word boundaries. We use (?<!\w) and (?!\w) to handle 
                    # terms that might end in non-word chars if they had aliases, though 
                    # usually ambiguous are single letters.
                    pattern = re.compile(rf'(?<!\w){escaped_variant}(?!\w)')
                    self.ambiguous_patterns.append({
                        'pattern': pattern,
                        'name': name,
                        'category': category,
                        'variant': variant
                    })
                else:
                    # For normal skills, match on cleaned_text (lowercased)
                    # We ensure the pattern itself is lowercase
                    escaped_variant_lower = escaped_variant.lower()
                    # Using negative lookbehind/lookahead for word chars handles terms like C++, .NET
                    pattern = re.compile(rf'(?<!\w){escaped_variant_lower}(?!\w)')
                    self.unambiguous_patterns.append({
                        'pattern': pattern,
                        'name': name,
                        'category': category,
                        'variant': variant.lower()
                    })
                    
        # To handle overlap correctly across different skills, we will collect all matches
        # and then filter subsets.

    def extract_skills(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts skills from preprocessed text data.
        
        Args:
            preprocessed_data: The dictionary returned by TextPreprocessor.preprocess()
                               Must contain 'original_text' and 'cleaned_text'.
                               
        Returns:
            A dictionary containing canonical skill names and a detailed list of ExtractedSkill objects.
        """
        original_text = preprocessed_data.get('original_text', '')
        cleaned_text = preprocessed_data.get('cleaned_text', '')
        
        if not original_text and not cleaned_text:
            return {
                "extracted_skills": [],
                "canonical_names": []
            }
            
        matches = []
        
        # 1. Match Unambiguous Skills on cleaned_text
        if cleaned_text:
            for item in self.unambiguous_patterns:
                for match in item['pattern'].finditer(cleaned_text):
                    matches.append({
                        'start': match.start(),
                        'end': match.end(),
                        'name': item['name'],
                        'category': item['category'],
                        'text_source': 'cleaned'
                    })
                    
        # 2. Match Ambiguous Skills on original_text
        if original_text:
            for item in self.ambiguous_patterns:
                for match in item['pattern'].finditer(original_text):
                    # We add a fake offset/type so we don't directly overlap-check 
                    # original_text spans with cleaned_text spans trivially.
                    # Actually, ambiguous skills are usually single letters and rarely subsume or are subsumed
                    # by long phrases. We keep them separate.
                    matches.append({
                        'start': match.start(),
                        'end': match.end(),
                        'name': item['name'],
                        'category': item['category'],
                        'text_source': 'original'
                    })

        # 3. Filter overlapping matches
        # A match is filtered out if its span is completely inside another match's span
        # of the SAME text source.
        valid_matches = []
        for i, m1 in enumerate(matches):
            is_subsumed = False
            for j, m2 in enumerate(matches):
                if i == j or m1['text_source'] != m2['text_source']:
                    continue
                # If m1 is completely inside m2
                if m2['start'] <= m1['start'] and m2['end'] >= m1['end']:
                    # If they have the exact same span, keep the first one we saw or the one with a longer string
                    if m1['start'] == m2['start'] and m1['end'] == m2['end']:
                        if i > j:  # Let the first one win to avoid both dropping
                            is_subsumed = True
                            break
                    else:
                        is_subsumed = True
                        break
            if not is_subsumed:
                valid_matches.append(m1)

        # 4. Deduplicate to get final canonical set
        unique_skills: Dict[str, ExtractedSkill] = {}
        for m in valid_matches:
            name = m['name']
            if name not in unique_skills:
                unique_skills[name] = ExtractedSkill(name=name, category=m['category'])

        # Sort for deterministic output
        final_list = list(unique_skills.values())
        final_list.sort(key=lambda x: x.name)
        
        canonical_names = [skill.name for skill in final_list]
        
        return {
            "extracted_skills": [
                {"name": s.name, "category": s.category} for s in final_list
            ],
            "canonical_names": canonical_names
        }
