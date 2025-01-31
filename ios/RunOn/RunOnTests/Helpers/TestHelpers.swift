import Foundation
@testable import RunOn

func createMockEvent(
    id: String = "1",
    name: String = "Test Event",
    date: Date = Date(),
    location: String = "Test Location",
    description: String = "Test Description",
    url: String = "https://test.com",
    distance: Double = 5.0
) -> Event {
    Event(
        id: id,
        name: name,
        date: date,
        location: location,
        description: description,
        url: url,
        distance: distance
    )
}

extension Date {
    static func daysFromNow(_ days: Int) -> Date {
        Calendar.current.date(byAdding: .day, value: days, to: Date()) ?? Date()
    }
    
    static func monthsFromNow(_ months: Int) -> Date {
        Calendar.current.date(byAdding: .month, value: months, to: Date()) ?? Date()
    }
}

extension Event {
    static func mockEvents() -> [Event] {
        [
            createMockEvent(
                id: "1",
                name: "Local 5K",
                date: .daysFromNow(7),
                location: "Local Park",
                description: "Fun local 5K run",
                distance: 5.0
            ),
            createMockEvent(
                id: "2",
                name: "Half Marathon",
                date: .daysFromNow(14),
                location: "City Center",
                description: "Challenging half marathon",
                distance: 21.1
            ),
            createMockEvent(
                id: "3",
                name: "Marathon",
                date: .monthsFromNow(2),
                location: "Downtown",
                description: "Full marathon event",
                distance: 42.2
            ),
            createMockEvent(
                id: "4",
                name: "Fun Run",
                date: .daysFromNow(3),
                location: "Beach",
                description: "Family-friendly fun run",
                distance: 3.0
            )
        ]
    }
} 