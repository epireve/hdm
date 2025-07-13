#!/usr/bin/env python3
"""
Technical Concept Extraction from Research Papers Dataset
Extracts algorithms, frameworks, methodologies, and architectures from research papers
focusing on heterogeneous data integration, temporal-first architectures, and bespoke PKG systems.
"""

import csv
import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
from datetime import datetime

class TechnicalConceptExtractor:
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.papers = []
        self.concept_database = defaultdict(lambda: {
            'frequency': 0,
            'papers': [],
            'contexts': [],
            'category': '',
            'performance_metrics': [],
            'domains': set()
        })
        
        # Define technical concept patterns with categories
        self.concept_patterns = {
            'algorithms': [
                r'\b(?:Graph Neural Networks?|GNN|GCN|GAT|GraphSAGE|Graph Attention Networks?)\b',
                r'\b(?:Temporal Convolution|Temporal CNN|LSTM|GRU|Transformer|BERT|GPT|T5)\b',
                r'\b(?:Entity Resolution|Entity Linking|Entity Matching|Record Linkage)\b',
                r'\b(?:Knowledge Graph Embedding|TransE|TransR|RotatE|ComplEx|DistMult)\b',
                r'\b(?:Federated Learning|Distributed Learning|Multi-task Learning)\b',
                r'\b(?:Ontology Alignment|Schema Matching|Schema Mapping)\b',
                r'\b(?:Named Entity Recognition|NER|Part-of-Speech|POS|Dependency Parsing)\b',
                r'\b(?:Reinforcement Learning|Deep Q-Learning|Policy Gradient)\b',
                r'\b(?:Attention Mechanism|Self-Attention|Cross-Attention|Multi-Head Attention)\b',
                r'\b(?:Convolutional Neural Network|CNN|Recurrent Neural Network|RNN)\b',
                r'\b(?:Random Forest|Support Vector Machine|SVM|Decision Tree|Gradient Boosting)\b',
                r'\b(?:Clustering|K-Means|Hierarchical Clustering|DBSCAN)\b',
                r'\b(?:Dimensionality Reduction|PCA|t-SNE|UMAP)\b',
                r'\b(?:Natural Language Processing|NLP|Text Mining|Information Extraction)\b',
                r'\b(?:Computer Vision|Image Processing|Object Detection|Image Classification)\b',
                r'\b(?:Collaborative Filtering|Matrix Factorization|Recommendation Algorithm)\b',
                r'\b(?:Bayesian Network|Probabilistic Graphical Model|Markov Chain)\b',
                r'\b(?:Ensemble Learning|Bagging|Boosting|Stacking)\b',
                r'\b(?:Feature Engineering|Feature Selection|Feature Extraction)\b',
                r'\b(?:Cross-Validation|Hyperparameter Tuning|Grid Search)\b'
            ],
            'frameworks_tools': [
                r'\b(?:Neo4j|ArangoDB|JanusGraph|TigerGraph|Amazon Neptune)\b',
                r'\b(?:Apache Jena|RDF4J|Virtuoso|Blazegraph|GraphDB)\b',
                r'\b(?:Apache Spark|Hadoop|Kafka|Flink|Storm)\b',
                r'\b(?:TensorFlow|PyTorch|Keras|Scikit-learn|Pandas)\b',
                r'\b(?:Docker|Kubernetes|Apache Airflow|Jenkins)\b',
                r'\b(?:Elasticsearch|Solr|Lucene|Apache Tika)\b',
                r'\b(?:MongoDB|PostgreSQL|MySQL|Redis|Cassandra)\b',
                r'\b(?:Apache Beam|Apache NiFi|Talend|Pentaho)\b',
                r'\b(?:Jupyter|Google Colab|Apache Zeppelin)\b',
                r'\b(?:OpenAI|Hugging Face|spaCy|NLTK|Gensim)\b',
                r'\b(?:D3\.js|Plotly|Matplotlib|Seaborn|Bokeh)\b',
                r'\b(?:REST API|GraphQL|gRPC|WebSocket)\b',
                r'\b(?:Git|GitHub|GitLab|Bitbucket)\b',
                r'\b(?:AWS|Azure|Google Cloud|IBM Cloud)\b',
                r'\b(?:Prometheus|Grafana|ELK Stack|Splunk)\b'
            ],
            'methodologies': [
                r'\b(?:Schema Harmonization|Schema Integration|Schema Evolution)\b',
                r'\b(?:Temporal Modeling|Time-series Analysis|Temporal Reasoning)\b',
                r'\b(?:Multi-modal Fusion|Multi-source Integration|Heterogeneous Data Fusion)\b',
                r'\b(?:Upstream Data Orchestration|Data Pipeline|ETL|ELT)\b',
                r'\b(?:Real-time Processing|Stream Processing|Batch Processing)\b',
                r'\b(?:Data Quality Assessment|Data Validation|Data Cleansing)\b',
                r'\b(?:Semantic Interoperability|Ontology Mapping|Knowledge Integration)\b',
                r'\b(?:Federated Query|Distributed Query|Query Optimization)\b',
                r'\b(?:Privacy-preserving|Differential Privacy|Homomorphic Encryption)\b',
                r'\b(?:Incremental Learning|Online Learning|Continual Learning)\b',
                r'\b(?:Zero-shot Learning|Few-shot Learning|Meta-learning)\b',
                r'\b(?:Cross-domain Transfer|Domain Adaptation|Transfer Learning)\b',
                r'\b(?:Explainable AI|Interpretable ML|Model Explainability)\b',
                r'\b(?:Automated ML|AutoML|Neural Architecture Search)\b',
                r'\b(?:Data Augmentation|Synthetic Data Generation|GAN)\b',
                r'\b(?:Active Learning|Semi-supervised Learning|Weakly Supervised)\b',
                r'\b(?:Causal Inference|Causal Discovery|Causal Reasoning)\b',
                r'\b(?:Anomaly Detection|Outlier Detection|Fraud Detection)\b',
                r'\b(?:Sentiment Analysis|Opinion Mining|Emotion Recognition)\b',
                r'\b(?:Topic Modeling|Latent Dirichlet Allocation|LDA)\b'
            ],
            'architectures': [
                r'\b(?:Temporal-first Architecture|Event-driven Architecture|Microservices)\b',
                r'\b(?:Federated Architecture|Distributed Architecture|Service-oriented Architecture)\b',
                r'\b(?:Lambda Architecture|Kappa Architecture|Delta Architecture)\b',
                r'\b(?:Master-slave Architecture|Peer-to-peer|P2P)\b',
                r'\b(?:Client-server Architecture|Three-tier Architecture|N-tier)\b',
                r'\b(?:Hexagonal Architecture|Clean Architecture|Layered Architecture)\b',
                r'\b(?:CQRS|Command Query Responsibility Segregation|Event Sourcing)\b',
                r'\b(?:Pub-sub|Publisher-subscriber|Message Queue)\b',
                r'\b(?:Load Balancing|Horizontal Scaling|Vertical Scaling)\b',
                r'\b(?:Caching Strategy|CDN|Content Delivery Network)\b',
                r'\b(?:Serverless Architecture|Function as a Service|FaaS)\b',
                r'\b(?:Edge Computing|Fog Computing|Cloud Computing)\b',
                r'\b(?:Hybrid Cloud|Multi-cloud|On-premises)\b',
                r'\b(?:API Gateway|Service Mesh|Sidecar Pattern)\b',
                r'\b(?:Circuit Breaker|Bulkhead Pattern|Retry Pattern)\b'
            ],
            'data_integration': [
                r'\b(?:Data Lake|Data Warehouse|Data Mart|Data Hub)\b',
                r'\b(?:Data Mesh|Data Fabric|Data Virtualization)\b',
                r'\b(?:Master Data Management|MDM|Data Governance)\b',
                r'\b(?:Change Data Capture|CDC|Data Replication)\b',
                r'\b(?:Data Lineage|Data Provenance|Data Catalog)\b',
                r'\b(?:Data Streaming|Kafka Streaming|Kinesis)\b',
                r'\b(?:Data Transformation|Data Mapping|Data Enrichment)\b',
                r'\b(?:Schema Registry|Data Schema|Avro|Parquet)\b',
                r'\b(?:Data Synchronization|Data Consistency|ACID Properties)\b',
                r'\b(?:Data Partitioning|Data Sharding|Data Distribution)\b',
                r'\b(?:Data Compression|Data Deduplication|Data Archiving)\b',
                r'\b(?:Data Security|Data Encryption|Data Masking)\b',
                r'\b(?:Data Backup|Data Recovery|Disaster Recovery)\b',
                r'\b(?:Data Migration|Data Import|Data Export)\b',
                r'\b(?:Data Standardization|Data Normalization|Data Validation)\b'
            ],
            'knowledge_graph': [
                r'\b(?:Personal Knowledge Graph|PKG|Enterprise Knowledge Graph)\b',
                r'\b(?:Bespoke PKG|Custom Knowledge Graph|Domain-specific KG)\b',
                r'\b(?:Knowledge Graph Construction|KG Building|Graph Generation)\b',
                r'\b(?:Knowledge Graph Completion|Link Prediction|Triple Completion)\b',
                r'\b(?:Knowledge Graph Querying|SPARQL|Cypher|Gremlin)\b',
                r'\b(?:Knowledge Graph Visualization|Graph Visualization|Network Visualization)\b',
                r'\b(?:Knowledge Graph Reasoning|Logical Reasoning|Inference)\b',
                r'\b(?:Knowledge Graph Alignment|Graph Matching|Graph Merging)\b',
                r'\b(?:Knowledge Graph Quality|Graph Validation|Quality Assessment)\b',
                r'\b(?:Knowledge Graph Evolution|Graph Updates|Dynamic KG)\b',
                r'\b(?:Temporal Knowledge Graph|Time-aware KG|Temporal Reasoning)\b',
                r'\b(?:Multi-modal Knowledge Graph|Multimedia KG|Heterogeneous KG)\b',
                r'\b(?:Knowledge Graph Embedding|Graph Representation Learning)\b',
                r'\b(?:Knowledge Graph Mining|Graph Analytics|Graph Algorithms)\b',
                r'\b(?:Knowledge Graph Integration|Graph Fusion|Graph Combination)\b'
            ],
            'performance_metrics': [
                r'\b(?:Precision|Recall|F1-score|F-measure|Accuracy)\b',
                r'\b(?:AUC|ROC|Area Under Curve|Receiver Operating Characteristic)\b',
                r'\b(?:BLEU|ROUGE|METEOR|CIDEr|BERT Score)\b',
                r'\b(?:Mean Absolute Error|MAE|Root Mean Square Error|RMSE)\b',
                r'\b(?:Mean Reciprocal Rank|MRR|Normalized Discounted Cumulative Gain|NDCG)\b',
                r'\b(?:Hits@K|Hits@1|Hits@10|Top-K Accuracy)\b',
                r'\b(?:Latency|Throughput|Response Time|Processing Time)\b',
                r'\b(?:Scalability|Memory Usage|CPU Usage|GPU Usage)\b',
                r'\b(?:Compression Ratio|Storage Efficiency|I/O Operations)\b',
                r'\b(?:Availability|Reliability|Fault Tolerance|Uptime)\b'
            ]
        }
        
        # Additional domain-specific patterns for HDM focus
        self.hdm_specific_patterns = [
            r'\b(?:Human Digital Memory|HDM|Personal Data Management)\b',
            r'\b(?:Heterogeneous Data Integration|Multi-source Data Fusion|Cross-domain Integration)\b',
            r'\b(?:Temporal-first|Time-centric|Chronological Modeling)\b',
            r'\b(?:Upstream Data Orchestration|Early-stage Integration|Source-level Processing)\b',
            r'\b(?:Schema Harmonization|Dynamic Schema|Adaptive Schema)\b',
            r'\b(?:Bespoke System|Custom Architecture|Domain-specific Design)\b',
            r'\b(?:Cross-platform Integration|Multi-device Synchronization|Unified Data Model)\b',
            r'\b(?:Privacy-preserving Integration|Secure Data Fusion|Federated Privacy)\b',
            r'\b(?:Real-time Validation|Quality Assessment|Data Provenance)\b',
            r'\b(?:Semantic Harmonization|Ontology Alignment|Knowledge Unification)\b'
        ]
        
        # Performance metrics patterns
        self.performance_patterns = [
            r'(\d+(?:\.\d+)?)\s*%\s*(?:accuracy|precision|recall|F1|improvement)',
            r'(\d+(?:\.\d+)?)\s*%\s*(?:reduction|decrease|improvement)\s*in\s*(?:latency|time|memory)',
            r'(\d+(?:\.\d+)?)\s*x\s*(?:faster|speedup|improvement)',
            r'(\d+(?:\.\d+)?)\s*(?:ms|seconds?|minutes?)\s*(?:response|processing|execution)\s*time',
            r'(?:Hits@\d+|F1|Precision|Recall|Accuracy):\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*(?:GB|MB|KB)\s*(?:memory|storage|size)',
            r'(\d+(?:\.\d+)?)\s*(?:QPS|TPS|queries per second|transactions per second)'
        ]
        
    def load_papers(self):
        """Load papers from CSV file"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.papers = list(reader)
            print(f"Loaded {len(self.papers)} papers from {self.csv_file_path}")
        except Exception as e:
            print(f"Error loading papers: {e}")
            return False
        return True
    
    def extract_concepts_from_text(self, text: str, paper_id: str) -> Dict[str, List[str]]:
        """Extract technical concepts from text using regex patterns"""
        if not text or text.strip() == '' or text.lower() == 'nan':
            return {}
        
        concepts_found = {}
        text_lower = text.lower()
        
        # Extract concepts by category
        for category, patterns in self.concept_patterns.items():
            concepts_found[category] = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    concepts_found[category].extend(matches)
        
        # Extract HDM-specific concepts
        hdm_concepts = []
        for pattern in self.hdm_specific_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                hdm_concepts.extend(matches)
        
        if hdm_concepts:
            concepts_found['hdm_specific'] = hdm_concepts
        
        return concepts_found
    
    def extract_performance_metrics(self, text: str) -> List[str]:
        """Extract performance metrics from text"""
        if not text or text.strip() == '' or text.lower() == 'nan':
            return []
        
        metrics = []
        for pattern in self.performance_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                metrics.extend(matches)
        
        return metrics
    
    def process_papers(self):
        """Process all papers and extract technical concepts"""
        if not self.papers:
            print("No papers loaded. Please load papers first.")
            return
        
        print("Processing papers for technical concept extraction...")
        
        # Key columns to analyze for technical concepts
        key_columns = [
            'Methodology', 'Key Findings', 'Implementation Insights', 
            'Summary', 'Primary Outcomes', 'Insights', 'TL;DR',
            'Research Question', 'Conclusion', 'Future Work', 'Tags'
        ]
        
        processed_count = 0
        
        for paper in self.papers:
            paper_id = paper.get('cite_key', paper.get('title', f'paper_{processed_count}'))
            paper_title = paper.get('title', 'Unknown Title')
            paper_year = paper.get('year', 'Unknown Year')
            paper_authors = paper.get('authors', 'Unknown Authors')
            paper_domain = self.determine_domain(paper)
            
            # Extract concepts from all relevant columns
            all_concepts = {}
            all_performance_metrics = []
            
            for column in key_columns:
                if column in paper and paper[column]:
                    concepts = self.extract_concepts_from_text(paper[column], paper_id)
                    metrics = self.extract_performance_metrics(paper[column])
                    
                    all_performance_metrics.extend(metrics)
                    
                    # Merge concepts by category
                    for category, concept_list in concepts.items():
                        if category not in all_concepts:
                            all_concepts[category] = []
                        all_concepts[category].extend(concept_list)
            
            # Update concept database
            for category, concept_list in all_concepts.items():
                for concept in concept_list:
                    concept_normalized = concept.strip().lower()
                    if concept_normalized:
                        self.concept_database[concept_normalized]['frequency'] += 1
                        self.concept_database[concept_normalized]['category'] = category
                        self.concept_database[concept_normalized]['papers'].append({
                            'id': paper_id,
                            'title': paper_title,
                            'year': paper_year,
                            'authors': paper_authors
                        })
                        self.concept_database[concept_normalized]['domains'].add(paper_domain)
                        
                        # Add performance metrics if any
                        if all_performance_metrics:
                            self.concept_database[concept_normalized]['performance_metrics'].extend(all_performance_metrics)
            
            processed_count += 1
            if processed_count % 50 == 0:
                print(f"Processed {processed_count} papers...")
        
        print(f"Completed processing {processed_count} papers")
        print(f"Total unique concepts found: {len(self.concept_database)}")
    
    def determine_domain(self, paper: Dict) -> str:
        """Determine the domain of a paper based on its content"""
        content = (paper.get('title', '') + ' ' + 
                  paper.get('Summary', '') + ' ' + 
                  paper.get('Tags', '')).lower()
        
        domain_keywords = {
            'healthcare': ['health', 'medical', 'clinical', 'patient', 'diagnosis', 'treatment'],
            'education': ['learning', 'education', 'student', 'curriculum', 'pedagogical', 'mooc'],
            'enterprise': ['business', 'enterprise', 'corporate', 'organization', 'company'],
            'social': ['social', 'network', 'communication', 'collaboration', 'community'],
            'iot': ['iot', 'sensor', 'device', 'smart', 'embedded', 'wireless'],
            'finance': ['financial', 'banking', 'investment', 'trading', 'fintech'],
            'general': []
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content for keyword in keywords):
                return domain
        
        return 'general'
    
    def get_top_concepts(self, n: int = 100) -> List[Tuple[str, Dict]]:
        """Get top N concepts by frequency"""
        sorted_concepts = sorted(
            self.concept_database.items(), 
            key=lambda x: x[1]['frequency'], 
            reverse=True
        )
        return sorted_concepts[:n]
    
    def categorize_concepts(self) -> Dict[str, List[Tuple[str, Dict]]]:
        """Categorize concepts by type"""
        categorized = defaultdict(list)
        
        for concept, data in self.concept_database.items():
            category = data['category']
            categorized[category].append((concept, data))
        
        # Sort each category by frequency
        for category in categorized:
            categorized[category].sort(key=lambda x: x[1]['frequency'], reverse=True)
        
        return dict(categorized)
    
    def generate_report(self) -> Dict:
        """Generate comprehensive technical concepts report"""
        top_concepts = self.get_top_concepts(100)
        categorized = self.categorize_concepts()
        
        # Generate statistics
        stats = {
            'total_papers_processed': len(self.papers),
            'total_unique_concepts': len(self.concept_database),
            'concepts_by_category': {cat: len(concepts) for cat, concepts in categorized.items()},
            'top_domains': self.get_top_domains(),
            'processing_date': datetime.now().isoformat()
        }
        
        # Prepare detailed concept data
        detailed_concepts = {}
        for i, (concept, data) in enumerate(top_concepts, 1):
            detailed_concepts[concept] = {
                'rank': i,
                'frequency': data['frequency'],
                'category': data['category'],
                'domains': list(data['domains']),
                'paper_count': len(data['papers']),
                'sample_papers': data['papers'][:5],  # Top 5 papers
                'performance_metrics': list(set(data['performance_metrics']))[:10]  # Top 10 unique metrics
            }
        
        report = {
            'statistics': stats,
            'top_100_concepts': detailed_concepts,
            'concepts_by_category': {
                cat: [(concept, data['frequency']) for concept, data in concepts[:20]]
                for cat, concepts in categorized.items()
            },
            'hdm_specific_insights': self.generate_hdm_insights(),
            'methodology_summary': self.generate_methodology_summary()
        }
        
        return report
    
    def get_top_domains(self) -> Dict[str, int]:
        """Get top domains by concept frequency"""
        domain_counts = defaultdict(int)
        
        for concept, data in self.concept_database.items():
            for domain in data['domains']:
                domain_counts[domain] += data['frequency']
        
        return dict(sorted(domain_counts.items(), key=lambda x: x[1], reverse=True))
    
    def generate_hdm_insights(self) -> Dict:
        """Generate insights specific to HDM research focus"""
        hdm_concepts = []
        temporal_concepts = []
        integration_concepts = []
        
        for concept, data in self.concept_database.items():
            if data['category'] == 'hdm_specific':
                hdm_concepts.append((concept, data['frequency']))
            elif 'temporal' in concept or 'time' in concept:
                temporal_concepts.append((concept, data['frequency']))
            elif 'integration' in concept or 'fusion' in concept or 'harmonization' in concept:
                integration_concepts.append((concept, data['frequency']))
        
        return {
            'hdm_specific_concepts': sorted(hdm_concepts, key=lambda x: x[1], reverse=True)[:10],
            'temporal_concepts': sorted(temporal_concepts, key=lambda x: x[1], reverse=True)[:10],
            'integration_concepts': sorted(integration_concepts, key=lambda x: x[1], reverse=True)[:10]
        }
    
    def generate_methodology_summary(self) -> Dict:
        """Generate summary of methodological approaches"""
        method_freq = defaultdict(int)
        
        for concept, data in self.concept_database.items():
            if data['category'] == 'methodologies':
                method_freq[concept] += data['frequency']
        
        return {
            'top_methodologies': sorted(method_freq.items(), key=lambda x: x[1], reverse=True)[:15],
            'total_methodological_concepts': len(method_freq)
        }
    
    def save_report(self, filename: str = 'technical_concepts_extracted.json'):
        """Save the complete technical concepts report"""
        report = self.generate_report()
        
        # Convert sets to lists for JSON serialization
        def convert_sets_to_lists(obj):
            if isinstance(obj, dict):
                return {k: convert_sets_to_lists(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets_to_lists(item) for item in obj]
            elif isinstance(obj, set):
                return list(obj)
            else:
                return obj
        
        report = convert_sets_to_lists(report)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Technical concepts report saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False

def main():
    """Main execution function"""
    csv_file = '/Users/invoture/dev.local/hdm/hdm_research_papers_complete_20250710.csv'
    
    print("=== Technical Concept Extraction from HDM Research Papers ===")
    print(f"Dataset: {csv_file}")
    print("Focus: Heterogeneous Data Integration, Temporal-first Architectures, Bespoke PKG Systems")
    print()
    
    # Initialize extractor
    extractor = TechnicalConceptExtractor(csv_file)
    
    # Load and process papers
    if not extractor.load_papers():
        print("Failed to load papers. Exiting.")
        return
    
    # Extract concepts
    extractor.process_papers()
    
    # Generate and save report
    report = extractor.generate_report()
    extractor.save_report()
    
    # Print summary
    print("\n=== EXTRACTION SUMMARY ===")
    print(f"Papers processed: {report['statistics']['total_papers_processed']}")
    print(f"Unique concepts found: {report['statistics']['total_unique_concepts']}")
    print(f"Concepts by category:")
    for category, count in report['statistics']['concepts_by_category'].items():
        print(f"  {category}: {count} concepts")
    
    print(f"\nTop 10 most frequent concepts:")
    for i, (concept, data) in enumerate(list(report['top_100_concepts'].items())[:10], 1):
        print(f"  {i}. {concept} ({data['frequency']} occurrences, {data['category']})")
    
    print(f"\nTop domains by concept frequency:")
    for domain, count in list(report['statistics']['top_domains'].items())[:5]:
        print(f"  {domain}: {count} total concept occurrences")
    
    print(f"\nHDM-specific insights:")
    if report['hdm_specific_insights']['hdm_specific_concepts']:
        print("  HDM-specific concepts found:")
        for concept, freq in report['hdm_specific_insights']['hdm_specific_concepts'][:5]:
            print(f"    {concept}: {freq} occurrences")
    
    print(f"\nReport saved to: technical_concepts_extracted.json")

if __name__ == "__main__":
    main()