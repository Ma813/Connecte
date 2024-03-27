import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import routes from "./routes";
import Layout from "./components/Layout";
import Page404 from "./pages/Page404";
import { useAuth,AuthProvider } from './contexts/AuthContext';

function App() {

  
  const router = createBrowserRouter([
    {
      element: <Layout />,
      errorElement: <Page404 />,
      children: routes
    }
  ]);

  return (
    <AuthProvider> {/* Wrap RouterProvider in AuthProvider */}
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
