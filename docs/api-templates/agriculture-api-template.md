# Agriculture Monitoring System API Documentation

## System Overview

The Agriculture Monitoring System API provides programmatic access to agricultural data collection, monitoring, and analysis capabilities. This RESTful API enables developers to integrate with sensor networks, retrieve environmental data, and manage agricultural operations programmatically.

**Base URL**: `https://api.agriculture-monitoring.example.com/v1`
**API Version**: 1.0.0
**Contact**: api-support@agriculture-monitoring.example.com

## Authentication Methods

### API Key Authentication
All API endpoints require authentication using an API key sent in the `X-API-Key` header.

```http
GET /sensors HTTP/1.1
Host: api.agriculture-monitoring.example.com
X-API-Key: your-api-key-here
Content-Type: application/json
```

### OAuth 2.0 (Coming Soon)
Support for OAuth 2.0 authentication will be available in future versions.

## Endpoints

### Sensors Management

#### Get All Sensors
```http
GET /sensors
```

**Response**:
```json
{
  "sensors": [
    {
      "id": "sensor-001",
      "type": "temperature",
      "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      "status": "active",
      "lastReading": "2024-01-15T10:30:00Z",
      "batteryLevel": 85
    }
  ],
  "total": 1,
  "page": 1,
  "perPage": 20
}
```

#### Get Sensor Data
```http
GET /sensors/{sensorId}/data?from=2024-01-01&to=2024-01-15
```

### Environmental Data

#### Get Weather Data
```http
GET /weather?latitude=40.7128&longitude=-74.0060
```

#### Get Soil Moisture Data
```http
GET /soil/moisture?fieldId=field-001
```

### Crop Management

#### Get Crop Health
```http
GET /crops/{cropId}/health
```

#### Update Crop Status
```http
PUT /crops/{cropId}
Content-Type: application/json

{
  "status": "harvested",
  "yield": 1500,
  "harvestDate": "2024-01-15"
}
```

## Data Models

### Sensor Object
```json
{
  "id": "string",
  "type": "string",
  "location": {
    "latitude": "number",
    "longitude": "number"
  },
  "status": "string",
  "lastReading": "string",
  "batteryLevel": "number"
}
```

### Weather Data Object
```json
{
  "temperature": "number",
  "humidity": "number",
  "precipitation": "number",
  "windSpeed": "number",
  "timestamp": "string"
}
```

### Crop Object
```json
{
  "id": "string",
  "type": "string",
  "plantingDate": "string",
  "expectedHarvest": "string",
  "status": "string",
  "yield": "number"
}
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages in JSON format.

### Common Error Responses

**400 Bad Request**
```json
{
  "error": "Invalid parameters",
  "message": "Latitude must be between -90 and 90",
  "code": "VALIDATION_ERROR"
}
```

**401 Unauthorized**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key",
  "code": "AUTH_ERROR"
}
```

**404 Not Found**
```json
{
  "error": "Not found",
  "message": "Sensor not found",
  "code": "NOT_FOUND"
}
```

**429 Too Many Requests**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests",
  "code": "RATE_LIMIT_EXCEEDED"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

## Rate Limiting

### Standard Tier
- **Requests per minute**: 60
- **Requests per hour**: 1,000
- **Requests per day**: 10,000

### Premium Tier
- **Requests per minute**: 120
- **Requests per hour**: 5,000
- **Requests per day**: 50,000

### Enterprise Tier
- **Requests per minute**: 500
- **Requests per hour**: 20,000
- **Requests per day**: 200,000

Rate limits are tracked by API key. Exceeding limits will result in 429 responses.

### Rate Limit Headers
Each response includes rate limit information:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Unix timestamp when limit resets

## OpenAPI 3.0 Specification

This API follows OpenAPI 3.0 specification. The full OpenAPI specification can be generated using the documentation generation script.

### Supported Formats
- JSON (application/json)
- YAML (application/yaml)

### Content Negotiation
Clients can specify response format using the `Accept` header:
- `Accept: application/json` (default)
- `Accept: application/yaml`

## Versioning

API versioning is managed through the URL path (`/v1/`). Breaking changes will result in new major versions.

## Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Basic sensor data endpoints
- Weather and soil moisture APIs
- Crop management endpoints