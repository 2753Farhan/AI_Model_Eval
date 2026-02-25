
from abc import ABC, abstractmethod
import json
import csv
from typing import Dict, Any, List
from datetime import datetime
import logging
from pathlib import Path

from ..entities import Report

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    """Base class for all exporters"""
    
    @abstractmethod
    def export(self, report: Report, file_path: str) -> bool:
        """Export report to file"""
        pass


class CSVExporter(BaseExporter):
    """Export report as CSV"""
    
    def export(self, report: Report, file_path: str) -> bool:
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['Report ID', report.report_id])
                writer.writerow(['Evaluation ID', report.evaluation_id])
                writer.writerow(['Generated At', report.generated_at.isoformat()])
                writer.writerow([])
                
                # Write summary data
                if report.summary_data:
                    writer.writerow(['SUMMARY'])
                    self._write_dict_to_csv(writer, report.summary_data)
                
                # Write tables
                for table in report.tables:
                    writer.writerow([])
                    writer.writerow([table.get('title', 'Table')])
                    writer.writerow(table.get('headers', []))
                    for row in table.get('rows', []):
                        writer.writerow(row)
            
            logger.info(f"Exported CSV report to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False
    
    def _write_dict_to_csv(self, writer, data: Dict, prefix: str = ''):
        """Write dictionary to CSV"""
        for key, value in data.items():
            if isinstance(value, dict):
                self._write_dict_to_csv(writer, value, f"{prefix}{key}.")
            else:
                writer.writerow([f"{prefix}{key}", str(value)])


class JSONExporter(BaseExporter):
    """Export report as JSON"""
    
    def export(self, report: Report, file_path: str) -> bool:
        try:
            data = {
                'report_id': report.report_id,
                'evaluation_id': report.evaluation_id,
                'report_type': report.report_type.value,
                'format': report.format.value,
                'generated_at': report.generated_at.isoformat(),
                'summary': report.summary_data,
                'detailed': report.detailed_data,
                'charts': report.charts,
                'tables': report.tables,
                'metadata': report.metadata,
                'tags': report.tags
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Exported JSON report to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export JSON: {e}")
            return False


class PDFExporter(BaseExporter):
    """Export report as PDF"""
    
    def export(self, report: Report, file_path: str) -> bool:
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, landscape
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            import io
            import base64
            
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            story.append(Paragraph(f"Evaluation Report: {report.report_id}", title_style))
            story.append(Spacer(1, 12))
            
            # Metadata
            story.append(Paragraph(f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Paragraph(f"Evaluation ID: {report.evaluation_id}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Summary
            if report.summary_data:
                story.append(Paragraph("Summary", styles['Heading2']))
                story.append(Spacer(1, 6))
                
                summary_text = f"Total Results: {report.summary_data.get('total_results', 0)}<br/>"
                summary_text += f"Passed: {report.summary_data.get('passed_results', 0)}<br/>"
                summary_text += f"Pass Rate: {report.summary_data.get('pass_rate', 0)*100:.1f}%"
                
                story.append(Paragraph(summary_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Tables
            for table_data in report.tables:
                story.append(Paragraph(table_data.get('title', 'Table'), styles['Heading2']))
                story.append(Spacer(1, 6))
                
                data = [table_data.get('headers', [])]
                data.extend(table_data.get('rows', []))
                
                if data:
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 12))
            
            # Charts
            for name, chart_data in report.charts.items():
                if 'image' in chart_data:
                    story.append(Paragraph(name.replace('_', ' ').title(), styles['Heading2']))
                    story.append(Spacer(1, 6))
                    
                    # Decode base64 image
                    img_data = base64.b64decode(chart_data['image'])
                    img_buffer = io.BytesIO(img_data)
                    img = Image(img_buffer, width=6*inch, height=4*inch)
                    story.append(img)
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Exported PDF report to {file_path}")
            return True
            
        except ImportError:
            logger.error("ReportLab not installed. Install with: pip install reportlab")
            return False
        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            return False


class HTMLExporter(BaseExporter):
    """Export report as HTML"""
    
    def export(self, report: Report, file_path: str) -> bool:
        try:
            html = self._generate_html(report)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            logger.info(f"Exported HTML report to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export HTML: {e}")
            return False
    
    def _generate_html(self, report: Report) -> str:
        """Generate HTML content"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Evaluation Report: {report.report_id}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .chart {{
            margin: 30px 0;
            text-align: center;
        }}
        .chart img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <h1>Evaluation Report: {report.report_id}</h1>
    
    <div class="metadata">
        <p><strong>Generated:</strong> {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Evaluation ID:</strong> {report.evaluation_id}</p>
        <p><strong>Report Type:</strong> {report.report_type.value}</p>
    </div>
"""
        
        # Summary
        if report.summary_data:
            html += f"""
    <h2>Summary</h2>
    <div class="summary">
        <p><strong>Total Results:</strong> {report.summary_data.get('total_results', 0)}</p>
        <p><strong>Passed:</strong> {report.summary_data.get('passed_results', 0)}</p>
        <p><strong>Failed:</strong> {report.summary_data.get('total_results', 0) - report.summary_data.get('passed_results', 0)}</p>
        <p><strong>Pass Rate:</strong> {report.summary_data.get('pass_rate', 0)*100:.1f}%</p>
    </div>
"""
        
        # Detailed data
        if report.detailed_data:
            html += f"""
    <h2>Detailed Analysis</h2>
"""
            # Model statistics
            if 'model_statistics' in report.detailed_data:
                html += """
    <h3>Model Performance</h3>
    <table>
        <tr>
            <th>Model</th>
            <th>Total</th>
            <th>Passed</th>
            <th>Failed</th>
            <th>Pass Rate</th>
            <th>Avg Time (ms)</th>
            <th>Errors</th>
        </tr>
"""
                for model_id, stats in report.detailed_data['model_statistics'].items():
                    html += f"""
        <tr>
            <td>{model_id}</td>
            <td>{stats.get('total', 0)}</td>
            <td>{stats.get('passed', 0)}</td>
            <td>{stats.get('total', 0) - stats.get('passed', 0)}</td>
            <td>{stats.get('pass_rate', 0)*100:.1f}%</td>
            <td>{stats.get('avg_execution_time', 0):.2f}</td>
            <td>{stats.get('error_count', 0)}</td>
        </tr>
"""
                html += "</table>"
        
        # Tables
        for table in report.tables:
            html += f"""
    <h3>{table.get('title', 'Table')}</h3>
    <table>
        <tr>
"""
            for header in table.get('headers', []):
                html += f"            <th>{header}</th>\n"
            html += "        </tr>\n"
            
            for row in table.get('rows', []):
                html += "        <tr>\n"
                for cell in row:
                    html += f"            <td>{cell}</td>\n"
                html += "        </tr>\n"
            
            html += "    </table>\n"
        
        # Charts
        for name, chart_data in report.charts.items():
            if 'image' in chart_data:
                html += f"""
    <div class="chart">
        <h3>{name.replace('_', ' ').title()}</h3>
        <img src="data:image/png;base64,{chart_data['image']}" alt="{name}">
    </div>
"""
        
        # Footer
        html += f"""
    <div class="footer">
        <p>Generated by AI_ModelEval Report Generator</p>
        <p>Report ID: {report.report_id}</p>
    </div>
</body>
</html>
"""
        
        return html


class MarkdownExporter(BaseExporter):
    """Export report as Markdown"""
    
    def export(self, report: Report, file_path: str) -> bool:
        try:
            md = self._generate_markdown(report)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md)
            
            logger.info(f"Exported Markdown report to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export Markdown: {e}")
            return False
    
    def _generate_markdown(self, report: Report) -> str:
        """Generate Markdown content"""
        md = f"""# Evaluation Report: {report.report_id}

**Generated:** {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}  
**Evaluation ID:** {report.evaluation_id}  
**Report Type:** {report.report_type.value}

"""
        
        # Summary
        if report.summary_data:
            md += f"""## Summary

- **Total Results:** {report.summary_data.get('total_results', 0)}
- **Passed:** {report.summary_data.get('passed_results', 0)}
- **Failed:** {report.summary_data.get('total_results', 0) - report.summary_data.get('passed_results', 0)}
- **Pass Rate:** {report.summary_data.get('pass_rate', 0)*100:.1f}%

"""
        
        # Tables
        for table in report.tables:
            md += f"## {table.get('title', 'Table')}\n\n"
            
            # Headers
            md += "| " + " | ".join(table.get('headers', [])) + " |\n"
            md += "|" + "|".join([" --- " for _ in table.get('headers', [])]) + "|\n"
            
            # Rows
            for row in table.get('rows', []):
                md += "| " + " | ".join(str(cell) for cell in row) + " |\n"
            
            md += "\n"
        
        return md