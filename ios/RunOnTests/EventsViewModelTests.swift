import XCTest
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
    
    func testUnregisterFromEventSuccess() async {
        // Given
        let event = createMockEvent()
        viewModel.events = [event]
        
        // When
        viewModel.unregisterFromEvent(event)
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.unregisterCalled)
        XCTAssertTrue(viewModel.events.isEmpty)
        XCTAssertNil(viewModel.error)
    }
    
    func testUnregisterFromEventError() async {
        // Given
        let event = createMockEvent()
        viewModel.events = [event]
        mockEventService.mockError = APIError.unauthorized
        
        // When
        viewModel.unregisterFromEvent(event)
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.unregisterCalled)
        XCTAssertEqual(viewModel.events.count, 1)
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
} 