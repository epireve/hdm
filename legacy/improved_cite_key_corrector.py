#!/usr/bin/env python3
"""
Improved cite_key corrector with refined author extraction logic.
"""

import sqlite3
import re
import json
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovedCiteKeyCorrector:
    """Improved cite_key correction with better author extraction."""
    
    def __init__(self):
        self.name_prefixes = [
            'al', 'al-', 'ibn', 'ben', 'bin', 'abu', 'abd',  # Arabic
            'van', 'van der', 'van den', 'de', 'del', 'della', 'di',  # European
            'le', 'la', 'les', 'du', 'dos', 'das',  # French/Portuguese
            'von', 'zu', 'zur',  # German
            'mc', 'mac', 'o\'',  # Celtic
            'saint', 'st', 'santa'  # Religious
        ]
        
        self.institutional_indicators = [
            'university', 'univ', 'college', 'institute', 'institution', 'school',
            'academy', 'polytechnic', 'tech', 'laboratory', 'labs', 'lab',
            'corporation', 'corp', 'company', 'inc', 'ltd', 'llc',
            'foundation', 'center', 'centre', 'department', 'dept',
            'hospital', 'clinic', 'medical', 'health', 'research',
            'group', 'team', 'division', 'faculty', 'bureau'
        ]
        
        self.location_indicators = [
            # Countries
            'usa', 'uk', 'canada', 'germany', 'france', 'italy', 'spain', 'china', 'japan',
            'australia', 'brazil', 'india', 'russia', 'korea', 'netherlands', 'sweden',
            'switzerland', 'austria', 'belgium', 'denmark', 'norway', 'finland',
            # Major cities that might appear
            'berlin', 'london', 'paris', 'tokyo', 'beijing', 'mumbai', 'delhi',
            'moscow', 'sydney', 'toronto', 'vancouver', 'boston', 'chicago',
            'seattle', 'austin', 'tehran', 'istanbul', 'cairo', 'jerusalem',
            'madrid', 'barcelona', 'rome', 'milan', 'zurich', 'geneva',
            # States/regions
            'california', 'texas', 'new york', 'florida', 'illinois', 'massachusetts',
            'washington', 'oregon', 'ontario', 'quebec', 'bavaria', 'catalonia'
        ]
    
    def clean_author_string(self, authors_string: str) -> str:
        """Clean and normalize author string for processing."""
        if not authors_string:
            return ""
        
        # Remove common academic suffixes and symbols
        authors_string = re.sub(r'\s*(Fellow|IEEE|Dr\.?|Prof\.?|Ph\.?D\.?|M\.?D\.?|Ph\.D)\s*,?\s*', '', authors_string, flags=re.IGNORECASE)
        
        # Remove superscript symbols and markers
        authors_string = re.sub(r'\s*[∗*†‡§¶#0-9]+\s*', ' ', authors_string)
        
        # Remove email domains but keep the local part if it looks like a name
        authors_string = re.sub(r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', authors_string)
        
        # Clean up extra whitespace
        authors_string = re.sub(r'\s+', ' ', authors_string.strip())
        
        return authors_string
    
    def is_institutional_word(self, word: str) -> bool:
        """Check if a word indicates an institution."""
        word_lower = word.lower().strip('.,()-')
        return any(indicator in word_lower for indicator in self.institutional_indicators)
    
    def is_location_word(self, word: str) -> bool:
        """Check if a word indicates a location."""
        word_lower = word.lower().strip('.,()-')
        return word_lower in self.location_indicators
    
    def extract_person_name_from_mixed_string(self, text: str) -> Optional[str]:
        """Extract person name from mixed institutional/location text."""
        words = text.split()
        
        # Look for patterns that indicate a person name
        potential_names = []
        current_name_parts = []
        
        for i, word in enumerate(words):
            word_clean = word.strip('.,()-')
            
            # Skip if it's clearly institutional or location
            if self.is_institutional_word(word) or self.is_location_word(word):
                # If we've been building a name, save it
                if current_name_parts:
                    potential_names.append(' '.join(current_name_parts))
                    current_name_parts = []
                continue
            
            # Skip common domain parts
            if word_clean.lower() in ['com', 'org', 'edu', 'gov', 'net']:
                if current_name_parts:
                    potential_names.append(' '.join(current_name_parts))
                    current_name_parts = []
                continue
            
            # If it looks like a name part (starts with capital, reasonable length)
            if (word_clean and 
                word_clean[0].isupper() and 
                2 <= len(word_clean) <= 20 and
                re.match(r'^[A-Za-z.-]+$', word_clean)):
                current_name_parts.append(word_clean)
            else:
                # End of name sequence
                if current_name_parts:
                    potential_names.append(' '.join(current_name_parts))
                    current_name_parts = []
        
        # Don't forget the last name if we were building one
        if current_name_parts:
            potential_names.append(' '.join(current_name_parts))
        
        # Return the longest reasonable name found
        if potential_names:
            # Prefer names with 2+ parts, then longest single names
            multi_part_names = [name for name in potential_names if len(name.split()) >= 2]
            if multi_part_names:
                return max(multi_part_names, key=len)
            else:
                return max(potential_names, key=len) if potential_names else None
        
        return None
    
    def extract_first_author_lastname(self, authors_string: str) -> Optional[str]:
        """Improved extraction of first author's last name."""
        if not authors_string or authors_string.strip() == '':
            return None
        
        # Clean the author string
        authors_string = self.clean_author_string(authors_string)
        
        # Split by common author separators
        first_author = re.split(r'[,;]|\sand\s|\s&\s', authors_string)[0].strip()
        
        # Handle mixed institutional/personal strings
        if any(self.is_institutional_word(word) or self.is_location_word(word) 
               for word in first_author.split()):
            # Try to extract person name from mixed string
            person_name = self.extract_person_name_from_mixed_string(first_author)
            if person_name:
                first_author = person_name
            else:
                # Fallback: take first few words that look like names
                words = first_author.split()
                name_words = []
                for word in words[:4]:  # Max 4 words for a name
                    word_clean = word.strip('.,()-')
                    if (word_clean and 
                        word_clean[0].isupper() and 
                        2 <= len(word_clean) <= 20 and
                        not self.is_institutional_word(word) and
                        not self.is_location_word(word)):
                        name_words.append(word_clean)
                    else:
                        break
                
                if name_words:
                    first_author = ' '.join(name_words)
                else:
                    return None
        
        # Now extract lastname from the person name
        if ',' in first_author:
            # "Last, First" format
            lastname = first_author.split(',')[0].strip()
        else:
            # "First Last" or "First Middle Last" format
            parts = first_author.split()
            if len(parts) >= 2:
                lastname = parts[-1]  # Take last word as surname
            elif len(parts) == 1:
                lastname = parts[0]  # Single name
            else:
                return None
        
        # Clean up the lastname
        lastname = re.sub(r'[^\w\s-]', '', lastname).strip()
        
        # Handle name prefixes (Al, Van, De, etc.)
        lastname_lower = lastname.lower()
        
        # Check if we need to combine with a prefix
        if len(parts) >= 2:
            potential_prefix = parts[-2].lower().strip('.,()-')
            
            # Check if the second-to-last word is a name prefix
            if potential_prefix in self.name_prefixes:
                # Combine prefix with lastname
                if potential_prefix in ['al', 'al-']:
                    lastname = f"al{lastname}"  # al-khatib becomes alkhatib
                elif potential_prefix in ['van', 'de', 'von']:
                    lastname = f"{potential_prefix}{lastname}"  # van-der becomes vanderberg
                else:
                    lastname = f"{potential_prefix}{lastname}"
        
        # Final cleanup and validation
        lastname = lastname.lower()
        
        # Remove any remaining special characters except hyphens
        lastname = re.sub(r'[^\w-]', '', lastname)
        
        # Validate lastname
        if len(lastname) < 2 or not re.match(r'^[a-z-]+$', lastname):
            return None
        
        return lastname
    
    def test_extraction_on_examples(self) -> None:
        """Test the improved extraction on known problematic cases."""
        test_cases = [
            ("Mohannad Alhanahnah University of Wisconsin-Madison, USA mohannad@cs.wisc.edu", "alhanahnah"),
            ("Markus Klems Technische Universitat Berlin ¨ Information Systems Engineering Group Berlin, Germany mk@ise.tu-berlin.de", "klems"),
            ("Amir Reza Asadi Humind Labs Tehran", "asadi"),
            ("Hassan S. Al Khatib, Subash Neupane, Harish Kumar Manchukonda", "alkhatib"),
            ("Filip Ilievski, Saurav Joshi, Bradley P. Allen", "ilievski"),
            ("Roshan Rao UC Berkeley", "rao"),
            ("Saravanan Krishnan, Alex Mathai, Amith Singhee", "krishnan"),
            ("nudt.edu.cn liyitong", "liyitong"),
            ("Hussein Abdallah, Essam Mansour", "abdallah"),
            ("Jami Aho", "aho")
        ]
        
        print("\n🧪 TESTING IMPROVED EXTRACTION LOGIC:")
        print("="*80)
        
        all_correct = True
        for authors, expected in test_cases:
            result = self.extract_first_author_lastname(authors)
            status = "✅" if result == expected else "❌"
            if result != expected:
                all_correct = False
            
            print(f"{status} {authors[:60]}...")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            print()
        
        if all_correct:
            print("🎉 ALL TEST CASES PASSED!")
        else:
            print("⚠️  Some test cases failed - logic needs refinement")
        
        return all_correct

def main():
    """Test the improved extraction logic."""
    logger.info("Testing Improved Cite_Key Extraction Logic...")
    
    corrector = ImprovedCiteKeyCorrector()
    
    # Test on known problematic cases
    success = corrector.test_extraction_on_examples()
    
    if success:
        print("\n✅ Ready to apply improved extraction logic to database")
        print("💡 Next step: Run the corrector with improved logic")
    else:
        print("\n❌ Extraction logic needs further refinement")
        print("🔧 Please review and adjust the extraction rules")

if __name__ == "__main__":
    main()