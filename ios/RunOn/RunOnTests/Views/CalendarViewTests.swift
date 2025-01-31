import XCTest
import SwiftUI
@testable import RunOn

final class CalendarViewTests: XCTestCase {
    func testCalendarViewInitialization() {
        // Given
        let date = Date()
        let binding = Binding(
            get: { date },
            set: { _ in }
        )
        
        // When
        let sut = CalendarView(selectedDate: binding) { _ in
            EmptyView()
        }
        
        // Then
        XCTAssertNotNil(sut)
    }
    
    func testMonthDatesGeneration() {
        // Given
        let calendar = Calendar.current
        let components = DateComponents(year: 2025, month: 1, day: 1)
        let date = calendar.date(from: components)!
        
        // When
        let weeks = calendar.monthDates(for: date)
        
        // Then
        XCTAssertFalse(weeks.isEmpty)
        XCTAssertEqual(weeks.count, 5) // January 2025 has 5 weeks
        XCTAssertEqual(weeks[0].count, 7) // Each week should have 7 days
    }
    
    func testSequenceChunking() {
        // Given
        let numbers = Array(1...10)
        
        // When
        let chunks = numbers.chunked(into: 3)
        
        // Then
        XCTAssertEqual(chunks.count, 4)
        XCTAssertEqual(chunks[0], [1, 2, 3])
        XCTAssertEqual(chunks[1], [4, 5, 6])
        XCTAssertEqual(chunks[2], [7, 8, 9])
        XCTAssertEqual(chunks[3], [10])
    }
    
    func testDateNavigation() {
        // Given
        let date = Date()
        let binding = Binding(
            get: { date },
            set: { _ in }
        )
        let sut = CalendarView(selectedDate: binding) { _ in
            EmptyView()
        }
        
        // When - Move to next month
        let calendar = Calendar.current
        let currentMonth = sut.currentMonth
        sut.nextMonth()
        
        // Then
        let expectedNextMonth = calendar.date(
            byAdding: .month,
            value: 1,
            to: currentMonth
        )!
        XCTAssertEqual(
            calendar.component(.month, from: sut.currentMonth),
            calendar.component(.month, from: expectedNextMonth)
        )
        
        // When - Move to previous month
        sut.previousMonth()
        
        // Then
        XCTAssertEqual(
            calendar.component(.month, from: sut.currentMonth),
            calendar.component(.month, from: currentMonth)
        )
    }
} 