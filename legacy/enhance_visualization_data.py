#!/usr/bin/env python3
"""
Enhance visualization data with domain information and gap analysis
"""

import json
from typing import Dict, List, Any

def enhance_visualization_data():
    """Enhance the PKG Explorer visualization data with domain and gap analysis information"""
    
    # Load existing visualization data
    with open('/Users/invoture/dev.local/hdm/visualization/pkg_research_explorer/data/visualization_data.json', 'r') as f:
        viz_data = json.load(f)
    
    # Load technical concepts data
    with open('/Users/invoture/dev.local/hdm/technical_concepts_extracted.json', 'r') as f:
        concepts_data = json.load(f)
    
    # Create a mapping from concept names to domain information
    domain_mapping = {}
    for concept_name, concept_info in concepts_data.get('top_100_concepts', {}).items():
        domain_mapping[concept_name.lower()] = concept_info.get('domains', [])
    
    # Enhance nodes with domain information
    enhanced_nodes = []
    for node in viz_data['network']['nodes']:
        # Find matching concept in technical concepts data
        concept_name = node['name'].lower()
        if concept_name in domain_mapping:
            node['domains'] = domain_mapping[concept_name]
        else:
            # Default domain assignment based on concept characteristics
            node['domains'] = assign_default_domains(node)
        
        enhanced_nodes.append(node)
    
    # Update metadata
    viz_data['metadata']['domains'] = [
        'education', 'healthcare', 'social', 'iot', 'enterprise', 'general'
    ]
    viz_data['metadata']['total_opportunities'] = 926  # From gap analysis
    viz_data['metadata']['high_opportunity_concepts'] = [
        'pkg', 'heterogeneous data integration', 'temporal reasoning', 'privacy preserving'
    ]
    viz_data['metadata']['research_gaps'] = {
        'concept_intersections': 926,
        'cross_domain_opportunities': 52,
        'temporal_evolution_gaps': 0,
        'university_collaboration_ready': 26
    }
    
    # Update network nodes
    viz_data['network']['nodes'] = enhanced_nodes
    
    # Add gap analysis information
    viz_data['gap_analysis'] = {
        'high_opportunity_indicators': [
            'pkg', 'heterogeneous data integration', 'temporal reasoning', 'privacy preserving'
        ],
        'emerging_concepts': [node['name'] for node in enhanced_nodes if node['frequency'] < 5],
        'cross_domain_potential': [
            node['name'] for node in enhanced_nodes 
            if node.get('domains') and len(node['domains']) > 2
        ]
    }
    
    # Save enhanced data
    with open('/Users/invoture/dev.local/hdm/visualization/pkg_research_explorer/data/visualization_data.json', 'w') as f:
        json.dump(viz_data, f, indent=2)
    
    print("Enhanced visualization data with domain information and gap analysis")
    print(f"- Total concepts: {len(enhanced_nodes)}")
    print(f"- Concepts with domains: {len([n for n in enhanced_nodes if n.get('domains')])}")
    print(f"- Cross-domain concepts: {len([n for n in enhanced_nodes if n.get('domains') and len(n['domains']) > 2])}")
    
    return viz_data

def assign_default_domains(node: Dict[str, Any]) -> List[str]:
    """Assign default domains based on concept characteristics"""
    concept_name = node['name'].lower()
    category = node.get('category', '').lower()
    
    # Domain assignment based on concept name patterns
    if any(term in concept_name for term in ['learn', 'education', 'student', 'curriculum']):
        return ['education', 'general']
    elif any(term in concept_name for term in ['health', 'medical', 'clinical', 'patient']):
        return ['healthcare', 'general']
    elif any(term in concept_name for term in ['social', 'network', 'collaboration', 'community']):
        return ['social', 'general']
    elif any(term in concept_name for term in ['iot', 'sensor', 'device', 'smart']):
        return ['iot', 'general']
    elif any(term in concept_name for term in ['enterprise', 'business', 'organization']):
        return ['enterprise', 'general']
    elif category in ['knowledge_graph', 'hdm_specific']:
        return ['general', 'education', 'healthcare', 'enterprise']
    elif category == 'algorithms':
        return ['general', 'education', 'healthcare']
    elif category == 'data_integration':
        return ['enterprise', 'healthcare', 'general']
    else:
        return ['general']

if __name__ == "__main__":
    enhance_visualization_data()