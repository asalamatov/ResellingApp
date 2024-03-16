import { initializeApp} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged, signOut,GoogleAuthProvider, signInWithPopup } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';
import { sendPasswordResetEmail } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';
import { getDatabase, ref, set, remove } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js"
// import { getDatabase  } from firebase/database
const firebaseConfig = {
    apiKey: "AIzaSyDB8HRp2gYjteaS4hryqzQB2fh54FDzWn0",
    authDomain: "first-b689f.firebaseapp.com",
    databaseURL: "https://first-b689f-default-rtdb.firebaseio.com",
    projectId: "first-b689f",
    storageBucket: "first-b689f.appspot.com",
    messagingSenderId: "4977128071",
    appId: "1:4977128071:web:f816e9c1f1094020aefe22",
    measurementId: "G-TD7WF2EZ6X",
};

const app = initializeApp(firebaseConfig);

/*

if (!app) init:
else: getApp()
*/
const analytics = getAnalytics(app);
const auth = getAuth(app);
const database = getDatabase(app);

function writeUserData(userId, email) {
    return set(ref(database, 'users/' + userId), {
        email: email,
    });
}

// Function to update user status
function updateUserStatus(userId, email, isOnline) {
    const userData = {
        email: email,
        status: isOnline ? 'online' : 'offline',
    };
    return set(ref(database, 'users/' + userId), userData);
}

// Function to handle Google Sign-In
function googleSignIn() {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider)
        .then((result) => {
            // Google Sign In was successful
            const user = result.user;
            console.log('Google Sign In Successful', user);
            window.location.href='/getoffer'
            //window.location.href = '/templates/'; // Adjust the URL as needed
        })
        .catch((error) => {
            // Handle Errors here
            console.error('Google Sign In Error', error);
        });
}

// Function to handle password reset
function resetPassword(email) {
    return sendPasswordResetEmail(auth, email);
}

// Function to handle user sign-up
function signUp(email, password) {
    return createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Sign up success
            const user = userCredential.user;
            writeUserData(user.uid, email);
            console.log('Signed Up Successfully!', user);
        })
        .catch((error) => {
            // Handle Errors here
            console.error('Sign Up Error', error);
        });
}

// Function to handle user sign-in
function signIn(email, password) {
    return signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Sign in success
            console.log('Signed In Successfully!', userCredential.user);
            window.location.href = '/getoffer'
            //window.location.href = '/templates/'; // Adjust the URL as needed
        })
        .catch((error) => {
            // Handle Errors here
            console.error('Sign In Error', error);
        });
}

// Function to handle user sign-out
function userSignOut() {
    return signOut(auth)
        .then(() => {
            // Sign out success
            console.log('Signed Out Successfully!');
            window.location.href = '/templates/son.html'; // Adjust the URL as needed
        })
        .catch((error) => {
            // Handle Errors here
            console.error('Sign Out Error', error);
        });
}

// Exporting functions for use in HTML files
export { signUp, signIn, googleSignIn, resetPassword, userSignOut, updateUserStatus };

// Monitor auth state changes
onAuthStateChanged(auth, (user) => {
    if (user) {
        console.log('User is signed in', user);
        // Optionally, update UI or state to reflect sign-in
    } else {
        console.log('User is signed out');
        // Optionally, update UI or state to reflect sign-out
    }
});