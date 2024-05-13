import React from "react"
import PathConstants from "./constants"


const About = React.lazy(() => import("../pages/About"))
const CreateRoom = React.lazy(() => import("../pages/CreateRoom"))
const Room = React.lazy(() => import("../pages/Room"))
const PROFILE = React.lazy(() => import("../pages/Profile"))
const REGISTER = React.lazy(() => import("../pages/RegisterPage"))
const LOGIN = React.lazy(() => import("../pages/LoginPage"))
const VERIFY = React.lazy(() => import("../pages/Verify"))
const FORGOTPASSWORD = React.lazy(() => import("../pages/ForgotPassword"))
const CHANGEPASSWORD = React.lazy(() => import("../pages/ChangePassword"))
const RESET = React.lazy(() => import("../pages/ResetPasswordLink"))
const routes = [
    { path: PathConstants.ABOUT, element: <About /> },
    { path: PathConstants.CREATEROOM, element: <CreateRoom /> },
    { path: PathConstants.ROOM, element: <Room /> },
    { path: PathConstants.PROFILE, element: <PROFILE /> },
    { path: PathConstants.REGISTER, element: <REGISTER /> },
    { path: PathConstants.LOGIN, element: <LOGIN /> },
    { path: PathConstants.VERIFY, element: <VERIFY /> },
    { path: PathConstants.FORGOTPASSWORD, element: <FORGOTPASSWORD /> },
    { path: PathConstants.CHANGEPASSWORD, element: <CHANGEPASSWORD /> },
    { path: PathConstants.RESET, element: <RESET /> }
]
export default routes
