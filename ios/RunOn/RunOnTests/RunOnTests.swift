import XCTest
import Alamofire
@testable import RunOn

// MARK: - Mocks
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
                           encoding: ParameterEncoding = URLEncoding.default) async throws -> T {
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

// MARK: - Helper Functions
extension XCTestCase {
    func createMockEvent(id: String = "1") -> Event {
        return Event(
            id: id,
            name: "Test Event",
            date: Date(),
            location: "Test Location",
            description: "Test Description",
            distance: 5.0,
            registrationDeadline: Date().addingTimeInterval(86400)
        )
    }
} 