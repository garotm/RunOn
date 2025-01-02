import XCTest
import Alamofire
@testable import RunOn

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