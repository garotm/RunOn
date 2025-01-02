import Foundation
import Alamofire
@testable import RunOn

class MockAPIClient: APIClientProtocol {
    var mockResult: Any?
    var mockError: Error?
    
    var capturedEndpoint: String?
    var capturedMethod: HTTPMethod?
    var capturedParameters: Parameters?
    
    init() {} // Add explicit initializer
    
    func request<T>(_ endpoint: String, method: HTTPMethod, parameters: Parameters?) async throws -> T where T : Decodable {
        capturedEndpoint = endpoint
        capturedMethod = method
        capturedParameters = parameters
        
        if let error = mockError {
            throw error
        }
        
        if let result = mockResult as? T {
            return result
        }
        
        throw APIError.decodingError
    }
}

// Add EmptyResponse struct implementation
struct EmptyResponse: Codable {
    init() {} // Add explicit initializer
} 