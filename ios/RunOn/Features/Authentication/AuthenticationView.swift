import SwiftUI
import GoogleSignIn

struct AuthenticationView: View {
    @EnvironmentObject var viewModel: AuthenticationViewModel
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Welcome to RunOn")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Sign in to get started")
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Button(action: {
                viewModel.signInWithGoogle()
            }) {
                HStack {
                    Image(systemName: "g.circle.fill")
                        .foregroundColor(.blue)
                    Text("Sign in with Google")
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(8)
            }
        }
        .padding()
    }
} 