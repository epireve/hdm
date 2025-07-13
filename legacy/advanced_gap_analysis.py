#!/usr/bin/env python3
"""
Advanced Gap Analysis for Novel Research Opportunities
Analyzes extracted technical concepts and research gaps to identify unexplored areas
for university collaboration in heterogeneous data integration and PKG systems.
"""

import json
import csv
import re
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime
import itertools
from dataclasses import dataclass

@dataclass
class ResearchGap:
    """Represents an identified research gap with collaboration potential"""
    gap_id: str
    title: str
    description: str
    gap_type: str  # 'technical', 'performance', 'integration', 'domain'
    importance_score: float
    feasibility_score: float
    collaboration_potential: str  # 'high', 'medium', 'low'
    supporting_evidence: List[str]
    related_concepts: List[str]
    affected_domains: List[str]
    potential_solutions: List[str]
    university_suitability: str

class AdvancedGapAnalyzer:
    def __init__(self, concepts_file: str, papers_csv: str):
        self.concepts_file = concepts_file
        self.papers_csv = papers_csv
        self.concepts_data = {}
        self.papers_data = []
        self.identified_gaps = []
        
        # Define gap detection patterns
        self.gap_indicators = {
            'technical_gaps': [
                r'(?:lack|missing|absence|limited|insufficient)\s+(?:of\s+)?(?:implementation|solution|approach|method)',
                r'(?:not\s+)?(?:fully\s+)?(?:addressed|solved|implemented|developed)',
                r'(?:future\s+work|further\s+research|next\s+steps)\s+(?:should|could|needs?|requires?)',
                r'(?:remains?\s+)?(?:open|unsolved|challenging|difficult)\s+(?:problem|issue|question)',
                r'(?:no\s+)?(?:existing|current|available)\s+(?:solution|method|approach|framework)',
                r'(?:limited|little|minimal)\s+(?:work|research|study|investigation)'
            ],
            'performance_gaps': [
                r'(?:low|poor|suboptimal|insufficient)\s+(?:performance|accuracy|efficiency|speed)',
                r'(?:high|excessive|significant)\s+(?:latency|delay|overhead|cost)',
                r'(?:scalability|memory|storage|computational)\s+(?:issues?|problems?|limitations?)',
                r'(?:bottleneck|constraint|limitation)\s+(?:in|for|of)',
                r'(?:improve|enhance|optimize|increase)\s+(?:performance|efficiency|accuracy)'
            ],
            'integration_gaps': [
                r'(?:heterogeneous|multi-source|cross-domain)\s+(?:integration|fusion|combination)\s+(?:challenges?|issues?)',
                r'(?:interoperability|compatibility)\s+(?:problems?|issues?|challenges?)',
                r'(?:semantic|schema|ontology)\s+(?:alignment|mapping|harmonization)\s+(?:difficulties|challenges)',
                r'(?:data\s+)?(?:silos?|isolation|fragmentation)',
                r'(?:unified|integrated|holistic)\s+(?:approach|framework|solution)\s+(?:needed|required|missing)'
            ],
            'domain_gaps': [
                r'(?:cross-domain|interdisciplinary|multi-domain)\s+(?:applications?|approaches?|solutions?)',
                r'(?:domain-specific|specialized|customized)\s+(?:solutions?|approaches?|frameworks?)',
                r'(?:transfer|adaptation|application)\s+(?:to|across|between)\s+(?:different\s+)?(?:domains?|fields?|areas?)',
                r'(?:healthcare|education|enterprise|social)\s+(?:applications?|implementations?)\s+(?:lacking|missing|limited)'
            ]
        }
        
        # Define temporal evolution patterns
        self.temporal_patterns = {
            '2020-2021': ['early_adoption', 'experimental', 'proof_of_concept'],
            '2022-2023': ['development', 'implementation', 'validation'],
            '2024-2025': ['optimization', 'integration', 'deployment', 'scalability']
        }
        
        # Define cross-domain opportunity matrices
        self.domain_combinations = {
            'healthcare_education': ['patient_learning', 'medical_training', 'health_literacy'],
            'healthcare_enterprise': ['clinical_operations', 'medical_data_management', 'health_analytics'],
            'education_enterprise': ['workplace_learning', 'skills_development', 'knowledge_management'],
            'iot_healthcare': ['patient_monitoring', 'smart_health', 'connected_devices'],
            'iot_education': ['smart_classrooms', 'learning_analytics', 'educational_sensors'],
            'social_enterprise': ['collaboration_tools', 'social_learning', 'community_knowledge']
        }

    def load_data(self):
        """Load concepts and papers data"""
        try:
            with open(self.concepts_file, 'r', encoding='utf-8') as f:
                self.concepts_data = json.load(f)
            print(f"Loaded concepts data with {len(self.concepts_data.get('top_100_concepts', {}))} concepts")
            
            with open(self.papers_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.papers_data = list(reader)
            print(f"Loaded {len(self.papers_data)} papers")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        return True

    def extract_research_gaps_from_papers(self) -> List[Dict]:
        """Extract explicit research gaps mentioned in papers"""
        gaps = []
        
        for paper in self.papers_data:
            paper_gaps = []
            
            # Analyze key columns for gap indicators
            gap_columns = ['Research Gaps', 'Future Work', 'Limitations', 'Conclusion', 'Summary']
            
            for column in gap_columns:
                if column in paper and paper[column] and paper[column].lower() != 'nan':
                    text = paper[column]
                    
                    # Detect different types of gaps
                    for gap_type, patterns in self.gap_indicators.items():
                        for pattern in patterns:
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            if matches:
                                gap_context = self.extract_gap_context(text, pattern)
                                paper_gaps.append({
                                    'type': gap_type,
                                    'context': gap_context,
                                    'source_column': column,
                                    'pattern_matched': pattern
                                })
            
            if paper_gaps:
                gaps.append({
                    'paper_id': paper.get('cite_key', paper.get('title', 'unknown')),
                    'title': paper.get('title', 'Unknown'),
                    'year': paper.get('year', 'Unknown'),
                    'domain': self.determine_domain(paper),
                    'gaps': paper_gaps
                })
        
        return gaps

    def extract_gap_context(self, text: str, pattern: str, context_size: int = 100) -> str:
        """Extract context around gap indicators"""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - context_size)
            end = min(len(text), match.end() + context_size)
            return text[start:end].strip()
        return ""

    def determine_domain(self, paper: Dict) -> str:
        """Determine paper domain from content"""
        content = (paper.get('title', '') + ' ' + 
                  paper.get('Summary', '') + ' ' + 
                  paper.get('Tags', '')).lower()
        
        domain_keywords = {
            'healthcare': ['health', 'medical', 'clinical', 'patient', 'diagnosis', 'treatment'],
            'education': ['learning', 'education', 'student', 'curriculum', 'pedagogical', 'mooc'],
            'enterprise': ['business', 'enterprise', 'corporate', 'organization', 'company'],
            'social': ['social', 'network', 'communication', 'collaboration', 'community'],
            'iot': ['iot', 'sensor', 'device', 'smart', 'embedded', 'wireless'],
            'finance': ['financial', 'banking', 'investment', 'trading', 'fintech']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content for keyword in keywords):
                return domain
        return 'general'

    def analyze_concept_intersections(self) -> List[Dict]:
        """Find unexplored intersections between high-frequency concepts"""
        concepts = self.concepts_data.get('top_100_concepts', {})
        
        # Get high-frequency concepts by category
        by_category = defaultdict(list)
        for concept, data in concepts.items():
            if data['frequency'] >= 5:  # Only consider frequently mentioned concepts
                by_category[data['category']].append((concept, data))
        
        intersections = []
        
        # Find cross-category intersections
        for cat1, cat2 in itertools.combinations(by_category.keys(), 2):
            for concept1, data1 in by_category[cat1][:10]:  # Top 10 per category
                for concept2, data2 in by_category[cat2][:10]:
                    
                    # Check if this combination appears together in papers
                    co_occurrence = self.check_concept_co_occurrence(concept1, concept2)
                    
                    if co_occurrence['frequency'] < 3:  # Unexplored intersection
                        intersection = {
                            'concept1': concept1,
                            'concept2': concept2,
                            'category1': cat1,
                            'category2': cat2,
                            'frequency1': data1['frequency'],
                            'frequency2': data2['frequency'],
                            'co_occurrence': co_occurrence['frequency'],
                            'potential_domains': list(set(data1['domains']) | set(data2['domains'])),
                            'opportunity_score': self.calculate_opportunity_score(data1, data2, co_occurrence)
                        }
                        intersections.append(intersection)
        
        # Sort by opportunity score
        intersections.sort(key=lambda x: x['opportunity_score'], reverse=True)
        return intersections

    def check_concept_co_occurrence(self, concept1: str, concept2: str) -> Dict:
        """Check how often two concepts appear together in papers"""
        co_occurrence = 0
        papers_with_both = []
        
        for paper in self.papers_data:
            content = ' '.join([
                paper.get('Summary', ''),
                paper.get('Methodology', ''),
                paper.get('Key Findings', ''),
                paper.get('Tags', '')
            ]).lower()
            
            if concept1 in content and concept2 in content:
                co_occurrence += 1
                papers_with_both.append(paper.get('cite_key', paper.get('title', 'unknown')))
        
        return {
            'frequency': co_occurrence,
            'papers': papers_with_both
        }

    def calculate_opportunity_score(self, data1: Dict, data2: Dict, co_occurrence: Dict) -> float:
        """Calculate research opportunity score for concept intersection"""
        freq1 = data1['frequency']
        freq2 = data2['frequency']
        co_freq = co_occurrence['frequency']
        
        # Higher individual frequencies = more established concepts
        establishment_score = (freq1 + freq2) / 2
        
        # Lower co-occurrence = higher opportunity
        novelty_score = max(0, 10 - co_freq)
        
        # More domains = broader application potential
        domain_diversity = len(set(data1['domains']) | set(data2['domains']))
        
        # Combined score (normalized to 0-100)
        opportunity_score = (establishment_score * 0.3 + novelty_score * 0.5 + domain_diversity * 0.2) * 2
        
        return min(100, opportunity_score)

    def identify_temporal_evolution_gaps(self) -> List[Dict]:
        """Identify concepts that haven't evolved with recent advances"""
        temporal_gaps = []
        
        # Analyze concept evolution over time
        for concept, data in self.concepts_data.get('top_100_concepts', {}).items():
            papers = data.get('sample_papers', [])
            
            # Group papers by year
            years = defaultdict(int)
            for paper in papers:
                year = paper.get('year', 'Unknown')
                if year != 'Unknown' and year.isdigit():
                    years[int(year)] += 1
            
            if years:
                recent_activity = sum(years.get(y, 0) for y in [2024, 2025])
                total_activity = sum(years.values())
                
                # Concepts with low recent activity but high overall frequency
                if total_activity >= 10 and recent_activity / total_activity < 0.2:
                    temporal_gaps.append({
                        'concept': concept,
                        'category': data['category'],
                        'total_frequency': data['frequency'],
                        'recent_activity_ratio': recent_activity / total_activity,
                        'domains': data['domains'],
                        'modernization_potential': 'high' if data['frequency'] > 20 else 'medium'
                    })
        
        return temporal_gaps

    def identify_cross_domain_gaps(self) -> List[Dict]:
        """Identify successful techniques not applied across domains"""
        cross_domain_gaps = []
        
        # Find domain-specific successful concepts
        domain_concepts = defaultdict(list)
        
        for concept, data in self.concepts_data.get('top_100_concepts', {}).items():
            if data['frequency'] >= 10:  # High-frequency concepts
                primary_domain = max(data['domains'], key=lambda d: data['domains'].count(d)) if data['domains'] else 'general'
                domain_concepts[primary_domain].append((concept, data))
        
        # Find transfer opportunities
        for source_domain, concepts in domain_concepts.items():
            for target_domain in domain_concepts.keys():
                if source_domain != target_domain:
                    for concept, data in concepts:
                        if target_domain not in data['domains']:
                            # This concept is successful in source but not applied in target
                            cross_domain_gaps.append({
                                'concept': concept,
                                'source_domain': source_domain,
                                'target_domain': target_domain,
                                'frequency': data['frequency'],
                                'category': data['category'],
                                'transfer_potential': self.assess_transfer_potential(source_domain, target_domain, concept)
                            })
        
        return cross_domain_gaps

    def assess_transfer_potential(self, source_domain: str, target_domain: str, concept: str) -> str:
        """Assess potential for cross-domain concept transfer"""
        # High-potential domain combinations
        high_potential = [
            ('healthcare', 'education'),
            ('education', 'enterprise'),
            ('iot', 'healthcare'),
            ('social', 'enterprise')
        ]
        
        if (source_domain, target_domain) in high_potential or (target_domain, source_domain) in high_potential:
            return 'high'
        
        # Check concept transferability
        transferable_concepts = [
            'temporal', 'integration', 'fusion', 'knowledge graph', 'personalized',
            'recommendation', 'analytics', 'visualization', 'privacy', 'federated'
        ]
        
        if any(tc in concept.lower() for tc in transferable_concepts):
            return 'medium'
        
        return 'low'

    def generate_novel_research_opportunities(self) -> List[ResearchGap]:
        """Generate comprehensive list of novel research opportunities"""
        opportunities = []
        
        # 1. Concept intersection opportunities
        intersections = self.analyze_concept_intersections()
        for intersection in intersections[:20]:  # Top 20
            gap = ResearchGap(
                gap_id=f"intersection_{len(opportunities)+1}",
                title=f"Integration of {intersection['concept1'].title()} and {intersection['concept2'].title()}",
                description=f"Unexplored intersection between {intersection['concept1']} ({intersection['category1']}) and {intersection['concept2']} ({intersection['category2']}) with high potential for innovation.",
                gap_type="integration",
                importance_score=intersection['opportunity_score'] / 100,
                feasibility_score=0.7,  # Generally feasible for established concepts
                collaboration_potential="high",
                supporting_evidence=[f"High individual concept frequencies: {intersection['frequency1']}, {intersection['frequency2']}", f"Low co-occurrence: {intersection['co_occurrence']}"],
                related_concepts=[intersection['concept1'], intersection['concept2']],
                affected_domains=intersection['potential_domains'],
                potential_solutions=[f"Hybrid framework combining {intersection['concept1']} and {intersection['concept2']}", "Cross-disciplinary research approach"],
                university_suitability="Excellent for interdisciplinary research programs"
            )
            opportunities.append(gap)
        
        # 2. Temporal evolution opportunities
        temporal_gaps = self.identify_temporal_evolution_gaps()
        for gap in temporal_gaps[:10]:  # Top 10
            opportunity = ResearchGap(
                gap_id=f"temporal_{len(opportunities)+1}",
                title=f"Modernization of {gap['concept'].title()} Approaches",
                description=f"Application of recent advances (2024-2025) to established {gap['concept']} techniques with {gap['modernization_potential']} potential.",
                gap_type="temporal",
                importance_score=gap['recent_activity_ratio'] + 0.5,  # Lower recent activity = higher opportunity
                feasibility_score=0.8,  # High feasibility for modernization
                collaboration_potential="high",
                supporting_evidence=[f"High overall frequency: {gap['total_frequency']}", f"Low recent activity ratio: {gap['recent_activity_ratio']:.2f}"],
                related_concepts=[gap['concept']],
                affected_domains=gap['domains'],
                potential_solutions=["Integration with LLMs", "Application of recent deep learning advances", "Modern architectural patterns"],
                university_suitability="Ideal for funded research with industry collaboration"
            )
            opportunities.append(opportunity)
        
        # 3. Cross-domain transfer opportunities
        cross_domain_gaps = self.identify_cross_domain_gaps()
        high_potential_transfers = [gap for gap in cross_domain_gaps if gap['transfer_potential'] == 'high'][:15]
        
        for gap in high_potential_transfers:
            opportunity = ResearchGap(
                gap_id=f"transfer_{len(opportunities)+1}",
                title=f"{gap['concept'].title()} Transfer from {gap['source_domain'].title()} to {gap['target_domain'].title()}",
                description=f"Successful {gap['concept']} approaches from {gap['source_domain']} domain could be adapted for {gap['target_domain']} applications.",
                gap_type="domain",
                importance_score=min(1.0, gap['frequency'] / 50),
                feasibility_score=0.75,
                collaboration_potential="high",
                supporting_evidence=[f"Proven success in {gap['source_domain']}", f"High frequency: {gap['frequency']}"],
                related_concepts=[gap['concept']],
                affected_domains=[gap['source_domain'], gap['target_domain']],
                potential_solutions=[f"Domain adaptation techniques", "Cross-domain validation studies", "Collaborative pilot projects"],
                university_suitability="Perfect for cross-departmental collaboration"
            )
            opportunities.append(opportunity)
        
        return opportunities

    def generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive gap analysis report"""
        print("Generating comprehensive gap analysis report...")
        
        # Extract various types of gaps
        explicit_gaps = self.extract_research_gaps_from_papers()
        concept_intersections = self.analyze_concept_intersections()
        temporal_gaps = self.identify_temporal_evolution_gaps()
        cross_domain_gaps = self.identify_cross_domain_gaps()
        novel_opportunities = self.generate_novel_research_opportunities()
        
        # Generate statistics
        stats = {
            'total_papers_analyzed': len(self.papers_data),
            'papers_with_explicit_gaps': len(explicit_gaps),
            'novel_concept_intersections': len(concept_intersections),
            'temporal_evolution_gaps': len(temporal_gaps),
            'cross_domain_opportunities': len(cross_domain_gaps),
            'total_research_opportunities': len(novel_opportunities),
            'high_collaboration_potential': len([op for op in novel_opportunities if op.collaboration_potential == 'high']),
            'analysis_date': datetime.now().isoformat()
        }
        
        # Categorize opportunities by type
        opportunities_by_type = defaultdict(list)
        for op in novel_opportunities:
            opportunities_by_type[op.gap_type].append({
                'id': op.gap_id,
                'title': op.title,
                'importance_score': op.importance_score,
                'feasibility_score': op.feasibility_score,
                'collaboration_potential': op.collaboration_potential,
                'affected_domains': op.affected_domains
            })
        
        # Rank top opportunities for university collaboration
        university_ready_opportunities = sorted(
            [op for op in novel_opportunities if op.importance_score > 0.6 and op.feasibility_score > 0.7],
            key=lambda x: (x.importance_score + x.feasibility_score) / 2,
            reverse=True
        )[:20]
        
        report = {
            'executive_summary': {
                'analysis_scope': f"Analyzed {stats['total_papers_analyzed']} research papers spanning 2020-2025",
                'key_findings': [
                    f"Identified {stats['total_research_opportunities']} novel research opportunities",
                    f"{stats['high_collaboration_potential']} opportunities have high university collaboration potential",
                    f"Found {stats['novel_concept_intersections']} unexplored concept intersections",
                    f"Discovered {stats['temporal_evolution_gaps']} concepts ripe for modernization",
                    f"Identified {stats['cross_domain_opportunities']} cross-domain transfer opportunities"
                ],
                'collaboration_readiness': f"{len(university_ready_opportunities)} opportunities are immediately ready for university partnerships"
            },
            'statistics': stats,
            'gap_analysis_results': {
                'explicit_research_gaps': explicit_gaps[:50],  # Top 50
                'concept_intersections': concept_intersections[:30],  # Top 30
                'temporal_evolution_gaps': temporal_gaps,
                'cross_domain_opportunities': cross_domain_gaps[:40]  # Top 40
            },
            'novel_research_opportunities': {
                'by_type': dict(opportunities_by_type),
                'university_ready': [
                    {
                        'id': op.gap_id,
                        'title': op.title,
                        'description': op.description,
                        'gap_type': op.gap_type,
                        'importance_score': op.importance_score,
                        'feasibility_score': op.feasibility_score,
                        'collaboration_potential': op.collaboration_potential,
                        'affected_domains': op.affected_domains,
                        'university_suitability': op.university_suitability,
                        'supporting_evidence': op.supporting_evidence,
                        'potential_solutions': op.potential_solutions
                    } for op in university_ready_opportunities
                ],
                'all_opportunities': [
                    {
                        'id': op.gap_id,
                        'title': op.title,
                        'description': op.description,
                        'gap_type': op.gap_type,
                        'importance_score': op.importance_score,
                        'feasibility_score': op.feasibility_score,
                        'collaboration_potential': op.collaboration_potential,
                        'affected_domains': op.affected_domains,
                        'related_concepts': op.related_concepts
                    } for op in novel_opportunities
                ]
            },
            'collaboration_framework': {
                'immediate_opportunities': [op.title for op in university_ready_opportunities[:10]],
                'medium_term_opportunities': [op.title for op in university_ready_opportunities[10:20]],
                'funding_recommendations': [
                    "NSF Computer and Information Science and Engineering (CISE) programs",
                    "NIH Big Data to Knowledge (BD2K) initiative",
                    "DOE Advanced Scientific Computing Research (ASCR)",
                    "Industry partnerships for applied research"
                ],
                'collaboration_types': {
                    'joint_research_projects': len([op for op in novel_opportunities if 'integration' in op.gap_type]),
                    'student_exchange_programs': len([op for op in novel_opportunities if 'domain' in op.gap_type]),
                    'shared_infrastructure': len([op for op in novel_opportunities if 'temporal' in op.gap_type])
                }
            }
        }
        
        return report

    def save_report(self, filename: str = 'advanced_gap_analysis_report.json'):
        """Save the comprehensive gap analysis report"""
        report = self.generate_comprehensive_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Advanced gap analysis report saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False

def main():
    """Main execution function"""
    concepts_file = '/Users/invoture/dev.local/hdm/technical_concepts_extracted.json'
    papers_csv = '/Users/invoture/dev.local/hdm/hdm_research_papers_complete_20250710.csv'
    
    print("=== Advanced Gap Analysis for Novel Research Opportunities ===")
    print(f"Concepts Data: {concepts_file}")
    print(f"Papers Dataset: {papers_csv}")
    print("Focus: University Collaboration & Novel Research Vectors")
    print()
    
    # Initialize analyzer
    analyzer = AdvancedGapAnalyzer(concepts_file, papers_csv)
    
    # Load data
    if not analyzer.load_data():
        print("Failed to load data. Exiting.")
        return
    
    # Generate and save comprehensive report
    if analyzer.save_report():
        print("\n=== ANALYSIS COMPLETE ===")
        print("Advanced gap analysis report generated successfully!")
        print("Ready for university collaboration proposals.")
    else:
        print("Failed to generate report.")

if __name__ == "__main__":
    main()