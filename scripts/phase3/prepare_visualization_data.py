#!/usr/bin/env python3
"""
Prepare visualization data for the Research Explorer Tool.
Transforms JSON analysis results into a format optimized for D3.js visualization.
"""

import json
import os
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import math

class VisualizationDataProcessor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.technical_concepts = {}
        self.domain_analysis = {}
        self.cross_domain_opportunities = {}
        self.research_gaps = {}
        
    def load_analysis_files(self):
        """Load all JSON analysis files."""
        # Primary file - technical concepts
        tech_file = os.path.join(self.base_dir, 'technical_concepts_extracted.json')
        if os.path.exists(tech_file):
            with open(tech_file, 'r') as f:
                self.technical_concepts = json.load(f)
            print(f"Loaded technical_concepts_extracted.json")
            
            # Extract domain analysis from technical concepts
            self._extract_domain_analysis()
            # Generate research opportunities from gaps
            self._generate_opportunities_from_gaps()
        else:
            print(f"Error: technical_concepts_extracted.json not found")
    
    def create_concept_nodes(self) -> List[Dict]:
        """Create nodes for the network visualization."""
        nodes = []
        node_id = 0
        concept_to_id = {}
        
        # Process top 100 concepts
        if 'top_100_concepts' in self.technical_concepts:
            top_concepts = self.technical_concepts['top_100_concepts']
            # Handle both dict and list formats
            if isinstance(top_concepts, dict):
                for concept, data in top_concepts.items():
                    # Extract frequency from nested structure
                    freq = data['frequency'] if isinstance(data, dict) and 'frequency' in data else data
                    if isinstance(freq, (int, float)) and freq > 1:  # Filter out single occurrences
                        node = {
                            'id': node_id,
                            'name': concept,
                            'frequency': freq,
                            'category': data.get('category', self._categorize_concept(concept)) if isinstance(data, dict) else self._categorize_concept(concept),
                            'type': 'technical',
                            'size': math.log(freq + 1) * 10  # Logarithmic scaling for visual balance
                        }
                        nodes.append(node)
                        concept_to_id[concept] = node_id
                        node_id += 1
        
        # Add domain-specific concepts
        if 'domain_concept_analysis' in self.domain_analysis:
            for domain, data in self.domain_analysis['domain_concept_analysis'].items():
                if 'unique_concepts' in data:
                    for concept in data['unique_concepts'][:10]:  # Top 10 per domain
                        if concept not in concept_to_id:
                            node = {
                                'id': node_id,
                                'name': concept,
                                'frequency': 1,
                                'category': domain,
                                'type': 'domain',
                                'size': 8
                            }
                            nodes.append(node)
                            concept_to_id[concept] = node_id
                            node_id += 1
        
        return nodes, concept_to_id
    
    def create_concept_edges(self, concept_to_id: Dict) -> List[Dict]:
        """Create edges based on concept co-occurrences and relationships."""
        edges = []
        edge_weights = defaultdict(int)
        
        # Create edges based on category relationships
        if 'concepts_by_category' in self.technical_concepts:
            categories = self.technical_concepts['concepts_by_category']
            
            # Connect concepts within the same category
            for category, concept_list in categories.items():
                if isinstance(concept_list, list):
                    # Extract concept strings from list
                    concept_strings = []
                    for concept in concept_list:
                        if isinstance(concept, str):
                            concept_strings.append(concept)
                        elif isinstance(concept, dict) and 'concept' in concept:
                            concept_strings.append(concept['concept'])
                    
                    # Create edges between concepts in same category
                    for i in range(len(concept_strings)):
                        for j in range(i + 1, len(concept_strings)):
                            if concept_strings[i] in concept_to_id and concept_strings[j] in concept_to_id:
                                key = tuple(sorted([concept_to_id[concept_strings[i]], concept_to_id[concept_strings[j]]]))
                                edge_weights[key] += 1
        
        # Create edges between frequently co-occurring concepts
        # This is a simplified approach - connect top concepts that share domains
        if 'top_100_concepts' in self.technical_concepts:
            top_dict = self.technical_concepts['top_100_concepts']
            # Get top 30 concepts sorted by frequency
            top_concepts = sorted(top_dict.items(), 
                                key=lambda x: x[1]['frequency'] if isinstance(x[1], dict) else x[1], 
                                reverse=True)[:30]
            top_concept_names = [c[0] for c in top_concepts]
            
            # Connect temporal concepts
            temporal_concepts = [c for c in top_concept_names if 'temporal' in c.lower()]
            for i in range(len(temporal_concepts)):
                for j in range(i + 1, len(temporal_concepts)):
                    if temporal_concepts[i] in concept_to_id and temporal_concepts[j] in concept_to_id:
                        key = tuple(sorted([concept_to_id[temporal_concepts[i]], concept_to_id[temporal_concepts[j]]]))
                        edge_weights[key] += 3
            
            # Connect integration concepts
            integration_concepts = [c for c in top_concept_names if any(k in c.lower() for k in ['integration', 'heterogeneous', 'fusion'])]
            for i in range(len(integration_concepts)):
                for j in range(i + 1, len(integration_concepts)):
                    if integration_concepts[i] in concept_to_id and integration_concepts[j] in concept_to_id:
                        key = tuple(sorted([concept_to_id[integration_concepts[i]], concept_to_id[integration_concepts[j]]]))
                        edge_weights[key] += 3
        
        # Convert to edge list
        for (source, target), weight in edge_weights.items():
            edges.append({
                'source': source,
                'target': target,
                'weight': weight,
                'strength': min(weight / 5, 1.0)  # Normalize strength
            })
        
        return edges
    
    def process_research_opportunities(self) -> List[Dict]:
        """Process research gaps and opportunities for the opportunity explorer."""
        opportunities = []
        
        # Process gap opportunities
        if 'gap_opportunities' in self.research_gaps:
            for opp in self.research_gaps['gap_opportunities']:
                processed_opp = {
                    'id': f"gap_{len(opportunities)}",
                    'title': opp['opportunity'],
                    'type': 'research_gap',
                    'importance_score': opp.get('importance_score', 0.5),
                    'concepts': opp.get('concepts', []),
                    'gap_type': opp.get('gap_type', 'unknown'),
                    'description': self._generate_opportunity_description(opp),
                    'tags': self._extract_tags(opp),
                    'maturity': self._assess_maturity(opp)
                }
                opportunities.append(processed_opp)
        
        # Process cross-domain opportunities
        if 'cross_domain_opportunities' in self.cross_domain_opportunities:
            for opp in self.cross_domain_opportunities['cross_domain_opportunities']:
                processed_opp = {
                    'id': f"cross_{len(opportunities)}",
                    'title': opp['opportunity_description'],
                    'type': 'cross_domain',
                    'importance_score': 0.8,  # Cross-domain opportunities are generally high-value
                    'domains': opp.get('domains', []),
                    'shared_concepts': opp.get('shared_concepts', []),
                    'description': opp['opportunity_description'],
                    'tags': ['cross-domain'] + opp.get('domains', []),
                    'maturity': 'emerging'
                }
                opportunities.append(processed_opp)
        
        return opportunities
    
    def create_hierarchical_structure(self, nodes: List[Dict]) -> Dict:
        """Create hierarchical grouping for visualization."""
        hierarchy = {
            'name': 'PKG Research Landscape',
            'children': defaultdict(lambda: {'name': '', 'children': []})
        }
        
        # Group by category
        for node in nodes:
            category = node['category']
            if category not in hierarchy['children']:
                hierarchy['children'][category] = {
                    'name': category.replace('_', ' ').title(),
                    'children': []
                }
            hierarchy['children'][category]['children'].append({
                'name': node['name'],
                'value': node['frequency'],
                'id': node['id']
            })
        
        # Convert defaultdict to regular dict
        hierarchy['children'] = list(hierarchy['children'].values())
        return hierarchy
    
    def _categorize_concept(self, concept: str) -> str:
        """Categorize a concept based on keywords."""
        concept_lower = concept.lower()
        
        if any(term in concept_lower for term in ['temporal', 'time', 'chronological']):
            return 'temporal'
        elif any(term in concept_lower for term in ['heterogeneous', 'multi-modal', 'integration']):
            return 'integration'
        elif any(term in concept_lower for term in ['schema', 'ontology', 'model']):
            return 'schema'
        elif any(term in concept_lower for term in ['privacy', 'security', 'protection']):
            return 'privacy'
        elif any(term in concept_lower for term in ['performance', 'optimization', 'efficiency']):
            return 'performance'
        else:
            return 'general'
    
    def _generate_opportunity_description(self, opp: Dict) -> str:
        """Generate a detailed description for an opportunity."""
        desc_parts = []
        
        if 'concepts' in opp:
            desc_parts.append(f"Combines: {', '.join(opp['concepts'][:3])}")
        
        if 'gap_type' in opp:
            desc_parts.append(f"Gap type: {opp['gap_type']}")
        
        if 'importance_score' in opp:
            importance = 'High' if opp['importance_score'] > 0.7 else 'Medium' if opp['importance_score'] > 0.4 else 'Low'
            desc_parts.append(f"Importance: {importance}")
        
        return " | ".join(desc_parts)
    
    def _extract_tags(self, opp: Dict) -> List[str]:
        """Extract relevant tags from an opportunity."""
        tags = []
        
        # Extract from concepts
        if 'concepts' in opp:
            tags.extend([c.lower().replace(' ', '-') for c in opp['concepts'][:3]])
        
        # Add gap type
        if 'gap_type' in opp:
            tags.append(opp['gap_type'])
        
        return list(set(tags))
    
    def _extract_domain_analysis(self):
        """Extract domain-specific analysis from technical concepts data."""
        self.domain_analysis = {'domain_concept_analysis': {}}
        
        # Extract domains from concepts by category
        if 'concepts_by_category' in self.technical_concepts:
            categories = self.technical_concepts['concepts_by_category']
            
            # Map categories to domains
            domain_mapping = {
                'healthcare': ['healthcare', 'medical', 'clinical', 'patient'],
                'education': ['education', 'learning', 'teaching', 'student'],
                'enterprise': ['enterprise', 'business', 'organization', 'management'],
                'iot': ['iot', 'sensor', 'device', 'smart'],
                'social': ['social', 'network', 'community', 'collaborative']
            }
            
            for domain, keywords in domain_mapping.items():
                domain_concepts = []
                
                # Find concepts that match domain keywords
                for category, concept_list in categories.items():
                    if isinstance(concept_list, list):
                        for concept in concept_list:
                            if isinstance(concept, str) and any(keyword in concept.lower() for keyword in keywords):
                                domain_concepts.append(concept)
                            elif isinstance(concept, dict) and 'concept' in concept:
                                concept_str = concept['concept']
                                if any(keyword in concept_str.lower() for keyword in keywords):
                                    domain_concepts.append(concept_str)
                
                if domain_concepts:
                    self.domain_analysis['domain_concept_analysis'][domain] = {
                        'unique_concepts': list(set(domain_concepts))[:10],
                        'paper_count': len(domain_concepts)
                    }
    
    def _generate_opportunities_from_gaps(self):
        """Generate research opportunities from identified gaps."""
        self.research_gaps = {'gap_opportunities': []}
        
        # Extract gaps from HDM-specific insights
        if 'hdm_specific_insights' in self.technical_concepts:
            insights = self.technical_concepts['hdm_specific_insights']
            
            # Create opportunities from key integration points
            if 'key_integration_points' in insights:
                for point in insights['key_integration_points']:
                    self.research_gaps['gap_opportunities'].append({
                        'opportunity': f"Integration opportunity: {point}",
                        'concepts': self._extract_concepts_from_text(point),
                        'gap_type': 'integration',
                        'importance_score': 0.8
                    })
            
            # Create opportunities from research directions
            if 'research_directions' in insights:
                for direction in insights['research_directions']:
                    gap_type = self._determine_gap_type(direction)
                    self.research_gaps['gap_opportunities'].append({
                        'opportunity': direction,
                        'concepts': self._extract_concepts_from_text(direction),
                        'gap_type': gap_type,
                        'importance_score': 0.7
                    })
        
        # Generate cross-domain opportunities
        self.cross_domain_opportunities = {'cross_domain_opportunities': []}
        
        # Create cross-domain opportunities from domain analysis
        if self.domain_analysis and 'domain_concept_analysis' in self.domain_analysis:
            domains = list(self.domain_analysis['domain_concept_analysis'].keys())
            
            # Create opportunities for promising domain combinations
            domain_pairs = [
                ('healthcare', 'education', 'Patient education and health literacy systems'),
                ('healthcare', 'iot', 'IoT-enabled health monitoring and smart medical devices'),
                ('education', 'enterprise', 'Corporate learning and knowledge management platforms'),
                ('iot', 'social', 'Social IoT networks and collaborative sensing'),
                ('enterprise', 'healthcare', 'Healthcare enterprise resource management')
            ]
            
            for domain1, domain2, description in domain_pairs:
                if domain1 in domains and domain2 in domains:
                    # Find shared concepts between domains
                    concepts1 = set(self.domain_analysis['domain_concept_analysis'][domain1]['unique_concepts'])
                    concepts2 = set(self.domain_analysis['domain_concept_analysis'][domain2]['unique_concepts'])
                    shared = list(concepts1.intersection(concepts2))[:3]
                    
                    self.cross_domain_opportunities['cross_domain_opportunities'].append({
                        'opportunity_description': description,
                        'domains': [domain1, domain2],
                        'shared_concepts': shared if shared else ['knowledge graph', 'integration', 'temporal'],
                        'count': len(shared)
                    })
    
    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract relevant concepts from text based on top concepts."""
        concepts = []
        text_lower = text.lower()
        
        if 'top_100_concepts' in self.technical_concepts:
            top_dict = self.technical_concepts['top_100_concepts']
            # Get top 50 concepts sorted by frequency
            top_concepts = sorted(top_dict.items(), 
                                key=lambda x: x[1]['frequency'] if isinstance(x[1], dict) else x[1], 
                                reverse=True)[:50]
            
            for concept, data in top_concepts:
                if concept.lower() in text_lower:
                    concepts.append(concept)
        
        return concepts[:3]
    
    def _determine_gap_type(self, text: str) -> str:
        """Determine gap type from text content."""
        text_lower = text.lower()
        if 'temporal' in text_lower:
            return 'temporal'
        elif 'privacy' in text_lower or 'security' in text_lower:
            return 'privacy'
        elif 'performance' in text_lower:
            return 'performance'
        elif 'domain' in text_lower or 'cross' in text_lower:
            return 'cross-domain'
        else:
            return 'integration'
    
    def _assess_maturity(self, opp: Dict) -> str:
        """Assess the research maturity level of an opportunity."""
        if 'importance_score' in opp:
            if opp['importance_score'] > 0.8:
                return 'early_stage'
            elif opp['importance_score'] > 0.5:
                return 'emerging'
            else:
                return 'established'
        return 'unknown'
    
    def generate_visualization_data(self):
        """Generate the complete visualization dataset."""
        print("Creating concept nodes...")
        nodes, concept_to_id = self.create_concept_nodes()
        
        print("Creating concept edges...")
        edges = self.create_concept_edges(concept_to_id)
        
        print("Processing research opportunities...")
        opportunities = self.process_research_opportunities()
        
        print("Creating hierarchical structure...")
        hierarchy = self.create_hierarchical_structure(nodes)
        
        # Compile final dataset
        visualization_data = {
            'metadata': {
                'total_concepts': len(nodes),
                'total_edges': len(edges),
                'total_opportunities': len(opportunities),
                'categories': list(set(node['category'] for node in nodes)),
                'domains': list(set(node['category'] for node in nodes if node['type'] == 'domain'))
            },
            'network': {
                'nodes': nodes,
                'edges': edges
            },
            'hierarchy': hierarchy,
            'opportunities': opportunities,
            'filters': {
                'categories': sorted(list(set(node['category'] for node in nodes))),
                'types': ['technical', 'domain'],
                'maturity_levels': ['early_stage', 'emerging', 'established'],
                'gap_types': sorted(list(set(opp.get('gap_type', 'unknown') for opp in opportunities)))
            }
        }
        
        return visualization_data
    
    def save_visualization_data(self, data: Dict):
        """Save the processed visualization data."""
        output_path = os.path.join(self.base_dir, 'visualization', 'pkg_research_explorer', 'data', 'visualization_data.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nVisualization data saved to: {output_path}")
        print(f"Total concepts: {data['metadata']['total_concepts']}")
        print(f"Total relationships: {data['metadata']['total_edges']}")
        print(f"Total opportunities: {data['metadata']['total_opportunities']}")

def main():
    processor = VisualizationDataProcessor()
    processor.load_analysis_files()
    visualization_data = processor.generate_visualization_data()
    processor.save_visualization_data(visualization_data)

if __name__ == "__main__":
    main()