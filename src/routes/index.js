import React from "react"
import PathConstants from "./constants"

const Game = React.lazy(() => import("../pages/Game"))
const About = React.lazy(() => import("../pages/About"))
const CreateRoom = React.lazy(() => import("../pages/CreateRoom"))
const Room = React.lazy(() => import("../pages/Room"))
const routes = [
    { path: PathConstants.GAME, element: <Game /> },
    { path: PathConstants.ABOUT, element: <About /> },
    { path: PathConstants.CREATEROOM, element: <CreateRoom /> },
    { path: PathConstants.ROOM, element: <Room /> },
]
export default routes
