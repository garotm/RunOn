import XCTest
@testable import RunOn

@MainActor
final class SearchViewModelTests: XCTestCase {
    var mockEventService: MockEventService!
    var viewModel: SearchViewModel!
    
    override func setUp() {
        super.setUp()
        mockEventService = MockEventService()
        viewModel = SearchViewModel(eventService: mockEventService)
    }
    
    override func tearDown() {
        mockEventService = nil
        viewModel = nil
        super.tearDown()
    }
    
    func testSearchWithEmptyQuery() {
        // When
        viewModel.search(query: "")
        
        // Then
        XCTAssertFalse(mockEventService.searchCalled)
        XCTAssertTrue(viewModel.searchResults.isEmpty)
        XCTAssertNil(viewModel.error)
    }
    
    func testSearchSuccess() async {
        // Given
        let mockEvents = [createMockEvent(), createMockEvent(id: "2")]
        mockEventService.mockEvents = mockEvents
        
        // When
        viewModel.search(query: "test")
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.searchCalled)
        XCTAssertEqual(viewModel.searchResults.count, 2)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testSearchError() async {
        // Given
        mockEventService.mockError = APIError.networkError(NSError(domain: "", code: -1))
        
        // When
        viewModel.search(query: "test")
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.searchCalled)
        XCTAssertTrue(viewModel.searchResults.isEmpty)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNotNil(viewModel.error)
    }
    
    func testRegisterForEventSuccess() async {
        // Given
        let event = createMockEvent()
        
        // When
        viewModel.registerForEvent(event)
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.registerCalled)
        XCTAssertNil(viewModel.error)
    }
    
    func testRegisterForEventError() async {
        // Given
        let event = createMockEvent()
        mockEventService.mockError = APIError.unauthorized
        
        // When
        viewModel.registerForEvent(event)
        
        // Wait for async operation to complete
        await Task.yield()
        
        // Then
        XCTAssertTrue(mockEventService.registerCalled)
        XCTAssertNotNil(viewModel.error)
    }
} 