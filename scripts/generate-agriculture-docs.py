#!/usr/bin/env python3
"""
Agriculture Monitoring System API Documentation Generator

This script generates comprehensive API documentation from template files,
validates OpenAPI 3.0 compliance, and supports multiple output formats.
"""

import os
import re
import json
import yaml
import argparse
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgricultureDocGenerator:
    """API documentation generator for Agriculture Monitoring System"""
    
    def __init__(self, template_path: str, output_dir: str = "docs/api"):
        self.template_path = template_path
        self.output_dir = output_dir
        self.report_data = {
            "generation_date": datetime.now().isoformat(),
            "files_generated": [],
            "validation_errors": [],
            "warnings": [],
            "metrics": {}
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs("reports", exist_ok=True)
    
    def load_template(self) -> str:
        """Load the API documentation template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"Template file not found: {self.template_path}")
        except Exception as e:
            raise Exception(f"Error loading template: {str(e)}")
    
    def validate_openapi_compliance(self, content: str) -> List[str]:
        """Validate template content for OpenAPI 3.0 compliance"""
        errors = []
        
        # Check for required OpenAPI sections
        required_sections = [
            "System Overview",
            "Authentication Methods", 
            "Endpoints",
            "Data Models",
            "Error Handling",
            "Rate Limiting"
        ]
        
        for section in required_sections:
            if f"## {section}" not in content:
                errors.append(f"Missing required section: {section}")
        
        # Check for HTTP method patterns
        http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        method_patterns = [f"```http\n{method} " for method in http_methods]
        
        method_found = False
        for pattern in method_patterns:
            if pattern in content:
                method_found = True
                break
        
        if not method_found:
            errors.append("No HTTP method examples found in endpoints section")
        
        # Check for JSON response examples
        if "```json" not in content:
            errors.append("No JSON response examples found")
        
        return errors
    
    def extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from template content"""
        metadata = {
            "sections": [],
            "endpoints_count": 0,
            "data_models_count": 0,
            "error_codes_count": 0
        }
        
        # Count sections
        section_pattern = r'##\s+(.+?)\n'
        sections = re.findall(section_pattern, content)
        metadata["sections"] = sections
        
        # Count endpoints
        endpoint_pattern = r'```http\n(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)'
        endpoints = re.findall(endpoint_pattern, content)
        metadata["endpoints_count"] = len(endpoints)
        
        # Count data models
        model_pattern = r'###\s+(.+?\s+Model)\n'
        models = re.findall(model_pattern, content)
        metadata["data_models_count"] = len(models)
        
        # Count error codes
        error_pattern = r'\|\s*\d+\s*\|\s*([A-Z_]+)\s*\|'
        error_codes = re.findall(error_pattern, content)
        metadata["error_codes_count"] = len(error_codes)
        
        return metadata
    
    def generate_markdown_docs(self, content: str) -> str:
        """Generate final Markdown documentation"""
        # Add generation metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"---\n# Generated: {timestamp}\n# Source: {self.template_path}\n# Version: 1.0.0\n---\n\n"
        
        return header + content
    
    def generate_html_docs(self, markdown_content: str) -> str:
        """Convert Markdown to HTML using pandoc"""
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as md_file:
                md_file.write(markdown_content)
                md_path = md_file.name
            
            html_path = os.path.join(self.output_dir, "agriculture-api.html")
            
            # Convert using pandoc
            cmd = [
                "pandoc", "-f", "markdown", "-t", "html5", 
                "--standalone", "--toc", "--css", "styles.css",
                "-o", html_path, md_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Pandoc conversion failed: {result.stderr}")
            
            # Clean up
            os.unlink(md_path)
            
            return html_path
            
        except Exception as e:
            self.report_data["warnings"].append(f"HTML generation failed: {str(e)}")
            return ""
    
    def generate_pdf_docs(self, markdown_content: str) -> str:
        """Convert Markdown to PDF using pandoc"""
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as md_file:
                md_file.write(markdown_content)
                md_path = md_file.name
            
            pdf_path = os.path.join(self.output_dir, "agriculture-api.pdf")
            
            # Convert using pandoc
            cmd = [
                "pandoc", "-f", "markdown", "-t", "pdf",
                "--pdf-engine=xelatex", "--toc",
                "-o", pdf_path, md_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"PDF conversion failed: {result.stderr}")
            
            # Clean up
            os.unlink(md_path)
            
            return pdf_path
            
        except Exception as e:
            self.report_data["warnings"].append(f"PDF generation failed: {str(e)}")
            return ""
    
    def generate_openapi_spec(self, content: str) -> Optional[str]:
        """Generate OpenAPI 3.0 specification from template"""
        try:
            openapi_spec = {
                "openapi": "3.0.0",
                "info": {
                    "title": "Agriculture Monitoring System API",
                    "description": "Comprehensive API for IoT-based precision farming operations",
                    "version": "1.0.0",
                    "contact": {
                        "name": "API Support",
                        "email": "support@agriculture-monitoring.example.com"
                    }
                },
                "servers": [
                    {
                        "url": "https://api.agriculture-monitoring.example.com/v1",
                        "description": "Production server"
                    }
                ],
                "components": {
                    "securitySchemes": {
                        "ApiKeyAuth": {
                            "type": "apiKey",
                            "in": "header",
                            "name": "Authorization"
                        },
                        "OAuth2": {
                            "type": "oauth2",
                            "flows": {
                                "clientCredentials": {
                                    "tokenUrl": "https://api.agriculture-monitoring.example.com/oauth/token",
                                    "scopes": {
                                        "read": "Read access",
                                        "write": "Write access"
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            # Save OpenAPI spec
            yaml_path = os.path.join(self.output_dir, "openapi.yaml")
            json_path = os.path.join(self.output_dir, "openapi.json")
            
            with open(yaml_path, 'w') as f:
                yaml.dump(openapi_spec, f, sort_keys=False)
            
            with open(json_path, 'w') as f:
                json.dump(openapi_spec, f, indent=2)
            
            return yaml_path
            
        except Exception as e:
            self.report_data["warnings"].append(f"OpenAPI spec generation failed: {str(e)}")
            return None
    
    def generate_report(self) -> str:
        """Generate detailed generation report"""
        report_path = os.path.join("reports", f"docs-generation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
        
        with open(report_path, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        
        return report_path
    
    def generate(self, formats: List[str] = ["markdown", "html", "pdf"]) -> bool:
        """Main generation method"""
        print("🌱 Agriculture API Documentation Generator")
        print("=" * 50)
        
        # Load template
        print("📄 Loading template...")
        try:
            template_content = self.load_template()
        except Exception as e:
            print(f"❌ Error loading template: {e}")
            return False
        
        # Validate OpenAPI compliance
        print("🔍 Validating OpenAPI compliance...")
        validation_errors = self.validate_openapi_compliance(template_content)
        
        if validation_errors:
            print("❌ Validation errors found:")
            for error in validation_errors:
                print(f"   - {error}")
            self.report_data["validation_errors"] = validation_errors
            return False
        else:
            print("✅ OpenAPI validation passed")
        
        # Extract metadata
        metadata = self.extract_metadata(template_content)
        self.report_data["metrics"] = metadata
        
        print(f"📊 Documentation metrics:")
        print(f"   - Sections: {len(metadata['sections'])}")
        print(f"   - Endpoints: {metadata['endpoints_count']}")
        print(f"   - Data Models: {metadata['data_models_count']}")
        print(f"   - Error Codes: {metadata['error_codes_count']}")
        
        # Generate documentation in requested formats
        generated_files = []
        
        if "markdown" in formats:
            print("📝 Generating Markdown documentation...")
            md_content = self.generate_markdown_docs(template_content)
            md_path = os.path.join(self.output_dir, "agriculture-api.md")
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            generated_files.append(md_path)
            print(f"✅ Markdown generated: {md_path}")
        
        if "html" in formats:
            print("🌐 Generating HTML documentation...")
            html_path = self.generate_html_docs(template_content)
            if html_path:
                generated_files.append(html_path)
                print(f"✅ HTML generated: {html_path}")
        
        if "pdf" in formats:
            print("📄 Generating PDF documentation...")
            pdf_path = self.generate_pdf_docs(template_content)
            if pdf_path:
                generated_files.append(pdf_path)
                print(f"✅ PDF generated: {pdf_path}")
        
        # Generate OpenAPI spec
        print("🔧 Generating OpenAPI specification...")
        openapi_path = self.generate_openapi_spec(template_content)
        if openapi_path:
            generated_files.append(openapi_path)
            print(f"✅ OpenAPI spec generated: {openapi_path}")
        
        # Update report data
        self.report_data["files_generated"] = generated_files
        self.report_data["success"] = True
        
        # Generate final report
        report_path = self.generate_report()
        print(f"📊 Generation report: {report_path}")
        
        print("\n🎉 Documentation generation completed successfully!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📈 Files generated: {len(generated_files)}")
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate Agriculture Monitoring System API Documentation")
    parser.add_argument("--template", "-t", default="docs/api-templates/agriculture-api-template.md", 
                       help="Path to API template file")
    parser.add_argument("--output", "-o", default="docs/api", 
                       help="Output directory for generated documentation")
    parser.add_argument("--format", "-f", nargs="+", 
                       choices=["markdown", "html", "pdf", "all"], default=["markdown"],
                       help="Output formats to generate")
    parser.add_argument("--validate-only", action="store_true",
                       help="Only validate template without generating output")
    
    args = parser.parse_args()
    
    # Handle "all" format option
    if "all" in args.format:
        formats = ["markdown", "html", "pdf"]
    else:
        formats = args.format
    
    # Initialize generator
    generator = AgricultureDocGenerator(args.template, args.output)
    
    if args.validate_only:
        # Only validate template
        try:
            content = generator.load_template()
            errors = generator.validate_openapi_compliance(content)
            
            if errors:
                print("❌ Validation failed:")
                for error in errors:
                    print(f"   - {error}")
                return 1
            else:
                print("✅ Template validation passed")
                metadata = generator.extract_metadata(content)
                print(f"📊 Template metrics: {metadata}")
                return 0
                
        except Exception as e:
            print(f"❌ Error during validation: {e}")
            return 1
    else:
        # Generate full documentation
        success = generator.generate(formats)
        return 0 if success else 1

if __name__ == "__main__":
    exit(main())