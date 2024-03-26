import { Link } from "react-router-dom";
import "../styles/Header.css";
import PathConstants from "../routes/constants";
import '../styles/Default.css';
import { useAuth } from '../contexts/AuthContext';

export default function Header() {
  const { isAuthenticated, logout } = useAuth();
  return (
    <header>
      <div className="header-div">
        <h1 className="title">
          <Link to={PathConstants.Game}>Connect ė</Link>
        </h1>
        <nav className="navbar">
          <ul className="nav-list ">

            <li className="nav-item btn btn-secondary">
              <Link to={PathConstants.ABOUT}>About</Link>
            </li>
            <li className="nav-item btn btn-secondary">
              <Link to={PathConstants.CREATEROOM}>Play Game</Link>
            </li>
            {isAuthenticated ? (
              <>
                <li className="nav-item btn btn-secondary">
                  <Link to={PathConstants.PROFILE}>Profile</Link>
                </li>
                <li className="nav-item">
                  <button className="btn btn-secondary" onClick={logout}>Logout</button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item btn btn-secondary">
                  <Link to={PathConstants.REGISTER}>Register</Link>
                </li>
                <li className="nav-item btn btn-secondary">
                  <Link to={PathConstants.LOGIN}>Login</Link>
                </li>
              </>
            )}
          </ul>
        </nav>
      </div>
    </header>
  );
}
