import Foundation
@testable import RunOn

class MockEventService: EventServiceProtocol {
    var mockEvents: [Event] = []
    var mockError: Error?
    
    var fetchUserEventsCalled = false
    var unregisterCalled = false
    var searchCalled = false
    var registerCalled = false
    
    init() {} // Add explicit initializer
    
    func fetchUserEvents() async throws -> [Event] {
        fetchUserEventsCalled = true
        if let error = mockError {
            throw error
        }
        return mockEvents
    }
    
    func searchEvents(query: String) async throws -> [Event] {
        searchCalled = true
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