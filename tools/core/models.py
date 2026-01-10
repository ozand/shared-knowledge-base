"""
Core data models for Shared Knowledge Base.

Defines Pydantic models for knowledge entries, search filters, and results.
Used across CLI, MCP, and future API interfaces.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


class SeverityLevel(str):
    """Valid severity levels"""
    AUTHORIZED = ["critical", "high", "medium", "low"]


class ScopeLevel(str):
    """Valid scope levels"""
    AUTHORIZED = ["universal", "python", "javascript", "docker", "postgresql", "vps", "framework", "project"]


class EntryMetadata(BaseModel):
    """Metadata extracted from a knowledge entry"""
    id: str
    title: str
    severity: str
    scope: str
    category: str
    file_path: str
    line_number: Optional[int] = None
    has_prevention: bool = False
    has_code: bool = False
    has_explanation: bool = False
    tags: Optional[List[str]] = None

    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v: str) -> str:
        if v not in SeverityLevel.AUTHORIZED:
            raise ValueError(f"Invalid severity: {v}. Must be one of {SeverityLevel.AUTHORIZED}")
        return v

    @field_validator('scope')
    @classmethod
    def validate_scope(cls, v: str) -> str:
        if v not in ScopeLevel.AUTHORIZED:
            raise ValueError(f"Invalid scope: {v}. Must be one of {ScopeLevel.AUTHORIZED}")
        return v


class SearchFilter(BaseModel):
    """Filter criteria for knowledge base search"""
    query: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    scope: Optional[str] = None
    domain: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)

    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in SeverityLevel.AUTHORIZED:
            raise ValueError(f"Invalid severity: {v}. Must be one of {SeverityLevel.AUTHORIZED}")
        return v

    @field_validator('scope')
    @classmethod
    def validate_scope(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ScopeLevel.AUTHORIZED:
            raise ValueError(f"Invalid scope: {v}. Must be one of {ScopeLevel.AUTHORIZED}")
        return v


class SearchResult(BaseModel):
    """Single search result"""
    metadata: EntryMetadata
    preview: Optional[str] = None
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0)
    kb_type: Literal["project", "shared"] = "shared"  # project KB or shared KB


class SearchResults(BaseModel):
    """Aggregated search results"""
    query: str
    total: int
    project_results: List[SearchResult] = Field(default_factory=list)
    shared_results: List[SearchResult] = Field(default_factory=list)
    filters_applied: Optional[SearchFilter] = None
    execution_time_ms: Optional[float] = None

    @property
    def all_results(self) -> List[SearchResult]:
        """Get all results (project + shared)"""
        return self.project_results + self.shared_results


class QualityScore(BaseModel):
    """Quality score for a knowledge entry"""
    score: int = Field(ge=0, le=100)
    breakdown: Dict[str, int] = Field(default_factory=dict)
    issues: List[str] = Field(default_factory=list)


class RepositoryStats(BaseModel):
    """Repository-level statistics"""
    total_files: int
    total_lines: int
    total_size_kb: float
    yaml_files: int
    markdown_files: int
    python_files: int


class YamlStats(BaseModel):
    """YAML file statistics"""
    total_entries: int
    errors: int
    patterns: int
    avg_entry_size_lines: float
    largest_file: Dict[str, Any]
    domains: Dict[str, Dict[str, Any]]


class QualityDistribution(BaseModel):
    """Quality score distribution"""
    total_entries: int
    avg_score: float
    excellent: int  # 90-100
    good: int       # 75-89
    acceptable: int # 60-74
    poor: int       # 40-59
    critical: int   # 0-39


class Metrics(BaseModel):
    """Complete repository metrics"""
    timestamp: str
    repository_stats: RepositoryStats
    yaml_files: YamlStats
    domain_distribution: Dict[str, int]
    quality_scores: QualityDistribution
    version_distribution: Dict[str, int]
    validation_status: Dict[str, Any]
    health_status: str


class ValidationError(BaseModel):
    """Single validation error"""
    file_path: str
    line_number: Optional[int] = None
    error_type: str  # "syntax", "schema", "required_field", "format"
    message: str
    severity: str = "error"  # "error", "warning"
    field_path: Optional[str] = None


class ValidationResult(BaseModel):
    """Validation result for a file or directory"""
    is_valid: bool
    files_checked: int
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[ValidationError] = Field(default_factory=list)
    execution_time_ms: Optional[float] = None


class HealthStatus(BaseModel):
    """Health check response"""
    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    timestamp: str
    uptime_seconds: Optional[float] = None
    components: Dict[str, Literal["healthy", "unhealthy"]] = Field(default_factory=dict)
    issues: List[str] = Field(default_factory=list)
