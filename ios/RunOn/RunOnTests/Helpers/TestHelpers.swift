import Foundation
@testable import RunOn

func createMockEvent(id: String = "1") -> Event {
    Event(
        id: id,
        title: "Test Event",
        description: "Test Description",
        date: Date(),
        location: "Test Location",
        organizer: "Test Organizer",
        maxParticipants: 10,
        currentParticipants: 5,
        isRegistered: false
    )
} 