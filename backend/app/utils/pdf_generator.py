"""
PDF Generator for ATS-Compliant Resumes
Generates clean, ATS-friendly PDF resumes
"""

from typing import Dict, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import io


class PDFGenerator:
    """Generate ATS-compliant PDF resumes"""
    
    # ATS-friendly fonts
    ATS_FONTS = {
        'title': 'Helvetica-Bold',
        'heading': 'Helvetica-Bold',
        'body': 'Helvetica',
        'italic': 'Helvetica-Oblique'
    }
    
    @staticmethod
    def generate_resume_pdf(resume_data: Dict, filename: Optional[str] = None) -> bytes:
        """
        Generate ATS-compliant PDF from resume JSON
        
        Args:
            resume_data: Resume data in JSON format
            filename: Optional filename (not used, returns bytes)
            
        Returns:
            PDF bytes
        """
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        styles = PDFGenerator._get_styles()
        
        # Add personal info (header)
        PDFGenerator._add_personal_info(story, resume_data.get('personal_info', {}), styles)
        
        # Add summary
        if resume_data.get('summary'):
            PDFGenerator._add_section(story, 'SUMMARY', resume_data['summary'], styles)
        
        # Add skills
        if resume_data.get('skills'):
            PDFGenerator._add_skills_section(story, resume_data['skills'], styles)
        
        # Add work experience
        if resume_data.get('work_experience'):
            PDFGenerator._add_work_experience(story, resume_data['work_experience'], styles)
        
        # Add projects
        if resume_data.get('projects'):
            PDFGenerator._add_projects(story, resume_data['projects'], styles)
        
        # Add education
        if resume_data.get('education'):
            PDFGenerator._add_education(story, resume_data['education'], styles)
        
        # Add certifications
        if resume_data.get('certifications'):
            PDFGenerator._add_certifications(story, resume_data['certifications'], styles)
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @staticmethod
    def _get_styles():
        """Get paragraph styles for PDF"""
        styles = getSampleStyleSheet()
        
        # Name style
        styles.add(ParagraphStyle(
            name='Name',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#000000'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Contact info style
        styles.add(ParagraphStyle(
            name='Contact',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section heading style
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#000000'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#000000'),
            borderPadding=0,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Subsection heading (job title, company, etc.)
        styles.add(ParagraphStyle(
            name='SubHeading',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#000000'),
            spaceAfter=4,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        styles.add(ParagraphStyle(
            name='Body',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#000000'),
            spaceAfter=6,
            fontName='Helvetica',
            leading=14
        ))
        
        # Bullet points
        styles.add(ParagraphStyle(
            name='Bullet',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#000000'),
            spaceAfter=4,
            fontName='Helvetica',
            leftIndent=20,
            bulletIndent=10,
            leading=14
        ))
        
        return styles
    
    @staticmethod
    def _add_personal_info(story, personal_info: Dict, styles):
        """Add personal information header"""
        # Name
        name = personal_info.get('full_name', '')
        if name:
            story.append(Paragraph(name, styles['Name']))
        
        # Contact info
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        
        if contact_parts:
            contact_text = ' | '.join(contact_parts)
            story.append(Paragraph(contact_text, styles['Contact']))
        
        # Links
        link_parts = []
        if personal_info.get('linkedin'):
            link_parts.append(f"LinkedIn: {personal_info['linkedin']}")
        if personal_info.get('github'):
            link_parts.append(f"GitHub: {personal_info['github']}")
        if personal_info.get('portfolio'):
            link_parts.append(f"Portfolio: {personal_info['portfolio']}")
        
        if link_parts:
            link_text = ' | '.join(link_parts)
            story.append(Paragraph(link_text, styles['Contact']))
        
        story.append(Spacer(1, 0.1*inch))
    
    @staticmethod
    def _add_section(story, title: str, content: str, styles):
        """Add a simple text section"""
        # Section heading
        story.append(Paragraph(title, styles['SectionHeading']))
        
        # Content
        story.append(Paragraph(content, styles['Body']))
        story.append(Spacer(1, 0.1*inch))
    
    @staticmethod
    def _add_skills_section(story, skills: Dict, styles):
        """Add skills section"""
        story.append(Paragraph('SKILLS', styles['SectionHeading']))
        
        # Technical skills
        if skills.get('technical') and len(skills['technical']) > 0:
            tech_skills = ', '.join(skills['technical'])
            story.append(Paragraph(f"<b>Technical:</b> {tech_skills}", styles['Body']))
        
        # Soft skills
        if skills.get('soft') and len(skills['soft']) > 0:
            soft_skills = ', '.join(skills['soft'])
            story.append(Paragraph(f"<b>Soft Skills:</b> {soft_skills}", styles['Body']))
        
        # Tools
        if skills.get('tools') and len(skills['tools']) > 0:
            tools = ', '.join(skills['tools'])
            story.append(Paragraph(f"<b>Tools & Technologies:</b> {tools}", styles['Body']))
        
        story.append(Spacer(1, 0.1*inch))
    
    @staticmethod
    def _add_work_experience(story, experiences: list, styles):
        """Add work experience section"""
        story.append(Paragraph('WORK EXPERIENCE', styles['SectionHeading']))
        
        for exp in experiences:
            # Job title and company
            title_text = f"<b>{exp.get('title', 'Position')}</b>"
            if exp.get('company'):
                title_text += f" - {exp['company']}"
            story.append(Paragraph(title_text, styles['SubHeading']))
            
            # Duration and location
            meta_parts = []
            if exp.get('duration'):
                meta_parts.append(exp['duration'])
            if exp.get('location'):
                meta_parts.append(exp['location'])
            
            if meta_parts:
                story.append(Paragraph(' | '.join(meta_parts), styles['Body']))
            
            # Responsibilities
            if exp.get('responsibilities'):
                for resp in exp['responsibilities']:
                    bullet_text = f"• {resp}"
                    story.append(Paragraph(bullet_text, styles['Bullet']))
            
            story.append(Spacer(1, 0.1*inch))
    
    @staticmethod
    def _add_projects(story, projects: list, styles):
        """Add projects section"""
        story.append(Paragraph('PROJECTS', styles['SectionHeading']))
        
        for proj in projects:
            # Project name
            story.append(Paragraph(f"<b>{proj.get('name', 'Project')}</b>", styles['SubHeading']))
            
            # Description
            if proj.get('description'):
                story.append(Paragraph(proj['description'], styles['Body']))
            
            # Technologies
            if proj.get('technologies') and len(proj['technologies']) > 0:
                tech_text = '<b>Technologies:</b> ' + ', '.join(proj['technologies'])
                story.append(Paragraph(tech_text, styles['Body']))
            
            # Link
            if proj.get('link'):
                story.append(Paragraph(f"<b>Link:</b> {proj['link']}", styles['Body']))
            
            story.append(Spacer(1, 0.1*inch))
    
    @staticmethod
    def _add_education(story, education: list, styles):
        """Add education section"""
        story.append(Paragraph('EDUCATION', styles['SectionHeading']))
        
        for edu in education:
            # Degree and institution
            edu_text = f"<b>{edu.get('degree', 'Degree')}</b>"
            if edu.get('institution'):
                edu_text += f" - {edu['institution']}"
            story.append(Paragraph(edu_text, styles['SubHeading']))
            
            # Year and location
            meta_parts = []
            if edu.get('year'):
                meta_parts.append(edu['year'])
            if edu.get('location'):
                meta_parts.append(edu['location'])
            if edu.get('gpa'):
                meta_parts.append(f"GPA: {edu['gpa']}")
            
            if meta_parts:
                story.append(Paragraph(' | '.join(meta_parts), styles['Body']))
            
            story.append(Spacer(1, 0.05*inch))
    
    @staticmethod
    def _add_certifications(story, certifications: list, styles):
        """Add certifications section"""
        story.append(Paragraph('CERTIFICATIONS', styles['SectionHeading']))
        
        for cert in certifications:
            # Certification name and issuer
            cert_text = f"<b>{cert.get('name', 'Certification')}</b>"
            if cert.get('issuer'):
                cert_text += f" - {cert['issuer']}"
            story.append(Paragraph(cert_text, styles['Body']))
            
            # Year and credential ID
            meta_parts = []
            if cert.get('year'):
                meta_parts.append(cert['year'])
            if cert.get('credential_id'):
                meta_parts.append(f"ID: {cert['credential_id']}")
            
            if meta_parts:
                story.append(Paragraph(' | '.join(meta_parts), styles['Body']))
            
            story.append(Spacer(1, 0.05*inch))
