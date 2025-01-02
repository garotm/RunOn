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

class MockEventService: EventServiceProtocol {
    var mockEvents: [Event] = []
    var mockError: Error?
    var registerCalled = false
    var unregisterCalled = false
    var searchCalled = false
    var fetchUserEventsCalled = false
    
    func searchEvents(query: String) async throws -> [Event] {
        searchCalled = true
        if let error = mockError {
            throw error
        }
        return mockEvents
    }
    
    func fetchUserEvents() async throws -> [Event] {
        fetchUserEventsCalled = true
        if let error = mockError {
            throw error
        }
        return mockEvents
    }
    
    func registerForEvent(eventId: String) async throws {
        registerCalled = true
        if let error = mockError {
            throw error
        }
    }
    
    func unregisterFromEvent(eventId: String) async throws {
        unregisterCalled = true
        if let error = mockError {
            throw error
        }
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