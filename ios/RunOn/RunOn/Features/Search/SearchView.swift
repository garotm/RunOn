import SwiftUI

struct SearchView: View {
    @StateObject private var viewModel = SearchViewModel()
    @State private var searchText = ""
    
    var body: some View {
        NavigationView {
            ZStack {
                List {
                    if viewModel.searchResults.isEmpty && !searchText.isEmpty {
                        Text("No events found")
                            .foregroundColor(.secondary)
                    } else {
                        ForEach(viewModel.searchResults) { event in
                            EventRow(event: event)
                                .swipeActions {
                                    Button("Register") {
                                        viewModel.registerForEvent(event)
                                    }
                                    .tint(.green)
                                }
                        }
                    }
                }
                .searchable(text: $searchText)
                .onChange(of: searchText) { _, newValue in
                    viewModel.search(query: newValue)
                }
                .overlay {
                    if viewModel.isLoading {
                        ProgressView()
                    }
                }
                
                if let error = viewModel.error {
                    VStack {
                        Text(error)
                            .foregroundColor(.red)
                            .padding()
                            .background(
                                RoundedRectangle(cornerRadius: 8)
                                    .fill(Color(.systemBackground))
                                    .shadow(radius: 2)
                            )
                    }
                    .padding()
                }
            }
            .navigationTitle("Search Events")
        }
    }
} 