import SwiftUI

struct EventsView: View {
    @StateObject private var viewModel = EventsViewModel()
    @State private var selectedDate: Date = Date()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Filter chips
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(["Next month", "Near lockport, ny", "San Antonio", "Austin"], id: \.self) { filter in
                            FilterChip(
                                title: filter,
                                isSelected: false
                            ) {
                                viewModel.searchEvents(query: filter)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical, 8)
                
                // Calendar view
                CalendarView(selectedDate: $selectedDate) { date in
                    let dateEvents = viewModel.events.filter { event in
                        Calendar.current.isDate(event.date, inSameDayAs: date)
                    }
                    
                    if !dateEvents.isEmpty {
                        Text("\(dateEvents.count)")
                            .font(.caption)
                            .padding(4)
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .clipShape(Circle())
                    }
                }
                .padding(.horizontal)
                
                // Events for selected date
                ScrollView {
                    LazyVStack(spacing: 16) {
                        let filteredEvents = viewModel.events.filter { event in
                            Calendar.current.isDate(event.date, inSameDayAs: selectedDate)
                        }
                        
                        if filteredEvents.isEmpty {
                            Text("No events for this date")
                                .foregroundColor(.secondary)
                                .padding()
                        } else {
                            ForEach(filteredEvents) { event in
                                EventCard(event: event)
                            }
                        }
                    }
                    .padding()
                }
            }
            .navigationTitle("Running Events")
            .overlay {
                if viewModel.isLoading {
                    ProgressView()
                }
            }
            .alert("Error", isPresented: Binding(
                get: { viewModel.error != nil },
                set: { if !$0 { viewModel.error = nil } }
            )) {
                Text(viewModel.error ?? "")
            }
        }
        .onAppear {
            viewModel.loadEvents()
        }
    }
}

// MARK: - Supporting Views

struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isSelected ? Color.blue : Color.gray.opacity(0.2))
                .foregroundColor(isSelected ? .white : .primary)
                .clipShape(Capsule())
        }
    }
}

struct EventCard: View {
    let event: Event
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top) {
                // Date display
                VStack(alignment: .center) {
                    Text(event.date, format: .dateTime.month(.abbreviated))
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text(event.date, format: .dateTime.day())
                        .font(.title)
                        .fontWeight(.bold)
                }
                .frame(width: 50)
                
                VStack(alignment: .leading, spacing: 4) {
                    Text(event.name)
                        .font(.headline)
                    Text(event.location)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    if event.distance > 0 {
                        Text(String(format: "%.1f km", event.distance))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                Spacer()
                
                // Preview image or map
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.gray.opacity(0.2))
                    .frame(width: 60, height: 60)
                    .overlay {
                        Image(systemName: "map")
                            .foregroundColor(.secondary)
                    }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

// MARK: - Supporting Types

enum EventFilter: String, CaseIterable, Identifiable {
    case all
    case nextMonth = "next_month"
    case free
    case nearby
    
    var id: String { rawValue }
    
    var title: String {
        switch self {
        case .all: return "All"
        case .nextMonth: return "Next Month"
        case .free: return "Free"
        case .nearby: return "Nearby"
        }
    }
    
    func matches(_ event: Event) -> Bool {
        switch self {
        case .all:
            return true
        case .nextMonth:
            let calendar = Calendar.current
            guard let nextMonth = calendar.date(
                byAdding: .month,
                value: 1,
                to: calendar.startOfDay(for: Date())
            ) else { return false }
            return event.date <= nextMonth
        case .free:
            return event.isFree
        case .nearby:
            return event.isNearby // Implement distance calculation
        }
    }
} 
