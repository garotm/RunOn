import SwiftUI
import GoogleSignIn

@main
struct RunOnApp: App {
    @StateObject private var authViewModel = AuthenticationViewModel()
    
    init() {
        // Configure Google Sign In
        guard let clientID = Bundle.main.object(forInfoDictionaryKey: "GIDClientID") as? String else {
            fatalError("No Google Sign In client ID found in Info.plist")
        }
        GIDSignIn.sharedInstance.configuration = GIDConfiguration(clientID: clientID)
    }
    
    var body: some Scene {
        WindowGroup {
            if authViewModel.isAuthenticated {
                TabView {
                    SearchView()
                        .tabItem {
                            Label("Search", systemImage: "magnifyingglass")
                        }
                    
                    EventsView()
                        .tabItem {
                            Label("Events", systemImage: "calendar")
                        }
                }
                .environmentObject(authViewModel)
            } else {
                AuthenticationView()
                    .environmentObject(authViewModel)
                    .onAppear {
                        authViewModel.checkSignInStatus()
                    }
            }
        }
    }
} 