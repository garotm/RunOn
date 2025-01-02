import XCTest
@testable import RunOn

final class EventServiceTests: XCTestCase {
    var mockAPIClient: MockAPIClient!
    var eventService: EventService!
    
    override func setUp() {
        super.setUp()
        mockAPIClient = MockAPIClient()
        eventService = EventService(apiClient: mockAPIClient)
    }
    
    override func tearDown() {
        mockAPIClient = nil
        eventService = nil
        super.tearDown()
    }
    
    func testSearchEvents() async throws {
        // Given
        let mockEvents = [createMockEvent(), createMockEvent(id: "2")]
        mockAPIClient.mockResult = mockEvents
        
        // When
        let result = try await eventService.searchEvents(query: "test")
        
        // Then
        XCTAssertEqual(mockAPIClient.capturedEndpoint, "/events/search")
        XCTAssertEqual(mockAPIClient.capturedMethod, .get)
        XCTAssertEqual(mockAPIClient.capturedParameters as? [String: String], ["query": "test"])
        XCTAssertEqual(result.count, 2)
    }
    
    func testSearchEventsError() async {
        // Given
        mockAPIClient.mockError = APIError.networkError(NSError(domain: "", code: -1))
        
        // When/Then
        do {
            _ = try await eventService.searchEvents(query: "test")
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is APIError)
        }
    }
    
    func testFetchUserEvents() async throws {
        // Given
        let mockEvents = [createMockEvent()]
        mockAPIClient.mockResult = mockEvents
        
        // When
        let result = try await eventService.fetchUserEvents()
        
        // Then
        XCTAssertEqual(mockAPIClient.capturedEndpoint, "/events/user")
        XCTAssertEqual(mockAPIClient.capturedMethod, .get)
        XCTAssertEqual(result.count, 1)
    }
    
    func testRegisterForEvent() async throws {
        // Given
        mockAPIClient.mockResult = EmptyResponse()
        let eventId = "test-id"
        
        // When
        try await eventService.registerForEvent(eventId: eventId)
        
        // Then
        XCTAssertEqual(mockAPIClient.capturedEndpoint, "/events/\(eventId)/register")
        XCTAssertEqual(mockAPIClient.capturedMethod, .post)
    }
    
    func testUnregisterFromEvent() async throws {
        // Given
        mockAPIClient.mockResult = EmptyResponse()
        let eventId = "test-id"
        
        // When
        try await eventService.unregisterFromEvent(eventId: eventId)
        
        // Then
        XCTAssertEqual(mockAPIClient.capturedEndpoint, "/events/\(eventId)/unregister")
        XCTAssertEqual(mockAPIClient.capturedMethod, .delete)
    }
} 