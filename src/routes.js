import About from "./pages/About";
import CreateRoom from "./pages/CreateRoom";
import Room from "./pages/Room";
import Profile from "./pages/Profile"; // Assuming you want to include this as well
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import Verify from "./pages/Verify";

const routes = [
  { path: "/", element: <CreateRoom /> }, // Updated path for About page
  { path: "/about", element: <About /> }, // Updated path for CreateRoom page
  { path: "/room/:gameId", element: <Room /> }, // Updated path for Room page
  { path: "/profile", element: <Profile /> }, // Adding Profile to the routes
  { path: "/register", element: <RegisterPage /> }, // Adding RegisterPage to the routes
  { path: "/login", element: <LoginPage /> }, // Adding LoginPage to the routes
  { path: "/verify/:verifyID", element: <Verify />}
];

export default routes;