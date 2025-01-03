import Foundation
@testable import RunOn

func createMockEvent(id: String = "1") -> Event {
    Event(
        id: id,
        name: "Test Event",
        date: Date(),
        location: "Test Location",
        description: "Test Description",
        distance: 5.0,
        registrationDeadline: Date().addingTimeInterval(86400)
    )
} 