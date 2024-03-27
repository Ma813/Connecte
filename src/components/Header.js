import { Link } from "react-router-dom";
import "../styles/Header.css";
import PathConstants from "../routes/constants";
import '../styles/Default.css';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const { isAuthenticated, logout,CheckIfAuthenticated } = useAuth();
  const navigate = useNavigate();
  CheckIfAuthenticated()
  
  const handleSubmit = async (e) => {
    logout()
    navigate('/')
  }
  
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
                  <button className="btn btn-secondary" onClick={handleSubmit}>Logout</button>
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
