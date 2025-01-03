import Foundation
import GoogleSignIn
import SwiftUI

@MainActor
class AuthenticationViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var error: String?
    
    init() {
        print("AuthenticationViewModel initialized")
        // Check if user was previously signed in
        checkSignInStatus()
    }
    
    func signInWithGoogle() {
        print("signInWithGoogle() called")
        
        // Debug info
        print("=== Google Sign In Debug Info ===")
        print("Bundle ID: \(Bundle.main.bundleIdentifier ?? "Not found")")
        
        if let clientID = Bundle.main.object(forInfoDictionaryKey: "GIDClientID") as? String {
            print("Client ID: \(clientID)")
        } else {
            print("Client ID not found in Info.plist")
        }
        
        if let urlTypes = Bundle.main.object(forInfoDictionaryKey: "CFBundleURLTypes") as? [[String: Any]],
           let urlSchemes = urlTypes.first?["CFBundleURLSchemes"] as? [String] {
            print("URL Schemes: \(urlSchemes)")
        } else {
            print("URL Schemes not found in Info.plist")
        }
        print("===============================")
        
        guard let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
              let rootViewController = windowScene.windows.first?.rootViewController else {
            print("Failed to get root view controller")
            self.error = "Cannot find root view controller"
            return
        }
        
        print("About to call GIDSignIn.sharedInstance.signIn")
        GIDSignIn.sharedInstance.signIn(withPresenting: rootViewController) { [weak self] result, error in
            print("Inside GIDSignIn completion handler")
            guard let self = self else { return }
            
            if let error = error {
                print("Sign in error: \(error)")
                if let gidError = error as? GIDSignInError {
                    switch gidError.code {
                    case .canceled:
                        self.error = "Sign in was canceled"
                    case .hasNoAuthInKeychain:
                        self.error = "No authentication in keychain"
                    case .unknown:
                        self.error = "Unknown error: \(error.localizedDescription)"
                    @unknown default:
                        self.error = error.localizedDescription
                    }
                } else {
                    self.error = error.localizedDescription
                }
                return
            }
            
            guard let user = result?.user else {
                print("No user data received")
                self.error = "No user data received"
                return
            }
            
            // Print user information
            print("=== Successful Sign In ===")
            print("User ID: \(user.userID ?? "Not available")")
            print("Email: \(user.profile?.email ?? "Not available")")
            print("Full Name: \(user.profile?.name ?? "Not available")")
            print("Access Token: \(user.accessToken.tokenString)")
            print("========================")
            
            // Update the authentication state
            DispatchQueue.main.async {
                self.isAuthenticated = true
                print("Authentication state updated: isAuthenticated = true")
            }
        }
    }
    
    func signOut() {
        print("Signing out...")
        GIDSignIn.sharedInstance.signOut()
        DispatchQueue.main.async {
            self.isAuthenticated = false
            print("User signed out")
        }
    }
    
    func checkSignInStatus() {
        print("Checking sign in status...")
        if GIDSignIn.sharedInstance.hasPreviousSignIn() {
            print("Found previous sign in, attempting to restore...")
            GIDSignIn.sharedInstance.restorePreviousSignIn { [weak self] user, error in
                guard let self = self else { return }
                
                if let error = error {
                    print("Restore sign in error: \(error)")
                    self.error = error.localizedDescription
                    return
                }
                
                if let user = user {
                    print("Successfully restored previous sign in")
                    print("User email: \(user.profile?.email ?? "Not available")")
                    DispatchQueue.main.async {
                        self.isAuthenticated = true
                        print("Authentication state restored: isAuthenticated = true")
                    }
                } else {
                    print("No previous user found")
                }
            }
        } else {
            print("No previous sign in found")
        }
    }
} 