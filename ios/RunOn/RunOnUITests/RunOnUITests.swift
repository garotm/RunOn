//
//  RunOnUITests.swift
//  RunOnUITests
//
//  Created by Garot Conklin on 12/31/24.
//

import XCTest

final class RunOnUITests: XCTestCase {
    var app: XCUIApplication!
    
    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.

        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false

        // In UI tests it's important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
        app = XCUIApplication()
        app.launch()
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    @MainActor
    func testExample() throws {
        // UI tests must launch the application that they test.
        let app = XCUIApplication()
        app.launch()

        // Use XCTAssert and related functions to verify your tests produce the correct results.
    }

    @MainActor
    func testLaunchPerformance() throws {
        if #available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 7.0, *) {
            // This measures how long it takes to launch your application.
            measure(metrics: [XCTApplicationLaunchMetric()]) {
                XCUIApplication().launch()
            }
        }
    }

    func testCalendarViewNavigation() throws {
        // Test month navigation
        let prevMonthButton = app.buttons["chevron.left"]
        let nextMonthButton = app.buttons["chevron.right"]
        
        XCTAssertTrue(prevMonthButton.exists)
        XCTAssertTrue(nextMonthButton.exists)
        
        nextMonthButton.tap()
        // Verify month changed (specific assertions will depend on your UI implementation)
        
        prevMonthButton.tap()
        // Verify returned to current month
    }
    
    func testFilterChips() throws {
        // Test location-based filters
        let nextMonthFilter = app.buttons["Next month"]
        let lockportFilter = app.buttons["Near lockport, ny"]
        let sanAntonioFilter = app.buttons["San Antonio"]
        let austinFilter = app.buttons["Austin"]
        
        XCTAssertTrue(nextMonthFilter.exists)
        XCTAssertTrue(lockportFilter.exists)
        XCTAssertTrue(sanAntonioFilter.exists)
        XCTAssertTrue(austinFilter.exists)
        
        // Test filter selection
        nextMonthFilter.tap()
        // Verify filter applied
        
        lockportFilter.tap()
        // Verify filter applied
    }
    
    func testEventCardInteraction() throws {
        // Assuming there's at least one event card
        let eventCard = app.scrollViews.firstMatch
        
        XCTAssertTrue(eventCard.exists)
        
        // Test event card elements exist
        let eventTitle = eventCard.staticTexts.element(boundBy: 0)
        let eventLocation = eventCard.staticTexts.element(boundBy: 1)
        let eventTime = eventCard.staticTexts.element(boundBy: 2)
        let eventDistance = eventCard.staticTexts.element(boundBy: 3)
        
        XCTAssertTrue(eventTitle.exists)
        XCTAssertTrue(eventLocation.exists)
        XCTAssertTrue(eventTime.exists)
        XCTAssertTrue(eventDistance.exists)
    }
    
    func testCalendarDateSelection() throws {
        // Test date selection in calendar
        let calendar = app.otherElements["CalendarView"]
        XCTAssertTrue(calendar.exists)
        
        // Tap a date (you'll need to adjust the exact identifier based on your implementation)
        let dateCell = calendar.buttons.element(boundBy: 15) // Middle of month
        dateCell.tap()
        
        // Verify event list updated for selected date
        let eventsList = app.scrollViews["EventsList"]
        XCTAssertTrue(eventsList.exists)
    }
    
    func testLocationPermissionFlow() throws {
        // Test location permission dialog appears
        let locationAlert = app.alerts.firstMatch
        
        if locationAlert.exists {
            // Allow location access
            locationAlert.buttons["Allow While Using App"].tap()
            
            // Verify events list updated with location-based results
            let eventsList = app.scrollViews["EventsList"]
            XCTAssertTrue(eventsList.exists)
        }
    }
    
    func testEventListRefresh() throws {
        // Test pull to refresh
        let eventsList = app.scrollViews["EventsList"]
        
        // Perform pull to refresh gesture
        let start = eventsList.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
        let end = eventsList.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.8))
        start.press(forDuration: 0.1, thenDragTo: end)
        
        // Verify refresh indicator appeared
        let refreshControl = app.activityIndicators.firstMatch
        XCTAssertTrue(refreshControl.exists)
    }
}
