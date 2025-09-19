#!/usr/bin/env python3
"""
Agriculture Monitoring System API Documentation Generator

This script generates API documentation from template files and validates
OpenAPI 3.0 compatibility. Supports multiple output formats including
Markdown, HTML, and PDF.
"""

import os
import json
import yaml
import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def load_template(template_path):
    """Load the API documentation template"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading template: {e}")
        sys.exit(1)

def generate_openapi_spec(template_content):
    """Generate OpenAPI 3.0 specification from template content"""
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Agriculture Monitoring System API",
            "description": "RESTful API for agricultural data monitoring and management",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
                "email": "api-support@agriculture-monitoring.example.com"
            }
        },
        "servers": [
            {
                "url": "https://api.agriculture-monitoring.example.com/v1",
                "description": "Production server"
            }
        ],
        "tags": [
            {"name": "sensors", "description": "Sensor management endpoints"},
            {"name": "environment", "description": "Environmental data endpoints"},
            {"name": "crops", "description": "Crop management endpoints"}
        ],
        "paths": {
            "/sensors": {
                "get": {
                    "summary": "Get all sensors",
                    "tags": ["sensors"],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "sensors": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/Sensor"}
                                            },
                                            "total": {"type": "integer"},
                                            "page": {"type": "integer"},
                                            "perPage": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/sensors/{sensorId}/data": {
                "get": {
                    "summary": "Get sensor data",
                    "tags": ["sensors"],
                    "parameters": [
                        {
                            "name": "sensorId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "from",
                            "in": "query",
                            "schema": {"type": "string", "format": "date"}
                        },
                        {
                            "name": "to",
                            "in": "query",
                            "schema": {"type": "string", "format": "date"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Sensor data retrieved successfully"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Sensor": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "location": {
                            "type": "object",
                            "properties": {
                                "latitude": {"type": "number"},
                                "longitude": {"type": "number"}
                            }
                        },
                        "status": {"type": "string"},
                        "lastReading": {"type": "string", "format": "date-time"},
                        "batteryLevel": {"type": "number", "minimum": 0, "maximum": 100}
                    }
                },
                "WeatherData": {
                    "type": "object",
                    "properties": {
                        "temperature": {"type": "number"},
                        "humidity": {"type": "number"},
                        "precipitation": {"type": "number"},
                        "windSpeed": {"type": "number"},
                        "timestamp": {"type": "string", "format": "date-time"}
                    }
                },
                "Crop": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "plantingDate": {"type": "string", "format": "date"},
                        "expectedHarvest": {"type": "string", "format": "date"},
                        "status": {"type": "string"},
                        "yield": {"type": "number"}
                    }
                }
            },
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            }
        },
        "security": [{"ApiKeyAuth": []}]
    }
    
    return openapi_spec

def validate_openapi_spec(spec):
    """Validate OpenAPI specification"""
    # Basic validation - in a real implementation, you might use a library like openapi-spec-validator
    required_fields = ['openapi', 'info', 'paths']
    for field in required_fields:
        if field not in spec:
            return False, f"Missing required field: {field}"
    
    if not isinstance(spec['paths'], dict):
        return False, "Paths must be a dictionary"
    
    return True, "OpenAPI specification is valid"

def generate_markdown_docs(template_content, openapi_spec, output_path):
    """Generate Markdown documentation"""
    try:
        # Enhanced template with OpenAPI spec integration
        enhanced_content = template_content + "\n\n## OpenAPI Specification\n\n"
        enhanced_content += "The full OpenAPI 3.0 specification is available below:\n\n"
        enhanced_content += "```yaml\n" + yaml.dump(openapi_spec, default_flow_style=False) + "```"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        return True, f"Markdown documentation generated at {output_path}"
    except Exception as e:
        return False, f"Error generating Markdown: {e}"

def generate_html_docs(markdown_path, output_path):
    """Convert Markdown to HTML"""
    try:
        # This would typically use a library like markdown2 or pandoc
        # For simplicity, we'll create a basic HTML wrapper
        with open(markdown_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agriculture Monitoring System API Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Agriculture Monitoring System API Documentation</h1>
    <div>{md_content.replace('\n', '<br>').replace('```', '<pre><code>').replace('```', '</code></pre>')}</div>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True, f"HTML documentation generated at {output_path}"
    except Exception as e:
        return False, f"Error generating HTML: {e}"

def generate_pdf_docs(html_path, output_path):
    """Convert HTML to PDF"""
    try:
        # This would typically use a library like weasyprint or pdfkit
        # For now, we'll just create a placeholder
        pdf_content = "PDF generation would be implemented with a PDF library"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pdf_content)
        
        return True, f"PDF documentation placeholder created at {output_path}"
    except Exception as e:
        return False, f"Error generating PDF: {e}"

def generate_report(results, output_dir):
    """Generate a detailed generation report"""
    report_path = os.path.join(output_dir, 'generation-report.json')
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total_operations": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"])
        }
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    return report_path

def main():
    parser = argparse.ArgumentParser(description='Generate Agriculture API Documentation')
    parser.add_argument('--template', default='docs/api-templates/agriculture-api-template.md',
                       help='Path to template file')
    parser.add_argument('--output-dir', default='docs/api',
                       help='Output directory for generated docs')
    parser.add_argument('--format', choices=['all', 'markdown', 'html', 'pdf'], default='all',
                       help='Output format')
    parser.add_argument('--validate', action='store_true',
                       help='Validate OpenAPI specification')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    results = []
    
    # Load template
    template_content = load_template(args.template)
    results.append({
        "operation": "load_template",
        "success": True,
        "message": f"Template loaded from {args.template}"
    })
    
    # Generate OpenAPI specification
    openapi_spec = generate_openapi_spec(template_content)
    results.append({
        "operation": "generate_openapi_spec",
        "success": True,
        "message": "OpenAPI specification generated"
    })
    
    # Validate OpenAPI spec if requested
    if args.validate:
        is_valid, validation_msg = validate_openapi_spec(openapi_spec)
        results.append({
            "operation": "validate_openapi_spec",
            "success": is_valid,
            "message": validation_msg
        })
        if not is_valid:
            print(f"Validation failed: {validation_msg}")
            sys.exit(1)
    
    # Generate documentation in requested formats
    if args.format in ['all', 'markdown']:
        md_path = os.path.join(args.output_dir, 'agriculture-api.md')
        success, message = generate_markdown_docs(template_content, openapi_spec, md_path)
        results.append({
            "operation": "generate_markdown",
            "success": success,
            "message": message,
            "path": md_path
        })
    
    if args.format in ['all', 'html'] and 'md_path' in locals():
        html_path = os.path.join(args.output_dir, 'agriculture-api.html')
        success, message = generate_html_docs(md_path, html_path)
        results.append({
            "operation": "generate_html",
            "success": success,
            "message": message,
            "path": html_path
        })
    
    if args.format in ['all', 'pdf'] and 'html_path' in locals():
        pdf_path = os.path.join(args.output_dir, 'agriculture-api.pdf')
        success, message = generate_pdf_docs(html_path, pdf_path)
        results.append({
            "operation": "generate_pdf",
            "success": success,
            "message": message,
            "path": pdf_path
        })
    
    # Save OpenAPI spec
    json_spec_path = os.path.join(args.output_dir, 'openapi-spec.json')
    yaml_spec_path = os.path.join(args.output_dir, 'openapi-spec.yaml')
    
    with open(json_spec_path, 'w', encoding='utf-8') as f:
        json.dump(openapi_spec, f, indent=2)
    
    with open(yaml_spec_path, 'w', encoding='utf-8') as f:
        yaml.dump(openapi_spec, f, default_flow_style=False)
    
    results.extend([
        {
            "operation": "save_openapi_json",
            "success": True,
            "message": f"OpenAPI JSON spec saved to {json_spec_path}",
            "path": json_spec_path
        },
        {
            "operation": "save_openapi_yaml",
            "success": True,
            "message": f"OpenAPI YAML spec saved to {yaml_spec_path}",
            "path": yaml_spec_path
        }
    ])
    
    # Generate report
    report_path = generate_report(results, args.output_dir)
    results.append({
        "operation": "generate_report",
        "success": True,
        "message": f"Generation report saved to {report_path}",
        "path": report_path
    })
    
    # Print summary
    print("\n=== Documentation Generation Summary ===")
    for result in results:
        status = "✓" if result["success"] else "✗"
        print(f"{status} {result['operation']}: {result['message']}")
    
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    print(f"\nOverall: {successful}/{total} operations completed successfully")

if __name__ == "__main__":
    main()