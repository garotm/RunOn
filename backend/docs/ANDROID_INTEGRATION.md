# Android Integration Guide

This guide outlines the steps required to integrate the RunOn backend with the Android application.

## 1. Backend API Documentation

### Generate OpenAPI Specification

First, we need to generate OpenAPI/Swagger documentation for the Android team:

```bash
# In backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Current Endpoints

#### Authentication

```http
POST /auth/google
Content-Type: application/json
Authorization: Bearer {GOOGLE_ID_TOKEN}

Response: {
    "access_token": "string",
    "token_type": "bearer"
}
```

#### Event Search

```http
POST /events/search
Content-Type: application/json
Authorization: Bearer {ACCESS_TOKEN}

Query Parameters:
- query: string (required)

Response: [
    "event1",
    "event2"
]
```

## 2. Android Setup Requirements

### 1. Dependencies

Add to `app/build.gradle`:

```gradle
dependencies {
    // Retrofit for API calls
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    
    // Google Auth
    implementation 'com.google.android.gms:play-services-auth:20.7.0'
    
    // Coroutines for async operations
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3'
}
```

### 2. API Interface

Create `app/src/main/java/com/flexrpl/runon/api/RunOnApi.kt`:

```kotlin
interface RunOnApi {
    @POST("events/search")
    suspend fun searchEvents(
        @Query("query") query: String,
        @Header("Authorization") auth: String
    ): List<String>

    @POST("auth/google")
    suspend fun authenticateGoogle(
        @Header("Authorization") idToken: String
    ): AuthResponse

    data class AuthResponse(
        val access_token: String,
        val token_type: String
    )
}
```

### 3. API Client

Create `app/src/main/java/com/flexrpl/runon/api/ApiClient.kt`:

```kotlin
object ApiClient {
    private const val BASE_URL = "http://your-backend-url:8000/"
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        
    val api: RunOnApi = retrofit.create(RunOnApi::class.java)
}
```

## 3. Backend Deployment for Android Development

### 1. Local Testing

For local Android development:

```bash
# In backend directory
./scripts/run_local.sh
```

Update Android `BASE_URL` to:

```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/"  // Android Emulator
// or
private const val BASE_URL = "http://your-computer-ip:8000/"  // Physical Device
```

### 2. Production Deployment

For production:

1. Deploy backend to cloud provider (e.g., Google Cloud Run)
2. Update Android `BASE_URL` to production URL
3. Enable HTTPS
4. Update CORS settings in backend

## 4. Security Considerations

### 1. Backend Updates Required

Add to `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific Android app scheme
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Android Security

1. Store sensitive data in Android Keystore
2. Implement certificate pinning
3. Implement token refresh mechanism
4. Handle expired tokens gracefully

## 5. Testing Integration

### 1. Backend Integration Tests

Create `backend/tests/integration/test_android_integration.py`:

```python
def test_android_auth_flow():
    # Test complete Android authentication flow
    pass

def test_android_search_flow():
    # Test Android search functionality
    pass
```

### 2. Android Integration Tests

Create appropriate tests in Android project:

```kotlin
@Test
fun testBackendIntegration() {
    // Test API calls to backend
}
```

## 6. Debugging Tips

### Backend Debugging

1. Enable detailed logging:

   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Add Android-specific debug endpoints:

   ```python
   @app.get("/debug/android")
   async def debug_android():
       return {"status": "ok", "version": "1.0"}
   ```

### Android Debugging

1. Use OkHttp logging interceptor:

   ```kotlin
   implementation 'com.squareup.okhttp3:logging-interceptor:4.9.1'
   ```

2. Add debug logging:

   ```kotlin
   if (BuildConfig.DEBUG) {
       // Add logging interceptor
   }
   ```

## 7. Next Steps

1. Deploy backend to staging environment
2. Update Android app configuration
3. Implement error handling
4. Add monitoring and analytics
5. Set up CI/CD pipeline for both components
6. Plan for scalability and performance testing

## Common Integration Issues

1. **CORS Issues**
   - Verify CORS middleware configuration
   - Check Android network security config

2. **Authentication Flow**
   - Test token exchange process
   - Verify Google Sign-In configuration

3. **Network Issues**
   - Configure Android network security
   - Handle various network states

4. **Version Compatibility**
   - Maintain API version compatibility
   - Plan for backward compatibility

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Android Network Security Config](https://developer.android.com/training/articles/security-config)
- [Google Sign-In for Android](https://developers.google.com/identity/sign-in/android)
- [Retrofit Documentation](https://square.github.io/retrofit/)
