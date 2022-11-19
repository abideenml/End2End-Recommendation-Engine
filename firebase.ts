// Import the functions you need from the SDKs you need
import { initializeApp, getApp, getApps } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: "AIzaSyAttvegjAo-YvyceiPVGq9bTPdszeQbaQA",
  authDomain: "kryptonite-a5ac4.firebaseapp.com",
  projectId: "kryptonite-a5ac4",
  storageBucket: "kryptonite-a5ac4.appspot.com",
  messagingSenderId: "465371408926",
  appId: "1:465371408926:web:5e78c39466f36d03ed5c0f",
  measurementId: "G-MXHX7B67GC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore()
const auth = getAuth()

export default app
export { auth, db }
