import XCTest
import CoreLocation
@testable import RunOn

@MainActor
final class EventsViewModelTests: XCTestCase {
    var mockEventService: MockEventService!
    var viewModel: EventsViewModel!
    
    override func setUp() {
        super.setUp()
        mockEventService = MockEventService()
        viewModel = EventsViewModel(eventService: mockEventService)
    }
    
    override func tearDown() {
        mockEventService = nil
        viewModel = nil
        super.tearDown()
    }
    
    func testLoadEventsSuccess() async {
        // Given
        let mockEvents = [createMockEvent(), createMockEvent(id: "2")]
        mockEventService.mockEvents = mockEvents
        
        // When
        viewModel.loadEvents()
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.fetchUserEventsCalled)
        XCTAssertEqual(viewModel.events.count, 2)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testLoadEventsError() async {
        // Given
        mockEventService.mockError = APIError.networkError(NSError(domain: "", code: -1))
        
        // When
        viewModel.loadEvents()
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.fetchUserEventsCalled)
        XCTAssertTrue(viewModel.events.isEmpty)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNotNil(viewModel.error)
    }
    
    func testRefreshEventsSuccess() async {
        // Given
        let mockEvents = [createMockEvent()]
        mockEventService.mockEvents = mockEvents
        
        // When
        await viewModel.refreshEvents()
        
        // Then
        XCTAssertTrue(mockEventService.fetchUserEventsCalled)
        XCTAssertEqual(viewModel.events.count, 1)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testRefreshEventsError() async {
        // Given
        mockEventService.mockError = APIError.unauthorized
        
        // When
        await viewModel.refreshEvents()
        
        // Then
        XCTAssertTrue(mockEventService.fetchUserEventsCalled)
        XCTAssertTrue(viewModel.events.isEmpty)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNotNil(viewModel.error)
    }
    
    func testLoadEventsWithLocation() async {
        // Given
        let location = CLLocation(latitude: 43.1011, longitude: -78.9511) // Lockport, NY
        let expectedEvents = [
            createMockEvent(id: "1"),
            createMockEvent(id: "2")
        ]
        mockEventService.mockEvents = expectedEvents
        
        // When
        viewModel.userLocation = location
        await viewModel.loadEvents()
        
        // Then
        XCTAssertTrue(mockEventService.searchCalled)
        XCTAssertEqual(viewModel.events.count, expectedEvents.count)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testLoadEventsWithoutLocation() async {
        // Given
        let expectedEvents = [createMockEvent(id: "1")]
        mockEventService.mockEvents = expectedEvents
        
        // When
        await viewModel.loadEvents()
        
        // Then
        XCTAssertTrue(mockEventService.fetchUserEventsCalled)
        XCTAssertEqual(viewModel.events.count, expectedEvents.count)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testSearchEvents() async {
        // Given
        let query = "marathon"
        let expectedEvents = [createMockEvent(id: "1")]
        mockEventService.mockEvents = expectedEvents
        
        // When
        await viewModel.searchEvents(query: query)
        
        // Then
        XCTAssertTrue(mockEventService.searchCalled)
        XCTAssertEqual(viewModel.events.count, expectedEvents.count)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testSearchEventsError() async {
        // Given
        mockEventService.mockError = APIError.networkError
        
        // When
        await viewModel.searchEvents(query: "5k")
        
        // Then
        XCTAssertTrue(viewModel.events.isEmpty)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNotNil(viewModel.error)
    }
    
    func testLocationUpdateTriggersEventReload() {
        // Given
        let location = CLLocation(latitude: 43.1011, longitude: -78.9511)
        let locations = [location]
        
        // When
        viewModel.locationManager(CLLocationManager(), didUpdateLocations: locations)
        
        // Then
        XCTAssertEqual(viewModel.userLocation?.coordinate.latitude, location.coordinate.latitude)
        XCTAssertEqual(viewModel.userLocation?.coordinate.longitude, location.coordinate.longitude)
    }
    
    func testLocationErrorFallsBackToAllEvents() {
        // Given
        let error = NSError(domain: "test", code: 0, userInfo: nil)
        
        // When
        viewModel.locationManager(CLLocationManager(), didFailWithError: error)
        
        // Then
        XCTAssertTrue(mockEventService.fetchUserEventsCalled)
    }
} 