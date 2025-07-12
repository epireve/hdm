"""
Cleanup helper utilities for identifying and removing redundant files.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from collections import defaultdict

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus, Config


@dataclass
class FileInfo:
    """Information about a file for cleanup analysis."""
    path: Path
    size: int
    hash: str
    type: str
    last_modified: float


@dataclass
class CleanupSuggestion:
    """Suggestion for cleaning up files."""
    action: str  # 'delete', 'archive', 'consolidate'
    files: List[Path]
    reason: str
    space_saved: int
    risk_level: str = "low"  # low, medium, high


class CleanupHelper(BaseProcessor):
    """Helper for identifying and cleaning up redundant files."""
    
    def __init__(self, config: Config):
        super().__init__(config, "CleanupHelper")
        self.ignore_patterns = {
            '*.pyc', '__pycache__', '.DS_Store', '*.tmp', '*.log',
            '.pytest_cache', '.mypy_cache', '*.egg-info',
            'node_modules', '.git', '.venv', 'venv'
        }
    
    def process_item(self, item, **kwargs) -> ProcessingResult:
        """Process item interface - delegates to analyze_project."""
        if isinstance(item, Path):
            return self.analyze_project(item)
        else:
            return self.analyze_project()
        
    def analyze_project(self, base_path: Optional[Path] = None) -> ProcessingResult:
        """Analyze project for cleanup opportunities."""
        if base_path is None:
            base_path = self.config.paths.base_dir
            
        try:
            self.logger.info(f"Analyzing project at {base_path}")
            
            # Scan all files
            all_files = self._scan_files(base_path)
            
            # Find duplicates
            duplicates = self._find_duplicates(all_files)
            
            # Find large files
            large_files = self._find_large_files(all_files)
            
            # Find redundant scripts
            redundant_scripts = self._find_redundant_scripts(all_files)
            
            # Find temporary files
            temp_files = self._find_temporary_files(all_files)
            
            # Generate cleanup suggestions
            suggestions = self._generate_suggestions(
                duplicates, large_files, redundant_scripts, temp_files
            )
            
            # Calculate total potential space savings
            total_space = sum(s.space_saved for s in suggestions)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Found {len(suggestions)} cleanup opportunities",
                data={
                    'total_files_scanned': len(all_files),
                    'duplicate_groups': len(duplicates),
                    'large_files': len(large_files),
                    'redundant_scripts': len(redundant_scripts),
                    'temp_files': len(temp_files),
                    'cleanup_suggestions': [s.__dict__ for s in suggestions],
                    'potential_space_saved_mb': total_space / (1024 * 1024)
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Analysis failed: {str(e)}",
                error=e
            )
    
    def _scan_files(self, base_path: Path) -> List[FileInfo]:
        """Scan all files in the project."""
        files = []
        
        for root, dirs, filenames in os.walk(base_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(d)]
            
            for filename in filenames:
                if self._should_ignore(filename):
                    continue
                    
                file_path = Path(root) / filename
                try:
                    stat = file_path.stat()
                    file_hash = self._calculate_file_hash(file_path)
                    
                    files.append(FileInfo(
                        path=file_path,
                        size=stat.st_size,
                        hash=file_hash,
                        type=self._get_file_type(file_path),
                        last_modified=stat.st_mtime
                    ))
                except (OSError, PermissionError):
                    continue
        
        return files
    
    def _should_ignore(self, name: str) -> bool:
        """Check if file/directory should be ignored."""
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except (OSError, PermissionError):
            return ""
        return hash_md5.hexdigest()
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type from extension."""
        suffix = file_path.suffix.lower()
        type_map = {
            '.py': 'python',
            '.csv': 'csv_data',
            '.json': 'json_data',
            '.md': 'markdown',
            '.txt': 'text',
            '.log': 'log',
            '.pdf': 'pdf',
            '.yml': 'yaml',
            '.yaml': 'yaml'
        }
        return type_map.get(suffix, 'other')
    
    def _find_duplicates(self, files: List[FileInfo]) -> List[List[FileInfo]]:
        """Find duplicate files by content hash."""
        hash_groups = defaultdict(list)
        
        for file_info in files:
            if file_info.hash and file_info.size > 0:
                hash_groups[file_info.hash].append(file_info)
        
        # Return groups with more than one file
        return [group for group in hash_groups.values() if len(group) > 1]
    
    def _find_large_files(self, files: List[FileInfo]) -> List[FileInfo]:
        """Find files larger than 10MB."""
        large_threshold = 10 * 1024 * 1024  # 10MB
        return [f for f in files if f.size > large_threshold]
    
    def _find_redundant_scripts(self, files: List[FileInfo]) -> List[List[FileInfo]]:
        """Find potentially redundant Python scripts."""
        python_files = [f for f in files if f.type == 'python']
        
        # Group by similar names
        name_groups = defaultdict(list)
        
        for file_info in python_files:
            # Extract base name without version/variant suffixes
            base_name = self._extract_base_name(file_info.path.name)
            name_groups[base_name].append(file_info)
        
        # Return groups with multiple files
        redundant_groups = []
        for group in name_groups.values():
            if len(group) > 1:
                # Sort by modification time (newest first)
                group.sort(key=lambda x: x.last_modified, reverse=True)
                redundant_groups.append(group)
        
        return redundant_groups
    
    def _extract_base_name(self, filename: str) -> str:
        """Extract base name from filename, removing version suffixes."""
        # Remove extension
        base = filename.rsplit('.', 1)[0]
        
        # Remove common version patterns
        patterns = [
            r'_v\d+$', r'_version\d+$', r'_\d+$', 
            r'_final$', r'_new$', r'_old$', r'_backup$',
            r'_temp$', r'_tmp$', r'_test$', r'_simple$',
            r'_minimal$', r'_large$', r'_concurrent$'
        ]
        
        for pattern in patterns:
            base = re.sub(pattern, '', base, flags=re.IGNORECASE)
        
        return base
    
    def _find_temporary_files(self, files: List[FileInfo]) -> List[FileInfo]:
        """Find temporary and cache files."""
        temp_patterns = [
            r'.*\.tmp$', r'.*\.temp$', r'.*\.cache$',
            r'.*_temp\..*$', r'.*_tmp\..*$', r'.*_backup\..*$',
            r'.*checkpoint.*\.json$', r'.*\.log$'
        ]
        
        temp_files = []
        for file_info in files:
            filename = file_info.path.name.lower()
            for pattern in temp_patterns:
                if re.match(pattern, filename):
                    temp_files.append(file_info)
                    break
        
        return temp_files
    
    def _generate_suggestions(self, duplicates: List[List[FileInfo]], 
                            large_files: List[FileInfo],
                            redundant_scripts: List[List[FileInfo]],
                            temp_files: List[FileInfo]) -> List[CleanupSuggestion]:
        """Generate cleanup suggestions."""
        suggestions = []
        
        # Handle duplicates
        for dup_group in duplicates:
            # Keep the most recent, suggest archiving others
            keeper = max(dup_group, key=lambda x: x.last_modified)
            to_archive = [f for f in dup_group if f != keeper]
            
            if to_archive:
                space_saved = sum(f.size for f in to_archive)
                suggestions.append(CleanupSuggestion(
                    action="archive",
                    files=[f.path for f in to_archive],
                    reason=f"Duplicate of {keeper.path.name}",
                    space_saved=space_saved,
                    risk_level="low"
                ))
        
        # Handle large files
        for large_file in large_files:
            if large_file.type in ['csv_data', 'log', 'json_data']:
                suggestions.append(CleanupSuggestion(
                    action="archive",
                    files=[large_file.path],
                    reason=f"Large {large_file.type} file ({large_file.size / 1024 / 1024:.1f}MB)",
                    space_saved=large_file.size,
                    risk_level="medium"
                ))
        
        # Handle redundant scripts
        for script_group in redundant_scripts:
            if len(script_group) > 2:  # Only suggest if more than 2 similar scripts
                # Keep the most recent, archive older versions
                to_archive = script_group[1:]  # Skip the first (newest)
                space_saved = sum(f.size for f in to_archive)
                
                suggestions.append(CleanupSuggestion(
                    action="archive",
                    files=[f.path for f in to_archive],
                    reason=f"Redundant versions of {script_group[0].path.name}",
                    space_saved=space_saved,
                    risk_level="medium"
                ))
        
        # Handle temporary files
        if temp_files:
            space_saved = sum(f.size for f in temp_files)
            suggestions.append(CleanupSuggestion(
                action="delete",
                files=[f.path for f in temp_files],
                reason="Temporary and cache files",
                space_saved=space_saved,
                risk_level="low"
            ))
        
        return suggestions
    
    def execute_cleanup(self, suggestions: List[CleanupSuggestion], 
                       risk_level_limit: str = "medium") -> ProcessingResult:
        """Execute cleanup suggestions up to specified risk level."""
        risk_order = {"low": 0, "medium": 1, "high": 2}
        max_risk = risk_order[risk_level_limit]
        
        executed = []
        total_space_saved = 0
        
        for suggestion in suggestions:
            if risk_order[suggestion.risk_level] <= max_risk:
                try:
                    if suggestion.action == "delete":
                        self._delete_files(suggestion.files)
                    elif suggestion.action == "archive":
                        self._archive_files(suggestion.files)
                    
                    executed.append(suggestion)
                    total_space_saved += suggestion.space_saved
                    
                except Exception as e:
                    self.logger.warning(f"Failed to execute suggestion: {e}")
        
        return ProcessingResult(
            status=ProcessingStatus.COMPLETED,
            message=f"Executed {len(executed)} cleanup suggestions",
            data={
                'executed_suggestions': len(executed),
                'space_saved_mb': total_space_saved / (1024 * 1024),
                'executed_actions': [s.__dict__ for s in executed]
            }
        )
    
    def _delete_files(self, files: List[Path]):
        """Delete files safely."""
        for file_path in files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    self.logger.info(f"Deleted: {file_path}")
            except Exception as e:
                self.logger.warning(f"Failed to delete {file_path}: {e}")
    
    def _archive_files(self, files: List[Path]):
        """Archive files to archive directory."""
        archive_dir = self.config.paths.base_dir / "archive" / "automated_cleanup"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            try:
                if file_path.exists():
                    # Create relative path structure in archive
                    rel_path = file_path.relative_to(self.config.paths.base_dir)
                    archive_path = archive_dir / rel_path
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move file to archive
                    file_path.rename(archive_path)
                    self.logger.info(f"Archived: {file_path} -> {archive_path}")
            except Exception as e:
                self.logger.warning(f"Failed to archive {file_path}: {e}")
    
    def generate_cleanup_report(self, analysis_result: ProcessingResult, 
                              output_file: Optional[Path] = None) -> Path:
        """Generate detailed cleanup report."""
        if output_file is None:
            output_file = self.config.paths.output_dir / "cleanup_report.json"
        
        report = {
            'timestamp': self._get_timestamp(),
            'analysis_summary': analysis_result.data,
            'recommendations': self._generate_recommendations(analysis_result.data)
        }
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Cleanup report saved to {output_file}")
        return output_file
    
    def _generate_recommendations(self, analysis_data: Dict) -> List[str]:
        """Generate cleanup recommendations."""
        recommendations = []
        
        potential_mb = analysis_data.get('potential_space_saved_mb', 0)
        if potential_mb > 100:
            recommendations.append(f"High cleanup potential: {potential_mb:.1f}MB can be freed")
        
        duplicate_groups = analysis_data.get('duplicate_groups', 0)
        if duplicate_groups > 5:
            recommendations.append(f"Found {duplicate_groups} duplicate file groups - consider consolidation")
        
        redundant_scripts = analysis_data.get('redundant_scripts', 0)
        if redundant_scripts > 3:
            recommendations.append(f"Found {redundant_scripts} redundant script groups - archive old versions")
        
        large_files = analysis_data.get('large_files', 0)
        if large_files > 0:
            recommendations.append(f"Found {large_files} large files - consider archiving or compression")
        
        if not recommendations:
            recommendations.append("Project is well-organized with minimal cleanup opportunities")
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().isoformat()