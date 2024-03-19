import About from "./pages/About";
import CreateRoom from "./pages/CreateRoom";
import Room from "./pages/Room";

const routes = [
  { path: "/", element: <CreateRoom /> }, // Updated path for About page
  { path: "/about", element: <About /> }, // Updated path for CreateRoom page
  { path: "/room/:gameId", element: <Room /> } // Updated path for Room page
];

export default routes;