import Foundation
import Alamofire
@testable import RunOn

class MockAPIClient: APIClient {
    var mockResult: Any?
    var mockError: Error?
    
    var capturedEndpoint: String?
    var capturedMethod: HTTPMethod?
    var capturedParameters: Parameters?
    
    init() {
        super.init(baseURL: "https://mock.api.runon.app/v1")
    }
    
    override func request<T>(_ endpoint: String,
                           method: HTTPMethod = .get,
                           parameters: Parameters? = nil,
                           encoding: ParameterEncoding = URLEncoding.default) async throws -> T where T : Decodable {
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