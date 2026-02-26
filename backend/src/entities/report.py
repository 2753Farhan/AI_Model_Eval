
from datetime import datetime
from typing import List, Dict, Any, Optional
import secrets
from enum import Enum


class ReportFormat(Enum):
    HTML = "html"
    PDF = "pdf"
    JSON = "json"
    CSV = "csv"
    MARKDOWN = "md"
    LATEX = "latex"


class ReportType(Enum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    COMPARATIVE = "comparative"
    ERROR_ANALYSIS = "error_analysis"
    TUNING = "tuning"


class Report:
    def __init__(
        self,
        evaluation_id: str,
        report_type: ReportType,
        report_format: ReportFormat,
        report_id: Optional[str] = None
    ):
        self.report_id = report_id or self._generate_id()
        self.evaluation_id = evaluation_id
        self.report_type = report_type
        self.format = report_format
        self.file_path: Optional[str] = None
        self.summary_data: Dict[str, Any] = {}
        self.detailed_data: Dict[str, Any] = {}
        self.charts: Dict[str, Any] = {}
        self.tables: List[Dict[str, Any]] = []
        self.generated_at = datetime.now()
        self.download_count: int = 0
        self.last_downloaded: Optional[datetime] = None
        self.metadata: Dict[str, Any] = {}
        self.is_public: bool = False
        self.tags: List[str] = []

    def _generate_id(self) -> str:
        """Generate a unique report ID"""
        return f"rpt_{secrets.token_hex(8)}"

    def set_file_path(self, path: str) -> None:
        """Set the file path"""
        self.file_path = path

    def add_summary(self, data: Dict[str, Any]) -> None:
        """Add summary data"""
        self.summary_data.update(data)

    def add_detailed_data(self, data: Dict[str, Any]) -> None:
        """Add detailed data"""
        self.detailed_data.update(data)

    def add_chart(self, name: str, chart_data: Dict[str, Any]) -> None:
        """Add a chart"""
        self.charts[name] = chart_data

    def add_table(self, table: Dict[str, Any]) -> None:
        """Add a table"""
        self.tables.append(table)

    def increment_download(self) -> None:
        """Increment download count"""
        self.download_count += 1
        self.last_downloaded = datetime.now()

    def make_public(self) -> None:
        """Make report public"""
        self.is_public = True

    def make_private(self) -> None:
        """Make report private"""
        self.is_public = False

    def add_tag(self, tag: str) -> None:
        """Add a tag"""
        if tag not in self.tags:
            self.tags.append(tag)
# In src/entities/report.py, around line 94, replace the get_filename method:

    def get_filename(self) -> str:
        """Get the filename for this report"""
        timestamp = self.generated_at.strftime('%Y%m%d_%H%M%S')
        # Fix: If format is an Enum with value attribute, use that, otherwise use the string directly
        if hasattr(self.format, 'value'):
            format_str = self.format.value
        else:
        
            format_str = str(self.format)
        return f"report_{self.evaluation_id}_{timestamp}.{format_str}"

# In src/entities/report.py, around line 102, update the to_dict method:

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary"""
        return {
            'report_id': self.report_id,
            'evaluation_id': self.evaluation_id,
            'report_type': self.report_type.value if hasattr(self.report_type, 'value') else str(self.report_type),
            'format': self.format.value if hasattr(self.format, 'value') else str(self.format),
            'file_path': self.file_path,
            'summary_data': self.summary_data,
            'detailed_data': self.detailed_data,
            'charts': self.charts,
            'tables': self.tables,
            'generated_at': self.generated_at.isoformat(),
            'download_count': self.download_count,
            'last_downloaded': self.last_downloaded.isoformat() if self.last_downloaded else None,
            'metadata': self.metadata,
            'is_public': self.is_public,
            'tags': self.tags,
            'filename': self.get_filename()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Report':
        """Create report from dictionary"""
        report = cls(
            evaluation_id=data['evaluation_id'],
            report_type=ReportType(data['report_type']),
            report_format=ReportFormat(data['format']),
            report_id=data.get('report_id')
        )
        report.file_path = data.get('file_path')
        report.summary_data = data.get('summary_data', {})
        report.detailed_data = data.get('detailed_data', {})
        report.charts = data.get('charts', {})
        report.tables = data.get('tables', [])
        report.generated_at = datetime.fromisoformat(data['generated_at']) if 'generated_at' in data else datetime.now()
        report.download_count = data.get('download_count', 0)
        report.last_downloaded = datetime.fromisoformat(data['last_downloaded']) if data.get('last_downloaded') else None
        report.metadata = data.get('metadata', {})
        report.is_public = data.get('is_public', False)
        report.tags = data.get('tags', [])
        return report

    @classmethod
    def create_summary_report(
        cls,
        evaluation_id: str,
        format: ReportFormat = ReportFormat.HTML
    ) -> 'Report':
        """Create a summary report"""
        return cls(
            evaluation_id=evaluation_id,
            report_type=ReportType.SUMMARY,
            report_format=format
        )

    @classmethod
    def create_detailed_report(
        cls,
        evaluation_id: str,
        format: ReportFormat = ReportFormat.HTML
    ) -> 'Report':
        """Create a detailed report"""
        return cls(
            evaluation_id=evaluation_id,
            report_type=ReportType.DETAILED,
            report_format=format
        )