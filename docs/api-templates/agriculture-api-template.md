# Agriculture Monitoring System API Documentation

## System Overview

The Agriculture Monitoring System API provides comprehensive endpoints for managing IoT-based precision farming operations. This RESTful API enables real-time monitoring, data collection, and automated control of agricultural systems.

**Base URL**: `https://api.agriculture-monitoring.example.com/v1`
**API Version**: 1.0.0
**Format**: JSON

### Key Features
- Real-time sensor data collection and monitoring
- Automated irrigation system control
- Crop health analysis and reporting
- Weather data integration
- User and device management
- Historical data analytics

## Authentication Methods

### API Key Authentication
All API requests require authentication using an API key provided in the request header.

```http
GET /api/v1/sensors HTTP/1.1
Host: api.agriculture-monitoring.example.com
Authorization: Bearer your-api-key-here
Content-Type: application/json
```

### OAuth 2.0 Authentication
For advanced applications, OAuth 2.0 authentication is supported:

```http
POST /oauth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret
```

### Authentication Response
Successful authentication returns:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "read write"
}
```

## Endpoints

### Sensors Management

#### Get All Sensors
```http
GET /api/v1/sensors
```

**Response**:
```json
{
  "sensors": [
    {
      "id": "sensor-001",
      "type": "temperature",
      "location": "field-north",
      "value": 25.4,
      "unit": "celsius",
      "timestamp": "2024-01-15T10:30:00Z",
      "status": "active"
    }
  ],
  "total_count": 15,
  "page": 1,
  "per_page": 20
}
```

#### Get Sensor by ID
```http
GET /api/v1/sensors/{sensor_id}
```

#### Create New Sensor
```http
POST /api/v1/sensors
Content-Type: application/json

{
  "type": "humidity",
  "location": "greenhouse-1",
  "device_id": "device-123",
  "calibration_data": {
    "min_value": 0,
    "max_value": 100
  }
}
```

### Irrigation Control

#### Get Irrigation Status
```http
GET /api/v1/irrigation/status
```

#### Start Irrigation
```http
POST /api/v1/irrigation/start
Content-Type: application/json

{
  "zone": "field-a",
  "duration_minutes": 30,
  "water_flow_rate": 2.5
}
```

#### Stop Irrigation
```http
POST /api/v1/irrigation/stop
Content-Type: application/json

{
  "zone": "field-a"
}
```

### Crop Health Monitoring

#### Get Crop Health Data
```http
GET /api/v1/crops/health?crop_type=tomato&date_from=2024-01-01&date_to=2024-01-15
```

#### Upload Crop Image Analysis
```http
POST /api/v1/crops/analysis
Content-Type: multipart/form-data

{
  "image": "binary_image_data",
  "crop_type": "corn",
  "field_id": "field-001"
}
```

### Weather Integration

#### Get Weather Forecast
```http
GET /api/v1/weather/forecast?location=40.7128,-74.0060&days=7
```

#### Get Historical Weather
```http
GET /api/v1/weather/historical?location=40.7128,-74.0060&start_date=2024-01-01&end_date=2024-01-07
```

### User Management

#### User Registration
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "farm_name": "Green Valley Farm"
}
```

#### User Login
```http
POST /api/v1/users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

## Data Models

### Sensor Data Model
```json
{
  "id": "string",
  "type": "enum(temperature, humidity, soil_moisture, light_intensity)",
  "location": "string",
  "value": "number",
  "unit": "string",
  "timestamp": "datetime",
  "status": "enum(active, inactive, maintenance)",
  "device_id": "string",
  "battery_level": "number",
  "calibration_data": {
    "min_value": "number",
    "max_value": "number",
    "last_calibrated": "datetime"
  }
}
```

### Irrigation System Model
```json
{
  "zone": "string",
  "status": "enum(active, inactive, paused)",
  "current_flow_rate": "number",
  "total_water_used": "number",
  "last_activated": "datetime",
  "schedule": {
    "start_time": "time",
    "duration_minutes": "number",
    "days_of_week": "array",
    "enabled": "boolean"
  }
}
```

### Crop Health Model
```json
{
  "crop_id": "string",
  "crop_type": "string",
  "field_id": "string",
  "health_score": "number",
  "disease_detected": "boolean",
  "disease_type": "string",
  "nutrient_levels": {
    "nitrogen": "number",
    "phosphorus": "number",
    "potassium": "number"
  },
  "growth_stage": "enum(seedling, vegetative, flowering, fruiting, harvesting)",
  "last_assessment": "datetime"
}
```

### Weather Data Model
```json
{
  "location": {
    "latitude": "number",
    "longitude": "number"
  },
  "temperature": "number",
  "humidity": "number",
  "precipitation": "number",
  "wind_speed": "number",
  "wind_direction": "number",
  "solar_radiation": "number",
  "forecast_period": "string",
  "timestamp": "datetime"
}
```

### User Model
```json
{
  "id": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "farm_name": "string",
  "subscription_tier": "enum(basic, premium, enterprise)",
  "created_at": "datetime",
  "last_login": "datetime",
  "preferences": {
    "units": "enum(metric, imperial)",
    "notifications_enabled": "boolean",
    "auto_irrigation": "boolean"
  }
}
```

## Error Handling

### Standard Error Response
All error responses follow this format:

```json
{
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": "Additional error details",
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | VALIDATION_ERROR | Input validation failed |
| 401 | UNAUTHORIZED | Authentication required |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server internal error |
| 503 | SERVICE_UNAVAILABLE | Service temporarily unavailable |

### Example Error Responses

**Authentication Error**:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid API key",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Validation Error**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "location": "Field location is required",
      "sensor_type": "Must be one of: temperature, humidity, soil_moisture"
    },
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Rate Limiting

### Rate Limit Headers
All responses include rate limit headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642253400
Retry-After: 60
```

### Rate Limit Tiers

| Tier | Requests per minute | Burst capacity |
|------|---------------------|----------------|
| Free | 60 | 100 |
| Basic | 300 | 500 |
| Premium | 1000 | 2000 |
| Enterprise | 5000 | 10000 |

### Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Please try again in 60 seconds.",
    "retry_after": 60,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Best Practices
- Implement exponential backoff for retries
- Cache responses when appropriate
- Monitor rate limit headers in your application
- Consider using webhooks for real-time updates instead of polling

## OpenAPI 3.0 Specification Compliance

This API documentation follows OpenAPI 3.0 specification standards. The API supports:
- JSON Schema validation
- OpenAPI specification export
- Automated documentation generation
- Interactive API explorer

### OpenAPI Components

**Security Schemes**:
```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
    OAuth2:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://api.agriculture-monitoring.example.com/oauth/token
          scopes:
            read: Read access
            write: Write access
```

**Schema Definitions**:
All data models are defined using JSON Schema and can be exported as OpenAPI components.

## Versioning

The API uses semantic versioning (v1.0.0). Backward compatibility is maintained within major versions.

**Version Header**:
```http
Accept: application/vnd.agriculture-monitoring.v1+json
```

**Deprecation Policy**:
- Endpoints are deprecated for one major version before removal
- Deprecated endpoints return warning headers
- Migration guides are provided for breaking changes

## Support

For API support, contact:
- Email: support@agriculture-monitoring.example.com
- Documentation: https://docs.agriculture-monitoring.example.com
- Status Page: https://status.agriculture-monitoring.example.com

---

*This documentation was automatically generated from the agriculture-api-template.md template.*