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
        
        // Print configuration for debugging
        print("=== Google Sign In Configuration ===")
        print("Client ID: \(clientID)")
        if let urlTypes = Bundle.main.object(forInfoDictionaryKey: "CFBundleURLTypes") as? [[String: Any]],
           let urlSchemes = urlTypes.first?["CFBundleURLSchemes"] as? [String] {
            print("URL Schemes: \(urlSchemes)")
        }
        print("Bundle ID: \(Bundle.main.bundleIdentifier ?? "Not found")")
        print("===============================")
        
        // Configure Google Sign In
        let config = GIDConfiguration(clientID: clientID)
        GIDSignIn.sharedInstance.configuration = config
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