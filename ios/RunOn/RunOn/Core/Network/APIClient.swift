import Foundation
import Alamofire

enum APIError: Error {
    case invalidURL
    case decodingError
    case networkError(Error)
    case serverError(Int)
    case unauthorized
    
    var message: String {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .decodingError:
            return "Failed to decode response"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .serverError(let code):
            return "Server error: \(code)"
        case .unauthorized:
            return "Unauthorized access"
        }
    }
}

class APIClient {
    let baseURL: String
    
    init(baseURL: String = "http://127.0.0.1:8000") {
        self.baseURL = baseURL
    }
    
    private var headers: HTTPHeaders {
        var headers: HTTPHeaders = [
            "Content-Type": "application/json",
            "Accept": "application/json"
        ]
        
        // Use the Google client ID as the Bearer token for local development
        if let clientID = Bundle.main.object(forInfoDictionaryKey: "GIDClientID") as? String {
            headers["Authorization"] = "Bearer \(clientID)"
        }
        
        return headers
    }
    
    func request<T: Decodable>(_ endpoint: String,
                              method: HTTPMethod = .post,
                              parameters: Parameters? = nil,
                              encoding: ParameterEncoding = URLEncoding.default) async throws -> T {
        let url = baseURL + endpoint
        
        return try await withCheckedThrowingContinuation { continuation in
            AF.request(url,
                      method: method,
                      parameters: parameters,
                      encoding: encoding,
                      headers: headers)
            .validate()
            .responseDecodable(of: T.self) { response in
                // Print response for debugging
                print("Response status code: \(String(describing: response.response?.statusCode))")
                if let data = response.data, let str = String(data: data, encoding: .utf8) {
                    print("Response data: \(str)")
                }
                
                switch response.result {
                case .success(let value):
                    continuation.resume(returning: value)
                case .failure(let error):
                    if let statusCode = response.response?.statusCode {
                        switch statusCode {
                        case 401:
                            continuation.resume(throwing: APIError.unauthorized)
                        default:
                            continuation.resume(throwing: APIError.serverError(statusCode))
                        }
                    } else {
                        continuation.resume(throwing: APIError.networkError(error))
                    }
                }
            }
        }
    }
    
    func setAuthToken(_ token: String) {
        UserDefaults.standard.set(token, forKey: "auth_token")
    }
    
    func clearAuthToken() {
        UserDefaults.standard.removeObject(forKey: "auth_token")
    }
} 