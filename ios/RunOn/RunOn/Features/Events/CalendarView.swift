import SwiftUI

struct CalendarView<DateView: View>: View {
    @Binding var selectedDate: Date
    let content: (Date) -> DateView
    
    @State private var currentMonth: Date = Date()
    
    private let calendar = Calendar.current
    private let monthFormatter = DateFormatter()
    private let dayFormatter = DateFormatter()
    private let daysInWeek = 7
    private var weeks: [[Date]] {
        calendar.monthDates(for: currentMonth)
    }
    
    init(selectedDate: Binding<Date>, @ViewBuilder content: @escaping (Date) -> DateView) {
        self._selectedDate = selectedDate
        self.content = content
        
        monthFormatter.dateFormat = "MMMM yyyy"
        dayFormatter.dateFormat = "EEE"
    }
    
    var body: some View {
        VStack(spacing: 20) {
            // Month selector
            HStack {
                Button(action: previousMonth) {
                    Image(systemName: "chevron.left")
                }
                
                Text(monthFormatter.string(from: currentMonth))
                    .font(.title2)
                    .fontWeight(.semibold)
                
                Button(action: nextMonth) {
                    Image(systemName: "chevron.right")
                }
            }
            
            // Day headers
            HStack {
                ForEach(0..<daysInWeek, id: \.self) { index in
                    Text(dayFormatter.shortWeekdaySymbols[index])
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)
                        .frame(maxWidth: .infinity)
                }
            }
            
            // Date grid
            VStack(spacing: 8) {
                ForEach(weeks, id: \.self) { week in
                    HStack {
                        ForEach(week, id: \.self) { date in
                            if calendar.isDate(date, in: .month, of: currentMonth) {
                                Button(action: { selectedDate = date }) {
                                    VStack {
                                        Text("\(calendar.component(.day, from: date))")
                                            .font(.system(.body, design: .rounded))
                                            .fontWeight(calendar.isDate(date, inSameDayAs: selectedDate) ? .bold : .regular)
                                        
                                        content(date)
                                    }
                                    .frame(maxWidth: .infinity, minHeight: 40)
                                    .background(
                                        calendar.isDate(date, inSameDayAs: selectedDate)
                                            ? Color.blue.opacity(0.2)
                                            : Color.clear
                                    )
                                    .clipShape(RoundedRectangle(cornerRadius: 8))
                                }
                            } else {
                                Color.clear
                                    .frame(maxWidth: .infinity, minHeight: 40)
                            }
                        }
                    }
                }
            }
        }
    }
    
    private func previousMonth() {
        withAnimation {
            currentMonth = calendar.date(
                byAdding: .month,
                value: -1,
                to: currentMonth
            ) ?? currentMonth
        }
    }
    
    private func nextMonth() {
        withAnimation {
            currentMonth = calendar.date(
                byAdding: .month,
                value: 1,
                to: currentMonth
            ) ?? currentMonth
        }
    }
}

// MARK: - Calendar Helper Extensions

extension Calendar {
    func monthDates(for date: Date) -> [[Date]] {
        guard let monthInterval = dateInterval(of: .month, for: date),
              let monthFirstWeek = dateInterval(of: .weekOfMonth, for: monthInterval.start),
              let monthLastWeek = dateInterval(of: .weekOfMonth, for: monthInterval.end - 1)
        else { return [] }
        
        let weekDates = sequence(first: monthFirstWeek.start, next: { date -> Date? in
            guard date < monthLastWeek.end else { return nil }
            return self.date(byAdding: .day, value: 1, to: date)
        })
        
        return weekDates.chunked(into: 7)
    }
}

extension Sequence {
    func chunked(into size: Int) -> [[Element]] {
        var result: [[Element]] = []
        var iterator = self.makeIterator()
        var chunk: [Element] = []
        
        while let element = iterator.next() {
            chunk.append(element)
            if chunk.count == size {
                result.append(chunk)
                chunk = []
            }
        }
        
        if !chunk.isEmpty {
            result.append(chunk)
        }
        
        return result
    }
}

extension Array: Identifiable where Element: Hashable {
    public var id: Int {
        self.hashValue
    }
} 