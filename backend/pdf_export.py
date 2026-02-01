"""
PDF export utility using ReportLab.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from datetime import datetime
from typing import List


def generate_items_pdf(items: List, title: str = "Scraped Items Report") -> BytesIO:
    """
    Generate a PDF report from scraped items.
    
    Args:
        items: List of ScrapedItem objects
        title: Title for the PDF report
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#444444')
    )
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary statistics
    elements.append(Paragraph(f"Total Items: {len(items)}", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Process each item
    for idx, item in enumerate(items, 1):
        # Item header
        item_title = f"{idx}. {item.title[:100]}..." if len(item.title) > 100 else f"{idx}. {item.title}"
        elements.append(Paragraph(item_title, heading_style))
        
        # Item details
        data = [
            ["Source:", str(item.source)],
            ["URL:", Paragraph(str(item.url)[:80] + "..." if len(str(item.url)) > 80 else str(item.url), normal_style)],
        ]
        
        if item.summary:
            summary_text = str(item.summary)[:200] + "..." if len(str(item.summary)) > 200 else str(item.summary)
            data.append(["Summary:", Paragraph(summary_text, normal_style)])
        
        if item.tags:
            tags_str = ", ".join(item.tags) if isinstance(item.tags, list) else str(item.tags)
            data.append(["Tags:", tags_str])
        
        if item.published_at:
            data.append(["Published:", str(item.published_at.strftime('%Y-%m-%d %H:%M'))])
        
        data.append(["Scraped:", str(item.scraped_at.strftime('%Y-%m-%d %H:%M'))])
        
        # Create table for item details
        t = Table(data, colWidths=[1.2*inch, 5.8*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add page break every 3 items to avoid overflow
        if idx % 3 == 0 and idx < len(items):
            elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    buffer.seek(0)
    return buffer


def generate_simple_table_pdf(items: List) -> BytesIO:
    """
    Generate a simple table-based PDF report.
    
    Args:
        items: List of ScrapedItem objects
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("Scraped Items Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Prepare table data
    data = [['ID', 'Source', 'Title', 'Tags']]
    
    for item in items:
        tags_str = ", ".join(item.tags[:2]) if item.tags and isinstance(item.tags, list) else ""
        title_short = item.title[:50] + "..." if len(item.title) > 50 else item.title
        data.append([
            str(item.id),
            str(item.source),
            title_short,
            tags_str
        ])
    
    # Create table
    t = Table(data, colWidths=[0.5*inch, 1.5*inch, 3.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
